param(
    [Parameter(Mandatory=$true)]
    [string]$AccessKeyId,
    
    [Parameter(Mandatory=$true)]
    [string]$SecretAccessKey,
    
    [Parameter(Mandatory=$true)]
    [string]$SessionToken
)

$env:AWS_ACCESS_KEY_ID = $AccessKeyId
$env:AWS_SECRET_ACCESS_KEY = $SecretAccessKey
$env:AWS_SESSION_TOKEN = $SessionToken
$env:AWS_DEFAULT_REGION = "us-east-1"

$repoRoot    = Split-Path -Parent $PSScriptRoot
$awsDir      = $PSScriptRoot
$webDir      = Join-Path $repoRoot "octolab-web"
$serverDir   = Join-Path $repoRoot "octolab-server\OctoLab.Server"
$backendTf   = Join-Path $awsDir "backend.tf"
$apiConfig   = Join-Path $webDir "src\app\services\api.config.ts"

$content = Get-Content $backendTf -Raw
$content = $content -replace 'aws_access_key_id=.*',     "aws_access_key_id=$AccessKeyId"
$content = $content -replace 'aws_secret_access_key=.*', "aws_secret_access_key=$SecretAccessKey"
$content = $content -replace 'aws_session_token=.*',     "aws_session_token=$SessionToken"
Set-Content $backendTf $content

Set-Location $awsDir
terraform apply -auto-approve

Set-Content $apiConfig "export const API_BASE = 'https://api.octolab.site';"

Set-Location $serverDir
dotnet publish -c Release -o ./publish
aws s3 cp ./publish s3://octolab.site/backend/ --recursive
aws s3 cp (Join-Path $serverDir "Resources\Pdfs") s3://octolab.site/backend/Resources/Pdfs/ --recursive

Set-Location $webDir
pnpm build
aws s3 sync ".\dist\octolab-web\browser" s3://octolab.site
aws s3 cp ".\dist\octolab-web\browser\index.csr.html" s3://octolab.site/index.html
aws s3 cp ".\dist\octolab-web\browser\assets\pdf.worker.min.mjs" s3://octolab.site/assets/pdf.worker.min.mjs --content-type "application/javascript"

Write-Host "Despliegue completado."
Write-Host "Frontend: https://octolab.site"
Write-Host "Espera 15 minutos para que EC2 arranque el servidor con Nginx y SSL."