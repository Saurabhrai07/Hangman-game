import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import matplotlib.pyplot as plt

def display_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)

def is_word_guessed(word, guessed_letters):
    return all(letter in guessed_letters for letter in word)

def guess_letter():
    global attempts, correct_guesses
    guess = entry.get().lower()

    if len(guess) != 1 or not guess.isalpha():
        messagebox.showwarning("Invalid Input", "Please enter a single letter.")
        return

    if guess in guessed_letters:
        messagebox.showinfo("Already Guessed", "You've already guessed that letter.")
        return

    guessed_letters.append(guess)

    if guess in word:
        correct_guesses += 1
        word_display.set(display_word(word, guessed_letters))
        if is_word_guessed(word, guessed_letters):
            score = max_attempts - attempts
            update_high_score(score)
            accuracy = (correct_guesses / (attempts + correct_guesses)) * 100 if attempts + correct_guesses > 0 else 0
            show_result(score, accuracy)
    else:
        attempts += 1
        remaining_attempts.set(f"{max_attempts - attempts} attempts remaining")
        if attempts == max_attempts:
            accuracy = (correct_guesses / (attempts + correct_guesses)) * 100 if attempts + correct_guesses > 0 else 0
            show_result(0, accuracy)

    entry.delete(0, tk.END)

def show_result(score, accuracy):
    messagebox.showinfo("Game Over", f"Your score: {score}\nYour accuracy: {accuracy:.2f}%")
    plot_accuracy(accuracy, attempts)
    reset_game()

def start_game():
    global word, max_attempts, guessed_letters, attempts, correct_guesses
    guessed_letters = []
    attempts = 0
    correct_guesses = 0
    word = random.choice(words).lower()
    word_display.set(display_word(word, guessed_letters))
    remaining_attempts.set(f"{max_attempts} attempts remaining")

def reset_game():
    start_game()
    load_high_score()

def get_hint():
    global word, hints_used
    if hints_used < max_hints:
        hint_letter = random.choice([letter for letter in word if letter not in guessed_letters])
        guessed_letters.append(hint_letter)
        hints_used += 1
        word_display.set(display_word(word, guessed_letters))
        messagebox.showinfo("Hint", f"Here's a hint! One of the letters is: {hint_letter}")
    else:
        messagebox.showinfo("No Hints Left", "You've used all your hints.")

def update_high_score(score):
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    else:
        high_scores = {}

    theme_name = current_theme
    if theme_name not in high_scores or score > high_scores[theme_name]:
        high_scores[theme_name] = score
        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f)

    load_high_score()

def load_high_score():
    if os.path.exists("high_scores.json"):
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
            high_score_display.set(f"High Score: {high_scores.get(current_theme, 0)}")

def change_theme():
    global current_theme, words, hints_used
    current_theme = theme_var.get()
    words = themes[current_theme]
    hints_used = 0
    reset_game()

def plot_accuracy(accuracy, attempts):
    plt.figure(figsize=(6, 4))
    plt.scatter([accuracy], [attempts], color='blue')
    plt.xlim(0, 100)
    plt.ylim(0, max_attempts)
    plt.xlabel('Accuracy (%)')
    plt.ylabel('Number of Attempts')
    plt.title('Game Performance: Accuracy vs Attempts')
    plt.axvline(x=accuracy, color='red', linestyle='--', label=f'Accuracy: {accuracy:.2f}%')
    plt.legend()
    plt.show()

# Word lists by theme
themes = {
    "Animals": ['Rat', 'Cat', 'Elephant', 'Tiger', 'Giraffe', 'Dolphin'],
    "Technology": ['Computer', 'Smartphone', 'Tablet', 'Robot', 'Internet'],
    "Movies": ['Inception', 'Avatar', 'Titanic', 'Gladiator', 'Matrix'],
    "Food": ['Pizza', 'Sushi', 'Burger', 'Pasta', 'Taco', 'Chocolate', 'Ice Cream', 'Salad', 'Donut', 'Steak', 'Pancake'],
    "Countries": ['France', 'Brazil', 'India', 'Japan', 'Canada', 'Italy', 'Germany', 'Australia', 'Mexico', 'China', 'Russia', 'South Africa'],
    "Sports": ['Football', 'Basketball', 'Tennis', 'Cricket', 'Hockey', 'Baseball', 'Golf', 'Rugby', 'Swimming', 'Boxing', 'Volleyball']
}

# Set defaults
current_theme = "Animals"
words = themes[current_theme]
max_attempts = 8
max_hints = 3
hints_used = 0

# Create tkinter window
root = tk.Tk()
root.title("WordSphere: Analytics Meets Adventure")

# Load background image using Pillow
image = Image.open("background.jpg")  # Ensure the file path is correct
background_image = ImageTk.PhotoImage(image)
bg_label = tk.Label(root, image=background_image)
bg_label.place(relwidth=1, relheight=1)

# Create tkinter variables
word_display = tk.StringVar()
remaining_attempts = tk.StringVar()
high_score_display = tk.StringVar()

# Add title text
title_label = tk.Label(root, text="WORDSPHERE", font=("Helvetica", 36), bg="lightblue")
title_label.pack(pady=20)

# Theme selection dropdown
theme_label = tk.Label(root, text="Select Theme:", bg="lightblue")
theme_label.pack(pady=5)

theme_var = tk.StringVar(value=current_theme)
theme_menu = tk.OptionMenu(root, theme_var, *themes.keys(), command=lambda _: change_theme())
theme_menu.pack(pady=5)

# Layout
game_frame = tk.Frame(root, bg="lightblue")
game_frame.pack(pady=20)

word_label = tk.Label(game_frame, textvariable=word_display, font=("Helvetica", 24), bg="lightblue")
word_label.pack(pady=10)

attempts_label = tk.Label(game_frame, textvariable=remaining_attempts, bg="lightblue")
attempts_label.pack(pady=10)

high_score_label = tk.Label(game_frame, textvariable=high_score_display, bg="lightblue")
high_score_label.pack(pady=10)

entry = tk.Entry(game_frame)
entry.pack(pady=10)

guess_button = tk.Button(game_frame, text="Guess", command=guess_letter)
guess_button.pack(pady=10)

hint_button = tk.Button(game_frame, text="Get Hint", command=get_hint)
hint_button.pack(pady=10)

reset_button = tk.Button(game_frame, text="Reset Game", command=reset_game)
reset_button.pack(pady=10)

# Start the game
start_game()

# Load high score
load_high_score()

# Run the tkinter loop
root.geometry("600x500")  # Set window size
root.mainloop()
