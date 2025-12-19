# --- 1. S3 Bucket Creation ---
resource "aws_s3_bucket" "data_bucket" {
  bucket        = "${var.project_name}-${var.environment}-bucket"
  force_destroy = true
  tags = {
    Name        = "Data Pipeline Storage"
    Environment = var.environment
  }
}

# --- 2. Folder Structure (Raw , Staged, processed) ---
resource "aws_s3_object" "raw_folder" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "raw/"
}

resource "aws_s3_object" "quarantine_folder" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "quarantine/"
}

resource "aws_s3_object" "processed_folder" {
  bucket = aws_s3_bucket.data_bucket.id
  key    = "processed/"
}

# --- 3. Output ---
output "s3_bucket_name" {
  description = "S3 Bucket jiska naam hai"
  value       = aws_s3_bucket.data_bucket.bucket
}

# --- 4. IAM Role ---
resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# --- 5. Permission Policy ---
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# --- 6. S3 Access Permission ---
resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "${var.project_name}-lambda-s3-policy"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.data_bucket.arn,
          "${aws_s3_bucket.data_bucket.arn}/*"
        ]
      }
    ]
  })
}

# --- 7. Zipping the Code (Application Logic) ---
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/.." # Root folder par jao
  output_path = "${path.module}/lambda_function.zip"

  # Ye cheezein zip my nahi dalni
  excludes = [
    "infra",
    ".git",
    ".env",
    "venv",
    "__pycache__",
    ".gitignore",
    "tests",
    "data",
    "logs"
  ]
}

# --- 8. CUSTOM LAYER (Requests & Pydantic) --- [NEW ADDITION ✅]
# Pehlay 'infra/layers/common' folder ko zip karein
data "archive_file" "common_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/layers/common"
  output_path = "${path.module}/common_layer.zip"
}

# Phir AWS par Layer Create karein
resource "aws_lambda_layer_version" "common_layer" {
  filename   = data.archive_file.common_layer_zip.output_path
  layer_name = "${var.project_name}-common-dependencies"

  compatible_runtimes = ["python3.10"]
  source_code_hash    = data.archive_file.common_layer_zip.output_base64sha256
}

# --- 9. Lambda Function ---
resource "aws_lambda_function" "etl_lambda" {
  function_name = "${var.project_name}-function"
  role          = aws_iam_role.lambda_exec_role.arn

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  handler = "main.run_pipeline"
  runtime = "python3.10"

  timeout     = 60
  memory_size = 512

  environment {
    variables = {
      ENV_TYPE    = "cloud"
      BUCKET_NAME = aws_s3_bucket.data_bucket.id
      API_URL     = "https://dummyjson.com/products"
    }
  }

  # --- LAYERS CONFIGURATION ---
  layers = [
    # 1. AWS Provided Pandas Layer
    "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python310:16",

    # 2. Humari Custom Layer (Pydantic/Requests) [NEW ✅]
    aws_lambda_layer_version.common_layer.arn
  ]
}


# --- 10. Automation (EventBridge Scheduler) ---

# 1. Rule: Kab chalna hai? (Rozana Subah 9 Bajay UTC)
resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name        = "${var.project_name}-daily-rule"
  description = "Triggers Lambda every day at 9 AM UTC"

  # Cron Expression: (Minutes Hours Day Month Weekday Year)
  # '0 9 * * ? *' ka matlab: Rozana 9:00 AM UTC
  schedule_expression = "cron(15 22 * * ? *)"
  # schedule_expression = "rate(2 minutes)"
}

# 2. Target: Kis ko chalana hai? (Humara Lambda Function)
resource "aws_cloudwatch_event_target" "trigger_lambda" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "lambda"
  arn       = aws_lambda_function.etl_lambda.arn
}

# 3. Permission: EventBridge ko ijazat do k wo Lambda chala sakay
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.etl_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_trigger.arn
}
