from colorama import init, Fore, Style  
import subprocess, os

# cat command
def cat(self, user_input):
    try:
        args = user_input.split()[1:]
        if len(args) < 1:
            print(Fore.LIGHTBLACK_EX + "Usage: cat <file>")
            return
        filename = args[0]
        if self.bin_check(filename):
            print(Fore.LIGHTBLACK_EX + f"Error: File '{filename}' is a binary file. Cannot display content.")
            return
        output = subprocess.run([self.busybox_path, 'cat', filename], capture_output=True, text=True)
        
        if output.returncode == 0:
            print(Fore.LIGHTBLACK_EX + output.stdout)
        else:
            print(Fore.LIGHTBLACK_EX + f"Error reading file: {output.stderr.strip()}")

    except Exception as e:
        print(Fore.LIGHTBLACK_EX + f"An error occurred: {e}")

# tree command
def tree(self):
    # Read lines for the tree
    def get_tree_lines(path, prefix, is_main_folder=True):
        lines = []
        contents = os.listdir(path)

        # Separate directories and files
        dirs = [d for d in contents if os.path.isdir(os.path.join(path, d))]
        files = [f for f in contents if not os.path.isdir(os.path.join(path, f))]

        # Sort directories and files separately
        dirs.sort()
        files.sort()

        # Define folders/files to be hidden
        hidden_items = {".ffscore", "RunShell", ".RunShell.bat", ".install_req.bat", ".git", ".gitignore"}

        for item in dirs + files:
            try:
                full_path = os.path.join(path, item)
                if item not in hidden_items:
                    if os.path.isdir(full_path):
                        lines.append(f"{prefix}{'    ' if is_main_folder else '    '}{Fore.LIGHTBLACK_EX}\U0001F4C1 {item}{Fore.RESET}")
                        lines.extend(get_tree_lines(full_path, prefix + '    ', is_main_folder=False))
                    else:
                        lines.append(f"{prefix}{'    ' if is_main_folder else '    '}\U0001F4C4 {item}")
            except Exception as e:
                print(Fore.LIGHTBLACK_EX + f"An error occurred: {e}")

        return lines

    # Print out the tree itself, including emoji handling
    def print_tree(tree_lines):
        for line in tree_lines:
            if line.endswith('.fss'):
                print(line.replace("\U0001F4C4", "\U0001F4DC"))

            else:
                print(line)

    print(Fore.LIGHTYELLOW_EX + f" Directory Tree of {Fore.GREEN}{self.current_path}")
    tree_lines = get_tree_lines(self.current_path, '', is_main_folder=True)
    if len(tree_lines) > 50:
        warning_message = f"{Fore.RED}WARNING: TREE IS LONG ({len(tree_lines)} LINES)! " \
                            f"DO YOU STILL WANT TO PRINT?"

        print(warning_message.center(os.get_terminal_size().columns))
        user_input = input(Fore.MAGENTA + "(y/N): " + Fore.RESET).lower()
        if user_input == 'y' or user_input == 'Y':
            print_tree(tree_lines)

        else:
             return

    else:
        print_tree(tree_lines)