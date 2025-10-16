#!/bin/bash
# Health check script for ShvikiFitness K8s deployment
# Author: Alon Shviki
# Namespace: shviki-fitness

NS="shviki-fitness"
echo "------------------------------------------------------"
echo " ShvikiFitness Kubernetes Health Check"
echo " Namespace: $NS"
echo "------------------------------------------------------"

# Check if namespace exists
if ! kubectl get ns "$NS" &>/dev/null; then
  echo "❌ Namespace '$NS' not found. Please deploy first."
  exit 1
fi

echo "✅ Namespace found."

echo
echo "1️⃣  Checking pods..."
kubectl get pods -n "$NS"
echo

# Verify all pods are running
NOT_READY=$(kubectl get pods -n "$NS" --no-headers | awk '$3!="Running" || $2!="1/1" {print $1}')
if [ -z "$NOT_READY" ]; then
  echo "✅ All pods are running and healthy."
else
  echo "⚠️  Some pods not ready:"
  echo "$NOT_READY"
fi

echo
echo "2️⃣  Checking PersistentVolumeClaim..."
kubectl get pvc -n "$NS"
PVC_STATUS=$(kubectl get pvc -n "$NS" -o jsonpath='{.items[0].status.phase}')
if [ "$PVC_STATUS" == "Bound" ]; then
  echo "✅ PVC is bound successfully."
else
  echo "❌ PVC not bound — check storage class."
fi

echo
echo "3️⃣  Checking Services..."
kubectl get svc -n "$NS"
FLASK_SVC=$(kubectl get svc flask-service -n "$NS" --no-headers | awk '{print $3}')
MYSQL_SVC=$(kubectl get svc mysql-service -n "$NS" --no-headers | awk '{print $3}')
if [[ -n "$FLASK_SVC" && -n "$MYSQL_SVC" ]]; then
  echo "✅ Both Flask and MySQL services detected."
else
  echo "❌ Missing one or more services."
fi

echo
echo "4️⃣  Checking Pod Conditions..."
for POD in $(kubectl get pods -n "$NS" -o name); do
  echo "- $POD"
  kubectl get "$POD" -n "$NS" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' | grep True &>/dev/null \
    && echo "   ✅ Ready" || echo "   ❌ Not Ready"
done

echo
echo "5️⃣  Checking external access..."
URL=$(minikube service flask-service -n "$NS" --url 2>/dev/null)
if [ -n "$URL" ]; then
  echo "✅ Flask service exposed at: $URL"
  echo "   (Try opening this in your browser)"
else
  echo "⚠️  Could not detect NodePort service URL."
fi

echo
echo "6️⃣  Checking MySQL persistence..."
POD=$(kubectl get pod -n "$NS" -l app=mysql -o name)
if [ -n "$POD" ]; then
  kubectl exec -n "$NS" "$POD" -- mysql -u shviki_user -pshviki_pass -e "USE shviki_db; SELECT COUNT(*) AS user_count FROM users;" 2>/dev/null \
    && echo "✅ Database reachable and query executed successfully." \
    || echo "⚠️  Database not responding."
else
  echo "❌ MySQL pod not found."
fi

echo
echo "------------------------------------------------------"
echo " Health check completed."
echo "------------------------------------------------------"
