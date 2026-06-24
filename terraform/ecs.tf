resource "terraform_data" "clean_stale_service" {
  provisioner "local-exec" {
    when    = create
    command = "${path.module}/cleanup.sh"
  }
}

resource "aws_ecr_repository" "app_repo" {
  name                 = "etido-tdd-recap"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  depends_on = [terraform_data.clean_stale_service]
}

resource "aws_ecs_cluster" "app_cluster" {
  name = "etido-tdd-cluster-v2"
}