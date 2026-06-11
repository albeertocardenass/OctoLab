# OctoLab

***Trabajo de final de grado (2ºASIR) - OctoLab***

OctoLab es una plataforma educativa orientada a la ciberseguridad, desarrollada como Trabajo de Fin de Grado de Grado Superior en Administración de Sistemas Informáticos en Red (ASIR). Permite a los usuarios acceder a temarios de ciberseguridad, completar módulos interactivos, acumular puntos Octo y participar en una comunidad. Incluye **SharHack**, una aplicación de escritorio descargable desde la web donde el usuario puede practicar ataques reales con máquinas Kali Linux y Metasploitable en un entorno controlado.

---

## Autores

| Nombre | Github |
| ------ | ------ |
| Juan Alberto Campaña Espejo | [@jace7867](https://github.com/jace7867) |
| Alberto Cárdenas Palomo | [@albeertocardenass](https://github.com/albeertocardenass) |

---

## Información Académica

- **Ciclo Formativo:** Administración de Sistemas Informáticos en Red (ASIR)
- **Centro educativo:** IES Miguel Romero Esteo
- **Curso académico:** 2025/2026

---

## Descripción

OctoLab consta de dos componentes grandes:

- **Web (octolab.site):** Plataforma web accesible desde cualquier navegador (Recomendación: Chrome). Incluye temario de ciberseguridad en PDF, sistemas de puntos Octo, comunidad con publicaciones y likes, donaciones con Stripe y noticias.

- **SharHack:** Aplicación de escritorio descargable desde la web. Permite practicar los conocimientos adquiridos en los temas de la web, utilizando máquinas virtuales Kali Linux y Metasploitable en un entorno controlado.

---

## Tecnologías utilizadas

### Frontend
- Angular + TypeScript
- HTML + CSS

### Backend
- ASP.NET Core (.NET 10)
- Entity Framework Core
- JWT Authentication
- Stripe

### Base de datos
- MySQL 8.0 (Amazon RDS en producción / local en desarrollo)

### Infraestructura
- Amazon Web Services (EC2, S3, RDS)
- Terraform (Infrastructure as Code)
- Nginx + Let's Encrypt SSL
- Cloudflare (HTTPS, WAF, DNS, SSL/TLS)

### Aplicación
- Pyhton
- Docker (Kali Linux + Metasploitable)

---

## Modelo Relacional

<img width="728" height="641" alt="Modelo Relacional drawio" src="https://github.com/user-attachments/assets/cc99f91a-d9bf-4711-a865-75176abc0aad" />

---

## Ejecución en local

### Requisitos Previos

- [.NET 10 SDK](https://dotnet.microsoft.com/es-es/download/dotnet/10.0)
- [Node.js](https://nodejs.org/es) + [pnpm](https://pnpm.io/) (`npm install -g pnpm`)
- [Angular CLI](https://angular.dev/tools/cli) (`npm install -g @angular/cli`)
- [MySQL 8.0](https://dev.mysql.com/downloads/installer/) con:
  - Puerto: `3306`
  - Usuario: `root`
  - Contraseña: `octolab1234`

> **IMPORTANTE:** Se requiere la instalación de MySQL para un correcto funcionamiento.
 
### Pasos

**1. Clonar el repositorio**
```bash 
git clone https://github.com/albeertocardenass/OctoLab.git
```

**2. Arrancar el backend**
```bash
cd octolab-server/OctoLab.Server
dotnet run
```
> La base de datos se crea automáticamente.

**3. Arrancar el frontend** (en otra terminal)
```bash
cd octolab-web
pnpm install
ng serve
```
**4. Abrir la App Desktop**

Descarga `OctolabDesktop-local.exe` desde [GitHub Releases](https://github.com/albeertocardenass/OctoLab/releases/tag/v1.0.0) y ejecútala directamente.

> Apunta automáticamente a localhost:5276

**5. Abrir el navegador**
```
http://localhost:4200
```

### Credenciales de prueba

| Email | Contraseña | Rol |
| ----- | ---------- | --- |
| `paco@prueba.com` | `1234` | Admin |
| `jace123@octolab.com` | `123456` | Admin |
| `cardenasboy123@octolab.com` | `123456` | Admin |

---


## Tutorial de uso

### OctoLab Web

**1. Inicio de sesión**
<img width="1919" height="946" alt="image" src="https://github.com/user-attachments/assets/7b9ec9f4-31a9-42dd-a565-e332f6ac0012" />

**2. Registro de usuario**
<img width="1915" height="945" alt="image" src="https://github.com/user-attachments/assets/92a3f35f-5dcc-48c4-bf29-124b96e85d1f" />

**3. Página de inicio**
<img width="1917" height="942" alt="image" src="https://github.com/user-attachments/assets/f9ff3642-a4d7-4015-9e7e-0d477e5b83fe" />

**4. Temario**
<img width="1918" height="946" alt="image" src="https://github.com/user-attachments/assets/d63ca3b9-2665-4db9-950d-538440a7afdd" />

<img width="1919" height="942" alt="image" src="https://github.com/user-attachments/assets/3d83a00d-ec8b-47f4-a6cb-9a5f4945111b" />


**5. Comunidad**
<img width="1918" height="942" alt="image" src="https://github.com/user-attachments/assets/bfa95026-d486-47b9-9ba9-be1be62be489" />

**6. Donaciones**
<img width="620" height="657" alt="image" src="https://github.com/user-attachments/assets/de14a23c-e3a7-4b7b-8e44-ae7770bfcee0" />

**7. Sobre nosotros**
<img width="893" height="944" alt="image" src="https://github.com/user-attachments/assets/1c65924b-f5b3-4808-a6f9-6cbe67a6d0ef" />

**8. Configuración de cuenta**
<img width="1917" height="945" alt="image" src="https://github.com/user-attachments/assets/555117d9-683b-41ab-9617-82dc72a4d2fc" />

**9. Panel de administración**
<img width="1917" height="933" alt="image" src="https://github.com/user-attachments/assets/950e7221-171e-4313-a1a1-db38fb5d7174" />

> El panel de administración permite borrar mensajes, usuarios y asignar el rol de administrador a otros usuarios.

---

### OctoLab Desktop

**1. Inicio de la aplicación**
<img width="1182" height="856" alt="image" src="https://github.com/user-attachments/assets/0a2dca92-343b-45fb-bae7-65d586b72574" />

**2. Requisitos del sistema**
<img width="674" height="652" alt="image" src="https://github.com/user-attachments/assets/3a9fde02-bad3-425e-bee0-1d49082c3330" />

**3. Bienvenida**
<img width="1918" height="1032" alt="image" src="https://github.com/user-attachments/assets/d2663f54-2ea5-4461-8098-815f34631665" />

**4. Laboratorios**
<img width="1918" height="1031" alt="image" src="https://github.com/user-attachments/assets/c950d60b-5e08-4d84-a9ea-58a5c91f90b3" />

**5. Laboratorio iniciado**
<img width="1918" height="611" alt="image" src="https://github.com/user-attachments/assets/2ff8fa08-4653-4885-acd4-2744acb0be9a" />

<img width="623" height="509" alt="image" src="https://github.com/user-attachments/assets/a96a8f8f-3072-4619-91b2-12168ea509ac" />

> El código hexadecimal es aleatorio, para cada usuario y tema es diferente.

<img width="622" height="511" alt="image" src="https://github.com/user-attachments/assets/810b5da8-96fe-426b-ace1-3d079daad816" />



**6. Configuración**
<img width="1919" height="495" alt="image" src="https://github.com/user-attachments/assets/262109d9-c6ac-4a78-856a-c2a7da26d676" />




## URL de producción

**[https://octolab.site](https://octolab.site)**

---

## Vídeo

---

## Bibliografía
- OWASP Foundation WebGoat Project https://owasp.org/www-project-webgoat/
- OWASP Foundation OWASP Top 10 https://owasp.org/www-project-top-ten/
- Microsoft Documentación de ASP.NET Core https://learn.microsoft.com/es-es/aspnet/core/?view=aspnetcore-10.0
- Microsoft Documentación de Entity Framework Core https://learn.microsoft.com/es-es/ef/core/
- Google Documentación de Angular https://angular.dev/overview
- Amazon Web Services Documentación de AWS https://docs.aws.amazon.com/
- HashiCorp Documentación de Terraform https://developer.hashicorp.com/terraform/docs
- MySQL Documentación de MySQL 8.0 https://dev.mysql.com/doc/refman/8.0/en/
- Cloudflare Documentación de Cloudflare WAF https://developers.cloudflare.com/waf/
- Let’s Encrypt Documentación de la API de Stripe https://docs.stripe.com/api
- DVWA https://github.com/digininja/DVWA
- Nginx https://nginx.org/en/docs/
- OpenWebinars https://openwebinars.net/
- Docker https://docs.docker.com/
- Python https://docs.python.org/es/3/
