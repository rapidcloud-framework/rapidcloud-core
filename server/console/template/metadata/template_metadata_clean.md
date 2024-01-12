This removes all metadata for the environment 

From CLI: `kc metadata remove` 

Important: this does not destroy environment resources. 

If your goal is to remove the environment and all resources, then first do `Deploy -> Terraform Actions -> Destroy` (`kc tf destroy`) and then `Metadata -> Remove Metadata` (`kc metadata remove`)