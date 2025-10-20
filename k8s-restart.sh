#!/bin/bash
# Restart (or redeploy) script for ShvikiFitness Helm release
# Author: Alon Shviki

RELEASE="shviki"
NS="sh"
MODE=$1
CHART_PATH="./helm/helm-chart"

echo "------------------------------------------------------"
echo " 🔁 Restarting ShvikiFitness Helm environment"
echo " Namespace: $NS"
echo " Mode: ${MODE:---keep}"
echo "------------------------------------------------------"

# Ensure namespace exists
if ! kubectl get ns "$NS" &>/dev/null; then
  echo "🆕 Creating namespace $NS..."
  kubectl create ns "$NS"
fi

# Check if release exists
if helm list -n "$NS" | grep -q "$RELEASE"; then
  echo "🧹 Deleting old Helm release '$RELEASE'..."
  helm uninstall "$RELEASE" -n "$NS"
else
  echo "ℹ️ No existing Helm release found — fresh start."
fi

# Handle PVC preservation or deletion
if [ "$MODE" == "--fresh" ]; then
  echo "⚠️  FRESH MODE: Deleting all PVCs (MySQL data will be lost)"
  kubectl delete pvc --all -n "$NS" --ignore-not-found
else
  echo "✅ KEEP MODE: Preserving existing PVCs (MySQL data kept)"
fi

# Reinstall via Helm
echo
echo "🚀 Installing Helm release..."
helm install "$RELEASE" "$CHART_PATH" --namespace "$NS" --create-namespace

if [ $? -ne 0 ]; then
  echo "❌ Helm install failed. Exiting."
  exit 1
fi

# Wait for workloads to start
echo
echo "⏳ Waiting for pods to become Ready..."
kubectl rollout status deployment/"${RELEASE}-app" -n "$NS" --timeout=180s || true
kubectl rollout status statefulset/"${RELEASE}-mysql" -n "$NS" --timeout=180s || true

# Show current state
echo
echo "✅ Restart complete!"
kubectl get pods -n "$NS"
kubectl get svc -n "$NS"

# Show external access
echo
SERVICE_URL=$(minikube service "${RELEASE}-service" -n "$NS" --url 2>/dev/null)
if [ -n "$SERVICE_URL" ]; then
  echo "🌐 Access Flask via: $SERVICE_URL"
else
  echo "⚠️  Flask service URL not available — check NodePort or Ingress."
fi

echo
echo "------------------------------------------------------"
echo " ✅ ShvikiFitness Helm environment redeployed successfully."
echo "------------------------------------------------------"
