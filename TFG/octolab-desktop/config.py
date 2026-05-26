import os

# -- API Backend -------------------------------------------------------
API_BASE_URL    = os.getenv("OCTOLAB_API",  "http://localhost:5276")
WEB_BASE_URL    = os.getenv("OCTOLAB_WEB",  "http://localhost:4200")
API_LOGIN       = f"{API_BASE_URL}/api/Usuarios/login"
API_REGISTER    = f"{API_BASE_URL}/api/Auth/register"
API_VERIFY_CODE = f"{API_BASE_URL}/api/Temario/verificar-codigo"
API_PROGRESO    = f"{API_BASE_URL}/api/Temario/progreso"

# -- Docker ------------------------------------------------------------
KALI_IMAGE           = "octolab-kali:latest"          # imagen custom con todas las herramientas
KALI_BASE_IMAGE      = "kalilinux/kali-rolling"       # base para construir la imagen
METASPLOITABLE_IMAGE = "tleemcjr/metasploitable2"
KALI_CONTAINER       = "octolab-kali"
META_CONTAINER       = "octolab-metasploitable"
DOCKER_NETWORK       = "octolab-net"

# -- Quiz --------------------------------------------------------------
# Secreto compartido con el backend para verificar códigos de test
QUIZ_SECRET = os.getenv("OCTOLAB_QUIZ_SECRET", "octolab-quiz-s3cr3t-2026")

# -- App ---------------------------------------------------------------
APP_NAME    = "OctolabDesktop"
APP_VERSION = "1.0.0"
THEME       = "dark"   # "dark" | "light"

# -- Rutas locales -----------------------------------------------------
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR   = os.path.join(BASE_DIR, "assets")
IMAGES_DIR   = os.path.join(ASSETS_DIR, "images")
DOCKER_DIR   = os.path.join(BASE_DIR, "docker")
LOG_FILE     = os.path.join(BASE_DIR, "octolab.log")
SESSION_FILE = os.path.join(BASE_DIR, ".session")
THEME_FILE   = os.path.join(BASE_DIR, ".theme")
