import math
import tkinter as tk
import tkinter.ttk as ttk
import time
import random


class WordsPerMinute(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WPM Calculator")
        self.minsize(width=200, height=200)
        self.config(pady=20, padx=20)

        self.total_keys_pressed = 0
        self.start_time = 0
        self.end_time = 0
        self.elapsed_time_min = 0
        self.words_per_min = 0
        self.correct_keys_pressed = 0
        self.accuracy = 0
        self.adjusted_wpm = 0
        self.words = []
        self.random_word_string = ""
        self.char_index = 0
        self.word_index = 0
        self.line_word_list = []
        self.has_started = False

        self.wpm_label = ttk.Label(text=f"WPM: {self.words_per_min}", padding=(0, 20))

        self.wpm_label.grid(column=0, row=0)

        self.adjusted_wpm_label = ttk.Label(text="AWPM: 0")
        self.adjusted_wpm_label.grid(column=1, row=0)

        self.text = tk.Text(width=40,
                            height=4,
                            padx=50,
                            pady=10,
                            spacing1=20,
                            font=("Helvetica", 22))
        self.text.grid(column=0, row=2, columnspan=2)

        self.user_input_entry = ttk.Entry(width=40,
                                          justify="center",
                                          font=("Helvetica", 22))
        self.user_input_entry.grid(column=0,
                                   row=3,
                                   columnspan=2,
                                   pady=5)
        self.user_input_entry.bind("<Key>", self.key_is_pressed)
        self.user_input_entry.bind("<space>", self.end_of_word)
        self.user_input_entry.bind("<Return>", self.stop_timer)

        self.instructions_label = ttk.Label(text="1. Type the top line only.\n"
                                                 "2. Press space to move to next word. \n"
                                                 "3. Press enter to stop timer and see wpm.")
        self.instructions_label.grid(column=0, row=4)

        self.get_words()
        self.display_words()
        self.display_words()

    def calculate_wpm(self):
        print(f"keys pressed: {self.total_keys_pressed}")
        total_number_words = self.total_keys_pressed / 5
        print(f"total words: {total_number_words}")
        print(f"elasped time: {self.elapsed_time_min}")
        self.words_per_min = (round(math.floor(total_number_words / self.elapsed_time_min * 60), 1))
        self.wpm_label.config(text=f"WPM: {self.words_per_min}")
        print(f"wpm: {self.words_per_min}")
        self.calculate_accuracy()

    def calculate_accuracy(self):
        self.accuracy = (self.correct_keys_pressed / self.total_keys_pressed) * 100
        self.correct_keys_pressed = 0
        self.total_keys_pressed = 0
        print(f"accuracy: {self.accuracy}")
        self.calculate_adjusted_wpm()

    def calculate_adjusted_wpm(self):
        self.adjusted_wpm = math.floor(self.words_per_min * (self.accuracy / 100))
        self.adjusted_wpm_label.config(text=f"AWPM: {self.adjusted_wpm}")

    def display_words(self):
        num_lines = int(self.text.index("end - 1 line").split(".")[0])
        self.text["state"] = "normal"

        if num_lines == 2:
            self.text.delete(1.0, 2.0)
        if self.text.index("end-1c") != "1.0":
            self.text.insert("end", "\n")

        self.random_word_string = self.get_random_word_string()
        self.text.insert("end", self.random_word_string)
        self.text['state'] = "disabled"

    # TODO figure out to highlight the current word being typed
    # def highlight_word(self):
    #     self.text.tag_configure("word", background="#000080", foreground="white")
    #     self.text.tag_add("word", "1.0", "end")

    def key_is_pressed(self, key):
        if not self.has_started:
            self.has_started = True
            self.start_time = time.time()

        self.total_keys_pressed += 1

        # print(f"char index: {self.char_index}")
        lines = self.text.get("1.0", tk.END).splitlines()
        line_string = ""
        word_length = []
        for char in lines[0]:
            line_string += char
        # print(line_string)
        self.line_word_list = line_string.split()
        # print(words)

        if self.char_index < len(self.line_word_list[self.word_index]) - 1:
            if key.char == self.line_word_list[self.word_index][self.char_index]:
                self.correct_keys_pressed += 1
            if key.char != " ":
                self.char_index += 1
        else:
            if key.char == self.line_word_list[self.word_index][self.char_index]:
                self.correct_keys_pressed += 1
            # self.end_of_word()

    def end_of_word(self, key):
        if self.char_index != 0:
            # print("end of word")
            self.char_index = 0
            if self.word_index + 1 >= len(self.line_word_list):
                # print("new line")
                if self.word_index + 1 >= len(self.line_word_list):
                    self.user_input_entry.delete(0, tk.END)
                self.word_index = 0
                self.char_index = 0
                self.display_words()
            else:
                self.word_index += 1

    def get_words(self):
        with open("words.txt") as word_file:
            word_list = word_file.readlines()
        for word in word_list:
            self.words.append(word.strip("\n"))

    def get_random_word_string(self):
        random_words = []
        for i in range(5):
            random_words.append(random.choice(self.words))
        random_word_string = '  '.join(word for word in random_words)
        return random_word_string

    # def clear_entry(self, key):
    #     # only clear when end of line is detected
    #     self.end_of_word()

    def stop_timer(self, key):
        self.has_started = False
        self.end_time = time.time()
        self.elapsed_time_min = self.end_time - self.start_time
        self.calculate_wpm()
        print(self.correct_keys_pressed)


root = WordsPerMinute()
root.mainloop()
