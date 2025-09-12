import socket
import json

PI_IP = "192.168.100.228"   # <-- replace with your Pi’s IP address
PORT = 5000

def send_command(cmd):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((PI_IP, PORT))
        s.sendall(json.dumps(cmd).encode())
        try:
            response = s.recv(4096).decode()
            if response:
                print("Response:", response)
        except:
            pass

# --- Test 1: Get current macros from Pi
print("Requesting current macros...")
send_command({"get_macros": True})

# --- Test 2: Update macros
print("Sending new macros...")
send_command({"set_macros": {"blink": "CTRL+C", "look_left": "ALT+TAB"}})

# --- Test 3: Confirm they updated
print("Requesting updated macros...")
send_command({"get_macros": True})
