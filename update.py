import subprocess
import requests

GITHUB_REPO = "litelis/AutoRoleCreator-Discord-Bot"
CURRENT_VERSION = "1.0.0"

def get_latest_version():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["tag_name"]
    else:
        print("Error al consultar GitHub")
        return None

latest_version = get_latest_version()
print(f"Versión actual: {CURRENT_VERSION}")
print(f"Última versión en GitHub: {latest_version}")

if latest_version and latest_version != CURRENT_VERSION:
    choice = input("¿Quieres actualizar? (Y/N): ").strip().upper()
    if choice == "Y":
        print("Actualizando desde GitHub...")
        subprocess.run(["git", "pull", "https://github.com/litelis/AutoRoleCreator-Discord-Bot.git"])
        print("Actualización completada. Reinicia el bot si es necesario.")
    else:
        print("Actualización cancelada.")
else:
    print("Ya tienes la última versión.")
