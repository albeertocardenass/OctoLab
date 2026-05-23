import hashlib
import time

def generar_codigo_hex(usuario_id: int, tema_id: int) -> str:
    """Genera un código hex único por usuario y tema."""
    raw = f"{usuario_id}-{tema_id}-{int(time.time() // 86400)}-octolab"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()
