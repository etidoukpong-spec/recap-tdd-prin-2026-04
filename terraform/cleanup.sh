#!/usr/bin/env bash
set -e

SERVICE_EXISTS=$(aws ecs list-services --cluster etido-tdd-cluster-v2 --region eu-west-2 --query "serviceArns[?contains(@, 'etido-tdd-recap-363b')]" --output text 2>/dev/null)

if [ -n "$SERVICE_EXISTS" ] && [ "$SERVICE_EXISTS" != "None" ]; then
  echo "Found stale service. Forcing deletion..."
  aws ecs delete-service --cluster etido-tdd-cluster-v2 --service etido-tdd-recap-363b --force --region eu-west-2
  
  aws ecs wait services-inactive --cluster etido-tdd-cluster-v2 --services etido-tdd-recap-363b --region eu-west-2
else
  echo "No stale service detected. Proceeding safely."
fi