#!/bin/bash
# Restart (or redeploy) script for ShvikiFitness Helm release
# Author: Alon Shviki

RELEASE="shviki"
NS="sh"
CHART_PATH="./helm/helm-chart"
MODE=$1

echo "------------------------------------------------------"
echo " Restarting ShvikiFitness Helm environment"
echo " Namespace: $NS"
echo " Mode: ${MODE:---keep}"
echo "------------------------------------------------------"

# Ensure namespace exists
if ! kubectl get ns "$NS" &>/dev/null; then
  echo "Creating namespace $NS..."
  kubectl create ns "$NS"
fi

# Uninstall existing release if present
if helm list -n "$NS" | grep -q "$RELEASE"; then
  echo "Deleting old Helm release '$RELEASE'..."
  helm uninstall "$RELEASE" -n "$NS"
else
  echo "No existing Helm release found — fresh start."
fi

# Delete PVCs only if requested
if [ "$MODE" == "--fresh" ]; then
  echo "FRESH MODE: Deleting PVCs (MySQL data will be lost)"
  kubectl delete pvc --all -n "$NS" --ignore-not-found
else
  echo "KEEP MODE: Preserving PVCs (MySQL data kept)"
fi

# Install new release
echo
echo "Installing Helm release..."
helm install "$RELEASE" "$CHART_PATH" --namespace "$NS" --create-namespace || {
  echo "Helm install failed."
  exit 1
}

# Wait for workloads
echo
echo "Waiting for pods to become Ready..."
kubectl rollout status deployment/shviki-app -n "$NS" --timeout=180s || true
kubectl rollout status statefulset/shviki-fitness-mysql -n "$NS" --timeout=180s || true

# Show state
echo
echo "Deployment summary:"
kubectl get pods -n "$NS"
kubectl get svc -n "$NS"

# Determine actual Flask service name
SERVICE_NAME=$(kubectl get svc -n "$NS" -o jsonpath='{.items[?(@.metadata.name=="shviki-fitness-service")].metadata.name}')
if [ -z "$SERVICE_NAME" ]; then
  SERVICE_NAME=$(kubectl get svc -n "$NS" -o jsonpath='{.items[0].metadata.name}')
fi

echo
if [ -n "$SERVICE_NAME" ]; then
  echo "Detecting service URL for: $SERVICE_NAME ..."
  SERVICE_URL=$(minikube service "$SERVICE_NAME" -n "$NS" --url 2>/dev/null)
  if [ -n "$SERVICE_URL" ]; then
    echo "Flask service available at: $SERVICE_URL"
  else
    echo "Flask service detected but URL could not be resolved (maybe ClusterIP type)."
  fi
else
  echo "No Flask service found in namespace '$NS'."
fi

echo
echo "------------------------------------------------------"
echo " ShvikiFitness Helm environment redeployed successfully."
echo "------------------------------------------------------"
