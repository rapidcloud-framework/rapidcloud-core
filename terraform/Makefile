.ONESHELL:
SHELL := /bin/bash
.PHONY: help
AWS_VAULT_ACCT="kc-bigdata"
STS_TTL="1h"




help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

kc-init-debug: ## build infra from dynamo source with debug output
		@git pull && AWS_PROFILE=${p} ./bin/kc-init.py --table aws_infra --profile ${p} --debug

kc-init: ## build infra from dynamo source
		@git pull && AWS_PROFILE=${p} ./bin/kc-init.py --table aws_infra --profile ${p}

init: kc-init ## init terraform
	@AWS_PROFILE=${p}  terraform init

refresh: ## refresh the state metadata
	@AWS_PROFILE=${p} terraform refresh

plan: init
	@AWS_PROFILE=${p} terraform plan

plan-destroy: init ## Creates a destruction plan.
	@AWS_PROFILE=${p} terraform plan  -out .plan.out

destroy: init ## executes a destruction plan.
	@AWS_PROFILE=${p} terraform destroy

apply: init ## apply all resources but one at a time (-parallelism=1) use for initial dms
	@AWS_PROFILE=${p} terraform apply -parallelism=1

output: ## display outputs
	@AWS_PROFILE=${p} terraform output

force-unlock: ## force unlock a dynamo state lock table, provide l=xxx-lock-id
	@[ "${lock}" ] && echo "unlocking ${lock}" || ( echo "no lock id provided"; exit 1 )
	@AWS_PROFILE=${p} terraform force-unlock ${lock}
