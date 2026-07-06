## Setting up
```shell
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
## Testing the app
```shell
pytest
```
## Running the app
```shell
flask run # defaults to debug mode
```
## Information
### Terraform
The terraform is made up of the initialisation files, 6 files I created and a shell script dependency to delete a stale service.
| File Name | Purpose / Contents |
| :--- | :--- |
| `terraform.tf` | Contains the `terraform {}` block and a nested backend block to connect the remote state file. |
| `main.tf` | Contains the `provider {}` block and the S3 resources. |
| `iam.tf` | Contains the IAM roles and policies needed for GitHub and ECS to create the service. |
| `network.tf` | Contains the minimal network configuration required for Express. |
| `ecs.tf` | Contains the necessary Elastic Container Registry (ECR), the ECS cluster, and the `clean_stale_service` dependency. |
| `outputs.tf` | Contains the subnet IDs to be outputted and used by the CI/CD workflow. |

* Note on the `cleanup.sh`: 
    * checks if the service exists
    * if a service is returned by aws, delete it using `delete-express-gateway-service`
    * checks through a loop to ensure the service is gone

### Test Coverage
Comparing the percentage of test types results in this:
 - End-to-end: 4.5%
 - Integration: 18.2%
 - Unit: 77.3%

The coverage report is below:

src/__init__.py — 0 Stmts | 0 Miss | 100% Cover

src/app/__init__.py — 0 Stmts | 0 Miss | 100% Cover

src/app/app.py — 14 Stmts | 0 Miss | 100% Cover

src/app/core.py — 39 Stmts | 0 Miss | 100% Cover

src/tests/__init__.py — 0 Stmts | 0 Miss | 100% Cover

src/tests/test_duty.py — 79 Stmts | 0 Miss | 100% Cover

src/tests/test_e2e.py — 26 Stmts | 0 Miss | 100% Cover

TOTAL — 158 Stmts | 0 Miss | 100% Cover