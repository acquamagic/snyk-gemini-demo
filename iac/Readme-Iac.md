# Demo-only insecure bastion (for IaC scanning)

## Apply (example)
```bash
cd iac
terraform init
terraform apply -var="project_id=YOUR_DEMO_PROJECT_ID"
