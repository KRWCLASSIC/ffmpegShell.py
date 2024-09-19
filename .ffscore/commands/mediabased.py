from colorama import init, Fore, Style  
import subprocess, os

# fps command
def set_fps(self, user_input):
    try:
        args = user_input.split()[1:]

        if len(args) < 2:
            raise ValueError(Fore.LIGHTBLACK_EX + "Usage: fps <fps amount> <input file> [<output file>]")

        fps_amount = args[0]
        input_file = args[1]

        if not os.path.isfile(input_file):
            print(Fore.LIGHTBLACK_EX + f"Error: {input_file} does not exist.")
            return

        if len(args) >= 3:
            output_file = args[2]

        else:
            filename, ext = os.path.splitext(input_file)
            output_file = f"{filename}_fps{ext}"

        override = ''
        if os.path.isfile(output_file):
            override = input(Fore.LIGHTBLACK_EX + f"File '{output_file}' already exists. Overwrite? (y/N): ")

        else:
            override = 'y'

        if override == 'y':
            command = [
                self.ffmpeg_path,
                '-hide_banner',
                '-y',
                '-i', input_file,
                '-r', fps_amount,
                output_file
            ]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break

                if output:
                    print(f"{Fore.LIGHTBLACK_EX}{output.strip()}{Fore.RESET}")

            return_code = process.wait()

            if return_code != 0:
                print(Fore.LIGHTBLACK_EX + f"An error occurred while running the command. Return code: {return_code}")

        else:
            print(Fore.LIGHTBLACK_EX + "Operation aborted.")

    except Exception as e:
        print(Fore.LIGHTBLACK_EX + f"An error occurred: {e}")

# bitrate command
def set_bitrate(self, user_input):
    try:
        args = user_input.split()[1:]
        if len(args) < 3:
            raise ValueError(Fore.LIGHTBLACK_EX + "Usage: bitrate <number> <-v(ideo) or -a(udio)> <input file> [<output file>]")

        bitrate = args[0]
        audioorvid = args[1]
        input_file = args[2]

        if audioorvid == '-v':
            audioorvid = ':v'
        elif audioorvid == '-a':
            audioorvid = ':a'
        else:
            print(Fore.LIGHTBLACK_EX + "Please specify if it's video or audio")
            return

        if not os.path.isfile(input_file):
            print(Fore.LIGHTBLACK_EX + f"Error: {input_file} does not exist.")
            return

        if len(args) >= 4:
            output_file = args[3]
        else:
            filename, ext = os.path.splitext(input_file)
            output_file = f"{filename}_bitrate{ext}"

        override = ''
        if os.path.isfile(output_file):
            override = input(Fore.LIGHTBLACK_EX + f"File '{output_file}' already exists. Overwrite? (y/N): ")

        else:
            override = 'y'

        if override == 'y':
            command = [
                self.ffmpeg_path,
                '-hide_banner',
                '-y',
                '-i', input_file,
                f'-b{audioorvid}', bitrate,
                '-map_metadata', '-1',
                output_file
            ]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(f"{Fore.LIGHTBLACK_EX}{output.strip()}{Fore.RESET}")

            return_code = process.wait()

            if return_code != 0:
                print(Fore.LIGHTBLACK_EX + f"An error occurred while running the command. Return code: {return_code}")

        else:
            print(Fore.LIGHTBLACK_EX + "Operation aborted.")

    except Exception as e:
        print(Fore.LIGHTBLACK_EX + f"An error occurred: {e}")