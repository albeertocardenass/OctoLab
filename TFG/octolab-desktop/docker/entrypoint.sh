#!/bin/bash
# OctoLab Kali — Script de inicio
# Se ejecuta al arrancar el contenedor e iniciar los servicios necesarios
# para que Metasploit funcione con base de datos.


service postgresql start >/dev/null 2>&1 || true


FLAG=/root/.msf4/.db_initialized
if [ ! -f "$FLAG" ]; then
    echo "[OctoLab] Inicializando base de datos de Metasploit..."
    mkdir -p /root/.msf4
    msfdb init >/dev/null 2>&1 && touch "$FLAG" && \
        echo "[OctoLab] Base de datos lista." || \
        echo "[OctoLab] Advertencia: msfdb init falló (se reintentará)."
fi


exec "$@"
