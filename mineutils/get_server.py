import argparse
import requests
import os

from datetime import datetime

# Default values when creating the 'run.sh' script ('-r')
min_ram = 2048
max_ram = 3072

# Default values for the download
chunk_size = 4096  # 4K
report_after = 64  # Report after 64 chunks (every 256K)

# Set up the argument parser, and parse the given arguments
parser = argparse.ArgumentParser()
parser.add_argument('version', help='indicates the version to be downloaded')
parser.add_argument('-p', '--properties', help="creates a default properties file",
                    action="store_true")

parser.add_argument('-e', '--eula', help="creates an already-accepted EULA file",
                    action="store_true")

parser.add_argument('-r', '--runscript', help="creates a script to run the server",
                    action="store_true")

parser.add_argument('-d', '--directory', help="specifies the output directory")
args = parser.parse_args()

# Change to the specified directory, if any was specified
if args.directory:
    os.makedirs(args.directory, exist_ok=True)
    os.chdir(args.directory)
    print('Changed directory to', args.directory)

# Determine the download url based on the given server version
url = 'https://s3.amazonaws.com/Minecraft.Download/versions/{0}/minecraft_server.{0}.jar'.format(args.version)

# Open a stream to it, don't download the whole file directly
r = requests.get(url, stream=True)
try:
    # Ensure we didn't get a 404
    r.raise_for_status()
    
    # Download the specified version
    done = 0.0
    total = float(r.headers.get('Content-Length', 0))
    with open('minecraft_server.jar', 'wb') as f:
        for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
            f.write(chunk)
            done += len(chunk)
            if total and i % report_after == 0:
                print('{:.2%} downloaded.'.format(done / total))
    
    print('100% downloaded.')
    
    # Create the accepted EULA file
    if args.eula:
        with open('eula.txt', 'w') as f:
            f.write('# By changing the setting below to TRUE you are ')
            f.write('indicating your agreement to our EULA ')
            f.write('(https://account.mojang.com/documents/minecraft_eula).\n')
            f.write(datetime.now().strftime('# %a %b %d %H:%M:%S %Z %Y\n'))
            f.write('eula=true\n')
        print('Created eula.txt file.')
    
    # Create a default server.properties files
    if args.properties:
        with open('server.properties', 'w') as f:
            f.write("""#Minecraft server properties
#{}
max-tick-time=60000
generator-settings=
force-gamemode=false
allow-nether=true
gamemode=0
enable-query=false
player-idle-timeout=0
difficulty=1
spawn-monsters=true
op-permission-level=4
announce-player-achievements=true
pvp=true
snooper-enabled=true
level-type=DEFAULT
hardcore=false
enable-command-block=true
max-players=4
network-compression-threshold=256
resource-pack-sha1=
max-world-size=29999984
server-port=25565
server-ip=
spawn-npcs=true
allow-flight=false
level-name=world
view-distance=10
resource-pack=
spawn-animals=true
white-list=false
generate-structures=true
online-mode=false
max-build-height=256
level-seed=
prevent-proxy-connections=false
use-native-transport=true
enable-rcon=false
motd=Server setup with getmc.py
""".format(datetime.now().strftime('#%a %b %d %H:%M:%S %Z %Y')))
        print('Created server.properties file.')
    
    # Create the run script
    if args.runscript:
        with open('run.sh', 'w') as f:
            f.write('java -Xms{}M -Xmx{}M -jar minecraft_server.jar nogui'\
                    .format(min_ram, max_ram))
        #                   -rwxr--r--
        os.chmod('run.sh', 0b111100100)
        print('Created run.sh file.')

except requests.exceptions.HTTPError:
    print('Error: Could not download .jar for version '+args.version)

