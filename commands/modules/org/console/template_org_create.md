### AWS Organizations

AWS Organizations is an account management service that enables you to consolidate multiple AWS accounts into an organization that you create and centrally manage.

**Name**

This is the internal RapidCloud name that your organizations will have.

**AWS Service Access Principals**

List of AWS service principal names for which you want to enable integration with your organization. This is typically in the form of a URL, such as service-abbreviation.amazonaws.com. Some services do not support enablement via Terraform, see more information [here](https://docs.aws.amazon.com/organizations/latest/APIReference/API_EnableAWSServiceAccess.html).

**Enabled Policy Types**

List of policy types to enable in the Organization Root, allowed values are `(AISERVICES_OPT_OUT_POLICY | BACKUP_POLICY | SERVICE_CONTROL_POLICY | TAG_POLICY)`. See more information [here](https://docs.aws.amazon.com/organizations/latest/APIReference/API_EnablePolicyType.html).
