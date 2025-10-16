#!/bin/bash
# Restart script for ShvikiFitness Kubernetes deployment
# Author: Alon Shviki

NS="shviki-fitness"
MODE=$1

echo "------------------------------------------------------"
echo " Restarting ShvikiFitness environment"
echo " Namespace: $NS"
echo " Mode: ${MODE:---keep}"
echo "------------------------------------------------------"

# Check namespace
if ! kubectl get ns "$NS" &>/dev/null; then
  echo "🆕 Creating namespace $NS..."
  kubectl create ns "$NS"
fi

# Clean up old resources
echo "🧹 Deleting old workloads in $NS..."
kubectl delete all --all -n "$NS" --ignore-not-found
kubectl delete configmap --all -n "$NS" --ignore-not-found
kubectl delete secret --all -n "$NS" --ignore-not-found

if [ "$MODE" == "--fresh" ]; then
  echo "⚠️  FRESH MODE: Deleting PVC and database volume (this erases MySQL data)"
  kubectl delete pvc --all -n "$NS" --ignore-not-found
else
  echo "✅ KEEP MODE: Preserving PVC and database data"
fi

# Redeploy manifests
echo
echo "🚀 Reapplying manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/db/ -n "$NS"
kubectl apply -f k8s/app/ -n "$NS"

echo
echo "⏳ Waiting for pods to start..."
kubectl rollout status statefulset/mysql -n "$NS" --timeout=180s || true
kubectl rollout status deploy/flask-deployment -n "$NS" --timeout=180s || true

echo
echo "✅ Restart complete!"
kubectl get pods -n "$NS"
kubectl get svc -n "$NS"

echo
echo "------------------------------------------------------"
echo " ShvikiFitness environment redeployed successfully."
echo " Access Flask via: $(minikube service flask-service -n $NS --url)"
echo "------------------------------------------------------"
