from datetime import datetime                                   # Used for prompts
import subprocess                                               # Used for running cmd proccesses
import winreg                                                   # Used for modifying windows registry (User's PATH) and exit function
import msvcrt                                                   # Used for pause command and clearing potential input buffering from commands
import shutil                                                   # Used for removing cache folder
import time                                                     # Used for timeout/wait command
import sys                                                      # Used for setting up self.script_path
import os                                                       # Used for using deafult cmd commands
try:                                                            # Stop it from crashing when package is not installed
    from prompt_toolkit.completion import Completer, Completion # Used for Auto Text Completion
    from prompt_toolkit import PromptSession, HTML              # Used for Auto Text Completion input handler and color encoding fix
    from colorama import init, Fore, Style                      # Used for colors
except:
    print("Please run '.install_req.bat' inside '.ffscore' folder")

# What ffmpegShell?
# Just tool and shell to make using ffmpeg easier, no more online converters etc.!
# ffs is equiped with many commands known from command prompt, powershell and bash
# Recommended to use PATH experiment

# Also yeah, I have severe OCD so most stuff is sorted from longest to shortest, alphabetical etc.

# Bro, I need to update 3 seperate functions when adding new command :sob: | ill fix that

# Colorama color auto reset
init(autoreset=True)

# Allow python interpreter to search for imports in .fsscore folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.ffscore')))

