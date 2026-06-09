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

**4. Abrir el navegador**
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


### Tutorial de uso

---

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
