# OctolabWeb

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.1.3.

> **Este proyecto usa [pnpm](https://pnpm.io/) como gestor de paquetes.** No uses `npm install` ni `yarn` — usa siempre `pnpm`.

## Instalación

### 1. Instalar pnpm

Este proyecto ha migrado de npm a pnpm por razones de seguridad. Instala pnpm antes de continuar.

**Windows (recomendado via winget):**
```powershell
winget install pnpm.pnpm
```

**macOS / Linux:**
```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

**Alternativa (via Node.js Corepack, incluido con Node.js 16+):**
```bash
corepack enable pnpm
```

Verifica la instalación:
```bash
pnpm --version
```

### 2. Instalar dependencias del proyecto

```bash
pnpm install
```

### Migrar desde npm (si ya tienes node_modules instalado con npm)

Si tienes el proyecto instalado con npm, sigue estos pasos:

```bash
# 1. Elimina los archivos de npm
rm -rf node_modules
rm package-lock.json

# 2. Instala con pnpm
pnpm install
```

En Windows (PowerShell):
```powershell
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
pnpm install
```

---

## Development server

To start a local development server, run:

```bash
pnpm start
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
pnpm ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
pnpm ng generate --help
```

## Building

To build the project run:

```bash
pnpm build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
pnpm test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
pnpm ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Referencia de comandos pnpm

| Acción | Comando |
|---|---|
| Instalar dependencias | `pnpm install` |
| Añadir una dependencia | `pnpm add <paquete>` |
| Añadir dependencia de desarrollo | `pnpm add -D <paquete>` |
| Eliminar una dependencia | `pnpm remove <paquete>` |
| Actualizar dependencias | `pnpm update` |
| Ejecutar un script | `pnpm run <script>` |

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
