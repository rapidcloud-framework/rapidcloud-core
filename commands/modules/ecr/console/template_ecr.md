### Elastic Container Registry

ECR is an AWS managed container image registry

**Name**

Repository name, will be prefixed with your RapidCloud environment name

**Image Tag Mutability**

Prevent image tags from being overwritten, allowed values are `(MUTABLE | IMMUTABLE)`

**Scan Images on Push**

Identify software vulnerabilities in your container images on image push. Scanning can still be performed manually if set to false.

**Encryption Type**

The encryption type to use for the repository, defaults to `AES256`. allowed values are `(AES256 | KMS)`.

**KMS Key**

The KMS Key ARN to use when the selected encryption type is `KMS`. If no KMS Key is provided then the default AWS managed key for ECR will be used.