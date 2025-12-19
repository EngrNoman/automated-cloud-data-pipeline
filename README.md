# Serverless AWS Data Pipeline 🚀

This project is a fully automated ETL pipeline deployed on AWS using Terraform.

## 🏗 Architecture

1. **Source:** Fetches data from external API (DummyJSON).
2. **Compute:** AWS Lambda (Python 3.10) for extraction, validation, and transformation.
3. **Storage:** AWS S3 (Raw, Quarantine, Processed zones).
4. **IaC:** Terraform for full infrastructure deployment.
5. **Validation:** Pydantic for data quality checks.

## 🛠 Tech Stack

- **Language:** Python (Pandas, Requests, Pydantic)
- **Cloud:** AWS (Lambda, S3, IAM, CloudWatch)
- **Infrastructure as Code:** Terraform
- **Deployment:** GitHub Actions / Terraform CLI

## 🚀 How to Deploy

1. Clone the repo.
2. `cd infra`
3. `terraform init`
4. `terraform apply`
