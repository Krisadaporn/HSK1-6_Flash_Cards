from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
MEANING_FONT = ("Ariel", 40, "bold")
START_FONT = ("Ariel", 50, "bold")
current_card = {}
original_path = ''
to_learn_path = ''
to_learn = {}
user_level = ''
flip_timer = None


# -----User input-----#
def user_input():
    global top, entry, user_level
    top = Toplevel(window)
    top.geometry("300x200")
    top.config(pady=50, padx=25)
    label = Label(top, text="Which level do you want to learn today? please input HSK level as number from 1 to 6",
                  foreground="white", wraplength=200,
                  justify="center")
    label.grid(column=1, row=0)
    entry = Entry(top, width=25)
    entry.grid(column=1, row=1)

    button = Button(top, text="Confirm", command=get_level)
    button.grid(column=1, row=2)


# -----Get level-------#

def get_level():
    global original_path, to_learn_path, to_learn, user_level, top, entry
    user_level = entry.get()
    top.destroy()

    print(user_level)
    original_path = f"data/HSK{user_level}/HSK{user_level}.csv"
    to_learn_path = f"data/HSK{user_level}/HSK{user_level}_to_learn.csv"

    try:
        try:
            chinese_word_to_learn = pandas.read_csv(to_learn_path)
        except FileNotFoundError:
            original_data = pandas.read_csv(original_path)
            to_learn = original_data.to_dict(orient="records")
        else:
            to_learn = chinese_word_to_learn.to_dict(orient="records")
    except FileNotFoundError:
        messagebox.showerror(title="Opps", message="Please input hsk level from 1 to 6")
        user_input()


# -----word to learn Function-----#

def remove_from_list():
    global to_learn, current_card
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv(to_learn_path, index=False)
    new_card()


# -----New card -------#
def new_card():
    global current_card, flip_timer, to_learn
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Chinese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Chinese"], fill="black", font=WORD_FONT)
    canvas.itemconfig(card_pinyin, text=current_card["Pinyin"], fill="black")
    canvas.itemconfig(card_image, image=front_card)
    flip_timer = window.after(3000, func=meaning)


# ---- Delay to the meaning ----#
def meaning():
    global current_card, flip_timer
    canvas.itemconfig(card_image, image=back_card)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white", font=MEANING_FONT)
    canvas.itemconfig(card_pinyin, text="", fill="black")
    flip_timer = window.after(3000, func=new_card)


# -----Get Start-------#
def get_start():
    global flip_timer
    flip_timer = window.after(5, func=new_card)
    wrong_button.config(command=new_card)
    right_button.config(command=remove_from_list)


# -----Close program after 30 seconds of no input------#
def end_code():
    messagebox.showerror(title="Opps", message="The program will close now as there is no input from user")
    window.destroy()


# ----- User interface-----#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

top = Toplevel(window)
top.geometry("300x200")
top.config(pady=50, padx=25)
label = Label(top, text="Which level do you want to learn today? please input HSK level as number from 1 to 6",
              foreground="white", wraplength=200, justify="center")
label.grid(column=1, row=0)
entry = Entry(top, width=25)
entry.grid(column=1, row=1)

button = Button(top, text="Confirm", command=get_level)
button.grid(column=1, row=2)

# Front Card
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)

front_card = PhotoImage(file="./images/card_front.png")
back_card = PhotoImage(file="./images/card_back.png")

card_image = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, text="Flashy is now start", font=TITLE_FONT, fill="black")
card_word = canvas.create_text(400, 263, text="Please input your HSK level", font=START_FONT, fill="black", width=700)
card_pinyin = canvas.create_text(400, 350, text="and click any button to begin", font=TITLE_FONT, fill="black",
                                 width=700)
canvas.grid(column=0, row=0, columnspan=2)

# Button
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, command=get_start, borderwidth=0, highlightbackground=BACKGROUND_COLOR)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, command=get_start, borderwidth=0, highlightbackground=BACKGROUND_COLOR)
right_button.grid(column=1, row=1)

window.mainloop()
