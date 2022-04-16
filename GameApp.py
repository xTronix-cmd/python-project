import random
import time
import urllib.request
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
from abc import ABC, abstractmethod

DEBUG = False
EMPTY = False


class WindowInit():  # class for initializing root and frames
    def __init__(self, width: int, height: int):
        self.number_frames = 4
        self.root = Tk()
        self.root.title("Games")
        self.root.geometry(f"{width}x{height}")
        self.root.columnconfigure(0, weight=1)
        # self.root.config(bg="black")
        self.frames = []
        self.game = ""
        self.word_list = []
        self.hangman_pic = PhotoImage(file="hangman.png")
        self.wordplay_pic = PhotoImage(file="wordplay.png")

        for row_num in range(self.number_frames):
            self.root.rowconfigure(row_num, weight=1)

        self.setup_frames()

    # Create and layout the frames
    def setup_frames(self):
        frame_colors = ['pink', 'red', 'green', 'yellow']

        # Create the frames for the window
        for frm_num in range(self.number_frames):
            self.frames.append(Frame(self.root))

        if DEBUG:
            for frm_num in range(self.number_frames):
                self.frames[frm_num].config(bg=frame_colors[frm_num], bd=2, relief=RAISED)
        # else:
        #     for frm_num in range(self.number_frames):
        #         self.frames[frm_num].config(bg="black")

        # Layout the frames in the window
        for frm_num in range(self.number_frames):
            if frm_num == 2:
                self.frames[frm_num].grid(row=frm_num, column=0, sticky="news")
            else:
                self.frames[frm_num].grid(row=frm_num, column=0, sticky="news")

    # function to clean up unnecessary widgets
    def clean_up_widgets(self):
        for frm_num in range(self.number_frames):
            if len(self.frames[frm_num].winfo_children()) is not EMPTY:
                for widgets in self.frames[frm_num].winfo_children():
                    widgets.destroy()

        # Button(self.frames[3], text="Get", command=self.get_dimension).pack(pady=25)

    # Resize Window
    def resize_window(self, width: int, height: int):
        self.root.geometry(f"{width}x{height}")


