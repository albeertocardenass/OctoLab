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

$backendUrl = terraform output -raw backend_api_url
$ip = $backendUrl -replace "http://", "" -replace ":5000", ""

Set-Content $apiConfig "export const API_BASE = 'http://$ip`:5000';"

Set-Location $serverDir
dotnet publish -c Release -o ./publish
aws s3 cp ./publish s3://octolab-web-frontend-prod-tfg/backend/ --recursive

Set-Location $webDir
pnpm build
aws s3 sync ".\dist\octolab-web\browser" s3://octolab-web-frontend-prod-tfg --delete
aws s3 cp ".\dist\octolab-web\browser\index.csr.html" s3://octolab-web-frontend-prod-tfg/index.html

Write-Host "Despliegue completado."
Write-Host "Frontend: http://octolab-web-frontend-prod-tfg.s3-website-us-east-1.amazonaws.com"
Write-Host "Backend: $backendUrl"
Write-Host "Espera 10 minutos para que EC2 arranque el servidor."