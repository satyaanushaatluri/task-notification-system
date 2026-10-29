# Kubernetes (Starter) — task-notification-system

## What is here
- `deployment.yaml` — 2 replicas of the FastAPI app on port 8000.
- `service.yaml` — ClusterIP Service (internal only, not public).

## Before you apply
1. Build and push the image to the ECR repository from `terraform/main.tf`,
   then replace the `<registry>/task-notification-system:latest` placeholder in `deployment.yaml`
   with the real ECR URL (`terraform apply` prints it as `ecr_repository_url`).
2. Create the database secret (replace the URL with your real database):
   ```bash
   kubectl create secret generic task-notification-system-db-secret \
     --from-literal=DATABASE_URL='postgresql://user:pass@db-host:5432/appdb'
   ```

## Apply
```bash
kubectl apply -f k8s/
kubectl get pods -l app=task-notification-system
kubectl port-forward svc/task-notification-system 8000:80
```
Then open http://127.0.0.1:8000/docs

## Notes
- ClusterIP is internal to the cluster. For public access, add an Ingress
  or change the Service type — that is not included in this starter.
- Committing these files deploys nothing on its own; `kubectl apply` does.
