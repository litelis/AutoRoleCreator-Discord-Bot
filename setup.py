import os
import subprocess
import sys

venv_dir = ".venv"

# 1️⃣ Crear entorno virtual si no existe
if not os.path.exists(venv_dir):
    print("Creando entorno virtual...")
    subprocess.run([sys.executable, "-m", "venv", venv_dir])
else:
    print("Entorno virtual ya existe.")

# 2️⃣ Instalar dependencias
pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
print("Instalando dependencias...")
subprocess.run([pip_path, "install", "-r", "requirements.txt"])

# 3️⃣ Preguntar si configurar el bot
configure = input("¿Quieres configurar el bot de Discord ahora? (Y/N): ").strip().upper()

if configure == "Y":
    token = input("Introduce tu token de Discord: ").strip()
    # Crear archivo .env
    with open(".env", "w") as f:
        f.write(f"DISCORD_TOKEN={token}\n")
    print("Archivo .env creado correctamente con tu token.")
else:
    print("Proceso finalizado. Puedes configurar el bot más tarde creando un archivo .env con tu token.")
