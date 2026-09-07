# 🎮 AR Fruit Ninja Game

An interactive **Augmented Reality (AR) hand-controlled Fruit Ninja game** built using Python, OpenCV, MediaPipe, and Pygame.

Instead of using a mouse or keyboard to control the game, the player uses their **real hand movements** through a webcam. The index finger is tracked in real time and acts as a virtual knife to slice fruits.

---

## 📌 Features

- ✋ Real-time hand tracking
- 📷 Webcam-based gameplay
- 🔪 Virtual knife controlled by index finger
- 🍎 Multiple fruits with different scores
- 💣 Bomb obstacles
- ❤️ Three lives system
- 🐌 Slow-motion power-up
- 💥 Visual slicing and explosion effects
- 🔊 Sound effects
- 🏆 High score system
- 🔄 Restart functionality
- 🎮 Smooth gameplay at 60 FPS

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| OpenCV | Webcam access and video processing |
| MediaPipe | Real-time hand tracking |
| Pygame | Game development and user interface |

---

## 🏗️ Project Architecture

```text
User Hand
    │
    ▼
Webcam
    │
    ▼
OpenCV
    │
    ▼
MediaPipe Hand Tracking
    │
    ▼
Index Finger Position
    │
    ▼
Virtual Knife
    │
    ▼
Collision Detection
    │
    ├───────────────┐
    ▼               ▼
Fruits            Bomb
    │               │
    ▼               ▼
Score          Lose Life
    │               │
    └───────┬───────┘
            ▼
        Game Screen


📂 Project Structure
AR-Fruit_Ninja-Game/
│
├── images/
│   ├── apple.png
│   ├── banana.png
│   ├── bomb.png
│   ├── grapes.png
│   ├── heart.png
│   ├── knife.png
│   ├── shield.png
│   ├── slow.png
│   └── strawberry.png
│
├── sounds/
│   ├── apple.mp3
│   ├── bomb.mp3
│   ├── level_up.mp3
│   └── win.mp3
│
├── fruit_ninja.py
├── requirements.txt
├── README.md
├── .gitignore
└── fruit_ninja.spec

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/Rajasekhar-WebDev/AR-Fruit_Ninja-Game.git
2️⃣ Navigate to the Project Folder
cd AR-Fruit_Ninja-Game
3️⃣ Create a Virtual Environment
py -m venv .venv
4️⃣ Activate the Virtual Environment
Windows PowerShell
.venv\Scripts\Activate.ps1
Windows CMD
.venv\Scripts\activate
5️⃣ Install Required Libraries
pip install -r requirements.txt
▶️ Run the Game
python fruit_ninja.py

Make sure:
Your webcam is connected
Camera permissions are enabled
All required libraries are installed

🎮 How to Play
Run the application.
Press SPACE to start the game.
Show your hand in front of the webcam.
Move your index finger.
Your finger controls the virtual knife.
Slice fruits to earn points.
Avoid bombs.
Collect power-ups.
Press R to restart after Game Over.

🍎 Game Objects
Object	Description
🍎 Apple	Fruit to slice
🍌 Banana	Fruit to slice
🍇 Grapes	Fruit to slice
🍓 Strawberry	Fruit to slice
💣 Bomb	Avoid hitting
🐌 Slow	Slow-motion power-up
🛡️ Shield	Protection power-up
❤️ Lives System

The player starts with three lives:

❤️ ❤️ ❤️

When the player hits a bomb, a life may be lost.

When all lives are lost:

GAME OVER
🐌 Slow Motion Power-Up

The game includes a slow-motion power-up.

When collected:

Fruits move slower
Gameplay becomes easier
The effect works for a limited time
🧠 Core Technologies Explained
🐍 Python

Python is the main programming language used to build the game logic.

It handles:

Game logic
Score calculation
Object movement
Collision detection
Game states
📷 OpenCV

OpenCV is used for computer vision and webcam processing.

It helps to:

Access the webcam
Capture video frames
Process camera input
Convert and display video data
✋ MediaPipe

MediaPipe is used for real-time hand tracking.

It helps to:

Detect the hand
Identify hand landmarks
Track finger positions
Detect the index finger

The index finger position is used to control the virtual knife.

🎮 Pygame

Pygame is used to create the game interface.

It handles:

Game window
Images
Sounds
Animations
Game objects
Score display
Keyboard controls
🔄 Application Workflow
Start Game
    ↓
Open Webcam
    ↓
Detect Hand
    ↓
Track Index Finger
    ↓
Move Virtual Knife
    ↓
Detect Collision
    ↓
Fruit Hit?
    ↓
Yes → Increase Score
    ↓
Bomb Hit?
    ↓
Yes → Reduce Life
    ↓
Check Game Over
    ↓
Restart or Exit
🎯 Concepts Demonstrated

This project demonstrates:

Computer Vision
Hand Tracking
Real-Time Video Processing
Collision Detection
Game Development
Augmented Reality Concepts
Python Programming
Webcam Integration
Interactive User Interface
🚀 Future Improvements
🎵 Background music
🎯 Multiple difficulty levels
👥 Multiplayer mode
🏆 Online leaderboard
📊 Advanced scoring system
🖐️ More hand gestures
🍉 More fruits
⚡ More power-ups
📱 Mobile version
👨‍💻 Author

Rajasekhar

Computer Science and Engineering Student
Aspiring Software Developer

🔗 GitHub: https://github.com/Rajasekhar-WebDev

⭐ Support

If you like this project, please consider giving it a ⭐ on GitHub!
