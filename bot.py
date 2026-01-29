import discord
from discord import app_commands
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("No se encontró el token de Discord en el archivo .env")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class RolCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rol", description="Crea un rol en los canales indicados")
    @app_commands.describe(
        nombre_rol="Nombre del rol a crear (opcional si todos los canales)",
        alcance_canales="Dónde aplicar el rol",
        canales="Canales específicos (si aplica)",
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
        nombre_rol: str = None,
        alcance_canales: app_commands.Choice[str] = None,
        canales: list[discord.TextChannel] = None,
        rol_por_canal: app_commands.Choice[str] = None
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
        elif alcance_canales.value in ["un_canal", "varios_canales"]:
            if not canales:
                await interaction.response.send_message("Debes seleccionar al menos un canal.", ephemeral=True)
                return
            target_channels = canales
            if not nombre_rol:
                nombre_rol = f"rol-{random.randint(1000,9999)}"

        # Crear roles
        if rol_por_canal.value == "unico":
            role = await guild.create_role(name=nombre_rol)
            created_roles.append(role)
            for channel in target_channels:
                await channel.set_permissions(role, read_messages=True, send_messages=True)
        elif rol_por_canal.value == "por_canal":
            for channel in target_channels:
                role = await guild.create_role(name=f"{nombre_rol}-{channel.name}")
                created_roles.append(role)
                await channel.set_permissions(role, read_messages=True, send_messages=True)

        await interaction.response.send_message(f"Roles creados: {', '.join(r.name for r in created_roles)}")

bot.add_cog(RolCog(bot))

if __name__ == "__main__":
    bot.run(TOKEN)
