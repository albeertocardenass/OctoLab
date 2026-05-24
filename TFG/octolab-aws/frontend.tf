# 1. El bucket para los archivos de Angular
resource "aws_s3_bucket" "frontend_bucket" {
  bucket        = "octolab-web-frontend-prod-tfg" 
  force_destroy = true                            
}

# 2. Configuración de alojamiento web estático
resource "aws_s3_bucket_website_configuration" "frontend_web_config" {
  bucket = aws_s3_bucket.frontend_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

# 3. Permitir el acceso público en el bucket
resource "aws_s3_bucket_public_access_block" "frontend_public_block" {
  bucket = aws_s3_bucket.frontend_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# 4. Política de lectura pública para que internet pueda cargar la web
resource "aws_s3_bucket_policy" "frontend_policy" {
  depends_on = [aws_s3_bucket_public_access_block.frontend_public_block]
  bucket     = aws_s3_bucket.frontend_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend_bucket.arn}/*"
      }
    ]
  })
}

# Output: La URL real para abrir vuestro frontend
output "s3_website_url" {
  value       = aws_s3_bucket_website_configuration.frontend_web_config.website_endpoint
  description = "La URL pública para acceder a la aplicación Angular"
}