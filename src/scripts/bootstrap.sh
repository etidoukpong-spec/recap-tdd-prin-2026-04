#!/bin/bash
set -e

if ! aws iam get-role --role-name EtidoTddRecapRole >/dev/null 2>&1; then
  aws iam create-role \
    --role-name EtidoTddRecapRole \
    --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::261219435789:oidc-provider/token.actions.githubusercontent.com"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
          "StringLike": { "token.actions.githubusercontent.com:sub": "repo:etidoukpong-spec/recap-tdd-prin-2026-04:*" }
        }
      }]
    }'
    
  aws iam attach-role-policy \
    --role-name EtidoTddRecapRole \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
fi

if ! aws s3api head-bucket --bucket etido-tdd-tf-state >/dev/null 2>&1; then
  aws s3api create-bucket \
    --bucket etido-tdd-tf-state \
    --region eu-west-2 \
    --create-bucket-configuration LocationConstraint=eu-west-2
fi