class WordPlayInit(WindowInit):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.process = dict()
        self.most = None
        self.least = None
        self.winner_word = ""

    # Initialize word play game setting
    def wordplay_setting_init(self):
        self.buttons = []
        self.process['counts'] = []
        self.process['words'] = []
        self.wrong_choice_count = 0
        self.right_choice_count = 0
        self.top_words = []
        self.strvar_list = []
        word_list = []
        word_list_selected = []
        new_list_selected = []

        # for x in range(18):
        #     self.strvar_list.append(StringVar())

        # for index in range(0, 18, 6):
        #     temp_strvar.append(self.strvar_list[index:index + 6])

        # self.strvar_list = temp_strvar
        # temp_strvar = []
        for _row in range(3):
            temp_strvar = []
            for _column in range(6):
                temp_strvar.append(StringVar())
            self.strvar_list.append(temp_strvar)

        print(f"self.strvar_list: {self.strvar_list}")
        self.word_list = self.get_random_word(self.new_word_list)
        word_list = random.sample(self.word_list, 50)
        word_list = [word.capitalize() for word in word_list]

        while True:  # keep picking random word until word length is at least 5 letters
            word_selected = random.choice(word_list)
            if len(word_selected) >= 5:
                if word_selected not in set(word_list_selected):
                    word_list_selected.append(word_selected)
            if len(word_list_selected) == 18:  # exit loop once it has selected 18 unique words
                print(f"words: {word_list_selected}")
                # input(f"word_list_selected: {len(word_list_selected)}")
                break

        # This randomly multiply each word in the list
        for word in word_list_selected:
            random.seed(time.time_ns())
            random_num = random.randint(1, 6)
            for x in range(random_num):
                new_list_selected.append(word)
            time.sleep(0.01)

        self.word_list = new_list_selected.copy()

    # starts the game
    def start_word_play(self):
        self.clean_up_widgets()
        self.resize_window(420, 400)
        self.wordplay_setting_init()
        self.game = "wordplay"
        # self.word_list = self.get_random_word(self.word_list, self.game)



        Label(self.frames[0], text="Welcome to Word Play!", font=("Arial Bold", 25)).pack()
        Label(self.frames[0], text="Created By: Marty Grefiel", font=("Arial", 8)).pack(pady=5)
        Label(self.frames[1], text="Click [START] to play").pack()

        Button(self.frames[2], text="START", image=self.wordplay_pic, compound=TOP, height=120, command=self.process_word).pack()
        Button(self.frames[2], text="QUIT", command=self.quit_game).pack(side=LEFT, padx=25, pady=25)
        Button(self.frames[2], text="How to Play?", command=self.show_how_to).pack(side=RIGHT, padx=25, pady=25)

    # Process the list of words. Create new list of the unique words and count the occurences of each word
    def process_word(self):
        self.clean_up_widgets()
        self.resize_window(420, 400)
        temp_word_list = []

        Label(self.frames[0], text="Generating words to pick...", font=("Arial Bold", 16)).pack(pady=50)
        prg_bar = Progressbar(self.frames[1], orient=HORIZONTAL, length=200)
        prg_bar.pack()

        for prg_value in range(10):
            time.sleep(0.25)
            prg_bar['value'] += 10
            self.frames[1].update_idletasks()

        # assign each unique word and number of occurance of each word
        for word in self.word_list:
            num = self.word_list.count(word)
            if word not in self.process['words']:
                self.process['counts'].append(num)
                self.process['words'].append(word)

        print("self.process['words'] begin")
        print(type(self.process['words']))
        print(self.process['words'])
        print(len(self.process['words']))
        print("self.proess[words'] ends")

        # This block to assign the 3x6 matrix for words
        for index in range(0, len(self.process['words']), 6):
            temp_word_list.append(self.process['words'][index:index + 6])

        self.word_list = temp_word_list  # 3x6 matrix words

        for _row in range(3):
            for _column in range(6):
                self.word_list[_row][_column] = self.word_list[_row][_column].capitalize()

        self.display_words()
        self.find_min_max()
        self.find_top_words()
        self.rearrange_word_list()

    # Display the words in buttons 3x6 matrix
    def display_words(self):
        self.clean_up_widgets()
        self.resize_window(435, 520)

        print(f"new self.word_list: {self.word_list}")

        # algorithm for StrVar 3x6 matrix per frame
        for _row in range(3):
            for _column in range(6):
                self.strvar_list[_row][_column].set(f"{self.word_list[_row][_column]}")

        # algorithm for buttons 3x6 matrix per frame
        for _row in range(3):
            temp_buttons = []
            for _column in range(6):
                temp_buttons.append(Button(self.frames[_row], textvariable=self.strvar_list[_row][_column], bg="grey",
                                    width=15, command=lambda word_chosen=self.word_list[_row][_column]: self.chosen_word(word_chosen)))

            self.buttons.append(temp_buttons)

        # this is to layout the buttons created
        column_grid = 0
        for _row in range(3):
            for _column in range(6):
                if _column > 2:
                    self.buttons[_row][_column].grid(row=1, column=column_grid, pady=25, padx=15)
                else:
                    self.buttons[_row][_column].grid(row=0, column=column_grid, pady=25, padx=15)
                column_grid += 1
                if column_grid > 2:
                    column_grid = 0

        Button(self.frames[3], text="Give up?", command=self.give_up).pack(side=LEFT, padx=25, pady=25)
        Button(self.frames[3], text="How to Play?", command=self.show_how_to).pack(side=RIGHT, padx=25, pady=25)
        Button(self.frames[3], text="Hint", command=self.hint_info).pack(side=RIGHT, padx=25, pady=25)
    
    def hint_info(self):
        number_words = len(self.top_words)
        messagebox.showwarning(title="WARNING!!", message=f"There are {number_words} lucky words!")

    def show_how_to(self):
        how_to_msg = """The game will generate random lucky words.
When you click one of the lucky words, the button will turn green.
Otherwise, it will be red. The game will tell you how many lucky words generated.
Picking all of the lucky words before using up all your tries will win the game."""

        messagebox.showinfo("How To Play", how_to_msg)

    # Function to see if the user wins or not
    def chosen_word(self, word_chosen):
        print("Chosen_words()")
        print(f"word_chosen: {word_chosen}")
        print(f"winner_word: {self.winner_word}")
        if word_chosen in self.top_words:
            self.right_choice_count += 1
            for _row in range(3):
                for _column in range(6):
                    # if statement: this is to disable the button chosen
                    if word_chosen == self.word_list[_row][_column]:
                        self.buttons[_row][self.word_list[_row].index(word_chosen)].config(
                            state=DISABLED, disabledforeground="red", bg="#138542", relief=GROOVE)
            if self.right_choice_count >= 3 or self.right_choice_count == len(self.top_words):
                self.winner()
        else:
            self.wrong_choice_count += 1  # Counts the number of mistakes made
            for _row in range(3):
                for _column in range(6):
                    # if statement: this is to disable the button chosen
                    if word_chosen == self.word_list[_row][_column]:
                        self.buttons[_row][self.word_list[_row].index(word_chosen)].config(
                            state=DISABLED, disabledforeground="red", bg="#821623", relief=GROOVE)
            print("Wrong!")
            if self.wrong_choice_count >= 5:
                self.loser()

     # game_over
    def wordplay_game_over(self):
        # self.clean_up_widgets()
        Label(self.frames[0], text="The lucky words are:", font=("Arial Bold", 10)).pack(side=BOTTOM)
        for _row in range(3):
            for _column in range(6):
                if self.word_list[_row][_column] in self.top_words:
                    Button(self.frames[1], width=15, bg="#138542", relief=GROOVE, text=f"{self.word_list[_row][_column]}").pack()
        print("wordplay_game_over executed")
        Button(self.frames[2], text="YES", command=self.wordplay_play_again).grid(row=0, column=1, pady=25)
        Button(self.frames[2], text="NO", command=self.root.destroy).grid(row=0, column=2, padx=10, pady=25)
        Label(self.frames[2], text="Play Again?", font=("Arial Bold", 16)).grid(row=0, column=0, padx=(100, 10), pady=25)
        Button(self.frames[3], text="RESTART", command=self.restart_word_play).pack(side=LEFT, padx=25, pady=25)
        Button(self.frames[3], text="Game Menu", command=self.game_menu).pack(side=RIGHT, padx=25, pady=25)

    # Play again
    def wordplay_play_again(self):
        self.clean_up_widgets()
        self.wordplay_setting_init()
        self.process_word()

    # return to main menu
    def restart_word_play(self):
        self.welcome()

    # execute if user lose
    def loser(self):
        self.clean_up_widgets()
        self.wordplay_game_over()
        Label(self.frames[0], text="Sorry, you lose!", font=("Arial Bold", 16)).pack()
        Label(self.frames[0], text="Better luck next time.", font=("Arial Bold", 10)).pack(side=BOTTOM)

    # execute if user wins
    def winner(self):
        self.clean_up_widgets()
        Label(self.frames[0], text="Congratulations, You win!", font=("Arial Bold", 16)).pack()
        self.wordplay_game_over()

    # Find the top words
    def find_top_words(self):
        # self.most has the highest number
        if self.process['counts'].count(self.most) > 1:
            # self.process['words'] length is 18
            print(f"self.process['words'] length is {len(self.process['words'])}")
            for x in range(len(self.process['words'])):
                # This checks if the word has the highest occurence
                if self.process['counts'][x] == self.most:
                    self.top_words.append(self.process['words'][x])

        # returns one word out of the highest word occurence
        self.winner_word = random.choice(self.top_words)
        self.winner_word = self.winner_word.capitalize()
        print(f"find_top_word(): {self.winner_word}")

    # Rearrange word list from most to least
    def rearrange_word_list(self):
        count_sorted = self.process['counts'].copy()
        count_sorted.sort(reverse=True)  # From highest to lowest counts
        print(f"count_sorted: {count_sorted}")
        sorted_words = []

        # This for loop block is to rearrange the list of words from highest to lowest occurence
        for x in count_sorted:
            new_count = self.process['counts'].count(x)
            for y in range(0, new_count):
                sorted_words.append(self.process['words'][self.process['counts'].index(x)])
                self.process['words'].remove(self.process['words'][self.process['counts'].index(x)])
                self.process['counts'].remove(x)

        self.process['words'] = sorted_words
        # self.process['counts'] = count_sorted
        # print(f"Sorted words: {self.process['words']}")
        # print(f"Sorted counts: {self.process['counts']}")
        print(f"Sorted words: {sorted_words}")
        # print(f"Sorted counts: {count_sorted}")

    # Find the max/min number of the top/least word occurance
    def find_min_max(self):
        self.most = max(self.process['counts'])
        self.least = min(self.process['counts'])

    # Print results
    def print_results(self):
        for x in range(len(self.process['words'])):
            percent = self.process['counts'][x] / len(self.word_list) * 100
            print(f"{self.process['words'][x]}, {self.process['counts'][x]}, {round(percent)}%")


