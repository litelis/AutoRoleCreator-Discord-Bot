import os

def create_env():
    print("--- Configuración del Token de Discord ---")
    token = input("Introduce tu Discord Token: ").strip()
    
    with open(".env", "w") as f:
        f.write(f"DISCORD_TOKEN={token}\n")
    print("Archivo .env generado correctamente.")

def install_deps():
    print("Instalando dependencias desde requirements.txt...")
    os.system("pip install -r requirements.txt")

if __name__ == "__main__":
    create_env()
    install_deps()
    print("\nConfiguración completada con éxito.")
