import socket
import pickle
import threading

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((server, port))
except socket.error as e:
    print("Bind error:", e)

s.listen(2)
print("Waiting for connections... Server started!")

# Shared game state for 2 players
players = [
    {"pos": (100, 300), "shield_pos": (90, 268), "bullets": [], "health": 4, "opponent_health": 4},
    {"pos": (900, 300), "shield_pos": (890, 277), "bullets": [], "health": 4, "opponent_health": 4},
]

connections = [None, None]
both_connected = threading.Event()


def threaded_client(conn, player_id):
    # Send the player their assigned ID
    conn.send(pickle.dumps(player_id))

    # Wait until both players are connected before starting game loop
    print(f"Player {player_id} waiting for opponent...")
    both_connected.wait()

    # Send "ready" signal
    conn.send(pickle.dumps("ready"))
    print(f"Player {player_id} game starting!")

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                print(f"Player {player_id} disconnected")
                break

            # Update this player's state
            player_state = pickle.loads(data)
            players[player_id] = player_state

            # Send back the OTHER player's state
            opponent_id = 1 - player_id
            reply = players[opponent_id]
            conn.sendall(pickle.dumps(reply))

        except Exception as e:
            print(f"Error with player {player_id}: {e}")
            break

    print(f"Player {player_id} lost connection")
    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print(f"Player {current_player} connected from {addr}")

    connections[current_player] = conn
    t = threading.Thread(target=threaded_client, args=(conn, current_player))
    t.daemon = True
    t.start()

    current_player += 1

    if current_player >= 2:
        print("Both players connected! Starting game...")
        both_connected.set()
        # Wait for next pair (reset for future games)
        break

# Keep main thread alive while game is running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nServer shutting down.")
    s.close()
