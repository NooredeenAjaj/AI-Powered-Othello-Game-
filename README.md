# 🏆 Othello AI - Minimax with Alpha-Beta Pruning

Othello AI is an advanced AI player for Othello that uses the **Minimax algorithm with Alpha-Beta Pruning** to select the best possible moves. The project includes board management and a heuristic function to evaluate board positions.

## 📌 Features
- 📜 **Minimax algorithm** with **Alpha-Beta Pruning** for optimized decision-making.
- 🔍 **Heuristic evaluation** for better strategic planning.
- 🎮 **Board management** including valid moves and score calculation.
- 🏁 **Capability to simulate AI vs AI matches**.

## 🛠 Installation
### 1️⃣ **Clone the repository**
```bash
git clone https://github.com/your-username/Othello-AI.git
cd Othello-AI
```

### 2️⃣ **Create and activate a virtual environment (optional but recommended)**
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 How to Run the Game
### 🎯 **Start the AI player**
```bash
python main.py
```

## 📌 File Structure
```
Othello-AI/
│── board/
│   │── board.py        # Handles board logic and rules
│   │── pos.py          # Position handling
│   │── direction.py    # Defines movement directions
│── ai/
│   │── ai_adv.py       # AI player with Minimax and heuristics
│── main.py             # Runs the game
│── README.md           # Project description
│── requirements.txt    # List of dependencies
```

## 🧠 Algorithm Implementation
Following the lecture notes and the book, we implemented the **Minimax algorithm**. The algorithm is located in the `AIAdv` class and begins in the function called `adversarial_search`.

We also integrated **Alpha-Beta Pruning** to reduce computation time. The most challenging part was implementing an effective **heuristic function** and **evaluation function**. To achieve this, we studied the game and determined the best strategies for winning.

Our heuristic and evaluation functions are effective because they do not simply calculate the score; they also encourage moves that place pieces in corners, edges, and central blocks. Additionally, a **dynamic control mechanism** is in place. The goal of dynamic control is to motivate the AI to choose moves that yield more pieces when many empty spaces remain on the board (early-game state). However, as the game progresses and fewer empty spaces remain, the heuristic function is weighted more heavily.

During testing, we observed that as the game advanced, it became more challenging for the human player to win. In some cases, the human player had no valid moves, while the AI had at least 10 more pieces than the human player.

## 👨‍💻 Authors
- **Your Name** - [GitHub Profile](https://github.com/your-username)

## 📜 License
This project is licensed under the **MIT License**.

---
