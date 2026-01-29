import requests
import subprocess
import os

# Configuración
REPO = "litelis/AutoRoleCreator-Discord-Bot"
BRANCH = "main"

def run_command(command):
    return subprocess.check_output(command, shell=True).decode('utf-8').strip()

def get_local_sha():
    try:
        return run_command("git rev-parse HEAD")
    except:
        return None

def update():
    url = f"https://api.github.com/repos/{REPO}/commits/{BRANCH}"
    local_sha = get_local_sha()
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            remote_sha = response.json()['sha']
            
            if local_sha != remote_sha:
                print(f"Nueva actualización detectada (Commit: {remote_sha[:7]})")
                print("Actualizando código...")
                # Ejecuta la actualización real
                run_command("git pull origin main")
                run_command("pip install -r requirements.txt")
                print("Bot actualizado con éxito.")
            else:
                print(f"Versión al día. Commit local: {local_sha[:7]}")
        else:
            print("No se pudo conectar con la API de GitHub.")
    except Exception as e:
        print(f"Error durante la actualización: {e}")

if __name__ == "__main__":
    update()
