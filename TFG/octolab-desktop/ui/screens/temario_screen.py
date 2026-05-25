"""
temario_screen.py — Grid de módulos + tests con código hex de validación.
"""
import customtkinter as ctk
import webbrowser
import random
from config import WEB_BASE_URL
from utils.crypto import generar_codigo_hex

# ── Paleta ───────────────────────────────────────────────────────────
C = {
    "primary":     "#4f46e5",
    "primary_hov": "#4338ca",
    "card":        ("white", "#1e293b"),
    "muted":       ("gray40", "#94a3b8"),
    "success":     "#10b981",
    "error":       "#ef4444",
    "divider":     ("gray80", "#334155"),
    "badge_lock":  ("gray78", "#334155"),
    "cost_bg":     ("gray88", "#334155"),
    "badge_ok_bg": ("#e0e7ff", "#312e81"),
}

# ── Módulos (id, titulo, desc, coste, recompensa) ────────────────────
MODULOS = [
    (1,  "Fundamentos de Ciberseguridad",     "Protección de sistemas, Tríada CIA e importancia en la era digital.",     180, 220),
    (2,  "Seguridad en Sistemas Operativos",  "Actualizaciones, parches, antivirus y gestión del menor privilegio.",      250, 280),
    (3,  "Redes y Seguridad de Redes",        "Protocolos TCP/IP, Firewalls, VPN, segmentación y Wi-Fi seguro.",          250, 280),
    (4,  "Ethical Hacking / Pentesting",      "Evaluación de resiliencia, simulacros y uso de Kali Linux o Metasploit.",  380, 420),
    (5,  "Análisis de Vulnerabilidades",      "Amenazas, vulnerabilidades, cálculo de riesgos y medidas de mitigación.",  320, 350),
    (6,  "Ingeniería Social",                 "Phishing, Vishing, Baiting y tácticas de manipulación psicológica.",       290, 310),
    (7,  "Seguridad Web",                     "Prevención de SQL Injection, XSS, CSRF y validación de entradas.",         340, 380),
    (8,  "Seguridad en Dispositivos Móviles", "Protección contra robo, malware, biometría y políticas BYOD/MDM.",         290, 310),
    (9,  "Criptografía Básica",               "Cifrado en reposo y tránsito, E2EE y certificados digitales (CA).",        380, 420),
    (10, "Seguridad en la Nube",              "Modelos SaaS, PaaS, IaaS, riesgos asociados y gobernanza IAM/SLA.",       320, 350),
    (11, "Respuesta ante Incidentes",         "Fases de respuesta, contención, recuperación y Regla de Backup 3-2-1.",    320, 350),
    (12, "Legalidad y Ética",                 "Cumplimiento del GDPR, principios éticos y diferencias de seguridad.",     260, 250),
]

