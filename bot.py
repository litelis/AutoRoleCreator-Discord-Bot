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

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print(f'ID del bot: {bot.user.id}')
    try:
        # Sincronizar comandos slash con Discord
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} comandos slash')
    except Exception as e:
        print(f'Error al sincronizar comandos: {e}')

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
        self, 
        interaction: discord.Interaction,
        alcance_canales: app_commands.Choice[str],
        rol_por_canal: app_commands.Choice[str],
        nombre_rol: str = None,
        canal_target: discord.TextChannel = None,
        canales: str = None
    ):
        # Verificar que no se esté usando en DM
        if interaction.guild is None:
            await interaction.response.send_message(
                "Este comando solo puede usarse en servidores, no en mensajes directos.",
                ephemeral=True
            )
            return

        guild = interaction.guild
        
        # Verificar permisos del bot
        bot_member = guild.me
        if not bot_member.guild_permissions.manage_roles:
            await interaction.response.send_message(
                "❌ No tengo permiso para gestionar roles. Por favor, dame el permiso 'Gestionar Roles'.",
                ephemeral=True
            )
            return
        
        if not bot_member.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "❌ No tengo permiso para gestionar canales. Por favor, dame el permiso 'Gestionar Canales'.",
                ephemeral=True
            )
            return

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
                await interaction.response.send_message(
                    "Para 'Un canal', debes seleccionar un canal en `canal_target` o mencionarlo en `canales`.",
                    ephemeral=True
                )
                return

            
            if not nombre_rol:
                nombre_rol = f"rol-{random.randint(1000,9999)}"

        elif alcance_canales.value == "varios_canales":
            if not canales:
                await interaction.response.send_message(
                    "Para 'Varios canales', debes escribir las menciones en `canales` (ej: #general #chat).",
                    ephemeral=True
                )
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
                await interaction.response.send_message(
                    "No se encontraron canales válidos en las menciones.",
                    ephemeral=True
                )
                return

            if not nombre_rol:
                nombre_rol = f"rol-{random.randint(1000,9999)}"

        # Crear roles
        await interaction.response.defer() # Operation might take a moment

        try:
            if rol_por_canal.value == "unico":
                # Verificar que el rol no exista ya
                existing_role = discord.utils.get(guild.roles, name=nombre_rol)
                if existing_role:
                    await interaction.followup.send(
                        f"⚠️ El rol '{nombre_rol}' ya existe. Usa otro nombre.",
                        ephemeral=True
                    )
                    return
                
                role = await guild.create_role(name=nombre_rol)
                created_roles.append(role)
                for channel in target_channels:
                    await channel.set_permissions(role, read_messages=True, send_messages=True)
                    
            elif rol_por_canal.value == "por_canal":
                for channel in target_channels:
                    role_name = f"{nombre_rol}-{channel.name}"
                    # Verificar que el rol no exista ya
                    existing_role = discord.utils.get(guild.roles, name=role_name)
                    if existing_role:
                        await interaction.followup.send(
                            f"⚠️ El rol '{role_name}' ya existe. Omite este canal o usa otro nombre base.",
                            ephemeral=True
                        )
                        continue
                    
                    role = await guild.create_role(name=role_name)
                    created_roles.append(role)
                    await channel.set_permissions(role, read_messages=True, send_messages=True)
            
            if created_roles:
                await interaction.followup.send(
                    f"✅ Roles creados con éxito: {', '.join(r.name for r in created_roles)}"
                )
            else:
                await interaction.followup.send(
                    "⚠️ No se crearon roles. Es posible que ya existieran.",
                    ephemeral=True
                )
                    
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ No tengo permisos suficientes para crear roles o modificar canales. "
                "Asegúrate de que mi rol esté por encima de los roles que intento crear.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"❌ Error de Discord al crear roles: {e.text}",
                ephemeral=True
            )
        except Exception as e:
             await interaction.followup.send(
                 f"❌ Ocurrió un error inesperado: {str(e)}",
                 ephemeral=True
             )


async def setup_hook():
    await bot.add_cog(RolCog(bot))

bot.setup_hook = setup_hook

if __name__ == "__main__":
    bot.run(TOKEN)
