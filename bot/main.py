import os
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

roll_url = "http://localhost:8000/roll"
schedule_url = "http://localhost:8000/reminder"
customweapon_url = "http://localhost:8000/customweapon"
lookup_url = "http://localhost:8000/search"
character_url = "http://localhost:8000/character"
attack_url = "http://localhost:8000/attack"

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

    # Link for the fix to syncing the bot commands:
    # https://github.com/PaulMarisOUMary/Discord-Bot/blob/main/bot.py
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

# slash command for creating a character
@client.tree.command(name="create_character", description="Create a new character.")
@app_commands.describe(name="Character's name", other_info="Other character information")
async def create_character(interaction: discord.Interaction, name: str, other_info: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.post(character_url, json={"name": name, "other_info": other_info}) as resp:
            if resp.status == 200:
                await interaction.followup.send(f"Character `{name}` created!")
            else:
                await interaction.followup.send("Failed to create character.")

# slash command for viewing character
@client.tree.command(name="view_character", description="View a character by name.")
@app_commands.describe(name="Character's name")
async def view_character(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{character_url}/{name}") as resp:
            if resp.status == 200:
                character = await resp.json()
                await interaction.followup.send(f"Character details: `{character}`")
            else:
                await interaction.followup.send("Character not found.")

# slash command for updating a character
@client.tree.command(name="update_character", description="Update an existing character.")
@app_commands.describe(name="Character's name", other_info="New character info")
async def update_character(interaction: discord.Interaction, name: str, other_info: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{character_url}/{name}", json={"other_info": other_info}) as resp:
            if resp.status == 200:
                await interaction.followup.send(f"Character `{name}` updated!")
            else:
                await interaction.followup.send("Failed to update character.")

# slash command for deleting a character
@client.tree.command(name="delete_character", description="Delete a character by name.")
@app_commands.describe(name="Character's name")
async def delete_character(interaction: discord.Interaction, name: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{character_url}/{name}") as resp:
            if resp.status == 200:
                await interaction.followup.send(f"Character `{name}` deleted!")
            else:
                await interaction.followup.send("Failed to delete character.")

# slash command for attack
@client.tree.command(name="attack", description="Attack another character.")
@app_commands.describe(target_name="Target character's name", damage_dice="Damage dice (e.g. 1d6)")
async def attack(interaction: discord.Interaction, target_name: str, damage_dice: str):
    await interaction.response.defer()
    attacker_name = interaction.user.name

    async with aiohttp.ClientSession() as session:
        async with session.post(attack_url, json={
            "attacker_name": attacker_name,
            "target_name": target_name,
            "damage_dice": damage_dice
        }) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(result["message"])

                if "Dead" in result["message"]:
                    target_user = discord.utils.get(interaction.guild.members, name=target_name)
                    if target_user:
                        try:
                            await target_user.send(f"Your character `{target_name}` has been killed in combat!")
                        except discord.Forbidden:
                            await interaction.followup.send(f"Could not DM {target_name}.")
            else:
                await interaction.followup.send("Attack failed.")

intents = discord.Intents.default()
intents.message_content = True
#client = Client(command_prefix="!", intents=intents)
client = Client()

'''
Example for commands to take in arguments:

@client.tree.command(name="printer", description="I will print what you give me")
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

'''

# slash command for rolling dice
@client.tree.command(name="roll", description="roll a die")
async def roll(interaction: discord.Interaction, dice: str):
    await interaction.response.defer()  # Acknowledge the interaction

    async with aiohttp.ClientSession() as session:
        async with session.get(roll_url, params={"q": dice}) as resp:
            if resp.status == 200:
                result = await resp.json()
                await interaction.followup.send(f"You rolled `{dice}` and got: {result}")
            else:
                await interaction.followup.send("Error contacting the dice roller API.")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