# Main Class
class ffmpegShell:

    # Setting up requiered variables
    def __init__(self):

        # Initilize filebased commands
        from commands.filebased import cat; self.cat = lambda user_input: cat(self, user_input) # type: ignore
        from commands.filebased import tree; self.tree = lambda: tree(self) # type: ignore

        # Initilize filebased commands
        from commands.mediabased import set_fps; self.set_fps = lambda user_input: set_fps(self, user_input) # type: ignore
        from commands.mediabased import set_bitrate; self.set_bitrate = lambda user_input: set_bitrate(self, user_input) # type: ignore

        # Initilize misc commands
        from commands.misc import restart; self.restart = lambda: restart(self) # type: ignore

        self.ffs_ver = '0.3 (Main Branch - NonRelease)'
        self.running = False
        self.current_path = os.getcwd()
        self.ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.ffscore', 'ffmpeg', 'bin', 'ffmpeg.exe')
        self.variables = {}
        self.ffscore_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.ffscore')
        self.nanoeditor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.ffscore', 'nano', 'nano.exe')
        self.busybox_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.ffscore', 'busybox', 'busybox.exe')
        self.fss_plugins_path = os.path.join(self.ffscore_path, '.fssPlugins')
        self.auto_exec_file = os.path.join(self.fss_plugins_path, 'auto.ffexec')
        script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        root, tail = os.path.splitdrive(script_path)
        self.script_path = os.path.join(root.upper(), tail)
        self.scripts_to_run = self.parse_script_args()
        self.update_prompt_vars()
        self.promptchng('')
        self.remove_pycache()

    # Welcome Message, Plugin Loading, Script Argument Executing, Path Correction, ATC and Shell Input Handler
    def start(self):
        initial_directory = os.getcwd()
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.update_current_directory()
        self.running = True
        os.system('cls')

        # Add autoexec plugins into running queue
        self.load_plugins()

        # Running argument scripts using full path
        for filename in self.scripts_to_run:
            script_path = os.path.join(initial_directory, filename)
            self.execute_script(script_path)

        print(Fore.GREEN + "Welcome to ffmpegShell.py!")
        print("Type 'help' for assistance")
    
        if self.script_path != initial_directory:
            print("Opened in", Fore.GREEN + f"{self.current_path}")

        # ATC    
        session = PromptSession(
            completer=CommandCompleter(self.get_commands()),
            enable_system_prompt=True,
            complete_while_typing=False,
        )
    
        # Input Handler with ATC support
        while self.running:
            try:
                user_input = session.prompt(
                    HTML(f'<ansiyellow>ffmpegShell.py {self.prompt}>>> </ansiyellow>')
                )
            except:
                self.exit()
                break
            
            if user_input.strip():
                self.handle_regular_command(user_input)
            else:
                pass

    # Remove pycache folder on ffs start
    def remove_pycache(self):
        try:
            pycache_path = os.path.join(self.script_path, "__pycache__")
            if os.path.exists(pycache_path) and os.path.isdir(pycache_path):
                shutil.rmtree(pycache_path)
        except:
            pass

    # Update some variables that need to be UTD
    def update_prompt_vars(self):
        self.time = datetime.now().time()

    # Bug fix for entering from outside of the script folder (Why this shit broken :skull:)
    def update_current_directory(self):
        self.current_path = os.getcwd()

    # Loading scripts specified in "run()" launch argument
    def parse_script_args(self):
        scripts = []
        args = sys.argv[1:]
        joined_args = ' '.join(args) 

        if joined_args.startswith('run'):
            arg_str = joined_args[joined_args.find('(')+1:joined_args.rfind(')')]
            scripts = arg_str.split(',')
            scripts = [script.strip() for script in scripts if script.strip()]

        return scripts

    # Loading plugins
    def load_plugins(self):
        if not os.path.exists(self.fss_plugins_path):
            os.makedirs(self.fss_plugins_path)

        if not os.path.exists(self.auto_exec_file):
            with open(self.auto_exec_file, 'w') as auto_file:
                auto_file.write("# List of scripts to auto-execute on shell start: \n\n")
                auto_file.write("# DeafultVideoFolder.fss \n")
                auto_file.write("# AttachingExample.fss \n")
                auto_file.write("# CleanShell.fss")

        with open(self.auto_exec_file, 'r') as auto_file:
            scripts_to_execute = auto_file.readlines()

            for script in scripts_to_execute:
                script = script.strip()

                if not script or script.startswith("#"):
                    continue

                script_path = os.path.join(self.fss_plugins_path, script)

                if os.path.exists(script_path):
                    self.execute_script(script_path)
                else:
                    print(f"Script '{script}' not found in fssPlugins directory.")
        
        self.remove_pycache()

    # Testing function you can attach to using fss scripts and fssPlugins
    def test(self, user_input):
        print(Fore.LIGHTBLACK_EX + '.fss Script attached to the ffmpegShell.py')
        print(Fore.LIGHTBLACK_EX + f'Script Message: {user_input}')

    # Command list for Auto Text Completion system
    def get_commands(self):
        commands = [
            'help', 'tree', 'exit', 'cat', 'cmd', 'fps', 'nano', 'pause',
            'prompt', 'restart', 'bitrate', 'pwd', 'cd', 'dir', 'ls',
            'cls', 'clear', 'echo', 'print', 'wait', 'timeout', 'experiment', 'exp', 'fss'
        ]
        return commands

    # Execute user specified commands
    def handle_regular_command(self, user_input):
        command = user_input.split()[0].lower()

        if command == 'help':
            self.display_help()
        elif command == 'tree':
            self.tree()
        elif command == 'exit':
            self.exit()
        elif command == 'open':
            self.open_cwd()
        elif command == 'info':
            self.show_info()
        elif command == 'cmd':
            self.cmd(user_input)
        elif command == 'cat':
            self.cat(user_input)
        elif command == 'pause':
            self.pause(user_input)
        elif command == 'restart':
            self.restart()
        elif command == 'fps':
            self.set_fps(user_input) 
        elif command == 'nano':
            self.nanoedit(user_input)
        elif command == 'fss':
            self.fss_handler(user_input)
        elif command == 'prompt':
            self.promptchng(user_input)
        elif command == 'bitrate':
            self.set_bitrate(user_input)
        elif command == 'pwd':
            self.print_working_directory()
        elif command == 'cd':
            self.cd_handler(user_input)
        elif command == 'dir' or command == 'ls':
            self.list_directory()
        elif command == 'cls' or command == 'clear':
            self.clear_screen()
        elif command == 'echo' or command == 'print':
            self.echo(user_input)
        elif command == 'wait' or command == 'timeout':
            self.wait(user_input)
        elif command == 'experiment' or command == 'exp':
            self.experiment(user_input)

        else:
            print(Fore.LIGHTBLACK_EX + "Error: Unknown command \"" + command + "\" ")

    # Execute script specified commands
    def execute_command(self, cmd):
        command = cmd.split()[0].lower()

        if command == 'fps':
            self.set_fps(cmd)
        elif command == 'tree':
            self.tree()
        elif command == 'open':
            self.open_cwd()
        elif command == 'exit':
            self.exit()
        elif command == 'info':
            self.show_info()
        elif command == 'pause':
            self.pause(cmd)
        elif command == 'prompt':
            self.promptchng(cmd)
        elif command == 'bitrate':
            self.set_bitrate(cmd)
        elif command == 'pwd':
            self.print_working_directory()
        elif command == 'cd':
            self.cd_handler(cmd)
        elif command == 'dir' or command == 'ls':
            self.list_directory()
        elif command == 'cls' or command == 'clear':
            self.clear_screen()
        elif command == 'echo' or command == 'print':
            self.echo(cmd)
        elif command == 'wait' or command == 'timeout':
            self.wait(cmd)
        elif command == 'experiment' or command == 'exp':
            self.experiment(cmd)
        elif command == 'fss':
            print(Fore.LIGHTBLACK_EX + "Error: 'fss' command is disallowed in .fss script files.")
        elif command == 'cmd':
            print(Fore.LIGHTBLACK_EX + "Error: 'cmd' command is disallowed in .fss script files.")
        elif command == 'nano':
            print(Fore.LIGHTBLACK_EX + "Error: 'nano' command is disallowed in .fss script files.")
        elif command == 'help':
            print(Fore.LIGHTBLACK_EX + "Error: 'help' command is disallowed in .fss script files.")
        elif command == 'restart':
            print(Fore.LIGHTBLACK_EX + "Error: 'restart' command is disallowed in .fss script files.")
        else:
            print(Fore.LIGHTBLACK_EX + "Error: Unknown command \"" + command + "\" ")

    # Execute script itself (Python code blocks and file handler)
    def execute_script(self, filename):
        try:
            fss_file = filename + ".fss"
            if not os.path.exists(filename) and os.path.exists(fss_file):
                filename = fss_file

            with open(filename, 'r') as file:
                commands = file.readlines()
                python_block = False
                python_code = ""

                for cmd in commands:
                    cmd = cmd.strip()

                    if not cmd:
                        continue
                    elif cmd == "[python]":
                        python_block = True
                        continue
                    elif cmd == "[/python]":
                        python_block = False
                        try:
                            exec(python_code, self.variables)
                        except Exception as e:
                            print(Fore.LIGHTBLACK_EX + f"Error: Python code error: {e}")

                        python_code = ""
                        continue

                    if python_block:
                        python_code += cmd + "\n"
                    else:
                        self.execute_command(cmd)

        except FileNotFoundError:
            print(Fore.LIGHTBLACK_EX + f"Error: File '{filename}' not found.")

        except Exception as e:
            print(Fore.LIGHTBLACK_EX + f"Error: An error occurred while executing the script: {e}")

    # fss handler
    def fss_handler(self, user_input):
        if len(user_input.split()) == 2:
            filename = user_input.split()[1]
            self.execute_script(filename)
            pass
        else:
            print(Fore.LIGHTBLACK_EX + "Usage: fss <filename>")
            return


    # Add user specified text to command input prompt
    def promptchng(self, user_input):
        args = user_input.split(maxsplit=1)

        # Supports ANSI html color encodings!
        # e.g. <ansiblack>text</ansiblack>

        # Garbage \/
        # Musisz zrobić tak jak windows, wiec jak -t to dodajesz self.time w zamiast tego cn

        if len(args) > 1:
            words = args[1]

        try:
            self.promptqueue = words
            self.prompt = f'{self.promptqueue} '
            return

        except:
            self.promptqueue = ''
            self.prompt = ''
            return
            
    # wait / timeout command
    def wait(self, user_input):
        try:
            waittime = int(user_input.split()[1])
            time.sleep(waittime)

        except:
            time.sleep(1)

    # pause command
    def pause(self, user_input):
        args = user_input.split(maxsplit=1)

        if len(args) > 1:
            words = args[1]

        try:
            if words == '/':
                words = 'Press any key to continue...'

        except:
            pass

        try:
            print(words)
            msvcrt.getch()

        except:
            msvcrt.getch()

    # echo command
    def echo(self, user_input):
        args = user_input.split(maxsplit=1)

        try:
            if len(args) > 1:
                echomesg = args[1]

            print(f'{echomesg}')

        except:
            print('')

    # exit command
    def exit(self):
        sys.exit()

    # cmd command
    def cmd(self, user_input):
        command = user_input.split(maxsplit=1)

        try:
            if len(command) > 1:
                cmnd = command[1]
            
            os.system(cmnd)

        except Exception:
            print(Fore.LIGHTBLACK_EX + "Usage: cmd <command>")
    
    # experiment / exp command
    def experiment(self, user_input):
        try:
            args = user_input.split()
            if len(args) < 2:
                print(Fore.LIGHTBLACK_EX + "Error: Please specify the experiment you want to toggle.")
                return

            experiment = args[1].lower()

            if experiment == 'path':
                if len(args) < 3:
                    print(Fore.LIGHTBLACK_EX + "Error: Please specify 'add' or 'remove' after 'path'.")
                    return

                action = args[2].lower()

                ffmpegshell_directory = os.path.dirname(os.path.abspath(__file__))
                drive, path = os.path.splitdrive(ffmpegshell_directory)
                ffmpegshell_directory = drive.upper() + path + "\RunShell"

                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
                user_path, _ = winreg.QueryValueEx(key, 'Path')
                user_paths = user_path.split(os.pathsep)

                if action == 'add':
                    if ffmpegshell_directory not in user_paths:
                        user_path += os.pathsep + ffmpegshell_directory
                        winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, user_path)
                        winreg.CloseKey(key)
                        print(f"{Fore.LIGHTGREEN_EX}Added '{ffmpegshell_directory}' to user-specific PATH.")
                        print(f"{Fore.LIGHTGREEN_EX}You can enter the shell by typing 'ffmpegshell' or 'ffs' in cmd.")
                        print(f"{Fore.LIGHTBLACK_EX}Changes may require console restart or computer reboot.{Style.RESET_ALL}")

                    else:
                        print(f"{Fore.GREEN}'{ffmpegshell_directory}' is already in user-specific PATH.")
                        print(f"{Fore.LIGHTGREEN_EX}You can enter the shell by typing 'ffmpegshell' or 'ffs' in cmd.")
                        print(f"{Fore.LIGHTBLACK_EX}Changes may require console restart or computer reboot.{Style.RESET_ALL}")
                        winreg.CloseKey(key)

                elif action == 'remove':
                    if ffmpegshell_directory in user_paths:
                        user_paths.remove(ffmpegshell_directory)
                        user_path = os.pathsep.join(user_paths)
                        winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, user_path)
                        winreg.CloseKey(key)
                        print(f"{Fore.GREEN}Removed '{ffmpegshell_directory}' from user-specific PATH.")
                        print(f"{Fore.LIGHTBLACK_EX}Changes may require console restart or computer reboot.{Style.RESET_ALL}")

                    else:
                        print(f"{Fore.GREEN}'{ffmpegshell_directory}' is not in user-specific PATH.")
                        print(f"{Fore.LIGHTBLACK_EX}Changes may require console restart or computer reboot.{Style.RESET_ALL}")
                        winreg.CloseKey(key)

                else:
                    print(Fore.LIGHTBLACK_EX + "Error: Invalid argument. Please use 'add' or 'remove' after 'path'.")

            elif experiment == 'test':
                print(Fore.LIGHTBLACK_EX + "This is a test.")

            else:
                print(Fore.LIGHTBLACK_EX + "Error: Unknown Experiment.")

        except IndexError:
            print(Fore.LIGHTBLACK_EX + "Error: Please specify the experiment you want to toggle.")

    # help command
    def display_help(self):
        print(Fore.LIGHTYELLOW_EX + " Available commands:")
        print(Fore.CYAN + "    bitrate <number> <arg> <input file> [<output file>]\t" + Fore.RESET + "- Change bitrate of a video or audio")
        print(Fore.CYAN + "    fps <number> <input file> [<output file>]\t\t" + Fore.RESET + "- Change fps of a video")
        print(Fore.CYAN + "    wait or timeout [<number>]\t\t\t\t" + Fore.RESET + "- Wait for given time")
        print(Fore.CYAN + "    echo or print [<text>]\t\t\t\t" + Fore.RESET + "- Print out given text")
        print(Fore.CYAN + "    cd [<directory>]\t\t\t\t\t" + Fore.RESET + "- Change directory")
        print(Fore.CYAN + "    cmd [<command>]\t\t\t\t\t" + Fore.RESET + "- Allows user to execute Command Prompt commands")
        print(Fore.CYAN + "    pause [<text>]\t\t\t\t\t" + Fore.RESET + "- Pause until any key gets pressed")
        print(Fore.CYAN + "    cls or clear\t\t\t\t\t" + Fore.RESET + "- Clear the screen")
        print(Fore.CYAN + "    dir or ls\t\t\t\t\t\t" + Fore.RESET + "- List directory contents")
        print(Fore.CYAN + "    restart\t\t\t\t\t\t" + Fore.RESET + "- Restarts ffmpegShell")
        print(Fore.CYAN + "    help\t\t\t\t\t\t" + Fore.RESET + "- Display help information")
        print(Fore.CYAN + "    exit\t\t\t\t\t\t" + Fore.RESET + "- Exit ffmpegShell")
        print(Fore.CYAN + "    tree\t\t\t\t\t\t" + Fore.RESET + "- Display directory structure")
        print(Fore.CYAN + "    pwd\t\t\t\t\t\t\t" + Fore.RESET + "- Print current working directory")

    # info command
    def show_info(self):
        print(Fore.GREEN + "ffmpegShell.py " + Fore.RESET + "| " + Fore.CYAN + f"Version: win-{self.ffs_ver}")

    # open command
    def open_cwd(self):
        os.startfile(self.current_path)
    # cd handler
    def cd_handler(self, user_input):
        if len(user_input.split()) == 1:
            self.print_working_directory()
        else:
            self.change_directory(user_input)

    # cd command
    def change_directory(self, user_input):
        try:
            directory = user_input.split()[1]

            if directory == "~":
                os.chdir(self.script_path)
                self.current_path = self.script_path
                print(Fore.LIGHTYELLOW_EX + f" Directory changed to: {Fore.GREEN}{self.current_path}")
                return

            if ".ffscore" in directory:
                print(Fore.LIGHTBLACK_EX + "Error: You are not allowed to access this folder from the ffmpegShell.py")
                return

            os.chdir(directory)
            self.current_path = os.getcwd()
            print(Fore.LIGHTYELLOW_EX + f" Directory changed to: {Fore.GREEN}{self.current_path}")

        except Exception as e:
            print(Fore.LIGHTBLACK_EX + f"An error occurred: {e}")
    
    # pwd command
    def print_working_directory(self):
        print(Fore.GREEN + f" {self.current_path}")

    # cls / clear command
    def clear_screen(self):
        os.system('cls')

    # dir / ls command
    def list_directory(self):
        print(Fore.LIGHTYELLOW_EX + f" Directory of {Fore.GREEN}{self.current_path}")
        directory_list = os.listdir()
        directory_list.sort(key=lambda x: (os.path.isdir(os.path.join(os.getcwd(), x)), x.lower()))

        for item in directory_list:
            full_path = os.path.join(os.getcwd(), item)

            if os.path.isdir(full_path) and item != ".ffscore" and item != "RunShell" and item != ".git":
                print(Fore.LIGHTBLACK_EX + f"    \U0001F4C1 {item}")

        for item in directory_list:
            full_path = os.path.join(os.getcwd(), item)

            if os.path.isfile(full_path) and item != ".RunShell.bat" and item != ".install_req.bat" and item != ".gitignore":
                if item.endswith('.fss'):
                    print(Fore.WHITE + f"    \U0001F4DC {item}")

                else:
                    print(Fore.WHITE + f"    \U0001F4C4 {item}")

    # nano command (Nano Text Editor)
    def nanoedit(self, user_input):
        try:
            args = user_input.split()[1:]
            command = [self.nanoeditor_path] + args

            subprocess.run(command, check=True)

        except Exception as e:
            print(f"An error occurred: {e}")

    # Checking if filename is binary file
    def bin_check(self, filename):
        with open(filename, 'rb') as file:
            content = file.read(1024)  # Read a portion of the file
            return b'\x00' in content  # Check for null byte

# Text completion Class
class CommandCompleter(Completer):

    # Linking commands variable from Main Class to this class
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()

        if word_before_cursor and not word_before_cursor.startswith(' '):

            # Suggest commands
            for command in self.commands:
                if command.startswith(word_before_cursor):
                    yield Completion(command, -len(word_before_cursor))

            # Suggest files and folders
            current_path = os.getcwd()
            for item in os.listdir(current_path):
                if item.startswith(word_before_cursor):
                    yield Completion(item, -len(word_before_cursor))

# Starting up the shell
if __name__ == "__main__":
    ffshell = ffmpegShell()
    try:
        ffshell.start()
    except:
        pass

# Ideas: Build it as a module/package so you can use ffshell.start from any script without input, just "import ffmpegshell"
#        Aliases stored in aliases.json inside .ffscore folder, alias command
#        .fss scripts runnable as executeables???? (add filehandler.py)

# Fixes: Add variables support to echo
#        Add proper prompt command support

# Death: ffmpegShellGUI.py

# Evolve: Finish this project and make Project::Quartz (Python Based Windows Shell with Cmd, Powershell and Bash syntaxes)