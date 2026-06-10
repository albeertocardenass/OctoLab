@echo off
echo Compilando OctolabDesktop (LOCAL)...
pyinstaller OctolabDesktop-local.spec --clean
echo.
echo Listo: dist\OctolabDesktop-local.exe  ->  localhost:5276
