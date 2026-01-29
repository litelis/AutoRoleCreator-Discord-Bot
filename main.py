import os
import subprocess
import sys

def run_command(command):
    return subprocess.run(command, shell=True)

def main():
    venv_dir = ".venv"
    # Detectar el ejecutable de python según el sistema operativo
    python_venv = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(venv_dir):
        choice = input("No se encontró el entorno virtual (.venv). ¿Quieres ejecutar setup.py? (y/n): ")
        if choice.lower() == 'y':
            print("Creando entorno virtual...")
            subprocess.run([sys.executable, "-m", "venv", venv_dir])
            
            print("Ejecutando configuración inicial...")
            # Usamos el python del venv para instalar dependencias y configurar
            run_command(f"{python_venv} setup.py")
        else:
            print("Cerrando. Necesitas el entorno para continuar.")
            return

    # Iniciar el bot (asumiendo que el archivo principal es index.py o similar)
    # Cambia 'index.py' por el nombre real de tu script de bot
    bot_file = "index.py" 
    if os.path.exists(bot_file):
        print(f"Lanzando {bot_file}...")
        run_command(f"{python_venv} {bot_file}")
    else:
        print(f"Error: No se encontró el archivo {bot_file}")

if __name__ == "__main__":
    main()
