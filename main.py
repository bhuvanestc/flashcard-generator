from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
words_to_learned = {}

try:
    data = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learned = original_data.to_dict(orient="records")
else:
    words_to_learned = data.to_dict(orient="records")


def next_word():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(words_to_learned)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_word["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_word["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    words_to_learned.remove(current_word)
    print(len(words_to_learned))
    datas = pandas.DataFrame(words_to_learned)
    datas.to_csv("data/words_to_learn.csv", index=False)
    next_word()


window = Tk()
window.title("Flash Card Generator")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 265, image=card_front_img)
canvas.create_image(400, 265, image=card_front_img)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 265, text="", font=("Ariel", 40, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_word)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=next_word)
right_button.grid(row=1, column=1)

next_word()

window.mainloop()
