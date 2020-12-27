from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card['French'], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    # curr_french_word = canvas.itemcget(card_word, 'text')
    # # curr_english_word = next((item for item in data_dict if item["French"] == curr_french_word))
    # print([d["English"] for d in data_dict if d["French"]==curr_french_word])
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white")


def is_known():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card App")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_img, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
