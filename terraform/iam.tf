resource "aws_iam_role" "admin_role" {
  name = "EtidoTddRecapRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = "arn:aws:iam::261219435789:oidc-provider/token.actions.githubusercontent.com"
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:etidoukpong-spec/recap-tdd-prin-2026-04:*"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "admin_role_policy" {
  role       = aws_iam_role.admin_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_role" "express_infrastructure_role" {
  name = "ecsInfrastructureRoleForExpressServices"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# Commentted out blocks in this policy loosen it 
# by removing the AmazonECSManaged requirement
# to allow express mode to provisioned 
# with minimal terraform in `network.tf`
resource "aws_iam_policy" "express_policy" {
  name = "ecs-express-infrastructure-policy"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "ServiceLinkedRoleCreateOperations",
        "Effect" : "Allow",
        "Action" : "iam:CreateServiceLinkedRole",
        "Resource" : "*",
        "Condition" : {
          "StringEquals" : {
            "iam:AWSServiceName" : [
              "ecs.application-autoscaling.amazonaws.com",
              "elasticloadbalancing.amazonaws.com"
            ]
          }
        }
      },
      {
        "Sid" : "ELBOperations",
        "Effect" : "Allow",
        "Action" : [
          "elasticloadbalancing:CreateListener",
          "elasticloadbalancing:CreateLoadBalancer",
          "elasticloadbalancing:CreateRule",
          "elasticloadbalancing:CreateTargetGroup",
          "elasticloadbalancing:ModifyListener",
          "elasticloadbalancing:ModifyRule",
          "elasticloadbalancing:AddListenerCertificates",
          "elasticloadbalancing:RemoveListenerCertificates",
          "elasticloadbalancing:RegisterTargets",
          "elasticloadbalancing:DeregisterTargets",
          "elasticloadbalancing:DeleteTargetGroup",
          "elasticloadbalancing:DeleteLoadBalancer",
          "elasticloadbalancing:DeleteRule",
          "elasticloadbalancing:DeleteListener"
        ],
        "Resource" : [
          "arn:aws:elasticloadbalancing:*:*:loadbalancer/app/*/*",
          "arn:aws:elasticloadbalancing:*:*:listener/app/*/*/*",
          "arn:aws:elasticloadbalancing:*:*:listener-rule/app/*/*/*/*",
          "arn:aws:elasticloadbalancing:*:*:targetgroup/*/*"
        ],
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:ResourceTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "TagOnCreateELBResources",
        "Effect" : "Allow",
        "Action" : "elasticloadbalancing:AddTags",
        "Resource" : [
          "arn:aws:elasticloadbalancing:*:*:loadbalancer/app/*/*",
          "arn:aws:elasticloadbalancing:*:*:listener/app/*/*/*",
          "arn:aws:elasticloadbalancing:*:*:listener-rule/app/*/*/*/*",
          "arn:aws:elasticloadbalancing:*:*:targetgroup/*/*"
        ],
        "Condition" : {
          "StringEquals" : {
            "elasticloadbalancing:CreateAction" : [
              "CreateLoadBalancer",
              "CreateListener",
              "CreateRule",
              "CreateTargetGroup"
            ]
          }
        }
      },
      {
        "Sid" : "BlanketAllowCreateSecurityGroupsInVPCs",
        "Effect" : "Allow",
        "Action" : "ec2:CreateSecurityGroup",
        "Resource" : "arn:aws:ec2:*:*:vpc/*"
      },
      {
        "Sid" : "CreateSecurityGroupResourcesWithTags",
        "Effect" : "Allow",
        "Action" : [
          "ec2:CreateSecurityGroup",
          "ec2:AuthorizeSecurityGroupEgress",
          "ec2:AuthorizeSecurityGroupIngress"
        ],
        "Resource" : [
          "arn:aws:ec2:*:*:security-group/*",
          "arn:aws:ec2:*:*:security-group-rule/*",
          "arn:aws:ec2:*:*:vpc/*"
        ],
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:RequestTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "ModifySecurityGroupOperations",
        "Effect" : "Allow",
        "Action" : [
          "ec2:AuthorizeSecurityGroupEgress",
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:DeleteSecurityGroup",
          "ec2:RevokeSecurityGroupEgress",
          "ec2:RevokeSecurityGroupIngress"
        ],
        "Resource" : [
          "arn:aws:ec2:*:*:security-group/*",
          "arn:aws:ec2:*:*:vpc/*"
        ],
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:ResourceTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "TagOnCreateEC2Resources",
        "Effect" : "Allow",
        "Action" : "ec2:CreateTags",
        "Resource" : [
          "arn:aws:ec2:*:*:security-group/*",
          "arn:aws:ec2:*:*:security-group-rule/*"
        ],
        "Condition" : {
          "StringEquals" : {
            "ec2:CreateAction" : [
              "CreateSecurityGroup",
              "AuthorizeSecurityGroupIngress",
              "AuthorizeSecurityGroupEgress"
            ]
          }
        }
      },
      {
        "Sid" : "CertificateOperations",
        "Effect" : "Allow",
        "Action" : [
          "acm:RequestCertificate",
          "acm:AddTagsToCertificate",
          "acm:DeleteCertificate",
          "acm:DescribeCertificate"
        ],
        "Resource" : [
          "arn:aws:acm:*:*:certificate/*"
        ],
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:ResourceTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "ApplicationAutoscalingCreateOperations",
        "Effect" : "Allow",
        "Action" : [
          "application-autoscaling:RegisterScalableTarget",
          "application-autoscaling:TagResource",
          "application-autoscaling:DeregisterScalableTarget"
        ],
        "Resource" : [
          "arn:aws:application-autoscaling:*:*:scalable-target/*"
        ],
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:ResourceTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "ApplicationAutoscalingPolicyOperations",
        "Effect" : "Allow",
        "Action" : [
          "application-autoscaling:PutScalingPolicy",
          "application-autoscaling:DeleteScalingPolicy"
        ],
        "Resource" : [
          "arn:aws:application-autoscaling:*:*:scalable-target/*"
        ],
        "Condition" : {
          "StringEquals" : {
            "application-autoscaling:service-namespace" : "ecs"
          }
        }
      },
      {
        "Sid" : "ApplicationAutoscalingReadOperations",
        "Effect" : "Allow",
        "Action" : [
          "application-autoscaling:DescribeScalableTargets",
          "application-autoscaling:DescribeScalingPolicies",
          "application-autoscaling:DescribeScalingActivities"
        ],
        "Resource" : [
          "arn:aws:application-autoscaling:*:*:scalable-target/*"
        ]
      },
      {
        "Sid" : "CloudWatchAlarmCreateOperations",
        "Effect" : "Allow",
        "Action" : [
          "cloudwatch:PutMetricAlarm",
          "cloudwatch:TagResource"
        ],
        "Resource" : [
          "arn:aws:cloudwatch:*:*:alarm:*"
        ],
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:RequestTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "CloudWatchAlarmOperations",
        "Effect" : "Allow",
        "Action" : [
          "cloudwatch:DeleteAlarms",
          "cloudwatch:DescribeAlarms"
        ],
        "Resource" : [
          "arn:aws:cloudwatch:*:*:alarm:*"
        ],
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:ResourceTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "ELBReadOperations",
        "Effect" : "Allow",
        "Action" : [
          "elasticloadbalancing:DescribeLoadBalancers",
          "elasticloadbalancing:DescribeTargetGroups",
          "elasticloadbalancing:DescribeTargetHealth",
          "elasticloadbalancing:DescribeListeners",
          "elasticloadbalancing:DescribeRules"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "VPCReadOperations",
        "Effect" : "Allow",
        "Action" : [
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeSubnets",
          "ec2:DescribeRouteTables",
          "ec2:DescribeVpcs"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "CloudWatchLogsCreateOperations",
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:TagResource"
        ],
        "Resource" : "arn:aws:logs:*:*:log-group:*",
        # "Condition" : {
        #   "StringEquals" : {
        #     "aws:RequestTag/AmazonECSManaged" : "true"
        #   }
        # }
      },
      {
        "Sid" : "CloudWatchLogsReadOperations",
        "Effect" : "Allow",
        "Action" : [
          "logs:DescribeLogGroups"
        ],
        "Resource" : "*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "express_attachment" {
  role       = aws_iam_role.express_infrastructure_role.name
  policy_arn = aws_iam_policy.express_policy.arn
}

resource "aws_iam_role" "execution_role" {
  name        = "ecsTaskExecutionRole"
  description = "Allows ECS tasks to call AWS services on your behalf."
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [{
      "Sid" : "",
      "Effect" : "Allow",
      "Principal" : {
        "Service" : [
          "ecs-tasks.amazonaws.com",
          "ecs.amazonaws.com"
        ]
      },
      "Action" : "sts:AssumeRole"
      "Condition" : {
        "ArnLike" : {
          "aws:SourceArn" : "arn:aws:ecs:eu-west-2:261219435789:*"
        },
        "StringEquals" : {
          "aws:SourceAccount" : "261219435789"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "execution_role_attachment" {
  role       = aws_iam_role.execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}