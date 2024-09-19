from colorama import init, Fore, Style  
import subprocess, os

# restart command
def restart(self):
    try:
        self.clear_screen()
        os.system(f'call \"{self.script_path}\.RunShell.bat\"')

    except Exception as e:
        print(Fore.LIGHTBLACK_EX + f"An error occurred: {e}")