import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
lang_font = ("Arial", 40, "italic")
word_font = ("Arial", 50, "bold")
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/sr_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(lang_label, text="Serbian", fill="black")
    canvas.itemconfig(word_label, text=current_card["Serbian"], fill="black")
    canvas.itemconfig(card, image=card_front_img)
    flip_timer = window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(lang_label, text="English", fill="white")
    canvas.itemconfig(word_label, text=current_card["English"], fill="white")
    canvas.itemconfig(card, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()



window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashcards")

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front_img)
lang_label = canvas.create_text(400, 150, text="", font=lang_font)
word_label = canvas.create_text(400, 263, text="", font=word_font)
canvas.grid(row=0, column=0, columnspan=2)


no_icon = PhotoImage(file="images/wrong.png")
no_button = Button(image=no_icon, highlightthickness=0, command=next_card)
no_button.grid(row=1, column=0)

yes_icon = PhotoImage(file="images/right.png")
yes_button = Button(image=yes_icon, highlightthickness=0, command=is_known)
yes_button.grid(row=1, column=1)

next_card()


window.mainloop()