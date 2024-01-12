**Generate Terraform Modules**

This runs `kc tf init`, which in turn executes `terraform init`. Hang on ... this may take a minute. You can view the log in the terminal window. Generated terraform modules for your environment will be saved in `kc-rapid-cloud/terraform/{env}` directory

**Generate Terraform Deployment Plan**

This runs `kc tf plan`, which in turn executes `terraform plan`. Hang on ... this may take a few minutes. You can view the log in the terminal window. Terraform plan will be saved in `kc-rapid-cloud/terraform/{env}/plan.log`

**Apply Terraform Plan - Deploy Infrastructure**

This runs `kc tf apply`, which in turn executes `terraform apply`. Hang on ... this may take a while, depending on your environment complexity. 

_**We recommend running this from your RapidCloud terminal, to see the progress, instead of running via console.**_

**Destroy Current Environment Infrastructure**

This runs `kc tf destroy`, which in turn executes `terraform destroy`. Hang on ... this may take a few minutes. 

_**Note: S3 buckets which are not empty will not be deleted. You must empty the buckets first.**_



