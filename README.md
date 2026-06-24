# Setting up
```shell
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
# Testing the app
```shell
pytest
```
# Running the app
```shell
flask run # defaults to debug mode
```
# Information
## Terraform
The terraform is made up of the initialisation files, 6 files I created and a shell script dependency to delete a stale service.
| File Name | Purpose / Contents |
| :--- | :--- |
| **`terraform.tf`** | Contains the `terraform {}` block and a nested backend block to connect the remote state file. |
| **`main.tf`** | Contains the `provider {}` block and the S3 resources. |
| **`iam.tf`** | Contains the IAM roles and policies needed for GitHub and ECS to create the service. |
| **`network.tf`** | Contains the minimal network configuration required for Express. |
| **`ecs.tf`** | Contains the necessary Elastic Container Registry (ECR), the ECS cluster, and the `clean_stale_service` dependency. |
| **`outputs.tf`** | Contains the subnet IDs to be outputted and used by the CI/CD workflow. |

* Note on the `cleanup.sh`: 
    * checks if the service exists
    * if a service is returned by aws, delete it using `delete-express-gateway-service`
    * checks through a loop to ensure the service is gone