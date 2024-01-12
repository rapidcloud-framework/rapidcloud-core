__author__ = "Igor Royzis"
__copyright__ = "Copyright 2020, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging

from commands import print_utils
from commands.kc_metadata_manager.aws_metadata import Metadata

class Pricing(Metadata):

    TABLE_NAME = 'pricing'
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.INFO)


    def __init__(self, args):
        super().__init__(args)
        self.service_codes = {}
        for svc in super().get_dynamodb_resource().Table(self.TABLE_NAME).scan()['Items']:
            self.service_codes[svc['resource_type']] = svc


    def describe_services(self, service_code):
        return super().get_pricing_client().describe_services(
            FormatVersion='aws_v1',
            MaxResults=1,
            ServiceCode=service_code,
        )


    def get_pricing_info(self, service_code, filters_dict={}):
        # print(json.dumps(filters_dict, indent=2))
        filters = []
        for k,v in filters_dict.items():
            if k not in ['usagetypes', 'resource_type']:
                filters.append({
                    'Type': 'TERM_MATCH',
                    'Field': k,
                    'Value': v
                })

        # print(json.dumps(filters, indent=2))
        response = super().get_pricing_client().get_products(
            ServiceCode=service_code,
            Filters=filters,
            FormatVersion='aws_v1',
            MaxResults=100
        )

        prices = []
        usagetypes = []
        for price_str in response['PriceList']:
            attrs = {}
            price = json.loads(price_str)
            attrs['ServiceCode'] = service_code
            attrs['location'] = price['product']['attributes']['location']

            if 'usagetype' in price['product']['attributes']:
                # self.logger.debug(price['product']['attributes']['usagetype'])
                attrs['usagetype'] = price['product']['attributes']['usagetype']
            else:
                attrs['usagetype'] = 'n/a'

            if attrs['usagetype'] in filters_dict['usagetypes'] and attrs['usagetype'] not in usagetypes:
                usagetypes.append(attrs['usagetype'])
                for k1, v1 in price['terms']['OnDemand'].items():
                    for k2, v2 in v1['priceDimensions'].items():
                        attrs['unit'] = v2['unit']
                        attrs['description'] = v2['description']
                        attrs['pricePerUnitUSD'] = v2['pricePerUnit']['USD']

                prices.append(attrs)

        # if service_code == 'AmazonS3':
        #     print(json.dumps(prices, indent=2))
    
        return prices


    def get_pricing(self):
        pricing_info = []
        i = 1
        for resource in super().get_all_resources():
            params = self.service_codes.get(resource['resource_type'])
            if params:
                self.logger.info(f"{i}. {resource['resource_type']} -> {params['ServiceCode']}")
                resource_prices = self.get_pricing_info(params['ServiceCode'], params)
                for resource_price in resource_prices:
                    resource_price['ResourceName'] = resource['resource_name']
                    resource_price['ResourceType'] = resource['resource_type']
                    pricing_info.append(resource_price)

                # print(json.dumps(pricing_info, indent=2))
                # return 
                
            else:
                self.logger.warn(f"{i}. {resource['resource_type']} -> ???")
            
            i += 1
        
        pricing_info.sort(key=lambda item: (item['ResourceType'],item['ResourceName']))
        print_utils.print_grid_from_json(pricing_info, ['ResourceName','ResourceType','ServiceCode','unit','pricePerUnitUSD','usagetype'])

        with open(f"config/environments/{super().get_env()}_pricing.json", 'w') as f:
            json.dump(pricing_info, f, indent=2)

        return pricing_info


    def init(self):

        items = [
            {
                "resource_type": "s3_bucket", 
                "ServiceCode": "AmazonS3",
                "usagetypes": [
                    "TimedStorage-ByteHrs"
                ]
            },
            {
                "resource_type": "dms_replication_instance",
                "ServiceCode": "AWSDatabaseMigrationSvc",
                "usagetypes": [
                    "Multi-AZUsg:dms.t2.small"
                ],
                "availabilityZone": "Multiple"
            },
            {
                "resource_type": "emr_cluster",
                "ServiceCode": "ElasticMapReduce",
                "usagetypes": [
                    "BoxUsage:m4.large"
                ]
            },
            {
                "resource_type": "redshift_cluster",
                "ServiceCode": "AmazonRedshift",
                "usagetypes": [
                    "Node:dc2.large"
                ]
            },
            {
                "resource_type": "glue_job",
                "ServiceCode": "AWSGlue",
                "usagetypes": [
                    "USE1-ETL-DPU-Hour"
                ]
            },
            {
                "resource_type": "glue_crawler",
                "ServiceCode": "AWSGlue",
                "usagetypes": [
                    "USE1-ETL-DPU-Hour"
                ]
            },
            {
                "resource_type": "lambda_function",
                "ServiceCode": "AWSLambda",
                "usagetypes": [
                    "Request",
                    "Lambda-GB-Second"
                ]
            }
        ]

        with super().get_dynamodb_resource().Table(self.TABLE_NAME).batch_writer() as batch:
            for item in items:
                try:
                    item['Location'] = "US East (N. Virginia)" # TODO
                    batch.put_item(
                        Item=item
                    )
                except Exception as e:
                    self.logger.error(e)
                    self.traceback.print_exc()
