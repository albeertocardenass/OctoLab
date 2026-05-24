resource "aws_key_pair" "octolab_key" {
  key_name   = "octolab-key"
  public_key = file("~/.ssh/octolab-key.pub")
}

resource "aws_security_group" "backend_sg" {
  name        = "octolab-backend-sg"
  description = "Permitir trafico entrante al Backend de OctoLab"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "backend_server" {
  ami           = "ami-0c7217cdde317cfec"
  instance_type = "t3.micro"
  key_name      = aws_key_pair.octolab_key.key_name

  vpc_security_group_ids = [aws_security_group.backend_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io awscli
              systemctl start docker
              systemctl enable docker
              aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 442387715169.dkr.ecr.us-east-1.amazonaws.com
              docker pull 442387715169.dkr.ecr.us-east-1.amazonaws.com/octolab-server-backend:latest
              docker run -d -p 5000:5000 \
                -e ConnectionStrings__DefaultConnection="Server=terraform-20260524183934351700000002.cjyuv9ydwwre.us-east-1.rds.amazonaws.com;Port=3306;Database=octolab;User=root;Password=octolab1234;" \
                -e Jwt__Key="Esta_Es_Una_Clave_Super_Secreta_De_Octolab_2024_🦈" \
                -e Stripe__SecretKey="sk_test_51TNsyoR897G8mIVm9JMsRVr4nQiK25WljPWV6d0m2qRzrtrhEsu1443mrvoRdPjJqtMePwtAJ977JRm22TLHTqC600gf5HQX54" \
                442387715169.dkr.ecr.us-east-1.amazonaws.com/octolab-server-backend:latest
              EOF

  tags = {
    Name = "octolab-backend-server"
  }
}

output "backend_api_url" {
  value       = "http://${aws_instance.backend_server.public_ip}:5000"
  description = "La URL pública de la API del Backend"
}