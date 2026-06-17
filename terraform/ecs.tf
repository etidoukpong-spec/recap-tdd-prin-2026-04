resource "aws_ecr_repository" "app_repo" {
  name                 = "etido-tdd-recap"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecs_cluster" "app_cluster" {
  name = "etido-tdd-cluster"
}