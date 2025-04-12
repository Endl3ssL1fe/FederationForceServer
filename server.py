import socket
import threading
import struct

# === CONFIG ===
HOST = '0.0.0.0'  # Listen on all interfaces (for local testing)
PORT = 30000       # Default port for Federation Force or Pretendo server

# === Authentication Protocol ===
def handle_authentication(conn):
    """
    Handle client authentication by sending a challenge and receiving the response.
    """
    challenge = b'\x01\x02\x03\x04'  # Placeholder challenge data
    conn.sendall(challenge)
    print("[>] Sent authentication challenge")

    # Wait for the client’s response (example: expecting a specific sequence)
    response = conn.recv(1024)
    if response == b'\x04\x03\x02\x01':  # Example: valid response from the client
        print("[+] Authentication successful")
        return True
    else:
        print("[!] Authentication failed")
        return False

# === Packet Handling and Game Protocol ===
def handle_packet(data):
    """
    Parse the incoming packet and return an appropriate response.
    This is where you will implement the actual game-specific logic.
    """
    # For this example, just look at the first byte to determine packet type
    packet_type = data[0]

    # Here, we emulate some simple responses based on the packet type.
    if packet_type == 0x01:
        response = b'\x01\x01'  # Example: valid response to packet type 0x01
    else:
        response = b'\x00\x00'  # Default invalid response

    return response

# === Client Handler ===
def handle_client(conn, addr):
    """
    Handle the client connection, including authentication and packet communication.
    """
    print(f"[+] New connection from {addr}")

    try:
        # Step 1: Handle authentication
        if not handle_authentication(conn):
            conn.close()
            return

        # Step 2: Handle packet communication (e.g., gameplay or multiplayer interactions)
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Client disconnected
            print(f"[>] Received: {data.hex()}")

            # Step 3: Parse packet and send a response
            response = handle_packet(data)
            conn.sendall(response)
            print(f"[<] Sent: {response.hex()}")

    except Exception as e:
        print(f"[!] Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection from {addr} closed")

# === Server Setup ===
def start_server():
    """
    Set up the server to listen for incoming connections and handle them.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Set max backlog to 5 (maximum number of queued connections)
    print(f"[*] Server listening on {HOST}:{PORT}")

    # Main loop to accept client connections
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()  # Start a new thread to handle the client

if __name__ == '__main__':
    start_server()
