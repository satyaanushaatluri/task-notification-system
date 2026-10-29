# Task and Notification System

FastAPI + SQLAlchemy project for tasks and notifications.

## What it does
- Creates tasks and assigns them to a user
- Sends notifications as background tasks, so API responses stay fast
- Records notification status (`pending` / `sent` / `failed`) in the database
- Retries a failed notification

## Run it
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Tests
```bash
pytest
```

## Next step for production
Move `send_notification` to Celery workers and replace the print with a real email/SMTP sender.

## Infrastructure

Starter Terraform + Kubernetes files. Committing them creates or deploys nothing.

- `terraform/main.tf` — AWS provider + ECR repository only (no EKS cluster, no production deployment).
  ```bash
  cd terraform
  terraform init
  terraform plan
  terraform apply   # only this step creates AWS resources; needs AWS credentials
  ```
- `k8s/deployment.yaml`, `k8s/service.yaml` — 2-replica Deployment (port 8000) and ClusterIP Service.
  ```bash
  kubectl apply -f k8s/
  ```
  See `k8s/README.md` for the image placeholder and database secret you must replace first.

Validate Kubernetes YAML syntax locally:
```bash
python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('k8s/*.yaml')]"
```
Terraform formatting was NOT checked in the environment where this was added
because Terraform is not installed there — run `terraform fmt -check` and
`terraform validate` yourself before applying.
