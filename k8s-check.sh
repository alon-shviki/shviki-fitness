#!/bin/bash
# Health check script for ShvikiFitness Helm deployment (NodePort-aware)

NAMESPACE="sh"
RELEASE="shviki"

echo "------------------------------------------------------"
echo " ✅ ShvikiFitness Helm Deployment Health Check"
echo " Namespace: $NAMESPACE | Release: $RELEASE"
echo "------------------------------------------------------"

# ✅ 1. Check Namespace
if ! kubectl get ns "$NAMESPACE" &>/dev/null; then
  echo "❌ Namespace '$NAMESPACE' not found. Deploy Helm release first."
  exit 1
fi
echo "✅ Namespace exists."

# ✅ 2. Check Pods
echo -e "\n2️⃣ Checking Pods..."
kubectl get pods -n "$NAMESPACE"
if kubectl get pods -n "$NAMESPACE" --no-headers | awk '$3!="Running"' | grep -q .; then
  echo "⚠️ Some pods are not healthy!"
else
  echo "✅ All pods are healthy."
fi

# ✅ 3. Check PVC
echo -e "\n3️⃣ Checking PVC..."
kubectl get pvc -n "$NAMESPACE"
PVC_STATUS=$(kubectl get pvc -n "$NAMESPACE" -o jsonpath='{.items[0].status.phase}' 2>/dev/null)
echo "PVC Status: $PVC_STATUS"

# ✅ 4. Check Services
echo -e "\n4️⃣ Checking Services..."
kubectl get svc -n "$NAMESPACE"

# ✅ 5. Check NodePort Access for Flask Service
echo -e "\n5️⃣ Checking Flask Service Exposure..."

SERVICE_NAME="${RELEASE}-service"
SERVICE_TYPE=$(kubectl get svc "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.type}' 2>/dev/null)

if [ "$SERVICE_TYPE" == "NodePort" ]; then
  NODE_PORT=$(kubectl get svc "$SERVICE_NAME" -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].nodePort}')
  MINIKUBE_IP=$(minikube ip)
  echo "✅ Flask is exposed via NodePort"
  echo "🌐 Access at: http://$MINIKUBE_IP:$NODE_PORT"
elif [ "$SERVICE_TYPE" == "ClusterIP" ]; then
  echo "⚠️ Service is ClusterIP (internal only) — No external browser access"
else
  echo "❌ Flask service not found or unsupported service type."
fi

# ✅ 6. Check MySQL Access
echo -e "\n6️⃣ Checking MySQL Database..."
MYSQL_POD=$(kubectl get pod -n "$NAMESPACE" -l app=mysql -o jsonpath='{.items[0].metadata.name}')
if [ -n "$MYSQL_POD" ]; then
  kubectl exec -n "$NAMESPACE" "$MYSQL_POD" -- \
    mysql -u shviki -pshviki123 -e "USE shviki_db; SHOW TABLES;" &>/dev/null
  if [ $? -eq 0 ]; then
    echo "✅ MySQL is reachable & responding."
  else
    echo "❌ MySQL is running but rejecting queries."
  fi
else
  echo "❌ MySQL pod not found."
fi

echo "------------------------------------------------------"
echo " ✅ Health Check Done."
echo "------------------------------------------------------"
