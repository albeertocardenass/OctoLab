import os


API_BASE_URL    = os.getenv("OCTOLAB_API", "https://api.octolab.site")
WEB_BASE_URL    = os.getenv("OCTOLAB_WEB",  "https://octolab.site")
API_LOGIN       = f"{API_BASE_URL}/api/Usuarios/login"
API_REGISTER    = f"{API_BASE_URL}/api/Auth/register"
API_VERIFY_CODE = f"{API_BASE_URL}/api/Temario/verificar-codigo"
API_PROGRESO    = f"{API_BASE_URL}/api/Temario/progreso"


KALI_IMAGE           = "octolab-kali:latest"          
KALI_BASE_IMAGE      = "kalilinux/kali-rolling"       
META_IMAGE           = "octolab-meta:latest"          
META_BASE_IMAGE      = "tleemcjr/metasploitable2"     
METASPLOITABLE_IMAGE = META_IMAGE                     
KALI_CONTAINER       = "octolab-kali"
META_CONTAINER       = "octolab-metasploitable"
DOCKER_NETWORK       = "octolab-net"



QUIZ_SECRET = os.getenv("OCTOLAB_QUIZ_SECRET", "octolab-quiz-s3cr3t-2026")


APP_NAME    = "OctolabDesktop"
APP_VERSION = "1.0.0"
THEME       = "dark"   


BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR   = os.path.join(BASE_DIR, "assets")
IMAGES_DIR   = os.path.join(ASSETS_DIR, "images")
DOCKER_DIR   = os.path.join(BASE_DIR, "docker")
LOG_FILE     = os.path.join(BASE_DIR, "octolab.log")
SESSION_FILE = os.path.join(BASE_DIR, ".session")
THEME_FILE   = os.path.join(BASE_DIR, ".theme")
