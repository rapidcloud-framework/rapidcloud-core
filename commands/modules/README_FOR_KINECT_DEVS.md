## Creating RapidCloud modules (aka features)

### Planning/tracking

1. Finalize module requirements and document high level as Jira Epic

    * Use case / workload narrative
    * List of AWS resources
    * Security
    * Orchestration/workflow

3. Break Epic into stories

    * Story per AWS resource not currrently supported by RapidCloud

        * Sample `aws_infra` json item

        * Create *.tf for each resource not currently implemented in https://bitbucket.org/kinect-consulting/workspace/projects/TFAWS

        * Create *.j2 for each resource not currently implemented in https://bitbucket.org/kinect-consulting/kc-big-data/src/master/terraform/templates/

    * CLI implementation story
        * module.json
        * python code for module initialization

    * Console templates story

    * Story for each additional `command` (e.g. activation/deactivation, orchestration/workflow related functionality)


#### Notes: each story must have clearly defined `acceptance criteria`


### Development process

* Each story must have its own branch using following naming convention: `[jira id]-[short jira title]` (e.g `KFBD-87-Create-pricing-module`)
* Commit changes to the branch often, at least once per day
* Test eveything with RapidCloud CLI on your localhost before creating a PR
* Formal code review will be required before any PR is approved
* Deployment to RapidCloud dev server will be discussed and performed as needed


### Bitbucket Repos

- RapidCloud: `git@bitbucket.org:kinect-consulting/kc-big-data.git`
- RapidCloud Console: `git@bitbucket.org:kinect-consulting/kinect-theia-console.git`
- RapidCloud Roles tf: `git@bitbucket.org:kinect-consulting/theia-roles.git`
- Terraform Repos: `https://bitbucket.org/kinect-consulting/workspace/projects/TFAWS`
	- these get into RapidCloud `terraform/modules` folder based on `terraform/templates/source.json` contents


### Setting up your environment

* `kc init create-env` and follow prompts
* `kc status` - show status of AWS resources for your environment
* `kc tf init` - initialize terraform and generate modules
* `kc tf plan` - run terraform plan
* `kc tf apply` - run terraform apply
* `kc tf destroy` - run terraform destroy


### Create new RapidCloud module

* `kc module create`

* This creates following skeleton:
    
    * ./commands/modules/<module-name>
        * module.json
        * __init__py
        * console/
            * template_module_[module-name].json
            * template_module_[module-name].md