class HangmanInit(WindowInit):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.response = None
        self.guess = None
        self.guess_letter_input = None
        self.lbl_tries_left = None
        self.game_setting = None
        self.ent_name = None
        self.lbl_response = None
        self.user_name = None
        self.game_setting = dict()
        # game_setting = dict()

        # Placeholder for response display
        self.lbl_response = Label(self.frames[0])
        self.lbl_response.pack()

        # self.game_setting = self.game_setting_init()

    # Initialize game settings
    def game_setting_init(self):
        game_setting = dict()
        word_list = []
        word_selected = ""

        game_setting['guessed_letters'] = []
        game_setting['total_incorrect_guesses'] = 0
        game_setting['StrVar_hidden_word'] = StringVar()
        game_setting['StrVar_tries_left'] = StringVar()
        game_setting['num_letter_word'] = StringVar()

        word_list = self.get_random_word(self.new_word_list)
        while True:  # keep picking random word until word length is at least 5 letters
            word_selected = random.choice(word_list)
            if len(word_selected) >= 5:
                break
        # return word_selected
        # game_setting['word_selected'] = self.get_random_word(self.new_word_list)
        game_setting['word_selected'] = word_selected.upper()
        # below assigns the total unique letters in the word + 3; the total number of guesses allowed
        game_setting['num_allowed_guesses'] = len(set(game_setting['word_selected'])) + 3
        game_setting['hidden_word'] = list("_" * len(game_setting['word_selected']))
        game_setting['remaining_letters'] = len(game_setting['word_selected'])

        game_setting['status'] = "started"

        return game_setting

    # Displays the "selecting random word" window
    def select_random_word(self):
        self.resize_window(420, 350)
        self.clean_up_widgets()

        Label(self.frames[0], text="Selecting a random word...", font=("Arial Bold", 16)).pack(pady=50)
        prg_bar = Progressbar(self.frames[1], orient=HORIZONTAL, length=200)
        prg_bar.pack()

        for prg_value in range(10):
            time.sleep(0.25)
            prg_bar['value'] += 10
            self.frames[1].update_idletasks()

        self.guess_word()

    # Welcomes and ask user for his/her name
    def start_hangman(self):
        self.resize_window(420, 400)

        self.game = "hangman"
        self.clean_up_widgets()
        self.game_setting = self.game_setting_init()
        # Executes after the first game
        if self.game_setting['status'] != "started":
            self.game_setting = self.game_setting_init()
            self.setup_frames()

        Label(self.frames[0], text="Welcome to Hangman!",
              font=("Arial Bold", 25)).pack()
        Label(self.frames[0], text="Created By: Marty Grefiel",
              font=("Arial", 8)).pack(pady=5)
        Label(self.frames[1], text="Click [START] to play").pack()
        # Label(self.frames[1], text="Click [START] to play").pack(pady=25)

        # Button(self.frames[2], text="START", image=self.hangman_pic, compound=TOP, command=self.select_random_word).pack(padx=75, pady=25)
        # Button(self.frames[2], text="QUIT", command=self.quit_game).pack(padx=75, pady=25)
        Button(self.frames[2], text="START", image=self.hangman_pic,
               compound=TOP, height=120, command=self.select_random_word).pack()
        Button(self.frames[2], text="QUIT", command=self.quit_game).pack(pady=25)

    # Window to input user's guess for the hidden word
    def guess_word(self):
        self.resize_window(420, 400)
        self.clean_up_widgets()  # Cleans up existing widgets

        # Display the hidden word to guess
        self.game_setting['StrVar_hidden_word'].set(" ".join(self.game_setting['hidden_word']))
        Label(self.frames[1], textvariable=self.game_setting['StrVar_hidden_word'],
              font=("Arial Bold", 25)).pack(padx=25)

        if DEBUG:
            # this is used only for debugging
            print(self.game_setting['word_selected'])

        # Display the number of tries left
        self.game_setting['StrVar_tries_left'].set(f"Tries Left: {self.game_setting['num_allowed_guesses']}")
        self.lbl_tries_left = Label(self.frames[3], textvariable=self.game_setting['StrVar_tries_left'])
        self.lbl_tries_left.pack(side=RIGHT, pady=25, fill=X, expand=True)

        # Display and prompt user to guess a letter
        Label(self.frames[2], text="Enter letter to guess: ", font=25).grid(row=0, column=0, padx=(100, 0))
        self.guess_letter_input = Entry(self.frames[2], fg="#5FFF5C", bg="Black", width=2, font=25)
        self.guess_letter_input.grid(row=0, column=1)
        self.guess_letter_input.focus()
        self.guess_letter_input.bind("<Return>", self.check_user_guess)

        # Display [give up] button
        Button(self.frames[3], text="Give up?", command=self.give_up).pack(side=LEFT, padx=25, pady=25)

    # Checks the user's input
    # Attribute self.response is used for guess_response() method to display response based on its value
    def check_user_guess(self, event):
        # used for counting how many in the hidden word your correct guessed letter
        num_letter_word = 0
        self.guess = self.guess_letter_input.get().upper()
        self.guess_letter_input.delete(0, END)

        if not self.guess.isalpha() or len(self.guess) > 1:  # invalid guess input character
            if DEBUG:
                print("INVALID")
            self.response = "invalid"
        # if letter been already guessed
        elif self.guess in self.game_setting['guessed_letters']:
            if DEBUG:
                print("USED")
            self.response = "used"
        # if guessed letter in the hidden word
        elif self.guess in self.game_setting['word_selected']:
            self.response = "correct"
            # assign guess letter to letters to guess
            for i in range(len(self.game_setting['word_selected'])):
                if self.guess == self.game_setting['word_selected'][i]:
                    # I used this approach to print the incomplete word
                    self.game_setting['hidden_word'][i] = self.guess
                    self.game_setting['StrVar_hidden_word'].set(" ".join(self.game_setting['hidden_word']))
                    self.game_setting['remaining_letters'] -= 1
                    num_letter_word += 1

                    # game_over, user won!
                    if self.game_setting['remaining_letters'] == 0:
                        self.game_setting['status'] = "won"
                        self.game_over()
            if DEBUG:
                print("CORRECT")
        else:  # executes if the letter guessed is not in the word
            if DEBUG:
                print("INCORRECT")
            self.game_setting['num_allowed_guesses'] -= 1
            self.game_setting['total_incorrect_guesses'] += 1
            # This is to warn user of the number of tries left
            if self.game_setting['num_allowed_guesses'] == 3:
                self.lbl_tries_left.configure(fg="red")
                message = f"You have {self.game_setting['num_allowed_guesses']} tries left\nBe more careful!"
                messagebox.showwarning(title="WARNING!!", message=message)
            self.game_setting['StrVar_tries_left'].set(f"Tries Left: {self.game_setting['num_allowed_guesses']}")

            # executes when the user lost
            if self.game_setting['num_allowed_guesses'] == 0:
                self.game_setting['status'] = "lost"
                self.game_over()
                if DEBUG:
                    print("LOST")
            self.response = "incorrect"

        # appends the guessed letter to the list if it's not already in it.
        if self.guess not in self.game_setting['guessed_letters']:
            if self.guess.isalpha() and len(self.guess) == 1:
                self.game_setting['guessed_letters'].append(self.guess)

        if DEBUG:
            print(self.game_setting['guessed_letters'])

        # Calls the guess_response() method if game is not over yet
        if self.game_setting['num_allowed_guesses'] > 0 and self.game_setting['remaining_letters'] > 0:
            self.guess_response(num_letter_word)

    # Displays response based on the user's guess
    def guess_response(self, num_letter_word):
        self.lbl_response.destroy()

        if self.response == "invalid":
            self.lbl_response = Label(self.frames[0], text="Invalid input, try again...", font=("Arial Bold", 10))
        elif self.response == "used":
            self.lbl_response = Label(
                self.frames[0], text=f"You already guessed: {self.guess}. Try again...", font=("Arial Bold", 10))
        elif self.response == "incorrect":
            self.lbl_response = Label(self.frames[0], text="Incorrect.", font=("Arial Bold", 10))
        elif self.response == "correct":
            temp_var = ['time' if num_letter_word == 1 else 'times']
            temp_var = " ".join(temp_var)
            self.game_setting['num_letter_word'].set(f"Correct! {self.guess} is in the word {num_letter_word} {temp_var}")
            self.lbl_response = Label(self.frames[0], textvariable=self.game_setting['num_letter_word'], font=("Arial Bold", 10))

        self.lbl_response.pack(pady=50)

    # Game is over: displays message(s) according to the reason of why game ended
    def hangman_game_over(self):
        self.resize_window(420, 400)
        self.clean_up_widgets()
        self.lbl_response.destroy()

        Label(self.frames[0], text="The word is:", font=("Arial Bold", 10)).pack(side=BOTTOM)
        # self.game_setting['hidden_word'] = self.game_setting['word_selected']
        self.game_setting['StrVar_hidden_word'].set(" ".join(self.game_setting['word_selected']))
        # Label is added here because somehow it doesn't show on guess_word() method
        Label(self.frames[1], textvariable=self.game_setting['StrVar_hidden_word'], font=("Arial Bold", 25)).pack(padx=25)

        print(f"The word to print is: {self.game_setting['word_selected']}")


        Button(self.frames[2], text="YES", command=self.hangman_play_again).grid(row=0, column=1, pady=25)
        Button(self.frames[2], text="NO", command=self.root.destroy).grid(row=0, column=2, padx=10, pady=25)
        Label(self.frames[2], text="Play Again?", font=("Arial Bold", 16)).grid(row=0, column=0, padx=(100, 10), pady=25)
        Button(self.frames[3], text="RESTART", command=self.restart_hangman).pack(side=LEFT, padx=25, pady=25)
        Button(self.frames[3], text="Game Menu", command=self.game_menu).pack(side=RIGHT, padx=25, pady=25)

        if self.game_setting['status'] == "won":
            if self.game_setting['total_incorrect_guesses'] == 1:
                verb, noun = "was", "guess"
            else:
                verb, noun = "were", "guesses"

            total_wrong_guesses = f"There {verb} {self.game_setting['total_incorrect_guesses']} incorrect {noun} made."
            Label(self.frames[0], text=total_wrong_guesses, font=("Arial Bold", 10)).pack(side=BOTTOM)
            winner_message = f"Congratulations, {self.user_name}. You win!!"
            Label(self.frames[0], text=winner_message, font=("Arial Bold", 16)).pack(side=BOTTOM)
            if DEBUG:
                print("You won!!")
        else:
            Label(self.frames[0], text="Better luck next time.", font=("Arial Bold", 10)).pack(side=BOTTOM)
            if self.game_setting['status'] == "gave_up":
                if DEBUG:
                    print("too bad you gave up")
                Label(self.frames[0], text="Too bad you gave up..", font=("Arial Bold", 16)).pack(side=BOTTOM)
            elif self.game_setting['status'] == "lost":
                if DEBUG:
                    print("You lost!!")
                Label(self.frames[0], text="Sorry, you lose.", font=("Arial Bold", 16)).pack(side=BOTTOM)

    # restarts hangman
    def restart_hangman(self):
        self.clean_up_widgets()
        self.welcome()

    # Asks confirmation from user to give up
    # def give_up(self):
    #     if messagebox.askokcancel(message="Are you sure?"):
    #         self.game_setting['status'] = "gave_up"
    #         self.game_over()

    # Asks confirmation from user to quit
    def quit_game(self):
        if messagebox.askokcancel(message="Are you want to quit?"):
            self.root.destroy()

    # Gets called when user decided to play again
    def hangman_play_again(self):
        self.game_setting = self.game_setting_init()
        self.select_random_word()


