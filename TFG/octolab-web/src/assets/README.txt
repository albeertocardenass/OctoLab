OctoLab Desktop - v1.0
======================

INSTALACIÓN
-----------
1. Ejecuta OctoLabDesktop.exe directamente, no requiere instalación.
2. Si Windows muestra un aviso de seguridad, haz clic en "Más información" y luego en "Ejecutar de todas formas".

REQUISITOS
----------
- Windows 10 / 11 (64 bits)
- Almacenamiento Minimo "10Gb"
- Conexión a Internet para sincronizar tu progreso con la plataforma web
- Dependencia a Docker Desktop actualizado para la realización de los laboratorios practicos.
    - Instala "Docker Desktop" aquí ---> "https://docs.docker.com/desktop/setup/install/windows-install/"

USO
---
Inicia sesión con las mismas credenciales que usas en octolab.site.
Tu progreso, puntos y módulos desbloqueados se sincronizan automáticamente.

SOPORTE
-------
Web: https://octolab.site
Email: soporte@octolab.site


APP MODO LOCAL
--------------
Para una ejecución en Local hace falta ejecutar una serie de comandos para lanzar
la web, el servidor y la app desktop.

Requisitos previos:
  - MySQL activo en localhost:3306 (db: octolab, user: root, pass: octolab1234)
  - Docker Desktop abierto (para los labs)

Ejecutar en este orden (cada uno en una terminal separada):

-> Servidor:
   cd octolab-server\OctoLab.Server
   dotnet run    (escucha en http://localhost:5276)

-> Web:
   cd octolab-web
   pnpm start
   (disponible en http://localhost:4200)

-> App Desktop:
   Ejecutar directamente: octolab-desktop\dist\OctolabDesktop-local.exe
   (ya compilada, apunta a localhost:5276)