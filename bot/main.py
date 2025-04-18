import os
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp # handles async HTTP requests
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

roll_url = "http://localhost:8000/roll"
schedule_url = "http://localhost:8000/reminder"
customweapon_url = "http://localhost:8000/customweapon"
lookup_url = "http://localhost:8000/search"

GUILD_ID = 1359588987391578342

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    '''
    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        #await self.tree.sync(guild=guild)
        await self.tree.sync()
    '''
    async def startup(self) -> None:
        """Sync application commands"""
        await self.wait_until_ready()
		
		# Sync application commands
        synced = await self.tree.sync()
		
    async def setup_hook(self) -> None:
        """Initialize the bot, database, prefixes & cogs."""
        # Initialize the DiscordBot setup hook
        await super().setup_hook()

		# Sync application commands
        self.loop.create_task(self.startup())


    async def on_ready(self):
        print(f'We have logged in as {self.user}')

intents = discord.Intents.default()
intents.message_content = True

client = Client()

# slash command for rolling dice
@client.tree.command(name="roll", description="roll a die")
async def roll(interaction: discord.Interaction, dice: str):
    await interaction.response.defer()  # Acknowledge the interaction

    async with aiohttp.ClientSession() as session:
        async with session.get(roll_url, params={"dice": dice}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"You rolled `{dice}` and got: {result}")
            else:
                await interaction.followup.send("Error contacting the dice roller API.")

# slash command for creating a custom weapon
@client.tree.command(name="customweapon", description="Create a custom weapon.")
@app_commands.describe(name="Weapon name", damage="weapon damage", range="weapon range")
async def customweapon(interaction: discord.Interaction, name: str, damage: int, range: int):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(customweapon_url, params={"name": name, "damage": damage, "range": range}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await interaction.followup.send((f"success {data.name} created successfully."))
                else:
                    error_message = await resp.text()
                    await interaction.followup.send(f"Failed to create weapon. Server said: {error_message}")
    except Exception as e:
        await interaction.followup.send(f"an error occurred: {e}")


# slash command for scheduler
@client.tree.command(name="reminder", description="set a reminder with a date and time")
@app_commands.describe(date="Date in YYYY-MM-DD", time="Time in HH:MM (24hr)", message="Reminder message")
async def reminder(interaction: discord.Interaction, date: str, time: str, message: str):
    await interaction.response.defer()

    channel_id = str(interaction.channel_id)

    async with aiohttp.ClientSession() as session:
        async with session.post(schedule_url, json={"date": date,"time": time,"message": message,"channel_id": channel_id}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"{result}")
            else:
                await interaction.followup.send("Failed to schedule")

# slash command for lookup
@client.tree.command(name="lookup", description="search a specific type of entity")
@app_commands.describe(name="the name of the entity", ltype="enter monster or weapons")
async def lookup(interaction: discord.Interaction, name: str, ltype: str):
    await interaction.response.defer()

    async with aiohttp.ClientSession() as session:
        async with session.get(lookup_url, params={"name": name, "ltype": ltype}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"{name} is found in the {ltype} data table")
            else:
                await interaction.followup.send("Failed to search entity.")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
