import json
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
import pygame
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

class WordGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title(" Word Guessing Game")
        self.root.geometry("800x600")
        
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Load word data
        with open('word_data.json', 'r') as f:
            self.data = json.load(f)
        
        # Prepare ML components
        self.prepare_ml_model()
        
        # Game variables
        self.current_word = None
        self.guessed_letters = []
        self.remaining_attempts = 6
        self.score = 0
        self.hint_level = 0
        self.word_history = []
        
        # GUI elements
        self.create_widgets()
        
        # Start a new game
        self.new_game()
    
    def prepare_ml_model(self):
        """Prepare ML model for adaptive hints"""
        # Create a corpus of all hints
        self.all_hints = []
        self.word_to_hints = defaultdict(list)
        
        for item in self.data['words']:
            for hint in item['hints']:
                self.all_hints.append(hint)
                self.word_to_hints[item['word']].append(hint)
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        self.hint_vectors = self.vectorizer.fit_transform(self.all_hints)
    
    def get_adaptive_hint(self, word):
        """Get an adaptive hint based on previous guesses"""
        if not self.guessed_letters:
            return random.choice(self.word_to_hints[word])
        
        # Get all hints for this word
        word_hints = self.word_to_hints[word]
        if not word_hints:
            return "No hints available"
        
        # Vectorize the guessed letters
        guessed_text = ' '.join(self.guessed_letters)
        guessed_vector = self.vectorizer.transform([guessed_text])
        
        # Calculate similarity between guessed letters and hints
        similarities = cosine_similarity(guessed_vector, self.vectorizer.transform(word_hints))
        hint_index = np.argmin(similarities)  # Get least similar hint
        
        return word_hints[hint_index]
    
    def create_widgets(self):
        """Create GUI elements"""
        # Background
        self.bg_color = "#f0f8ff"
        self.root.config(bg=self.bg_color)
        
        # Header
        self.header = tk.Label(
            self.root, 
            text=" Word Guessing Game", 
            font=("Arial", 24, "bold"), 
            bg=self.bg_color,
            fg="#2c3e50"
        )
        self.header.pack(pady=20)
        
        # Word display
        self.word_display = tk.Label(
            self.root, 
            text="", 
            font=("Courier", 36), 
            bg=self.bg_color,
            fg="#2c3e50"
        )
        self.word_display.pack(pady=20)
        
        # Hint display
        self.hint_label = tk.Label(
            self.root, 
            text="Hint: ", 
            font=("Arial", 14), 
            bg=self.bg_color,
            fg="#34495e"
        )
        self.hint_label.pack()
        
        # Category display
        self.category_label = tk.Label(
            self.root, 
            text="Category: ", 
            font=("Arial", 12), 
            bg=self.bg_color,
            fg="#7f8c8d"
        )
        self.category_label.pack()
        
        # Attempts display
        self.attempts_label = tk.Label(
            self.root, 
            text="Attempts left: 6", 
            font=("Arial", 12), 
            bg=self.bg_color,
            fg="#e74c3c"
        )
        self.attempts_label.pack()
        
        # Score display
        self.score_label = tk.Label(
            self.root, 
            text=f"Score: {self.score}", 
            font=("Arial", 12), 
            bg=self.bg_color,
            fg="#27ae60"
        )
        self.score_label.pack()
        
        # Keyboard frame
        self.keyboard_frame = tk.Frame(self.root, bg=self.bg_color)
        self.keyboard_frame.pack(pady=20)
        
        # Create keyboard buttons
        self.create_keyboard()
        
        # Control buttons
        self.control_frame = tk.Frame(self.root, bg=self.bg_color)
        self.control_frame.pack(pady=10)
        
        self.new_game_btn = tk.Button(
            self.control_frame, 
            text="New Game", 
            command=self.new_game,
            font=("Arial", 12),
            bg="#3498db",
            fg="white"
        )
        self.new_game_btn.grid(row=0, column=0, padx=10)
        
        self.hint_btn = tk.Button(
            self.control_frame, 
            text="Get Hint", 
            command=self.give_hint,
            font=("Arial", 12),
            bg="#f39c12",
            fg="white"
        )
        self.hint_btn.grid(row=0, column=1, padx=10)
        
        self.solve_btn = tk.Button(
            self.control_frame, 
            text="Solve", 
            command=self.solve_word,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white"
        )
        self.solve_btn.grid(row=0, column=2, padx=10)
    
    def create_keyboard(self):
        """Create keyboard buttons"""
        # First row (Q-P)
        first_row = "QWERTYUIOP"
        for i, letter in enumerate(first_row):
            btn = tk.Button(
                self.keyboard_frame,
                text=letter,
                width=3,
                height=2,
                font=("Arial", 12, "bold"),
                command=lambda l=letter: self.guess_letter(l),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            btn.grid(row=0, column=i, padx=2, pady=2)
        
        # Second row (A-L)
        second_row = "ASDFGHJKL"
        for i, letter in enumerate(second_row):
            btn = tk.Button(
                self.keyboard_frame,
                text=letter,
                width=3,
                height=2,
                font=("Arial", 12, "bold"),
                command=lambda l=letter: self.guess_letter(l),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            btn.grid(row=1, column=i+1, padx=2, pady=2)
        
        # Third row (Z-M)
        third_row = "ZXCVBNM"
        for i, letter in enumerate(third_row):
            btn = tk.Button(
                self.keyboard_frame,
                text=letter,
                width=3,
                height=2,
                font=("Arial", 12, "bold"),
                command=lambda l=letter: self.guess_letter(l),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            btn.grid(row=2, column=i+2, padx=2, pady=2)
    
    def new_game(self):
        """Start a new game"""
        # Select a word that hasn't been played recently
        available_words = [w for w in self.data['words'] if w['word'] not in self.word_history]
        if not available_words:
            available_words = self.data['words']  # Reset if all words have been played
            self.word_history = []
        
        self.current_word = random.choice(available_words)
        self.word_history.append(self.current_word['word'])
        self.guessed_letters = []
        self.remaining_attempts = 6
        self.hint_level = 0
        
        # Update display
        self.update_word_display()
        self.attempts_label.config(text=f"Attempts left: {self.remaining_attempts}")
        self.category_label.config(text=f"Category: {self.current_word['category'].capitalize()}")
        self.hint_label.config(text="Hint: ")
        
        # Reset keyboard buttons
        for child in self.keyboard_frame.winfo_children():
            child.config(state=tk.NORMAL, bg="#ecf0f1")
        
        # Play sound
        self.play_sound("start")
    
    def update_word_display(self):
        """Update the displayed word with guessed letters"""
        display = []
        for letter in self.current_word['word'].upper():
            if letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append("_")
        
        self.word_display.config(text=" ".join(display))
        
        # Check if word is complete
        if all(letter in self.guessed_letters for letter in self.current_word['word'].upper()):
            self.word_guessed()
    
    def guess_letter(self, letter):
        """Process a letter guess"""
        letter = letter.lower()
        
        # Ignore if already guessed
        if letter in self.guessed_letters:
            return
        
        # Add to guessed letters
        self.guessed_letters.append(letter)
        
        # Update keyboard button
        for child in self.keyboard_frame.winfo_children():
            if child.cget('text').lower() == letter:
                if letter in self.current_word['word'].lower():
                    child.config(bg="#2ecc71", state=tk.DISABLED)  # Green for correct
                    self.play_sound("correct")
                else:
                    child.config(bg="#e74c3c", state=tk.DISABLED)  # Red for incorrect
                    self.remaining_attempts -= 1
                    self.play_sound("wrong")
                break
        
        # Update displays
        self.update_word_display()
        self.attempts_label.config(text=f"Attempts left: {self.remaining_attempts}")
        
        # Check if game over
        if self.remaining_attempts <= 0:
            self.game_over()
    
    def give_hint(self):
        """Provide a hint to the player"""
        if self.hint_level < len(self.current_word['hints']):
            hint = self.get_adaptive_hint(self.current_word['word'])
            self.hint_label.config(text=f"Hint: {hint}")
            self.hint_level += 1
            self.play_sound("hint")
        else:
            messagebox.showinfo("No More Hints", "You've used all available hints for this word!")
    
    def solve_word(self):
        """Let the player solve the word"""
        answer = simpledialog.askstring("Solve", "What's the word?")
        if answer and answer.lower() == self.current_word['word'].lower():
            self.guessed_letters = list(self.current_word['word'].upper())
            self.update_word_display()
            self.play_sound("win")
        elif answer:
            messagebox.showinfo("Incorrect", f"Sorry, '{answer}' is not correct.")
            self.remaining_attempts -= 2
            if self.remaining_attempts <= 0:
                self.game_over()
            self.attempts_label.config(text=f"Attempts left: {self.remaining_attempts}")
    
    def word_guessed(self):
        """Handle when word is guessed correctly"""
        self.score += self.remaining_attempts * 10
        self.score_label.config(text=f"Score: {self.score}")
        messagebox.showinfo("Congratulations!", f"You guessed the word: {self.current_word['word']}")
        self.play_sound("win")
        self.root.after(1500, self.new_game)
    
    def game_over(self):
        """Handle game over"""
        messagebox.showinfo("Game Over", f"The word was: {self.current_word['word']}")
        self.play_sound("lose")
        self.root.after(1500, self.new_game)
    
    def play_sound(self, sound_type):
        """Play appropriate sound effect"""
        try:
            if sound_type == "correct":
                pygame.mixer.Sound("correct.wav").play()
            elif sound_type == "wrong":
                pygame.mixer.Sound("wrong.wav").play()
            elif sound_type == "win":
                pygame.mixer.Sound("win.wav").play()
            elif sound_type == "lose":
                pygame.mixer.Sound("lose.wav").play()
            elif sound_type == "hint":
                pygame.mixer.Sound("hint.wav").play()
            elif sound_type == "start":
                pygame.mixer.Sound("start.wav").play()
        except:
            pass  # Ignore if sound files don't exist

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGuessingGame(root)
    root.mainloop()
