



import subprocess
import time
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import platform
import shutil

process = None
shouldrestart=1
fromrestart=0
BASE = Path(__file__).parent
hotboot_file = BASE / "hotBoot.txt"
restart_file = BASE / "restart.txt"
pause_file = BASE / "pauseTimes.txt"
bot_file = BASE / "discord_deadlock_bot.py"
raspberry_update_name="deadlock_bot_update"

with open(restart_file,"w") as f:
    f.write("1")

pauseStart=4
pauseEnd=12

def update():
    def copy_contents(scr,dest):
        for item in scr.iterdir():
            target=dest / item.name
            if item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item,target)
            else:
                shutil.copy2(item,target)
    def find_update_folder():
        paths=[
            Path("/media"),
            Path("/mnt"),
            Path("/run/media"),
        ]
        for base_path in paths:
            if not base_path.exists():
                continue
            for root, dirs, files in os.walk(base_path):
                if raspberry_update_name in dirs:
                    return Path(root) / raspberry_update_name
        return None
    path=find_update_folder()
    if path:
        try:
            copy_contents(path,Path(__file__).resolve().parent)
        except Exception as e:
            print(f"Update error {e}",flush=True)

while True:
    if process is None or process.poll() is not None:
        with open(pause_file,"r") as f:
            pauseStart=int(f.readline().strip())
            pauseEnd=int(f.readline().strip())
        with open(restart_file,"r") as f:
            shouldrestart=int(f.readline().strip())
        if shouldrestart==2 and pauseStart<=datetime.now(ZoneInfo("Europe/Berlin")).hour<=pauseEnd:
            time.sleep(1*60) #1 minute
        else:
            try:
                lindistr=platform.freedesktop_os_release()
            except:
                lindistr=None
            
            if shouldrestart:
                with open(hotboot_file,"w") as f:
                    f.write(str(fromrestart))
                
                if lindistr==None:
                    process = subprocess.Popen(["python", bot_file])
                else:
                    update()
                    process = subprocess.Popen(["python3", bot_file])

                fromrestart=1
            else:
                if lindistr==None:
                    exit()
                else:
                    subprocess.run(["sudo","shutdown","-h","now"])

    time.sleep(1)
