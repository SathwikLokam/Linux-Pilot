import json

# Correct mapping of the keywords to their argument structure and command representation
commands = {
    "DeAuth": {
        "arguments": {
            "file": ["Enter the name of the file", None],
            "type": ["What is the type of file", None]
        },
        "representation": "DeAuth"
    },
    "StopNetworkManager": {
        "arguments": {},
        "representation": "Stop_networkManager"
    },
    "TopProcesses": {
        "arguments": {},
        "representation": "top"
    },
    "CurrentDirectory": {
        "arguments": {},
        "representation": "pwd"
    },
    "SendICMP": {
        "arguments": {},
        "representation": "Send_ICMP"
    },
    "ListFiles": {
        "arguments": {},
        "representation": "ls"
    },
    "CheckDiskSpace": {
        "arguments": {},
        "representation": "df -h"
    },
    "SystemUptime": {
        "arguments": {},
        "representation": "uptime"
    },
    "MemoryUsage": {
        "arguments": {},
        "representation": "free -m"
    },
    "DisplayHostname": {
        "arguments": {},
        "representation": "hostname"
    },
    "ShowDateTime": {
        "arguments": {},
        "representation": "date"
    },
    "PingServer": {
        "arguments": {
            "server": ["Enter the server to ping", None]
        },
        "representation": "ping"
    },
    "ActiveConnections": {
        "arguments": {},
        "representation": "netstat -tuln"
    },
    "RoutingTable": {
        "arguments": {},
        "representation": "route -n"
    },
    "CurrentUser": {
        "arguments": {},
        "representation": "whoami"
    },
    "FindFileByName": {
        "arguments": {
            "filename": ["Enter the filename to search", None]
        },
        "representation": "find / -name <filename>"
    },
    "SearchWordInFile": {
        "arguments": {
            "word": ["Enter the word to search", None],
            "file": ["Enter the file to search in", None]
        },
        "representation": "grep <word> <file>"
    },
    "CPUInfo": {
        "arguments": {},
        "representation": "lscpu"
    },
    "HardwareInfo": {
        "arguments": {},
        "representation": "lshw"
    },
    "SystemLogs": {
        "arguments": {},
        "representation": "dmesg"
    },
    "RestartSystem": {
        "arguments": {},
        "representation": "reboot"
    },
    "ShutdownSystem": {
        "arguments": {},
        "representation": "shutdown -h now"
    },
    "MountDrive": {
        "arguments": {
            "drive": ["Enter the drive to mount", None],
            "mount_point": ["Enter the mount point", None]
        },
        "representation": "mount <drive> <mount_point>"
    },
    "UnmountDrive": {
        "arguments": {
            "drive": ["Enter the drive to unmount", None]
        },
        "representation": "umount <drive>"
    },
    "ChangePermissions": {
        "arguments": {
            "permissions": ["Enter the permissions to set", None],
            "file": ["Enter the file to modify", None]
        },
        "representation": "chmod <permissions> <file>"
    },
    "ChangeOwner": {
        "arguments": {
            "owner": ["Enter the new owner", None],
            "group": ["Enter the new group", None],
            "file": ["Enter the file to modify", None]
        },
        "representation": "chown <owner>:<group> <file>"
    },
    "ProcessTree": {
        "arguments": {},
        "representation": "pstree"
    },
    "KillProcessByID": {
        "arguments": {
            "pid": ["Enter the process ID", None]
        },
        "representation": "kill <pid>"
    },
    "DiskUsage": {
        "arguments": {
            "directory": ["Enter the directory to check", None]
        },
        "representation": "du -sh <directory>"
    },
    "ActiveUsers": {
        "arguments": {},
        "representation": "w"
    },
    "SystemLogs": {
        "arguments": {},
        "representation": "journalctl"
    },
    "IPInfo": {
        "arguments": {},
        "representation": "ip addr"
    },
    "ActiveSessions": {
        "arguments": {},
        "representation": "who"
    },
    "EnvVariables": {
        "arguments": {},
        "representation": "printenv"
    },
    "SoftwareUpdates": {
        "arguments": {},
        "representation": "apt update"
    },
    "InstallSoftware": {
        "arguments": {
            "package": ["Enter the package to install", None]
        },
        "representation": "apt install <package>"
    },
    "RemoveSoftware": {
        "arguments": {
            "package": ["Enter the package to remove", None]
        },
        "representation": "apt remove <package>"
    },
    "SearchSoftware": {
        "arguments": {
            "package": ["Enter the package to search", None]
        },
        "representation": "apt search <package>"
    },
    "NetworkInterfaces": {
        "arguments": {},
        "representation": "ifconfig"
    },
    "OpenPorts": {
        "arguments": {},
        "representation": "netstat -tulpn"
    },
    "MemoryStats": {
        "arguments": {},
        "representation": "vmstat"
    },
    "InstalledPackages": {
        "arguments": {},
        "representation": "dpkg -l"
    },
    "FirewallStatus": {
        "arguments": {},
        "representation": "ufw status"
    },
    "StartService": {
        "arguments": {
            "service": ["Enter the service to start", None]
        },
        "representation": "systemctl start <service>"
    },
    "StopService": {
        "arguments": {
            "service": ["Enter the service to stop", None]
        },
        "representation": "systemctl stop <service>"
    },
    "RestartService": {
        "arguments": {
            "service": ["Enter the service to restart", None]
        },
        "representation": "systemctl restart <service>"
    },
    "EnableServiceAtBoot": {
        "arguments": {
            "service": ["Enter the service to enable", None]
        },
        "representation": "systemctl enable <service>"
    },
    "DisableServiceAtBoot": {
        "arguments": {
            "service": ["Enter the service to disable", None]
        },
        "representation": "systemctl disable <service>"
    },
    "SystemLoad": {
        "arguments": {},
        "representation": "top"
    },
    "SystemInfo": {
        "arguments": {},
        "representation": "uname -a"
    },
    "NetworkSpeed": {
        "arguments": {},
        "representation": "speedtest-cli"
    },
    "ChangeDir": {
        "arguments": {
            "directory": ["Enter the directory to change to", None]
        },
        "representation": "cd <directory>"
    },
    "ShowFileContent": {
        "arguments": {
            "file": ["Enter the file to display", None]
        },
        "representation": "cat <file>"
    },
    "CreateDir": {
        "arguments": {
            "directory": ["Enter the directory to create", None]
        },
        "representation": "mkdir <directory>"
    },
    "CreateFile": {
        "arguments": {
            "file": ["Enter the file to create", None]
        },
        "representation": "touch <file>"
    },
    "RemoveFile": {
        "arguments": {
            "file": ["Enter the file to remove", None]
        },
        "representation": "rm <file>"
    },
    "RemoveDir": {
        "arguments": {
            "directory": ["Enter the directory to remove", None]
        },
        "representation": "rmdir <directory>"
    },
    "ShowDate": {
        "arguments": {},
        "representation": "date"
    },
    "FindLargestFiles": {
        "arguments": {
            "directory": ["Enter the directory to check", None]
        },
        "representation": "du -ah / | sort -n -r | head -n 10"
    },
    "DiskErrors": {
        "arguments": {
            "disk": ["Enter the disk to check", None]
        },
        "representation": "fsck <disk>"
    },
    "ListUsers": {
        "arguments": {},
        "representation": "cat /etc/passwd"
    },
    "HelloFrame": {
        "arguments": {},
        "representation": "hello_frame"
    },
    "OpenFile": {
        "arguments": {
            "file": ["Enter the name of the file", None],
            "type": ["What is the type of file", None]
        },
        "representation": "open"
    }
}

# Function to create JSON files for each command
def create_json_files(commands):
    for keyword, frame in commands.items():
        filename = f"{keyword}.json"
        with open(filename, "w") as f:
            json.dump(frame, f, indent=2)
        print(f"Created: {filename}")

# Create JSON files for all commands
create_json_files(commands)
