import discord
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

API_URL = "http://localhost:8000/api"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    #create character
    if message.content.startswith("/character create"):
        parts = message.content.split(" ", 3)
        if len(parts) < 4:
            await message.channel.send("Please provide the name and other information about your character.")
            return
        name = parts[2]
        other_info = parts[3]
        
        #send request to create character
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}/character", json={
                "name": name,
                "other_info": other_info
            })
        await message.channel.send(f"Character {name} created!")

    #view character
    if message.content.startswith("/character view"):
        parts = message.content.split(" ", 2)
        if len(parts) < 3:
            await message.channel.send("Please provide the character's name.")
            return
        name = parts[2]
        
        #send request to get character
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/character/{name}")
        
        if response.status_code == 200:
            character = response.json()
            await message.channel.send(f"Character details: {character}")
        else:
            await message.channel.send("Character not found.")

    #update character
    if message.content.startswith("/character update"):
        parts = message.content.split(" ", 3)
        if len(parts) < 4:
            await message.channel.send("Please provide the name and other info to update.")
            return
        name = parts[2]
        other_info = parts[3]
        
        #send request to update character
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{API_URL}/character/{name}", json={
                "other_info": other_info
            })
        
        await message.channel.send(f"Character {name} updated!")

    #delete character
    if message.content.startswith("/character delete"):
        parts = message.content.split(" ", 2)
        if len(parts) < 3:
            await message.channel.send("Please provide the character's name to delete.")
            return
        name = parts[2]
        
        #send request to delete character
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{API_URL}/character/{name}")
        
        await message.channel.send(f"Character {name} deleted!")

    #attack command
    if message.content.startswith("/attack"):
        parts = message.content.split(" ", 3)
        if len(parts) < 4:
            await message.channel.send("Please provide a target name and damage dice (e.g., /attack {target} 1d6).")
            return
        target_name = parts[2]
        damage_dice = parts[3]

        #perform attack
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}/attack", json={
                "attacker_name": message.author.name,
                "target_name": target_name,
                "damage_dice": damage_dice
            })
        
        attack_result = response.json()
        await message.channel.send(attack_result["message"])

        #if target dies, dm both players
        if "Dead" in attack_result["message"]:
            target_user = discord.utils.get(message.guild.members, name=target_name)
            if target_user:
                await target_user.send(f"Your character {target_name} has been killed in combat!")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
