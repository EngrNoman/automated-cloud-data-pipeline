# Serverless AWS Data Pipeline 🚀

This project is a fully automated ETL pipeline deployed on AWS using Terraform.

## 🏗 Architecture

1. **Source:** Fetches data from external API (DummyJSON).
2. **Compute:** AWS Lambda (Python 3.10) for extraction, validation, and transformation.
3. **Storage:** AWS S3 (Raw, Quarantine, Processed zones).
4. **IaC:** Terraform for full infrastructure deployment.
5. **Validation:** Pydantic for data quality checks.

## 🏗 Data Pipeline Architecture

```mermaid
graph TD
    %% --- Main Setup ---
    subgraph AWS [☁️ AWS Cloud Infrastructure]
        direction LR
        
        %% Nodes
        EB("⏱️ <b>EventBridge Scheduler</b><br/>(Daily Trigger)")
        LAM("⚙️ <b>AWS Lambda</b><br/>(Python ETL)")
        API("🌍 <b>External API</b><br/>(DummyJSON)")
        
        subgraph S3 [🪣 Amazon S3 Storage]
            RAW[📄 Raw Zone]
            PRO[📊 Processed Zone]
            LOG[🚫 Quarantine Zone]
        end
    end

    %% --- Connections ---
    EB -- "1. Trigger" --> LAM
    LAM -- "2. Fetch" --> API
    API -- "3. Data" --> LAM
    LAM -- "4. Store" --> RAW
    LAM -- "5. Clean" --> PRO
    LAM -- "6. Error" --> LOG

    %% --- Styling ---
    style EB fill:#FF4F8B,stroke:#333,color:white
    style LAM fill:#FF9900,stroke:#333,color:white
    style S3 fill:#3F8624,stroke:#333,color:white
    style RAW fill:#fff,stroke:#333
    style PRO fill:#e6fffa,stroke:#333
    style LOG fill:#ffe6e6,stroke:#ff0000
```

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
