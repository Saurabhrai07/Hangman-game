import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def is_word_guessed(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True

def guess_letter():
    global attempts
    guess = entry.get().lower()

    if len(guess) != 1 or not guess.isalpha():
        messagebox.showwarning("Invalid Input", "Please enter a single letter.")
        return

    if guess in guessed_letters:
        messagebox.showinfo("Already Guessed", "You've already guessed that letter.")
        return

    guessed_letters.append(guess)

    if guess in word:
        word_display.set(display_word(word, guessed_letters))
        if is_word_guessed(word, guessed_letters):
            messagebox.showinfo("Congratulations!", f"You guessed the word: {word}")
            root.quit()
    else:
        attempts += 1
        remaining_attempts.set(f"{max_attempts - attempts} attempts remaining")
        if attempts == max_attempts:
            messagebox.showinfo("Game Over", f"Sorry, you ran out of attempts. The word was: {word}")
            root.quit()

    entry.delete(0, tk.END)

def start_game():
    global word, max_attempts, guessed_letters, attempts
    guessed_letters = []
    attempts = 0
    word = random.choice(words).lower()
    word_display.set(display_word(word, guessed_letters))
    remaining_attempts.set(f"{max_attempts} attempts remaining")

# Initialize game variables
words = ['Bicycle', 'Elephant', 'Sunshine', 'Rainbow', 'Computer',
         'Balloon', 'Mountain', 'Delicious', 'Adventure', 'Friendly', 'Flower', 'Ocean',
         'Charming', 'Laptop', 'Cupcake', 'Guitar', 'Wonderful', 'Pineapple', 'Serene', 'Journey']
word = ""
max_attempts = 8
guessed_letters = []
attempts = 0

# Create tkinter window
root = tk.Tk()
root.title("Hangman Game")

# Load background image using Pillow
image = Image.open("background.jpg")  # Ensure the file path is correct
background_image = ImageTk.PhotoImage(image)
bg_label = tk.Label(root, image=background_image)
bg_label.place(relwidth=1, relheight=1)

# Create tkinter variables
word_display = tk.StringVar()
remaining_attempts = tk.StringVar()

# Add title text
title_label = tk.Label(root, text="HANGMAN GAME", font=("Helvetica", 36), bg="lightblue")
title_label.pack(pady=20)

# Layout
game_frame = tk.Frame(root, bg="lightblue")
game_frame.pack(pady=20)

word_label = tk.Label(game_frame, textvariable=word_display, font=("Helvetica", 24), bg="lightblue")
word_label.pack(pady=10)

attempts_label = tk.Label(game_frame, textvariable=remaining_attempts, bg="lightblue")
attempts_label.pack(pady=10)

entry = tk.Entry(game_frame)
entry.pack(pady=10)

guess_button = tk.Button(game_frame, text="Guess", command=guess_letter)
guess_button.pack(pady=10)

# Start the game
start_game()

# Run the tkinter loop
root.geometry("600x400")  # Set window size
root.mainloop()
