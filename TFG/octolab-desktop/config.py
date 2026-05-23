import os

# -- API Backend -------------------------------------------------------
API_BASE_URL    = os.getenv("OCTOLAB_API", "http://localhost:5276")
API_LOGIN       = f"{API_BASE_URL}/api/Auth/login"
API_REGISTER    = f"{API_BASE_URL}/api/Auth/register"
API_VERIFY_CODE = f"{API_BASE_URL}/api/Temario/verificar-codigo"
API_PROGRESO    = f"{API_BASE_URL}/api/Temario/progreso"

# -- Docker ------------------------------------------------------------
KALI_IMAGE           = "kalilinux/kali-rolling"
METASPLOITABLE_IMAGE = "tleemcjr/metasploitable2"
KALI_CONTAINER       = "octolab-kali"
META_CONTAINER       = "octolab-metasploitable"
DOCKER_NETWORK       = "octolab-net"

# -- App ---------------------------------------------------------------
APP_NAME    = "OctolabDesktop"
APP_VERSION = "1.0.0"
THEME       = "dark"   # "dark" | "light"

# -- Rutas locales -----------------------------------------------------
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR   = os.path.join(BASE_DIR, "assets")
IMAGES_DIR   = os.path.join(ASSETS_DIR, "images")
LOG_FILE     = os.path.join(BASE_DIR, "octolab.log")
SESSION_FILE = os.path.join(BASE_DIR, ".session")
