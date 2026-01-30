import discord
from discord import app_commands
from discord.ext import commands
import random
import os
import re
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró el token de Discord en el archivo .env")

intents = discord.Intents.default()
intents.guilds = True
# intents.members = True # Desactivado: Requiere 'Server Members Intent' en el Developer Portal

bot = commands.Bot(command_prefix="!", intents=intents)

class RolCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rol", description="Crea un rol en los canales indicados")
    @app_commands.describe(
        nombre_rol="Nombre del rol a crear (opcional si todos los canales)",
        alcance_canales="Dónde aplicar el rol",
        canal_target="Selecciona un canal (si el alcance es 'Un canal')",
        canales="Menciones de canales separados por espacios (si son varios)",
        rol_por_canal="Crear rol único o un rol por canal"
    )
    @app_commands.choices(
        alcance_canales=[
            app_commands.Choice(name="Un canal", value="un_canal"),
            app_commands.Choice(name="Varios canales", value="varios_canales"),
            app_commands.Choice(name="Todos los canales", value="todos_los_canales")
        ],
        rol_por_canal=[
            app_commands.Choice(name="Único para todos", value="unico"),
            app_commands.Choice(name="Uno por canal", value="por_canal")
        ]
    )
    async def rol(
        self, interaction: discord.Interaction,
        alcance_canales: app_commands.Choice[str], # Required argument first (conceptually, though discord.py handles keywargs)
        rol_por_canal: app_commands.Choice[str], # Required
        nombre_rol: str = None,
        canal_target: discord.TextChannel = None,
        canales: str = None
    ):
        guild = interaction.guild
        created_roles = []

        # Determinar canales
        target_channels = []
        
        if alcance_canales.value == "todos_los_canales":
            target_channels = guild.text_channels
            # Si no hay nombre, generar uno aleatorio
            if not nombre_rol:
                nombre_rol = f"rol-todos-{random.randint(1000,9999)}"
        
        elif alcance_canales.value == "un_canal":
            if canal_target:
                target_channels = [canal_target]
            elif canales:
                # Fallback to parsing mentions if they used the text field for one channel
                channel_ids = re.findall(r'<#(\d+)>', canales)
                if channel_ids:
                    channel = guild.get_channel(int(channel_ids[0]))
                    if channel and isinstance(channel, discord.TextChannel):
                        target_channels = [channel]
            
            if not target_channels:
                await interaction.response.send_message("Para 'Un canal', debes seleccionar un canal en `canal_target` o mencionarlo en `canales`.", ephemeral=True)
                return
            
            if not nombre_rol:
                nombre_rol = f"rol-{random.randint(1000,9999)}"

        elif alcance_canales.value == "varios_canales":
            if not canales:
                await interaction.response.send_message("Para 'Varios canales', debes escribir las menciones en `canales` (ej: #general #chat).", ephemeral=True)
                return
            # Parse channel mentions
            channel_ids = re.findall(r'<#(\d+)>', canales)
            target_channels = []
            for channel_id in channel_ids:
                channel = guild.get_channel(int(channel_id))
                if channel and isinstance(channel, discord.TextChannel):
                    target_channels.append(channel)
            
            # If they also selected one via the UI picker, add it conceptually? 
            # Usually better to stick to one method, but let's be inclusive if they did both.
            if canal_target and canal_target not in target_channels:
                 target_channels.append(canal_target)

            if not target_channels:
                await interaction.response.send_message("No se encontraron canales válidos en las menciones.", ephemeral=True)
                return
            if not nombre_rol:
                nombre_rol = f"rol-{random.randint(1000,9999)}"

        # Crear roles
        await interaction.response.defer() # Operation might take a moment

        try:
            if rol_por_canal.value == "unico":
                role = await guild.create_role(name=nombre_rol)
                created_roles.append(role)
                for channel in target_channels:
                    await channel.set_permissions(role, read_messages=True, send_messages=True)
            elif rol_por_canal.value == "por_canal":
                for channel in target_channels:
                    role_name = f"{nombre_rol}-{channel.name}" if rol_por_canal.value == "por_canal" else nombre_rol
                    role = await guild.create_role(name=role_name)
                    created_roles.append(role)
                    await channel.set_permissions(role, read_messages=True, send_messages=True)
            
            await interaction.followup.send(f"Roles creados con éxito: {', '.join(r.name for r in created_roles)}")
        except Exception as e:
             await interaction.followup.send(f"Ocurrió un error al crear los roles: {str(e)}")

async def setup_hook():
    await bot.add_cog(RolCog(bot))

bot.setup_hook = setup_hook

if __name__ == "__main__":
    bot.run(TOKEN)
