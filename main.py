import tkinter as tk
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- Data structure ------------------------------- #
try:
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df = pd.read_csv("data/french_words.csv")

# ---------------------------- Functions ------------------------------- #
def get_word():
    global random_word, flip_timer
    my_ui.after_cancel(flip_timer) #Every time I hit a button, it cancels the time and starts counting over again
    random_word = df.sample()
    my_ui.canvas.itemconfig(my_ui.canvas_image, image=my_ui.image_front)
    my_ui.canvas.itemconfig(my_ui.decline_text, text="French")
    my_ui.canvas.itemconfig(my_ui.accept_text, text=random_word["French"].values[0])
    flip_timer = my_ui.after(3000, lambda: flip_card())

def flip_card():
    my_ui.canvas.itemconfig(my_ui.decline_text, text="English")
    my_ui.canvas.itemconfig(my_ui.accept_text, text=random_word["English"].values[0])
    my_ui.canvas.itemconfig(my_ui.canvas_image, image=my_ui.image_back)

def accept():
    global df
    get_word()
    df = df.drop(random_word.index)
    df.to_csv("data/words_to_learn.csv", index=False, mode="w")

# ---------------------------- UI SETUP ------------------------------- #
class MyUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window
        self.title("Flash Cards")
        self.geometry("900x800")
        self.configure(bg=BACKGROUND_COLOR)

        #Images
        self.image_front = tk.PhotoImage(file="images/card_front.png")
        self.image_back = tk.PhotoImage(file="images/card_back.png")
        self.button_img_1 = tk.PhotoImage(file="images/wrong.png")
        self.button_img_2 = tk.PhotoImage(file="images/right.png")

        # Canvas
        self.canvas = tk.Canvas(self, width=800, height=526,bg=BACKGROUND_COLOR)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=50)
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.image_front)
        self.canvas.config(highlightthickness=0)

        # Canvas text
        self.decline_text = self.canvas.create_text((400, 150), text ="", font=("Ariel", 40, "italic"), fill="black")
        self.accept_text = self.canvas.create_text((400, 263), text="", font=("Ariel", 60, "bold"), fill="black")

        # Buttons
        self.decline_button = tk.Button(self, image=self.button_img_1)
        self.decline_button.config(highlightthickness=0, command=get_word)
        self.decline_button.grid(row=1, column=0)
        self.accept_button = tk.Button(self, image=self.button_img_2)
        self.accept_button.config(highlightthickness=0, command=accept)
        self.accept_button.grid(row=1, column=1)


my_ui = MyUI()
flip_timer = my_ui.after(3000, lambda: flip_card())
get_word()
my_ui.mainloop()