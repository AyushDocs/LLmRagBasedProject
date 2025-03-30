import os
import platform
import subprocess

def is_command_available(command):
    """Check if a command is available on the system."""
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def setup_linux():
    """Setup Node.js, npm, and Prettier on Linux"""
    print("[INFO] Detected Linux OS. Installing dependencies...")

    # Update system packages
    subprocess.run(["sudo", "apt", "update", "-y"], check=True)
    subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)

    # Install curl if not installed
    subprocess.run(["sudo", "apt", "install", "-y", "curl"], check=True)

    # Install Node.js if not installed
    if not is_command_available("node"):
        print("[INFO] Installing Node.js...")
        subprocess.run("curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -", shell=True, check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "nodejs"], check=True)
    else:
        print("[INFO] Node.js is already installed.")

    # Install npm if not installed
    if not is_command_available("npm"):
        print("[INFO] Installing npm...")
        subprocess.run(["sudo", "apt", "install", "-y", "npm"], check=True)
    else:
        print("[INFO] npm is already installed.")

    # Install Prettier globally
    subprocess.run(["npm", "install", "-g", "prettier"], check=True)
    print("[INFO] Setup complete on Linux!")

def setup_windows():
    """Setup Node.js, npm, and Prettier on Windows"""
    print("[INFO] Detected Windows OS. Installing dependencies...")

    # Download and install Node.js
    node_installer = "node.msi"
    if not is_command_available("node"):
        print("[INFO] Downloading Node.js installer...")
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri https://nodejs.org/dist/v18.16.0/node-v18.16.0-x64.msi -OutFile {node_installer}"], check=True)
        print("[INFO] Installing Node.js...")
        subprocess.run(["msiexec", "/i", node_installer, "/quiet", "/norestart"], check=True)
        os.remove(node_installer)
    else:
        print("[INFO] Node.js is already installed.")

    # Install Prettier globally
    subprocess.run(["npm", "install", "-g", "prettier"], check=True)
    print("[INFO] Setup complete on Windows!")

def init():
    os_type = platform.system()
    
    if os_type == "Linux":
        setup_linux()
    elif os_type == "Windows":
        setup_windows()
    else:
        print("[ERROR] Unsupported operating system!")

