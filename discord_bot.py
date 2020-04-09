import os
import shutil
import subprocess

import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()
os.chdir('/home/pi/MultiWorld-Utilities/')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
AVAILABLE_PLAYERS = []
SERVER_ADDRESS = "localhost:38281"
client = discord.Client()
multiworld_server = None


def _validate_player(player_name):
    if player_name not in AVAILABLE_PLAYERS:
        raise ValueError("{} is not a valid player name".format(player_name))


def _build_command_line(players_list):
    number_of_players = len(players_list)
    command = "python3 Mystery.py --multi {} ".format(len(players_list))
    for number, name in enumerate(players_list):
        _validate_player(name)
        command += "--p{} {}.yaml ".format(str(number + 1), name)
    command += "--create_spoiler --outputpath /tmp/chromebold_multiworld"
    return command


def _generate_randomized_game(channel, players_list):
    try:
        shutil.rmtree("/tmp/chromebold_multiworld")
    except:
        pass
    os.mkdir("/tmp/chromebold_multiworld")
    os.system(_build_command_line(players_list))
    for filename in sorted(os.listdir("/tmp/chromebold_multiworld")):
        yield "/tmp/chromebold_multiworld/{}".format(filename)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!kobold '):
        formatted_message = message.content.split('!kobold ', 1)[1]

        if formatted_message.startswith('player list') or formatted_message.startswith('available players'):
            await message.channel.send("Here's the current list of available players:")
            await message.channel.send(str(AVAILABLE_PLAYERS))
        elif formatted_message.startswith('roll a seed '):
            formatted_message = formatted_message.split('roll a seed ', 1)[1].lower()
            await message.channel.send("Generating new game. Please wait.")
            await message.channel.send("(This could take several minutes depending on the number of players; I'll raise an error if generation fails for any reason!)")
            try:
                for response in _generate_randomized_game(message.channel,
                                                          formatted_message.split(' ')):
                    if response.endswith("_multidata"):
                        multidata_filename = response
                    elif response.endswith("multisave"):
                        continue
                    else:
                        await message.channel.send(file=discord.File(response))
            except Exception as e:
                response = "Error generating game. Please try again."
                print(e)
                await message.channel.send(response)
                return

            global multiworld_server
            if multiworld_server is not None:
                multiworld_server.kill()
                multiworld_server = None

            multiworld_server = subprocess.Popen(["python3", "MultiServer.py", "--multidata", multidata_filename])
            await message.channel.send("Server available at: {}".format(SERVER_ADDRESS))
        elif formatted_message.startswith('server address') or formatted_message.startswith('server info'):
            await message.channel.send("Here's the current server address: {}".format(SERVER_ADDRESS))


client.run(TOKEN)
