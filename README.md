# 🎮 AmazonQ-Games: A Suite of Offline Mini-Games

Q-Games is a beautifully designed collection of offline mini-games built in Python. Developed using the powerful Amazon Q developer assistant, this project showcases a sleek, animated user interface and a modular design—perfect for casual play and Python GUI learning alike.

![image](https://github.com/user-attachments/assets/d70aa91d-5417-4580-b2c8-195c881a4993)

---

## 🧩 Features

- **Intuitive Menu** – Clean, responsive GUI built with Tkinter.
- **Graphics Support** – Uses Pillow (PIL) for rendering icons and images.
- **Expandable Architecture** – Easily add new games to the suite.
- **Offline Play** – Enjoy games anywhere, any time.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

```bash
git clone https://github.com/VinayVamsiKanakala/AmazonQ-GameChallenge.git
cd AmazonQ-GameChallenge
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Game Suite

```bash
python games_suite.py
```

---

## 📁 Project Structure

```
AmazonQ-GameChallenge/
├── assets/             # Icons, images, and other media
├── games_suite.py      # Main launcher and GUI
├── games/              # Folder for individual game modules
   ├── snake.py
   ├── chess.py
   ├── puzzle.py
   ├── memory_match.py
   ├── carrom.py
├── games_suite.py              
├── requirements.txt    # Python dependencies
└── README.md           # You're reading it!
```
> **Note:** The `venv/` folder is for development and should be added to `.gitignore` before committing.

---

## ⚙️ Powered by Amazon Q

This project was developed using Amazon Q, an AI-powered development assistant that accelerates coding, debugging, and UI design. Amazon Q provided smart suggestions and context-aware code completions, making development smoother and more efficient.

---

## 🧠 Contributing

Contributions are welcome! Have a game idea or want to add a feature?

1. Fork this repo
2. Create your feature branch:  
   `git checkout -b feature/cool-game`
3. Commit your changes:  
   `git commit -am 'Add cool game'`
4. Push to the branch:  
   `git push origin feature/cool-game`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---