class GameInit(HangmanInit, WordPlayInit):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        # self.hangman_pic = PhotoImage(file="hangman.png")
        # self.wordplay_pic = PhotoImage(file="wordplay.png")

        # self.word_list = []
        with urllib.request.urlopen('https://docs.python.org/3/tutorial/') as response:
            html = response.read().decode('utf-8')
        self.word_list = html.split()
        self.new_word_list = []

        # Only add the words that are only in the alphabets to the list
        for i in range(len(self.word_list)):
            if self.word_list[i].isalpha():
                self.new_word_list.append(self.word_list[i])

        # self.word_list = self.new_word_list.copy()
        # self.word_list = self.get_random_word(self.new_word_list.copy())
        # print(f"self.word_list: {len(self.word_list)}")

        self.welcome()

    # Create a new random list of words and return it to the caller
    @ staticmethod
    def get_random_word(word_list):  # Function to pick the random word
        # word_list_selected = []
        # new_list_selected = []

        random.seed(time.time_ns())
        word_list = random.sample(word_list, 100)
        return word_list

    # Dimension Info
    def get_dimension(self):
        Label(self.frames[3], text=self.root.winfo_geometry()).pack()

    # Welcomes and ask user for his/her ent_name
    def welcome(self):
        self.resize_window(420, 400)
        self.clean_up_widgets()
        self.word_list = self.get_random_word(self.new_word_list.copy())  # Get 100 unique words and assigns it to self.word_list

        Label(self.frames[0], text="Welcome!!", font=("Arial Bold", 35)).pack()
        Label(self.frames[0], text="Created By: Marty Grefiel", font=("Arial", 8)).pack(pady=5)
        # Label(self.frames[1], text="Enter your name: ", font=25).pack(side=LEFT, padx=15)

        # self.ent_name = Entry(self.frames[1], fg="#5FFF5C", bg="black", font=25, width=12)

        Label(self.frames[1], text="Enter your name: ", font=25).grid(row=0, column=0, padx=(90, 0))

        self.ent_name = Entry(self.frames[1], fg="#5FFF5C", bg="black", font=25, width=12)
        self.ent_name.grid(row=0, column=1)       # self.ent_name.pack(side=LEFT)
        self.ent_name.focus()
        self.ent_name.bind("<Return>", self.ask_to_play)

    # Ask user which game to play
    def ask_to_play(self, event):
        self.user_name = self.ent_name.get().title()
        # self.resize_window(420, 400)

        self.clean_up_widgets()
        Label(self.frames[0], text=f"Hi, {self.user_name}", font=("Arial Bold", 25)).pack(pady=25)
        Label(self.frames[0], text="Which game would you like to play?").pack()
        Button(self.frames[1], text="Hangman", command=self.start_hangman, height=120, image=self.hangman_pic, compound=TOP).pack(side=LEFT, padx=75, pady=25)
        Button(self.frames[1], text="Wordplay", command=self.start_word_play, height=120, image=self.wordplay_pic, compound=TOP).pack(side=LEFT, pady=25)
    
    # game menu
    def game_menu(self):
        self.clean_up_widgets()
        Label(self.frames[0], text=f"Hi, {self.user_name}", font=("Arial Bold", 25)).pack(pady=25)
        Label(self.frames[0], text="Which game would you like to play?").pack()
        Button(self.frames[1], text="Hangman", command=self.start_hangman, height=120, image=self.hangman_pic, compound=TOP).pack(side=LEFT, padx=75, pady=25)
        Button(self.frames[1], text="Wordplay", command=self.start_word_play, height=120, image=self.wordplay_pic, compound=TOP).pack(side=LEFT, pady=25)

    # Asks confirmation from user to quit
    def quit_game(self):
        if messagebox.askokcancel(message="Are you want to quit?"):
            self.root.destroy()

    # game over
    def game_over(self):
        # self.clean_up_widgets()
        if self.game == "hangman":
            self.hangman_game_over()
        elif self.game == "wordplay":
            self.wordplay_game_over()

    # Asks confirmation from user to give up
    def give_up(self):
        if messagebox.askokcancel(message="Are you sure?"):
            self.clean_up_widgets()
            if self.game == "hangman":
                self.game_setting['status'] = "gave_up"
            elif self.game == "wordplay":
                Label(self.frames[0], text="Too bad you gave up..", font=("Arial Bold", 16)).pack()
            self.game_over()


game = GameInit(400, 400)

game.root.mainloop()
