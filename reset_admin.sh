#!/bin/bash
# ============================================================
# ShvikiFitness - Admin Reset Script
# Works with both Helm/Kubernetes and Docker Compose setups
# Author: Alon Shviki
# ============================================================

# --- CONFIGURATION ---
NAMESPACE="sh"                            # Kubernetes namespace
MYSQL_POD="shviki-fitness-mysql-0"        # Pod name (K8s)
DB_NAME="shviki_db"
EMAIL="alon.shviki@gmail.com"
FIRST_NAME="Alon"
LAST_NAME="Shviki"
NATIONAL_ID="123456789"
AGE=25
GENDER="male"
SUBSCRIPTION="premium"
ROLE="admin"

# --- PASSWORD HASH (Generated via werkzeug.security.generate_password_hash) ---
HASH="scrypt:32768:8:1\$D4pqGvMYNpIM6Haz\$2fd9039e9aaeb8c5d9845ce0c934cadacdf0525cef47e5ee3c514681824b5311e2b24248c0e7d4e39d626c747e5f4b0b2f9c7daa6c739d02399c5952416b0489"

# --- FUNCTION FOR KUBERNETES ---
reset_user_k8s() {
  echo "🔄 Resetting admin user in Kubernetes pod: $MYSQL_POD (namespace: $NAMESPACE)..."

  kubectl exec -n "$NAMESPACE" "$MYSQL_POD" -- bash -c "
  mysql -u root -p\"\$MYSQL_ROOT_PASSWORD\" $DB_NAME -e \"
  DELETE FROM users WHERE email='$EMAIL';
  INSERT INTO users (first_name, last_name, national_id, email, password_hash, age, gender, subscription, role, created_at)
  VALUES ('$FIRST_NAME', '$LAST_NAME', '$NATIONAL_ID', '$EMAIL', '$HASH', $AGE, '$GENDER', '$SUBSCRIPTION', '$ROLE', NOW());
  SELECT id, email, role, created_at FROM users WHERE email='$EMAIL';\"
  "
}

# --- FUNCTION FOR DOCKER COMPOSE ---
reset_user_docker() {
  echo "🔄 Resetting admin user in Docker Compose container..."

  docker exec -i shviki_fitness-db-1 bash -c "
  mysql -u root -p\"\$MYSQL_ROOT_PASSWORD\" $DB_NAME -e \"
  DELETE FROM users WHERE email='$EMAIL';
  INSERT INTO users (first_name, last_name, national_id, email, password_hash, age, gender, subscription, role, created_at)
  VALUES ('$FIRST_NAME', '$LAST_NAME', '$NATIONAL_ID', '$EMAIL', '$HASH', $AGE, '$GENDER', '$SUBSCRIPTION', '$ROLE', NOW());
  SELECT id, email, role, created_at FROM users WHERE email='$EMAIL';\"
  "
}

# --- MAIN EXECUTION ---
if kubectl get pod -n "$NAMESPACE" "$MYSQL_POD" &>/dev/null; then
  reset_user_k8s
elif docker ps --format '{{.Names}}' | grep -q "shviki_fitness-db-1"; then
  reset_user_docker
else
  echo "❌ Could not find running MySQL (neither in Kubernetes nor Docker)."
  echo "Please check your environment and try again."
  exit 1
fi

echo "✅ Admin reset complete."
