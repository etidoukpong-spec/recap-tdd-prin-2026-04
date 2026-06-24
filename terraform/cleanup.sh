#!/usr/bin/env bash
set -e

SERVICE_EXISTS=$(aws ecs list-services --cluster etido-tdd-cluster-v2 --region eu-west-2 --query "serviceArns[?contains(@, 'etido-tdd-recap-363b')]" --output text 2>/dev/null)

if [ -n "$SERVICE_EXISTS" ] && [ "$SERVICE_EXISTS" != "None" ]; then
    echo "Found stale service. Forcing deletion..."

    aws ecs delete-express-gateway-service --cluster etido-tdd-cluster-v2 --service etido-tdd-recap-363b --force --region eu-west-2

    echo "Waiting for Express service to turn INACTIVE..."

    while aws ecs list-services --cluster etido-tdd-cluster-v2 --region eu-west-2 --query "serviceArns[?contains(@, 'etido-tdd-recap-363b')]" --output text | grep -q "etido-tdd-recap-363b"; do
        echo "Still deleting... sleeping for 5 seconds..."
        sleep 5
    done
        echo "Express service deleted successfully."
  
else
    echo "No stale service detected. Proceeding safely."
fi