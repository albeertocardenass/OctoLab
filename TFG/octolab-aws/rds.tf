data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "rds_sg" {
  name        = "octolab-rds-sg"
  description = "Permitir trafico entrante al MySQL de OctoLab"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 3306
    to_port     = 3306
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

resource "aws_db_instance" "mysql_db" {
  allocated_storage     = 20
  max_allocated_storage = 100
  engine                = "mysql"
  engine_version        = "8.0"
  instance_class        = "db.t3.micro"
  db_name               = "octolab"
  username              = "root"
  password              = "octolab1234"
  parameter_group_name  = "default.mysql8.0"
  skip_final_snapshot   = true
  publicly_accessible   = true

  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  tags = {
    Name = "octolab-mysql-db"
  }
}

output "rds_endpoint" {
  value       = aws_db_instance.mysql_db.endpoint
  description = "La URL de tu nueva Base de Datos en AWS"
}