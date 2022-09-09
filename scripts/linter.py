"""
    Project --> Linter
"""
import subprocess
from pathlib import Path


def shell_cmd(name=None, cmd=None, check=True):
    """
    Shell-Command Wrapper
    """
    print(f"""Running... < {name} >""")
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError:
        print(f"""Error while running {name}""")


# Watch Directories
main_folders = ["src"] # , "tests"

# Base Directory
base_dir = Path(__file__).parents[1]

# Cleaner
def cleaner(path_to_watch):
    shell_cmd("isort", f'''python -m isort --profile black "{ path_to_watch }"''')
    shell_cmd("black", f'''python -m black "{ path_to_watch }"''')
    shell_cmd("pylint", f'''python -m pylint "{ path_to_watch }"''', check=False)

for folder in main_folders:
    cleaner(folder)