@echo off
echo Compilando OctolabDesktop (PRODUCCION)...
pyinstaller OctolabDesktop.spec --clean
echo.
echo Listo: dist\OctolabDesktop.exe  ->  api.octolab.site
