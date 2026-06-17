



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

pauseStart=4
pauseEnd=12

def update():
    print("update",flush=True)
    def copy_contents(scr,dest):
        print("copying content",flush=True)
        for item in scr.iterdir():
            target=dest / item.name
            if item.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item,target)
            else:
                shutil.copy2(item,target)
    def find_update_folder():
        print("finding folder",flush=True)
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
    print("folder: ",path,flush=True)
    if path:
        try:
            copy_contents(path,Path(__file__).resolve().parent)
        except Exception as e:
            print(f"Update error {e}",flush=True)
    print("update done",flush=True)

while True:
    if process is None or process.poll() is not None:
        with open(pause_file,"r") as f:
            pauseStart=int(f.readline().strip())
            pauseEnd=int(f.readline().strip())
        with open(restart_file,"r") as f:
            shouldrestart=int(f.readline().strip())
        if shouldrestart==2 and pauseStart<=datetime.now(ZoneInfo("Europe/Berlin")).hour<=pauseEnd:
            time.sleep(1*60*60) #1 hour
        else:
            if shouldrestart:
                with open(hotboot_file,"w") as f:
                    f.write(str(fromrestart))
                if platform.freedesktop_os_release()==None:
                    process = subprocess.Popen(["python", bot_file])
                else:
                    print("a",flush=True)
                    update()
                    process = subprocess.Popen(["python3", bot_file])
                fromrestart=1
            else:
                if platform.freedesktop_os_release()==None:
                    exit()
                else:
                    subprocess.run(["sudo","shutdown","-h","now"])

    time.sleep(1)
