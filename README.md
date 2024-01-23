# ffmpegShell.py

## Introduction

ffmpegShell is a Python-based shell that provides a command-line interface for the FFmpeg multimedia framework. It allows users to interact with FFmpeg using a set of predefined commands, as well as execute custom scripts.

## Features

- Command-line Interface: ffmpegShell provides a command-line interface for interacting with FFmpeg. Users can enter commands directly into the shell, and the shell will execute them.

- Auto Text Completion: The shell supports auto text completion, which can be enabled by pressing the Tab key. This feature can help users quickly enter commands and filenames.

- .fss Scripts: ffmpegShell can execute custom scripts written in a special format. These scripts can contain a series of commands to be executed by the shell. They can be executed using ```fss``` command, as a plugin in ```.ffscore/.fssPlugins``` directory (Look into ``auto.ffexec`` file) or by using "run" argument. e.g.: ```ffs run(test.fss, test_2.fss)```

- Python Code Blocks: .fss Scripts support python code blocks, shell will execute them as if they were usual python script (You can import packages). You can make code block like this:

```
[python]
print('code')
[/python]
```

- Plugin System: The shell supports a plugin system, which allows users to extend its functionality by writing custom plugins. Plugins can be written in ffmpegShell Commands or Python Code Blocks.

- Experiments: The shell has experiments feature, which allows users to e.g. add or remove ffmpegShell directory to the system PATH. This can be useful for running the shell from any directory using cmd.

- Color Support: The shell supports ANSI color codes, which can be used to colorize the output of commands. (Currently not supported by echo/print command)

Colors:
```
- <ansiblack> - Black
- <ansired> - Red
- <ansigreen> - Green
- <ansiyellow> - Yellow
- <ansiblue> - Blue
- <ansimagenta> - Magenta
- <ansicyan> - Cyan
- <ansigray> - Gray
- <ansibrightblack> - Bright Black
- <ansibrightred> - Bright Red
- <ansibrightgreen> - Bright Green
- <ansibrightyellow> - Bright Yellow
- <ansibrightblue> - Bright Blue
- <ansibrightmagenta> - Bright Magenta
- <ansibrightcyan> - Bright Cyan
- <ansibrightwhite> - Bright White
```