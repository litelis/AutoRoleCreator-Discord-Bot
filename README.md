# 🤖 AutoRoleCreator Discord Bot

¡Crea roles de forma masiva y automática! Este bot elimina la tarea tediosa de configurar roles uno por uno en tu servidor de Discord. Perfecto para servidores de comunidad o gaming que necesitan una jerarquía organizada rápido.

---

## 🔥 Características
* **Multiplataforma:** Funciona en Windows, Linux y Android (Termux).
* **Instalación Inteligente:** Detecta tu sistema y configura el entorno virtual automáticamente.
* **Eficiente:** Crea múltiples roles con un solo comando slash.
* **Seguro:** Usa variables de entorno para proteger tu Token de Discord.
* **Flexible:** Permite crear roles únicos o por canal, aplicados a uno, varios o todos los canales.

---

## 📋 Requisitos
- Python 3.8 o superior
- Un token de bot de Discord (obtenlo desde [Discord Developer Portal](https://discord.com/developers/applications))

---

## 🛠️ Instalación

### 1. Preparación
Primero, clona este repositorio en tu máquina:
```bash
git clone https://github.com/litelis/AutoRoleCreator-Discord-Bot.git
cd AutoRoleCreator-Discord-Bot
```

### 2. Configuración del Token
Ejecuta el script de configuración para crear el archivo `.env` con tu token:
```bash
python config.py
```
O manualmente crea un archivo `.env` en la raíz del proyecto con:
```
DISCORD_TOKEN=tu_token_aqui
```

### 3. Instalación y Ejecución
Ejecuta el script principal que configurará el entorno virtual y lanzará el bot:
```bash
python main.py
```

Alternativamente, puedes usar el script de setup para preparar el entorno:
```bash
python setup.py
```
Luego activa el entorno virtual y ejecuta el bot:
- Windows: `.venv\Scripts\activate` luego `python bot.py`
- Linux/Mac/Termux: `source .venv/bin/activate` luego `python bot.py`

---

## 🚀 Uso

### Invitar el Bot a tu Servidor
1. Ve al [Discord Developer Portal](https://discord.com/developers/applications)
2. Selecciona tu aplicación y ve a "OAuth2" > "URL Generator"
3. Marca "bot" y "applications.commands"
4. Copia la URL generada e invítalo a tu servidor

### Comando Disponible
El bot utiliza comandos slash. Una vez invitado, usa `/rol` en tu servidor.

#### `/rol`
Crea roles automáticamente en los canales especificados.

**Parámetros:**
- `nombre_rol` (opcional): Nombre del rol a crear. Si no se especifica, se genera uno aleatorio.
- `alcance_canales`: **Campo requerido**. Define dónde aplicar el rol:
  - `Un canal`: Aplica a un solo canal.
  - `Varios canales`: Aplica a una lista de canales.
  - `Todos los canales`: Aplica a todos los canales de texto del servidor.
- `rol_por_canal`: **Campo requerido**. Define el tipo de creación:
  - `Único para todos`: Crea un solo rol y lo aplica a los canales seleccionados.
  - `Uno por canal`: Crea un rol distinto para cada canal (ej: `rol-general`, `rol-chat`).
- `canal_target` (opcional): Úsalo si elegiste "Un canal" para seleccionarlo de la lista desplegable.
- `canales` (opcional): Úsalo si elegiste "Varios canales" (escribe menciones como `#general #chat`) o como fallback para "Un canal".

**Ejemplos de uso:**

1.  **Rol único en un canal específico (Usando el selector):**
    *   `alcance_canales`: Un canal
    *   `rol_por_canal`: Único para todos
    *   `canal_target`: [Selecciona #general]
    *   `nombre_rol`: Visitante

2.  **Roles individuales en varios canales (Por texto):**
    *   `alcance_canales`: Varios canales
    *   `rol_por_canal`: Uno por canal
    *   `canales`: #general #juegos #música
    *   `nombre_rol`: Monitor

3.  **Rol masivo en todo el servidor:**
    *   `alcance_canales`: Todos los canales
    *   `rol_por_canal`: Único para todos
    *   `nombre_rol`: @everyone-ping

---

## 🔧 Actualizaciones
Para actualizar el bot a la última versión:
```bash
python update.py
```

---

## 📝 Notas
- El bot requiere permisos de administrador (o al menos `Manage Roles` y `Manage Channels`) en el servidor.
- Los roles creados tendrán permisos de lectura y escritura en los canales especificados.

---

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si encuentras un error o tienes una sugerencia, abre un issue o envía un pull request.

---

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
