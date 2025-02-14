import csv
import tkinter as tk
from tkinter.ttk import Progressbar
import random
import time
from constants.colours import *
from speakers import get_speaker
from constants import APP_NAME, APP_VERSION


def handle_reveal(translation_label:tk.Label):
    translation = new_word[1].replace("|", "\n")
    if translation == translation_label.cget("text"):
        translation_label.config(text="", bg=BACK_GROUND_COLOUR)
    else:
        translation_label.config(text=translation, bg=BACK_GROUND_COLOUR_2)
def handle_next(_btn:tk.Button, _label:tk.Label, translation_label:tk.Label, r:tk.Tk):
    global new_word
    if new_word[1] != 'translation': 
        handle_reveal(translation_label)
        r.update()
        time.sleep(.2)
    _btn.config(text="Next (Z)")
    try:
        new_word = data.__next__()
        prg["value"] += 1
    except:
        new_word = ("finished", 'finished')
        speaker.say("No words left to practice")
        print(f"you practices {practice_word_count} with {len(errors)} errors")
        errors_window(errors)
        root.destroy()
        return
    _label.config(text=new_word[0])
    translation_label.config(text="", bg=BACK_GROUND_COLOUR)
    if not is_mute:
        r.update()
        speaker.say(new_word[0])

def toggle_mute(button:tk.Button):
    global is_mute
    is_mute = False if is_mute else True
    if is_mute:
        return button.config(text="Un-Mute (V)")
    button.config(text="Mute (V)")

def errors_window(error_list):
    window = tk.Tk()
    window.title("list of errors")
    lb = tk.Listbox(window, height=20, width=70,
                    bg=BACK_GROUND_COLOUR, fg=TEXT_COLOUR2) 
    scrollbar = tk.Scrollbar(window, command=lb.yview)
    lb.config(yscrollcommand=scrollbar.set)

    for item in error_list:
        count = 0
        for meaning in item[1].split("|"):
            gap = 90 - len(item[0]) - len(meaning)
            if not count: row = f"{item[0]}{' ' * gap}{meaning}"
            else: row = f"{' ' * (gap + len(item[0]))}{meaning}"
            lb.insert(tk.END, row) 
            count += 1
        lb.insert(tk.END, '-' * 90)
    lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def main_window():
    global prg, errors, root
    root = tk.Tk()
    root.title(f"{APP_NAME}: {APP_VERSION}")
    errors = set()
    root.title("Parham's vocab practice")
    root.geometry("450x600+150+150")
    root.config(bg=BACK_GROUND_COLOUR)
    word_label = tk.Label(root, text="Press start",
                        bg=BACK_GROUND_COLOUR_2,
                        fg=TEXT_COLOUR,
                        font=("monospace", 22, "bold")
    )
    translation_label = tk.Label(root, text="",
                        bg=BACK_GROUND_COLOUR,
                        fg=TEXT_COLOUR,
                        font=("monospace", 22, "bold")
    )
    prg = Progressbar(root, length=400, maximum=(practice_word_count + 1))
    btn_next = tk.Button(root, text="start (Z)", command=lambda: handle_next(btn_next, word_label, translation_label, root))
    btn_reveal = tk.Button(root, text="translation (X)", command=lambda: handle_reveal(translation_label))
    btn_say = tk.Button(root, text="Say (C)",
                        command=lambda: speaker.say(new_word[0]) if new_word[0] != "word"
                        else speaker.say("I'll pronounce the next words")
                        )
    btn_mute = tk.Button(root, text="Mute (V)", command=lambda: toggle_mute(btn_mute))

    btn_save = tk.Button(root, text="Save to errors (F)", command=lambda: errors.add(new_word))
    btn_show_errors = tk.Button(root, text="Show errors (G)", command=lambda: errors_window(errors))


    word_label.pack()
    btn_next.pack()
    btn_reveal.pack()
    btn_say.pack()
    btn_mute.pack()
    translation_label.pack()
    btn_save.pack()
    btn_show_errors.pack()
    prg.pack()

    root.bind("z", lambda _: handle_next(btn_next, word_label, translation_label, root))
    root.bind("Z", lambda _: handle_next(btn_next, word_label, translation_label, root))

    root.bind("x", lambda _: handle_reveal(translation_label))
    root.bind("X", lambda _: handle_reveal(translation_label))

    root.bind("c", lambda _: speaker.say(new_word[0]))
    root.bind("C", lambda _: speaker.say(new_word[0]))

    root.bind("v", lambda _: toggle_mute(btn_mute))
    root.bind("V", lambda _: toggle_mute(btn_mute))

    root.bind("f", lambda _: errors.add(new_word))
    root.bind("F", lambda _: errors.add(new_word))

    root.bind("g", lambda _: errors_window(errors))
    root.bind("G", lambda _: errors_window(errors))

    root.mainloop()


def config_window(word_count):

    #TODO: FINISH THIS FOR INITIAL CONFIG INSTEAD OF RELYING ON TERMINAL
    window = tk.Tk()
    window.geometry("450x280+250+250")
    window.title("start up")
    window.config(bg=BACK_GROUND_COLOUR_2)
    lbl_word_count = tk.Label(window,
            text=f'there are a total of {word_count} words',
            font=('arial', 22, 'underline bold'),
            bg=BACK_GROUND_COLOUR_2,
            fg=TEXT_COLOUR3
            )
    
    shuffle_variable = tk.BooleanVar()
    btn_shuffle = tk.Checkbutton(window,
                text="shuffle the words",
                variable=shuffle_variable,
                fg=TEXT_COLOUR3,
                activeforeground='black',
                activebackground=BACK_GROUND_COLOUR_3,
                background=BACK_GROUND_COLOUR_2,
                selectcolor=CHECK_LIST_SELECTOR
                )

    lbl_word_count.pack()
    btn_shuffle.pack()
    window.mainloop()
# config_window(232)

def vocab_practice():
    global speaker, new_word, is_mute, data, practice_word_count
    speaker = get_speaker("alan")
    new_word = "word", "translation"
    is_mute = False
    with open("./vocabs.csv", encoding="utf-8") as f:

        #TODO: add a GUI based configuration
        print("declare offset if any:")
        print("how many rows to skip from vocab.csv - press enter to skip" )
        data = [(row["word"], row["translation"]) for row in csv.DictReader(f, skipinitialspace=True)]
        total_lines = len(data)
        print(f"there are {total_lines} lines in the file")
        offset = input(f"choose a number between 0 to {total_lines}: ")
        try:
            offset = int(offset)
            if offset >= total_lines: raise ValueError
        except:
            offset = 0
        print(f"{offset} words will be skipped")
        if offset == 0:
            print(f"how many words would you like to practice after first word?")
        elif offset == 1:
            print(f"how many words would you like to practice after second word?")
        else:
            print(f"how many words would you like to practice after {offset+1}th word?")
        max_word = input("choose the number of last word you wish to practice: ")
        try:
            max_word = offset + int(max_word) + 1
            if max_word >= total_lines + 1: raise ValueError
        except ValueError: max_word = total_lines + 1
        data = data[offset:max_word]
        practice_word_count = max_word - offset - 1
        print(f"words in range [{offset}, {max_word}) will be practiced. ({practice_word_count} words)")
        shuffle_words = input("the words will be shuffled, enter 'No' to avoid it: ")
        shuffle_words += 'y'
        if shuffle_words[0].lower() != 'n': random.shuffle(data)
        data = data.__iter__()
    main_window()


if __name__ == '__main__':
    vocab_practice()
