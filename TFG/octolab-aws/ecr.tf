resource "aws_ecr_repository" "octolab_backend" {
  name                 = "octolab-server-backend"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = "Production"
    Project     = "OctoLab"
  }
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.octolab_backend.repository_url
  description = "La URL de tu ECR para subir el contenedor (.NET)"
}