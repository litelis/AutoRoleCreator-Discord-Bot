import os
import subprocess
import sys

def setup():
    # Detectar el sistema operativo y definir la ruta de la carpeta bin/Scripts
    if os.name == "nt":  # Windows
        venv_bin = os.path.join(".venv", "Scripts")
        python_exe = os.path.join(venv_bin, "python.exe")
        pip_exe = os.path.join(venv_bin, "pip.exe")
    else:  # Linux / Termux / MacOS
        venv_bin = os.path.join(".venv", "bin")
        python_exe = os.path.join(venv_bin, "python")
        pip_exe = os.path.join(venv_bin, "pip")

    if not os.path.exists(".venv"):
        print("Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    else:
        print("El entorno virtual ya existe.")

    if os.path.exists("requirements.txt"):
        print("Instalando dependencias...")
        subprocess.run([pip_exe, "install", "-r", "requirements.txt"])
    else:
        print("No se encontró requirements.txt.")

    print("\nConfiguración completada.")
    print(f"Para activar el entorno usa:")
    print(f"Windows: {venv_bin}\\activate")
    print(f"Linux/Termux: source {venv_bin}/activate")

if __name__ == "__main__":
    setup()