# ── Preguntas (pregunta, [A,B,C,D], índice_correcto) ─────────────────
PREGUNTAS: dict[int, list] = {
    1: [
        ("¿Cuántos incidentes de ciberseguridad analizó ENISA entre julio 2023 y junio 2024?",
         ["8.432", "11.079", "15.234", "9.871"], 1),
        ("¿Qué significa la Triada CIA en ciberseguridad?",
         ["Código, Integridad, Autenticación",
          "Confidencialidad, Integridad, Disponibilidad",
          "Control, Identificación, Autorización",
          "Cifrado, Integridad, Acceso"], 1),
        ("Según ENISA 2024, ¿qué porcentaje de vulnerabilidades se clasificaron como críticas?",
         ["5,1 %", "7,8 %", "9,3 %", "12,4 %"], 2),
        ("¿Cómo se llamaba el organismo español de ciberseguridad antes de ser INCIBE?",
         ["CNPIC", "INTECO", "CCN-CERT", "CSIRT-ES"], 1),
        ("¿Cuál es la amenaza número 1 según el informe ENISA Threat Landscape 2024?",
         ["Ransomware", "Phishing", "DDoS / DoS", "Malware"], 2),
        ("¿Qué garantiza la 'Disponibilidad' en la triada CIA?",
         ["Solo los autorizados pueden leer los datos",
          "Los datos no han sido modificados",
          "El acceso a la información está garantizado cuando se necesita",
          "Los datos están cifrados en todo momento"], 2),
        ("¿Qué actor de ataque está motivado principalmente por fines ideológicos?",
         ["Cibercrimen", "Estado-nación", "Hacktivistas", "PSOA"], 2),
        ("¿Qué porcentaje de los ataques observados por ENISA 2024 fueron DDoS o ransomware?",
         ["+30 %", "+40 %", "+50 %", "+60 %"], 2),
        ("¿Con qué herramientas se implementa la Confidencialidad según el NIST?",
         ["Backups y alta disponibilidad",
          "Hashes y firmas digitales",
          "Cifrado, control de acceso y MFA",
          "Parches y actualizaciones"], 2),
        ("¿Cuántos CVEs reportó ENISA en el periodo julio 2023 – junio 2024?",
         ["14.205", "19.754", "22.100", "17.342"], 1),
    ],
    2: [
        ("En la arquitectura de anillos de protección x86, ¿qué reside en el Ring 0?",
         ["Aplicaciones de usuario", "Navegadores web", "El kernel", "Las shells"], 2),
        ("¿En qué archivo de Linux se almacenan las contraseñas hasheadas de los usuarios?",
         ["/etc/passwd", "/etc/shadow", "/etc/group", "/etc/users"], 1),
        ("En Linux, ¿qué UID corresponde al usuario root?",
         ["100", "500", "1000", "0"], 3),
        ("En Windows, ¿cómo termina el SID del usuario Administrador integrado?",
         ["-100", "-300", "-500", "-1000"], 2),
        ("¿Qué representa el valor octal 755 en permisos POSIX?",
         ["rwxr-xr-x", "rwxrwxrwx", "rw-r--r--", "rwx------"], 0),
        ("¿Qué serie CCN-STIC aplica al bastionado de sistemas RHEL / Linux?",
         ["STIC-619", "STIC-642", "STIC-700", "STIC-815"], 1),
        ("¿Qué cuenta de Windows tiene el nivel de privilegio equivalente al kernel local?",
         ["Administrator", "Guest", "SYSTEM", "DefaultAccount"], 2),
        ("¿Qué modo de cifrado AES combina cifrado y autenticación en una sola operación?",
         ["ECB", "CBC", "CTR", "GCM"], 3),
        ("¿Qué organismo publica los CIS Benchmarks para bastionado de SO?",
         ["DISA", "CIS (Center for Internet Security)", "CCN-CERT", "NIST"], 1),
        ("¿Por qué un proceso en ring 3 no puede acceder directamente a ring 0?",
         ["Porque ring 3 tiene más velocidad",
          "Por la separación de privilegios que impone la CPU",
          "Porque ring 0 solo existe en Linux",
          "Porque el antivirus lo impide"], 1),
    ],
    3: [
        ("¿Cuántas capas tiene el modelo OSI?",
         ["4", "5", "6", "7"], 3),
        ("¿Qué protocolo traduce una dirección IP a dirección MAC en la red local?",
         ["DHCP", "DNS", "ARP", "ICMP"], 2),
        ("¿En qué puerto escucha DNS por defecto?",
         ["80", "443", "53", "25"], 2),
        ("¿Qué versión de TLS es la actual recomendada según el RFC 8446?",
         ["TLS 1.0", "TLS 1.1", "TLS 1.2", "TLS 1.3"], 3),
        ("¿Qué protocolo es 'rápido y sin garantías de entrega' (disparar y olvidar)?",
         ["TCP", "UDP", "IP", "ICMP"], 1),
        ("¿Qué rango de puertos se denomina 'well-known ports'?",
         ["1024 – 49151", "0 – 65535", "0 – 1023", "49152 – 65535"], 2),
        ("¿Qué tipo de ataque explota el protocolo ARP para interceptar tráfico?",
         ["DDoS", "Ransomware", "ARP Spoofing", "SQL Injection"], 2),
        ("¿Qué significa DoH (DNS over HTTPS)?",
         ["Un ataque de denegación de servicio",
          "Cifrado de consultas DNS sobre HTTPS",
          "Un tipo de firewall",
          "Un protocolo de enrutamiento dinámico"], 1),
        ("Según ENISA Threat Landscape 2024, ¿cuál es la amenaza de red número 1?",
         ["Ransomware", "Phishing", "DDoS", "MITM"], 2),
        ("¿Qué capa del modelo TCP/IP se encarga del enrutamiento de paquetes?",
         ["Aplicación", "Transporte", "Internet", "Acceso a red"], 2),
    ],
    4: [
        ("¿Cuál es la característica principal del 'White Hat' según PTES?",
         ["Ataca por lucro económico",
          "Investiga sin permiso pero reporta responsablemente",
          "Investiga con permiso explícito de la organización",
          "Vende exploits en el mercado negro"], 2),
        ("¿Qué significa 'black box' en una modalidad de pentest?",
         ["Usar solo herramientas de código cerrado",
          "El pentester tiene información completa del sistema",
          "El pentester tiene credenciales de usuario estándar",
          "El pentester arranca solo con el nombre de la empresa"], 3),
        ("¿Cuál es la primera fase de las 5 fases de un pentest según PTES?",
         ["Escaneo", "Reconocimiento", "Explotación", "Informe"], 1),
        ("¿Qué diferencia principal tiene un Red Team respecto a un pentest clásico?",
         ["El Red Team es más barato y rápido",
          "El pentest es más sigiloso que el Red Team",
          "El Red Team simula un APT completo durante semanas o meses",
          "El Red Team solo usa herramientas automatizadas"], 2),
        ("¿Qué es un programa Bug Bounty?",
         ["Un tipo de malware de doble extorsión",
          "Un programa continuo que paga por hallazgos validados",
          "Un estándar de seguridad como ISO 27001",
          "Una metodología de pentest interna"], 1),
        ("¿Qué significa 'grey box' en un pentest?",
         ["Sin información inicial sobre el objetivo",
          "Información completa: código fuente y arquitectura",
          "Información parcial: credenciales de usuario o diagramas de red",
          "Solo acceso físico a las instalaciones"], 2),
        ("¿Qué framework describe las tácticas y técnicas de los atacantes reales?",
         ["PTES", "OWASP Testing Guide", "MITRE ATT&CK", "ISO 27001"], 2),
        ("¿Qué documento legal es imprescindible antes de iniciar un pentest ético?",
         ["CVE", "NDA + Rules of Engagement firmadas", "CVSS", "KEV"], 1),
        ("¿Qué modalidad combina Red Team y Blue Team colaborando en tiempo real?",
         ["Black Box", "Bug Bounty", "Purple Team", "Vulnerability Assessment"], 2),
        ("¿Qué tipo de evaluación usa Nessus u OpenVAS sin explotar vulnerabilidades?",
         ["Pentest", "Red Team", "Bug Bounty", "Vulnerability Assessment"], 3),
    ],
    5: [
        ("¿Qué es un CVE (Common Vulnerabilities and Exposures)?",
         ["Una herramienta de escaneo de redes",
          "Un identificador único y público para cada vulnerabilidad conocida",
          "Un framework de ataque ofensivo",
          "Un sistema de puntuación de riesgo empresarial"], 1),
        ("¿Cuál fue la puntuación CVSS de Log4Shell (CVE-2021-44228)?",
         ["7.5", "8.8", "9.8", "10.0"], 3),
        ("¿Qué rango de puntuación CVSS se considera CRITICAL?",
         ["7.0 – 8.9", "8.0 – 9.9", "9.0 – 10.0", "6.0 – 8.0"], 2),
        ("¿Qué organismo gestiona el catálogo CVE desde 1999?",
         ["NIST", "FIRST", "MITRE", "ENISA"], 2),
        ("¿Cuál es la diferencia entre amenaza y vulnerabilidad?",
         ["Son sinónimos en ciberseguridad",
          "La amenaza es el fallo concreto; la vulnerabilidad es un actor",
          "La vulnerabilidad es el fallo concreto; la amenaza tiene potencial de daño",
          "El riesgo es la suma de ambos sin distinción"], 2),
        ("¿Qué significa el Attack Vector 'N' en el vector base de CVSS?",
         ["Físico (Physical)", "Local", "Adyacente (Adjacent)", "Red (Network)"], 3),
        ("¿Qué es el EPSS (Exploit Prediction Scoring System)?",
         ["Un escáner de vulnerabilidades open-source",
          "Una puntuación de probabilidad de que una vulnerabilidad sea explotada",
          "Un tipo de CVE de alta criticidad",
          "Un tipo de firewall de nueva generación"], 1),
        ("¿Qué herramienta comercial de escaneo de vulnerabilidades se menciona en el PDF?",
         ["Metasploit", "Burp Suite", "Nessus", "Wireshark"], 2),
        ("¿Qué significa KEV en el contexto de vulnerabilidades (CISA)?",
         ["Key Encryption Vulnerability",
          "Known Exploited Vulnerabilities",
          "Kernel Exploitation Vector",
          "Key Evidence Validation"], 1),
        ("Según la fórmula del PDF, ¿cómo se calcula el riesgo?",
         ["amenaza + vulnerabilidad",
          "amenaza × vulnerabilidad × impacto",
          "probabilidad / impacto",
          "CVE × CVSS"], 1),
    ],
    6: [
        ("Según Verizon DBIR 2024, ¿qué porcentaje de brechas incluye un elemento humano?",
         ["48 %", "55 %", "68 %", "75 %"], 2),
        ("¿Qué principio de Cialdini usa la frase 'Tu cuenta se bloquea en 5 minutos'?",
         ["Autoridad", "Urgencia", "Reciprocidad", "Escasez"], 1),
        ("¿Qué es el Spear Phishing?",
         ["Phishing masivo enviado a miles de personas",
          "Phishing personalizado a una persona o equipo concreto",
          "Phishing realizado mediante llamadas de voz",
          "Phishing mediante códigos QR"], 1),
        ("¿Cuáles son las 4 fases del ciclo de un ataque de ingeniería social según el PDF?",
         ["Recon, Scan, Exploit, Report",
          "Reconocimiento, Hook, Play, Exit",
          "Preparación, Ataque, Exfiltración, Borrado",
          "OSINT, Phishing, Acceso, Persistencia"], 1),
        ("¿Cuánto tarda de media un usuario en hacer clic en un phishing tras recibirlo?",
         ["< 10 segundos", "< 30 segundos", "< 60 segundos", "< 5 minutos"], 2),
        ("¿Qué es el Vishing?",
         ["Phishing por correo electrónico",
          "Phishing por SMS",
          "Phishing mediante llamada de voz",
          "Phishing mediante código QR"], 2),
        ("¿Qué principio de Cialdini aplica la frase 'Todo tu equipo ya ha rellenado este formulario'?",
         ["Autoridad", "Urgencia", "Prueba social", "Escasez"], 2),
        ("¿Qué es el Tailgating?",
         ["Seguir a una persona autorizada para acceder físicamente a zona restringida",
          "Phishing por correo electrónico corporativo",
          "Robo de credenciales mediante keylogger",
          "Ataque de fuerza bruta a contraseñas"], 0),
        ("¿Qué herramienta se menciona en el PDF para simular ataques de ingeniería social?",
         ["Metasploit", "Nmap", "SET (Social Engineering Toolkit)", "Burp Suite"], 2),
        ("¿Cuántas fases componen el ciclo completo de un ataque de ingeniería social?",
         ["3", "4", "5", "6"], 1),
    ],
    7: [
        ("¿Qué categoría ocupa el primer puesto del OWASP Top 10 2021?",
         ["A03 Injection",
          "A01 Broken Access Control",
          "A02 Cryptographic Failures",
          "A07 Auth Failures"], 1),
        ("¿Cuál es la defensa principal contra SQL Injection?",
         ["Usar contraseñas seguras en la BD",
          "Prepared statements (consultas parametrizadas)",
          "Cifrar el tráfico con HTTPS",
          "Instalar un firewall de red"], 1),
        ("¿Qué flag de cookie impide que JavaScript acceda a ella?",
         ["Secure", "SameSite", "HttpOnly", "Domain"], 2),
        ("¿Qué significa SSRF?",
         ["Secure Session Request Framework",
          "Server-Side Request Forgery",
          "SQL Server Resource Filter",
          "Security Standard for Remote Files"], 1),
        ("¿Dónde debe residir siempre la validación crítica en una webapp?",
         ["En el cliente (navegador)", "En el CDN", "En el backend", "En el DNS"], 2),
        ("¿Qué es un JWT según el RFC 7519?",
         ["Una herramienta de escaneo web",
          "Un token autoportante con header.payload.signature",
          "Un tipo de cookie segura con cifrado",
          "Un protocolo de autenticación federada"], 1),
        ("¿Qué categoría del OWASP Top 10 se relaciona con librerías sin parchear?",
         ["A03 Injection",
          "A05 Security Misconfiguration",
          "A06 Vulnerable and Outdated Components",
          "A09 Logging & Monitoring Failures"], 2),
        ("¿Qué es XSS (Cross-Site Scripting)?",
         ["Un ataque de denegación de servicio distribuido",
          "Inyección de scripts maliciosos en páginas web vistas por otros usuarios",
          "Un ataque de fuerza bruta sobre contraseñas",
          "Falsificación de peticiones en el servidor"], 1),
        ("¿Cuál es el riesgo del algoritmo 'alg:none' en un JWT?",
         ["El token expira de forma inesperadamente rápida",
          "Permite que el token no tenga firma, omitiendo la verificación de autenticidad",
          "El token no puede ser revocado por el servidor",
          "El payload del token queda expuesto en logs"], 1),
        ("¿Qué componente filtra ataques a nivel de capa 7 ante una aplicación web pública?",
         ["IDS de red", "VPN corporativa", "SIEM", "WAF (Web Application Firewall)"], 3),
    ],
    8: [
        ("¿En qué mecanismo se basa el aislamiento sandbox de apps en Android?",
         ["Cifrado de disco completo",
          "UID único por aplicación con SELinux obligatorio",
          "Permisos NTFS del sistema de archivos",
          "Certificados digitales de Google Play"], 1),
        ("¿Qué significa BYOD en el entorno empresarial?",
         ["Build Your Own Device",
          "Bring Your Own Device",
          "Backup Your Own Data",
          "Block Your Own Domain"], 1),
        ("¿Qué categoría del OWASP Mobile Top 10 2024 se refiere a credenciales embebidas en código?",
         ["M3 Insecure Authentication / Authorization",
          "M5 Insecure Communication",
          "M9 Insecure Data Storage",
          "M1 Improper Credential Use"], 3),
        ("¿Desde qué versión de Android se solicitan permisos en tiempo de ejecución (runtime)?",
         ["Android 4.4 (KitKat)", "Android 5.0 (Lollipop)",
          "Android 6.0 (Marshmallow)", "Android 8.0 (Oreo)"], 2),
        ("¿Qué mecanismo gestiona los permisos de las apps en iOS?",
         ["SELinux del kernel XNU",
          "Entitlements firmados por Apple",
          "Permisos POSIX estándar",
          "Listas de control de acceso NTFS"], 1),
        ("¿Qué significa MDM en el contexto de movilidad empresarial?",
         ["Mobile Data Management",
          "Mobile Device Management",
          "Multi-Device Module",
          "Managed Device Mode"], 1),
        ("¿Cuántos usuarios de smartphone hay aproximadamente en el mundo según el PDF?",
         ["~4,5 B", "~5,8 B", "~7,2 B", "~8,1 B"], 2),
        ("¿Qué vulnerabilidad representa M9 en el OWASP Mobile Top 10?",
         ["Credenciales hardcoded en el código fuente",
          "MFA débil o bypassable",
          "Datos sensibles almacenados sin cifrar",
          "Tráfico sin TLS"], 2),
        ("¿Qué singularidad tenía iOS en distribución de apps antes de la entrada en vigor del DMA europeo?",
         ["Permitía sideload activable por el usuario",
          "Tienda única sin alternativas",
          "Solicitud de permisos en runtime desde la versión 4",
          "Paquetes APK firmados con v3 signature scheme"], 1),
        ("¿Qué es el Secure Enclave en dispositivos Apple?",
         ["Una tienda de aplicaciones con verificación extra",
          "Un coprocesador de seguridad que gestiona datos biométricos y claves criptográficas",
          "Un tipo de sandbox de aplicaciones",
          "El sistema de permisos a nivel de proceso de iOS"], 1),
    ],
    9: [
        ("¿Qué modo de cifrado AES combina cifrado y autenticación en una sola operación (AEAD)?",
         ["ECB", "CBC", "CTR", "GCM"], 3),
        ("¿Cuál es el tamaño de bloque de AES según el estándar FIPS 197?",
         ["64 bits", "128 bits", "256 bits", "512 bits"], 1),
        ("¿Por qué nunca debe usarse el modo ECB para cifrar datos?",
         ["Es demasiado lento para uso en producción",
          "Solo funciona con claves RSA",
          "Los patrones del texto plano son visibles en el texto cifrado",
          "No soporta claves de 256 bits"], 2),
        ("¿Qué propiedad criptográfica garantiza que no puedes negar haber enviado un mensaje?",
         ["Confidencialidad", "Integridad", "Autenticidad", "No repudio"], 3),
        ("¿Qué algoritmo asimétrico usa curvas elípticas y es más eficiente que RSA?",
         ["3DES", "AES-256", "ECC (Elliptic Curve Cryptography)", "ChaCha20"], 2),
        ("¿Cuántos bits recomienda usar como mínimo RSA según los estándares actuales?",
         ["512", "1024", "2048", "4096"], 2),
        ("¿Qué significa AEAD en criptografía?",
         ["Advanced Encryption and Data",
          "Authenticated Encryption with Associated Data",
          "Asymmetric Encryption Algorithm Design",
          "Advanced Encryption Authentication Data"], 1),
        ("¿Cuántas veces más lenta es aproximadamente la criptografía asimétrica frente a la simétrica?",
         ["~10x", "~100x", "~1000x", "~10000x"], 2),
        ("¿Qué protocolo usa Diffie-Hellman como base para el intercambio de claves?",
         ["SSH directo", "TLS (Transport Layer Security)", "JWT", "IPsec IKE"], 1),
        ("¿Cuál de estos algoritmos de hash de contraseñas es el recomendado actualmente?",
         ["MD5", "SHA-1", "SHA-256 sin sal", "Argon2"], 3),
    ],
    10: [
        ("¿En qué modelo cloud el proveedor gestiona el runtime y la BD y tú gestionas el código?",
         ["IaaS", "PaaS", "SaaS", "FaaS"], 1),
        ("En el modelo de responsabilidad compartida, ¿de qué es siempre responsable el cliente?",
         ["Hardware físico del datacenter",
          "Hipervisores del proveedor",
          "Los datos y las identidades propias",
          "Seguridad del datacenter del proveedor"], 2),
        ("¿Qué significa el principio 'least privilege' en IAM cloud?",
         ["Dar acceso total a todos los administradores",
          "Asignar solo los permisos estrictamente necesarios",
          "Usar solo autenticación por contraseña sin MFA",
          "Deshabilitar MFA en cuentas de servicio"], 1),
        ("¿Qué servicio de AWS detecta amenazas mediante machine learning según el PDF?",
         ["CloudTrail", "GuardDuty", "IAM Access Analyzer", "Security Hub"], 1),
        ("¿Qué es una VPC en el contexto cloud?",
         ["Virtual Private Certificate",
          "Virtual Private Cloud — red virtual aislada",
          "Verified Permission Control",
          "Virtual Protocol Channel"], 1),
        ("¿Cómo se define un Security Group en AWS?",
         ["Un grupo de usuarios con permisos de administración",
          "Un firewall stateful por instancia que gestiona reglas inbound/outbound",
          "Una lista negra de direcciones IP bloqueadas",
          "Un servicio centralizado de logging"], 1),
        ("¿Qué herramienta de IaC (Infrastructure as Code) se menciona en el PDF?",
         ["Ansible", "Puppet", "Terraform", "Chef"], 2),
        ("Según el modelo de responsabilidad compartida, ¿qué gestiona el proveedor cloud?",
         ["La clasificación y cifrado de datos del cliente",
          "Las identidades y roles del cliente",
          "La seguridad física del datacenter, hardware e hipervisores",
          "Las configuraciones de red virtual del cliente"], 2),
        ("¿Qué estándar NIST define formalmente los modelos IaaS, PaaS y SaaS?",
         ["NIST SP 800-53", "NIST SP 800-145", "NIST SP 800-207", "NIST SP 800-171"], 1),
        ("¿Qué prohíbe el principio 'Cero claves en código' en IAM?",
         ["Usar contraseñas de más de 16 caracteres",
          "Incluir claves de acceso (access keys) hardcoded en repositorios o código",
          "Cifrar todas las claves simétricas con RSA",
          "Usar tokens de corta duración en CI/CD"], 1),
    ],
    11: [
        ("¿Cuántos días tarda de media detectar una intrusión según el informe IBM Cost of a Data Breach 2024?",
         ["94 días", "145 días", "194 días", "250 días"], 2),
        ("¿Cuál es el coste medio global de una brecha de seguridad según IBM 2024?",
         ["1,5 M$", "2,8 M$", "3,9 M$", "4,88 M$"], 3),
        ("¿Cuánto ahorra de media una empresa que tiene un IR plan probado regularmente?",
         ["-0,8 M$", "-1,5 M$", "-2,2 M$", "-3,1 M$"], 2),
        ("¿Cuáles son las 4 fases del marco NIST SP 800-61 para respuesta a incidentes?",
         ["Identificar, Proteger, Detectar, Responder",
          "Preparación · Detección y análisis · Contención/Erradicación/Recuperación · Post-incidente",
          "Reconocimiento, Análisis, Contención, Erradicación",
          "Triage, Escalada, Mitigación, Cierre"], 1),
        ("¿Qué es un playbook / runbook en el contexto de respuesta a incidentes?",
         ["Un registro centralizado de logs del SIEM",
          "Un procedimiento paso a paso predefinido para un escenario concreto",
          "Una herramienta de análisis forense de memoria",
          "Un informe ejecutivo post-incidente"], 1),
        ("¿Qué herramienta open-source de SIEM se menciona en el PDF?",
         ["Splunk", "Microsoft Sentinel", "Wazuh", "IBM QRadar"], 2),
        ("¿Qué significa PIR en la fase post-incidente?",
         ["Pre-Incident Response", "Post-Incident Review",
          "Primary Incident Report", "Protocol for Incident Resolution"], 1),
        ("¿Qué es el MTTR en el contexto de respuesta a incidentes?",
         ["Mean Time To Recover (tiempo medio de recuperación)",
          "Maximum Threat Tolerance Rate",
          "Multi-Team Triage Report",
          "Mean Threat Tracking Rate"], 0),
        ("¿En qué se diferencia el modelo SANS del NIST en las fases de IR?",
         ["SANS usa 3 fases y NIST usa 4",
          "SANS desglosa en 6 fases separando contención, erradicación y recuperación",
          "Son exactamente idénticos en nomenclatura y número",
          "NIST usa 6 fases y SANS usa 4"], 1),
        ("¿Qué herramienta proporciona telemetría de endpoint en tiempo real para detección?",
         ["SIEM (logs centralizados)", "NDR (análisis de red)",
          "EDR (Endpoint Detection & Response)", "Threat Intel feeds"], 2),
    ],
    12: [
        ("¿Qué reglamento europeo regula la protección de datos personales desde 2018?",
         ["LOPD española de 1999", "GDPR (General Data Protection Regulation)",
          "PCI-DSS", "ISO 27001"], 1),
        ("¿Cuánto tiempo tiene una organización para notificar una brecha de datos a la autoridad supervisora según el GDPR?",
         ["24 horas", "48 horas", "72 horas", "7 días"], 2),
        ("¿Qué artículos del Código Penal Español penalizan el acceso no autorizado a sistemas informáticos?",
         ["Art. 150 y 200", "Art. 197 y 264", "Art. 310 y 350", "Art. 425 y 430"], 1),
        ("¿Qué principio del GDPR establece que los datos solo deben usarse para el fin por el que se recogieron?",
         ["Minimización de datos", "Exactitud y actualización",
          "Limitación de la finalidad", "Integridad y confidencialidad"], 2),
        ("¿Qué es el Esquema Nacional de Seguridad (ENS)?",
         ["Un marco voluntario para empresas privadas europeas",
          "Un marco de seguridad obligatorio para las Administraciones Públicas españolas",
          "Un estándar internacional equivalente a ISO 27001",
          "Un protocolo de certificación de software seguro"], 1),
        ("¿Cuál es la principal diferencia entre un hacker ético y un ciberdelincuente?",
         ["El hacker ético dispone de mejores herramientas",
          "El hacker ético actúa con permiso explícito del propietario del sistema",
          "El hacker ético nunca reporta las vulnerabilidades encontradas",
          "El ciberdelincuente siempre cobra honorarios por su trabajo"], 1),
        ("¿Qué es la 'divulgación responsable' de una vulnerabilidad?",
         ["Publicarla de inmediato en redes sociales para máxima visibilidad",
          "Notificarla al fabricante / responsable antes de hacerla pública",
          "Venderla al mejor postor en el mercado de vulnerabilidades",
          "Explotarla primero y reportarla después"], 1),
        ("¿Qué organismo en España supervisa el cumplimiento del GDPR?",
         ["INCIBE", "CCN-CERT", "AEPD (Agencia Española de Protección de Datos)", "CNI"], 2),
        ("¿Qué principio ético obliga al profesional de ciberseguridad a no revelar información confidencial del cliente?",
         ["No maleficencia", "Confidencialidad profesional",
          "Transparencia total", "Autonomía del cliente"], 1),
        ("¿Qué ley española transpone el GDPR al ordenamiento jurídico nacional?",
         ["LOPD (1999)", "LOPDGDD (Ley Orgánica 3/2018)",
          "LSSI (Ley de Servicios de la Sociedad de la Información)",
          "LGT (Ley General de Telecomunicaciones)"], 1),
    ],
}


