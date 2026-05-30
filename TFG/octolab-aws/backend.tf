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
              exec > /var/log/octolab-startup.log 2>&1

              # Instalar dependencias
              apt-get update -y
              apt-get install -y wget awscli libicu70

              # Instalar .NET 10 con el script oficial
              wget https://dot.net/v1/dotnet-install.sh -O /tmp/dotnet-install.sh
              chmod +x /tmp/dotnet-install.sh
              /tmp/dotnet-install.sh --channel 10.0 --runtime aspnetcore --install-dir /usr/share/dotnet
              ln -sf /usr/share/dotnet/dotnet /usr/bin/dotnet

              # Configurar credenciales AWS para ubuntu
              mkdir -p /home/ubuntu/.aws
              cat > /home/ubuntu/.aws/credentials <<CREDS
              [default]
              aws_access_key_id=ASIAWOAC42RQXCK362L6
              aws_secret_access_key=ikqzGpDedKqrf/8GsJaxNxqeQlmV8Nu25+5M7VNw
              aws_session_token=IQoJb3JpZ2luX2VjEBQaCXVzLXdlc3QtMiJGMEQCIAlVhzySAxobItiFeo4VWiZwsN9/y8bmyNsbQQI1bIHjAiBOBg6gxYzTZNvZ6IfUudC0JO0hyzzMJfHif/ljkVOywCrAAgjd//////////8BEAEaDDQ0MjM4NzcxNTE2OSIMcwCQE8jsE1dgKU5rKpQCfDsB0jQYRLiZ6dMRXG1htMM9YBLAxl4xA5OTh/T34TXemdO8jhCBCIdeHh8tLHnV+Ab3HqJVuyTjKlusnCHJ8KkVtq6kihpHU13R5T3+R02G8h+uEcCf0/mArq7VNoDwDvwqjRcvisDVcjl93Ebw36U7ATiy/3orkx+pPQjr6fq60Sy1mOA4aKTDtbZjzAdD8VjQX/TEmzknwbiZDGMn5dqKudEv9QempwarV32XrKjbc+nKGqHhahoR0zUpunYFqlQMvsNg2YXpSlSRKlEb90OL4a2S2L2Gp/8jTZ9WFf0T218EktjT0OsTUjGJUko1n+Q32mq+MSJST/OGXGf4O95pL2+UeDZPp6pSr7oalBIip7SZMLmR69AGOp4Bw/zrzeuyTmv1lTyy/32Bsy7hQSlBBvf9opgnqQ6vvLlxQ07RjiEX9TnHYiS60FNN1fc5nyVqaSXEIfTyTG5PzTURRExQKVVaQMLQuiKHuIA418b+aEjksJwPskMuuPsiAj9uhxFicykspZvJXyVEoT62e9EN97+N/AZ3LSUNWFGhSVXeuns4vQ/IVYO0ayEvNCO/S9b9OVV0QbgS1A4=
              CREDS

              cat > /home/ubuntu/.aws/config <<CONFIG
              [default]
              region = us-east-1
              CONFIG

              chown -R ubuntu:ubuntu /home/ubuntu/.aws

              # Descargar backend desde S3
              mkdir -p /app
              chmod 777 /app
              sudo -u ubuntu aws s3 cp s3://octolab-web-frontend-prod-tfg/backend/ /app/ --recursive --region us-east-1

              # Crear servicio systemd
              cat > /etc/systemd/system/octolab.service <<SERVICE
              [Unit]
              Description=OctoLab Backend
              After=network.target

              [Service]
              WorkingDirectory=/app
              Environment="ASPNETCORE_URLS=http://+:5000"
              Environment="ConnectionStrings__DefaultConnection=Server=terraform-20260524183934351700000002.cjyuv9ydwwre.us-east-1.rds.amazonaws.com;Port=3306;Database=octolab;User=root;Password=octolab1234;"
              Environment="Jwt__Key=M2Y0YjU2N2UtYTg5Yi00YTMzLTkxZTUtNzVlOTk0M2I0MmUxN2M5YThkZTItZTg0Mi00YmU0LWJhM2EtM2Y0YjU2N2U="
              Environment="Stripe__SecretKey=sk_test_51TNsyoR897G8mIVm9JMsRVr4nQiK25WljPWV6d0m2qRzrtrhEsu1443mrvoRdPjJqtMePwtAJ977JRm22TLHTqC600gf5HQX54"
              ExecStart=/usr/share/dotnet/dotnet /app/OctoLab.Server.dll
              Restart=always
              RestartSec=10
              User=ubuntu

              [Install]
              WantedBy=multi-user.target
              SERVICE

              systemctl daemon-reload
              systemctl enable octolab
              systemctl start octolab
              EOF

  user_data_replace_on_change = true

  tags = {
    Name = "octolab-backend-server"
  }
}

output "backend_api_url" {
  value       = "http://${aws_instance.backend_server.public_ip}:5000"
  description = "La URL pública de la API del Backend"
}