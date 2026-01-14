# Star Wars Spaceship Game

A multiplayer Python game featuring iconic Star Wars spaceships (X-Wing and TIE Fighter). Built using `pygame` and custom socket networking.

## 🚀 Features

* **Multiplayer Gameplay**: Play against a friend over a local network (LAN) or the internet.
* **Iconic Ships**: Pilot an X-Wing or a TIE Fighter.
* **Combat System**: Shoot lasers and dodge enemy fire.
* **Client-Server Architecture**: Dedicated server script to manage game state and connections.

## 🛠️ Technologies Used

* **Language**: Python 3.x
* **Library**: [Pygame](https://www.pygame.org/) (for graphics and input handling)
* **Networking**: Python `socket` and `threading` (standard libraries)

## 📋 Prerequisites

Before running the game, ensure you have Python installed. You also need to install the `pygame` library.

```bash
pip install pygame

```

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/montg1/Starwar_spaceship_game.git

```


2. Navigate to the project directory:
```bash
cd Starwar_spaceship_game

```



## 🎮 How to Play

Since this is a multiplayer game, you must run the **Server** first, and then connect two **Clients**.

### 1. Start the Server

Run the server script to start listening for connections.
*(Note: The file is currently named `sever.py` in the repository)*

```bash
python sever.py

```

*The server will start and wait for players to connect.*

### 2. Start the Client(s)

Open a new terminal window (or two) and run the client script.

```bash
python client.py

```

* **Player 1** will connect as the first ship.
* **Player 2** (on a separate terminal/machine) will connect as the second ship.

### Controls

* **Movement**: Arrow Keys or WASD (depending on your configuration)
* **Shoot**: Spacebar

## 📂 Project Structure

* `sever.py`: The main server script that handles game state and player connections.
* `client.py`: The client-side script that connects to the server and renders the game.
* `Network.py`: Handles the networking logic (sending/receiving data).
* `X_Wing.py` / `Tie_Fighter.py`: Classes defining the specific spaceship behaviors and attributes.
* `Assets/`: Folder containing game images and sounds.

## 📝 Configuration (Optional)

If you are playing on different computers on the same network:

1. Open `Network.py` or `client.py`.
2. Change the IP address from `localhost` (or `127.0.0.1`) to the **IPv4 address** of the computer running `sever.py`.

## ⚠️ Disclaimer

This is a fan-made educational project. *Star Wars*, *X-Wing*, and *TIE Fighter* are trademarks of Disney and Lucasfilm. This project is not affiliated with or endorsed by them.
