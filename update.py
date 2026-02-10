import requests
import subprocess
import os
import shutil

# Configuración
REPO = "litelis/AutoRoleCreator-Discord-Bot"
BRANCH = "main"

def run_command(command):
    try:
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {command}")
        print(f"Salida: {e.output.decode('utf-8') if e.output else 'No hay salida'}")
        raise

def check_git_installed():
    """Verifica si Git está instalado en el sistema"""
    git_path = shutil.which("git")
    if git_path is None:
        return False
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_local_sha():
    try:
        return run_command("git rev-parse HEAD")
    except:
        return None

def update():
    # Verificar que Git esté instalado
    if not check_git_installed():
        print("❌ Error: Git no está instalado o no se encuentra en el PATH.")
        print("Por favor, instala Git:")
        print("  - Windows: https://git-scm.com/download/win")
        print("  - Linux: sudo apt-get install git (o equivalente)")
        print("  - Mac: brew install git")
        return

    url = f"https://api.github.com/repos/{REPO}/commits/{BRANCH}"
    local_sha = get_local_sha()
    
    if local_sha is None:
        print("⚠️ No se pudo obtener el commit local. ¿Estás en un repositorio Git?")
        print("Intentando actualizar de todos modos...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            remote_sha = response.json()['sha']
            
            if local_sha != remote_sha:
                print(f"🔄 Nueva actualización detectada (Commit remoto: {remote_sha[:7]})")
                print("📥 Actualizando código...")
                
                try:
                    # Ejecuta la actualización real
                    output = run_command("git pull origin main --allow-unrelated-histories")
                    print(f"Git output: {output}")
                    
                    # Actualizar dependencias
                    print("📦 Actualizando dependencias...")
                    run_command("pip install -r requirements.txt")
                    
                    print("✅ Bot actualizado con éxito.")
                    print("🔄 Por favor, reinicia el bot para aplicar los cambios.")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Error durante la actualización de Git: {e}")
                    print("Posibles soluciones:")
                    print("1. Verifica tu conexión a internet")
                    print("2. Asegúrate de tener permisos de escritura en el directorio")
                    print("3. Si hay conflictos, resuélvelos manualmente con 'git status'")
            else:
                print(f"✅ Versión al día. Commit: {local_sha[:7]}")
        else:
            print(f"❌ No se pudo conectar con la API de GitHub. Status: {response.status_code}")
            if response.status_code == 404:
                print("El repositorio no fue encontrado. Verifica la configuración.")
            elif response.status_code == 403:
                print("Límite de API alcanzado. Intenta más tarde.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("Verifica tu conexión a internet.")
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")

if __name__ == "__main__":
    update()
