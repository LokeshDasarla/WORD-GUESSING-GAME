WORD-GUESSING-GAME
A Python-based word guessing game with GUI, sound effects, and adaptive hints using machine learning.

 Features

- 🎨 **Tkinter GUI** with colorful interface
- 🔉 **Sound effects** for game events
- 🤖 **Adaptive hints** using TF-IDF and cosine similarity
- 📊 **Score tracking** system
- 🎮 **Virtual keyboard** interface
- 📚 **JSON word database** with categories and multiple hints
- 🔄 **Word history** to avoid repeats

 Requirements
- Python 3.6+

pip install numpy scikit-learn pygame
How to Run
1. Install dependencies:
 ```bash  pip install -r requirements.txt
3.Run the game:
python word_guessing_game.py

File Structure:
word-guessing-game/
├── word_guessing_game.py   # Main game code
├── word_data.json          # Word database
├── sounds/                 # Sound effects directory
│   ├── correct.wav
│   ├── wrong.wav
│   ├── win.wav
│   ├── lose.wav
│   ├── hint.wav
│   └── start.wav
└── README.md
Sample Outputs
1. Game Start Screen
+----------------------------------------+
|         WORD GUESSING GAME             |
+----------------------------------------+
| Category: Fruit                        |
| Word: _ _ _ _ _                        |
| Attempts left: 6                       |
+----------------------------------------+

2. Correct Guess:
+----------------------------------------+
|         WORD GUESSING GAME             |
+----------------------------------------+
| Word: A _ _ _ _                        |
| Guessed: A                             |
| Correct! Attempts left: 6              |
+----------------------------------------+

3. Wrong Guess
+----------------------------------------+
|         WORD GUESSING GAME             |
+----------------------------------------+
| Word: A _ _ _ _                        |
| Guessed: A, Z                          |
| Wrong! Attempts left: 5                |
+----------------------------------------+

4. Hint Display
+----------------------------------------+
| Hint: Think of iPhones and MacBooks    |
+----------------------------------------+

5. Game Won
+----------------------------------------+
| Congratulations!                       |
| You guessed: APPLE                     |
| Score: +60                             |
+----------------------------------------+

6. Game Over
+----------------------------------------+
| Game Over                              |
| The word was: BANANA                   |
| Better luck next time!                 |
+----------------------------------------+

Customization
Add more words: Edit word_data.json with additional words in the same format

{
  "word": "your_word",
  "category": "category_name",
  "hints": ["hint1", "hint2", "hint3"],
  "difficulty": 1
}