# ── Helpers ──────────────────────────────────────────────────────────
def _preparar_preguntas(mod_id: int) -> list:
    """Devuelve 10 preguntas del módulo con opciones barajadas."""
    pool = list(PREGUNTAS[mod_id])
    random.shuffle(pool)
    result = []
    for pregunta, opciones, correcto in pool[:10]:
        indices = list(range(len(opciones)))
        random.shuffle(indices)
        new_opts = [opciones[i] for i in indices]
        new_correct = indices.index(correcto)
        result.append((pregunta, new_opts, new_correct))
    return result


def _generar_codigo(user_id: int, mod_id: int) -> str:
    """Delega en utils.crypto — mismo algoritmo que el backend C#."""
    return generar_codigo_hex(user_id, mod_id)


# ── Ventana de test ───────────────────────────────────────────────────
class TestWindow(ctk.CTkToplevel):
    # Colores de las tarjetas de opción
    _OPT_NORMAL   = ("gray93", "#1e293b")
    _OPT_SELECTED = ("#e0e7ff", "#312e81")
    _OPT_BORDER_N = ("gray78", "#334155")
    _OPT_BORDER_S = "#4f46e5"

    def __init__(self, master, mod_id: int, mod_name: str, user_id: int):
        super().__init__(master)
        self.title(f"Test · {mod_name}")
        self.geometry("620x480")
        self.resizable(False, False)
        self.grab_set()

        self._mod_id   = mod_id
        self._mod_name = mod_name
        self._user_id  = user_id
        self._opt_btns: list[ctk.CTkButton] = []
        self._restart()

    # ── lifecycle ────────────────────────────────────────────────────
    def _restart(self):
        self._preguntas  = _preparar_preguntas(self._mod_id)
        self._idx        = 0
        self._respuestas = [None] * 10
        self._mostrar_pregunta()

    # ── pregunta ─────────────────────────────────────────────────────
    def _mostrar_pregunta(self):
        for w in self.winfo_children():
            w.destroy()
        self._opt_btns = []

        q = self._idx
        pregunta, opciones, _ = self._preguntas[q]
        seleccion = self._respuestas[q]  # puede ser None

        # Cabecera compacta
        hdr = ctk.CTkFrame(self, fg_color=("gray88", "#0f172a"), corner_radius=0)
        hdr.pack(fill="x")

        inner_hdr = ctk.CTkFrame(hdr, fg_color="transparent")
        inner_hdr.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(inner_hdr,
                     text=self._mod_name,
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=11)).pack(side="left")
        ctk.CTkLabel(inner_hdr,
                     text=f"{q + 1} / 10",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=C["primary"]).pack(side="right")

        bar = ctk.CTkProgressBar(hdr, height=4, corner_radius=0,
                                  progress_color=C["primary"])
        bar.pack(fill="x")
        bar.set((q + 1) / 10)

        # Enunciado
        ctk.CTkLabel(self, text=pregunta,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     wraplength=560, justify="left",
                     anchor="w").pack(padx=22, anchor="w", pady=(16, 10))

        # Opciones como tarjetas seleccionables
        for i, texto in enumerate(opciones):
            selected = (seleccion == i)
            btn = ctk.CTkButton(
                self,
                text=f"  {texto}",
                anchor="w",
                height=42,
                corner_radius=8,
                border_width=2,
                fg_color=self._OPT_SELECTED if selected else self._OPT_NORMAL,
                border_color=self._OPT_BORDER_S if selected else self._OPT_BORDER_N,
                hover_color=("gray85", "#253047"),
                text_color=("gray10", "white"),
                font=ctk.CTkFont(size=12),
                command=lambda idx=i: self._seleccionar(idx),
            )
            btn.pack(fill="x", padx=22, pady=3)
            self._opt_btns.append(btn)

        # Navegación
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=22, pady=(12, 16), side="bottom")

        if q > 0:
            ctk.CTkButton(nav, text="← Anterior", width=110, height=34,
                          fg_color=("gray78", "#334155"),
                          hover_color=("gray68", "#475569"),
                          font=ctk.CTkFont(size=12),
                          command=self._prev).pack(side="left")

        es_ultimo = (q == 9)
        ctk.CTkButton(nav,
                      text="Finalizar ✓" if es_ultimo else "Siguiente →",
                      width=120, height=34,
                      fg_color=C["success"] if es_ultimo else C["primary"],
                      hover_color="#059669" if es_ultimo else C["primary_hov"],
                      font=ctk.CTkFont(size=12),
                      command=self._finalizar if es_ultimo else self._next
                      ).pack(side="right")

    def _seleccionar(self, idx: int):
        """Actualiza el estado visual y guarda la respuesta."""
        self._respuestas[self._idx] = idx
        for i, btn in enumerate(self._opt_btns):
            if i == idx:
                btn.configure(fg_color=self._OPT_SELECTED,
                               border_color=self._OPT_BORDER_S)
            else:
                btn.configure(fg_color=self._OPT_NORMAL,
                               border_color=self._OPT_BORDER_N)

    def _next(self):
        self._idx += 1
        self._mostrar_pregunta()

    def _prev(self):
        self._idx -= 1
        self._mostrar_pregunta()

    def _finalizar(self):
        # Si la última pregunta no tiene respuesta guardada, no contar
        score = sum(
            1 for i, (_, _, correcto) in enumerate(self._preguntas)
            if self._respuestas[i] == correcto
        )
        self._mostrar_resultado(score)

    # ── resultado ────────────────────────────────────────────────────
    def _mostrar_resultado(self, score: int):
        for w in self.winfo_children():
            w.destroy()

        aprobado = score >= 7
        color    = C["success"] if aprobado else C["error"]

        # Banda superior de color
        banda = ctk.CTkFrame(self, fg_color=color, corner_radius=0, height=6)
        banda.pack(fill="x")

        # Puntuación
        scores_frame = ctk.CTkFrame(self, fg_color="transparent")
        scores_frame.pack(pady=(20, 4))
        ctk.CTkLabel(scores_frame, text=f"{score}",
                     font=ctk.CTkFont(size=56, weight="bold"),
                     text_color=color).pack(side="left")
        ctk.CTkLabel(scores_frame, text=" / 10",
                     font=ctk.CTkFont(size=28),
                     text_color=C["muted"]).pack(side="left", anchor="s", pady=(0, 8))

        ctk.CTkLabel(self,
                     text="¡Aprobado!" if aprobado else "No aprobado",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=color).pack()
        ctk.CTkLabel(self, text=self._mod_name,
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=11)).pack(pady=(2, 14))

        if aprobado:
            code = _generar_codigo(self._user_id, self._mod_id)

            ctk.CTkLabel(self, text="Tu código de validación:",
                         text_color=C["muted"],
                         font=ctk.CTkFont(size=11)).pack()

            # Caja código + botón copiar en la misma fila
            code_row = ctk.CTkFrame(self, fg_color="transparent")
            code_row.pack(pady=8)

            box = ctk.CTkFrame(code_row, fg_color=("gray88", "#334155"), corner_radius=10)
            box.pack(side="left")
            ctk.CTkLabel(box, text=code,
                         font=ctk.CTkFont(family="Courier New", size=26, weight="bold"),
                         text_color=C["primary"]).pack(padx=22, pady=10)

            copy_btn = ctk.CTkButton(code_row, text="Copiar",
                                      width=72, height=42,
                                      corner_radius=10,
                                      fg_color=("gray78", "#334155"),
                                      hover_color=("gray68", "#475569"),
                                      font=ctk.CTkFont(size=12))
            copy_btn.pack(side="left", padx=(6, 0))
            copy_btn.configure(command=lambda: self._copiar(code, copy_btn))

            ctk.CTkLabel(self,
                         text="Introduce el código en la web · Temario · Código lab",
                         text_color=C["muted"],
                         font=ctk.CTkFont(size=11)).pack(pady=(2, 12))

            ctk.CTkButton(self, text="Ir a la web →",
                          width=180, height=36,
                          fg_color=C["primary"], hover_color=C["primary_hov"],
                          font=ctk.CTkFont(size=12),
                          command=lambda: webbrowser.open(f"{WEB_BASE_URL}/temario")
                          ).pack(pady=(0, 6))
        else:
            ctk.CTkLabel(self,
                         text="Necesitas 7 / 10 para obtener el código.",
                         text_color=C["error"],
                         font=ctk.CTkFont(size=12)).pack(pady=(0, 4))
            ctk.CTkLabel(self,
                         text="Repasa el contenido del tema e inténtalo de nuevo.",
                         text_color=C["muted"],
                         font=ctk.CTkFont(size=11)).pack()
            ctk.CTkButton(self, text="Reintentar",
                          width=160, height=36,
                          fg_color=C["primary"], hover_color=C["primary_hov"],
                          font=ctk.CTkFont(size=12),
                          command=self._restart).pack(pady=(14, 6))

        ctk.CTkButton(self, text="Cerrar",
                      width=160, height=34,
                      fg_color=("gray78", "#334155"),
                      hover_color=("gray68", "#475569"),
                      font=ctk.CTkFont(size=12),
                      command=self.destroy).pack(pady=(0, 16))

    def _copiar(self, code: str, btn: ctk.CTkButton):
        """Copia el código al portapapeles y muestra feedback visual."""
        self.clipboard_clear()
        self.clipboard_append(code)
        self.update()
        btn.configure(text="✓ Copiado", fg_color=C["success"], hover_color="#059669")
        self.after(1800, lambda: btn.configure(
            text="Copiar",
            fg_color=("gray78", "#334155"),
            hover_color=("gray68", "#475569")
        ))


