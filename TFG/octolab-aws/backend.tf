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

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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

              apt-get update -y
              apt-get install -y wget awscli libicu70 nginx certbot python3-certbot-nginx

              wget https://dot.net/v1/dotnet-install.sh -O /tmp/dotnet-install.sh
              chmod +x /tmp/dotnet-install.sh
              /tmp/dotnet-install.sh --channel 10.0 --runtime aspnetcore --install-dir /usr/share/dotnet
              ln -sf /usr/share/dotnet/dotnet /usr/bin/dotnet

              mkdir -p /home/ubuntu/.aws
              cat > /home/ubuntu/.aws/credentials <<CREDS
              [default]
              aws_access_key_id=ASIAWOAC42RQ5XXAE53Y
              aws_secret_access_key=YbLRaqKtSVDVjOHc2jDq/vWSzkWgLMlYwBsgJe0J
              aws_session_token=IQoJb3JpZ2luX2VjELv//////////wEaCXVzLXdlc3QtMiJGMEQCIFtDwIlmavR67fEDE+Sm0xHwBLiyy3Sxmpsf5hqRMnwhAiANEWG+AK4dlnj3ocq5jQXeG0re4n6yddISS9pLxCOdHirAAgiE//////////8BEAEaDDQ0MjM4NzcxNTE2OSIMzcTY0lGLXk04o+sbKpQC07qFO9B7hdvR1Sjxnx4h20lYwQg1tKiJeaoPZ/m1ugXDW2V8clSVDfm5S4Q/98fjfNRjTWSCTRm3+e/JMDzYT62EBlmroK6ZCoVFvGIhljX+am1QlwVfh0nbWM/LPFOo2NKJ+t1zohD2ogldtv3G0b0OHnw1VaK2uBVltaA6a/vsNkXXcyYLkNQbDdgxLGriTb7ywIFDXdSBNWH4z/9oIZjLzK6Q8FDDvPY9FQwVYX+l1F/TsR0OrUBJVSTzkFUgLvNXIoedJdvk3KMSBWToo5eP8HJsHzlBU2u0fE+URv/fqZM/FfSYGfJPGVyer73/RKTJGZFCjPeIuDk76sEXrq9WHDO6CDiTxoSruA6039z8TTblMLn1j9EGOp4BfL0KF97ziNa0ZYiXyawBdsin2+R/aPUv9uUTEYH4WrVkYHUkIRSEA02hkP8kmtP//BI5MyVWiu/xFo5IsOpSxfj7CkTH4lcnBE5VyNri0XelTNuLXDSTbLM82MuXALD4xaVG7c1TZDbn1TE6EaT3I8yo2551Ok3gtZ1/iulFx0uCoCNvi0JcfZBmizir3DiS/Fiha1WnShElC2EiCRA=
              CREDS

              cat > /home/ubuntu/.aws/config <<CONFIG
              [default]
              region = us-east-1
              CONFIG

              chown -R ubuntu:ubuntu /home/ubuntu/.aws

              mkdir -p /app
              chmod 777 /app
              sudo -u ubuntu aws s3 cp s3://octolab.site/backend/ /app/ --recursive --region us-east-1

              cat > /etc/nginx/sites-available/api.octolab.site <<NGINX
              server {
                  listen 80;
                  server_name api.octolab.site;

                  location / {
                      if (\$request_method = 'OPTIONS') {
                          add_header 'Access-Control-Allow-Origin' '*';
                          add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
                          add_header 'Access-Control-Allow-Headers' '*';
                          add_header 'Content-Length' 0;
                          return 204;
                      }
                      proxy_pass http://localhost:5000;
                      proxy_http_version 1.1;
                      proxy_set_header Host \$host;
                      proxy_set_header X-Real-IP \$remote_addr;
                      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                      proxy_set_header X-Forwarded-Proto \$scheme;
                  }
              }
              NGINX

              ln -s /etc/nginx/sites-available/api.octolab.site /etc/nginx/sites-enabled/
              systemctl enable nginx
              systemctl start nginx

              sleep 10
              certbot --nginx -d api.octolab.site --non-interactive --agree-tos -m juanalbertito76@gmail.com

              cat > /etc/nginx/sites-available/api.octolab.site <<NGINX2
              server {
                  listen 80;
                  server_name api.octolab.site;

                  location / {
                      if (\$request_method = 'OPTIONS') {
                          add_header 'Access-Control-Allow-Origin' '*';
                          add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
                          add_header 'Access-Control-Allow-Headers' '*';
                          add_header 'Content-Length' 0;
                          return 204;
                      }
                      proxy_pass http://localhost:5000;
                      proxy_http_version 1.1;
                      proxy_set_header Host \$host;
                      proxy_set_header X-Real-IP \$remote_addr;
                      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                      proxy_set_header X-Forwarded-Proto \$scheme;
                  }
              }

              server {
                  listen 443 ssl;
                  server_name api.octolab.site;

                  location / {
                      if (\$request_method = 'OPTIONS') {
                          add_header 'Access-Control-Allow-Origin' '*';
                          add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
                          add_header 'Access-Control-Allow-Headers' '*';
                          add_header 'Content-Length' 0;
                          return 204;
                      }
                      proxy_pass http://localhost:5000;
                      proxy_http_version 1.1;
                      proxy_set_header Host \$host;
                      proxy_set_header X-Real-IP \$remote_addr;
                      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                      proxy_set_header X-Forwarded-Proto \$scheme;
                  }

                  ssl_certificate /etc/letsencrypt/live/api.octolab.site/fullchain.pem;
                  ssl_certificate_key /etc/letsencrypt/live/api.octolab.site/privkey.pem;
                  include /etc/letsencrypt/options-ssl-nginx.conf;
                  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
              }
              NGINX2

              systemctl reload nginx

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

resource "aws_eip" "backend_eip" {
  instance = aws_instance.backend_server.id
  domain   = "vpc"

  tags = {
    Name = "octolab-backend-eip"
  }
}

output "backend_api_url" {
  value       = "http://${aws_eip.backend_eip.public_ip}:5000"
  description = "La URL pública de la API del Backend"
}