# ── Pantalla principal ────────────────────────────────────────────────
class TemarioScreen(ctk.CTkFrame):
    def __init__(self, master, usuario: dict, api_client):
        super().__init__(master, fg_color="transparent")
        self.usuario = usuario
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Temario",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(
                         anchor="w", padx=40, pady=(24, 2))
        ctk.CTkLabel(self,
                     text="Módulos de ciberseguridad · completa el test para obtener tu código de validación",
                     text_color=C["muted"],
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=40, pady=(0, 14))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 16))
        scroll.grid_columnconfigure((0, 1, 2), weight=1, uniform="col")

        desbloqueados = set(map(int, self.usuario.get("modulosDesbloqueados", [])))
        user_id       = int(self.usuario.get("id", 0))

        for i, (mod_id, titulo, desc, coste, recompensa) in enumerate(MODULOS):
            row_idx = i // 3
            col_idx = i % 3
            desbloqueado = mod_id in desbloqueados

            border = C["primary"] if desbloqueado else C["divider"]
            card = ctk.CTkFrame(scroll, corner_radius=12,
                                fg_color=C["card"],
                                border_width=1 if desbloqueado else 1,
                                border_color=border)
            card.grid(row=row_idx, column=col_idx, padx=6, pady=6, sticky="nsew")

            inn = ctk.CTkFrame(card, fg_color="transparent")
            inn.pack(fill="both", expand=True, padx=14, pady=12)

            # Número + Título
            top = ctk.CTkFrame(inn, fg_color="transparent")
            top.pack(fill="x", pady=(0, 6))

            badge_fg = C["primary"] if desbloqueado else C["badge_lock"]
            bdg = ctk.CTkFrame(top, width=34, height=34, corner_radius=8, fg_color=badge_fg)
            bdg.pack(side="left")
            bdg.pack_propagate(False)
            ctk.CTkLabel(bdg, text=f"{mod_id:02d}",
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="white").place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(top, text=titulo,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         anchor="w", wraplength=160,
                         justify="left").pack(side="left", padx=(8, 0), fill="x", expand=True)

            # Descripción
            ctk.CTkLabel(inn, text=desc,
                         text_color=C["muted"],
                         font=ctk.CTkFont(size=10),
                         anchor="w", wraplength=210,
                         justify="left").pack(anchor="w", pady=(0, 8))

            # Badge estado / coste
            if desbloqueado:
                bf = ctk.CTkFrame(inn, fg_color=C["badge_ok_bg"], corner_radius=6)
                bf.pack(anchor="w", pady=(0, 8))
                ctk.CTkLabel(bf, text="✓  Contenido Disponible",
                             text_color=C["primary"],
                             font=ctk.CTkFont(size=10, weight="bold")).pack(padx=8, pady=3)
            else:
                bf = ctk.CTkFrame(inn, fg_color=C["cost_bg"], corner_radius=6)
                bf.pack(anchor="w", pady=(0, 8))
                ctk.CTkLabel(bf, text=f"Costo: {coste} pts",
                             text_color=C["muted"],
                             font=ctk.CTkFont(size=10)).pack(padx=8, pady=3)

            # Botones
            if desbloqueado:
                ctk.CTkButton(inn, text="▶  Abrir Tema",
                              height=30,
                              fg_color=C["primary"], hover_color=C["primary_hov"],
                              font=ctk.CTkFont(size=11),
                              command=lambda: webbrowser.open(f"{WEB_BASE_URL}/temario")
                              ).pack(fill="x", pady=(0, 4))
                ctk.CTkButton(inn, text="Realizar Test",
                              height=30,
                              fg_color="transparent",
                              hover_color=("gray82", "#1e293b"),
                              border_width=1, border_color=C["primary"],
                              text_color=C["primary"],
                              font=ctk.CTkFont(size=11),
                              command=lambda mid=mod_id, t=titulo, uid=user_id: (
                                  TestWindow(self, mid, t, uid)
                              )).pack(fill="x")
            else:
                ctk.CTkButton(inn, text="Desbloquear",
                              height=30,
                              fg_color="transparent",
                              hover_color=("gray82", "#1e293b"),
                              border_width=1, border_color=C["divider"],
                              text_color=C["muted"],
                              font=ctk.CTkFont(size=11),
                              command=lambda: webbrowser.open(f"{WEB_BASE_URL}/temario")
                              ).pack(fill="x")
