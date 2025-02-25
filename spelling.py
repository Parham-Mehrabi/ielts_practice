import random
from speakers import get_speaker
import time


def get_config():
    config = {
        "skip_errors": True,
        "repeat_errors": True,
        "highlight_errors": True,
        "shuffle_words": True
    }
    user_input = input("You will set the configs next, enter N to skip with default settings : ")
    user_input += "y"
    if user_input.lower()[0] == 'n': return config
    else:
        print("Answer following questions with Y[es] or N[o]")
    try:
        skip_errors = input("skip the word if mistake?Y/n (default Y)")
        skip_errors += 'y'
        skip_errors.lower()
        if skip_errors[0] == 'n':
            config["skip_errors"] = False
        repeat_errors = input("ask mistaken words again in the end ?Y/n (default Y)")
        repeat_errors += 'y'
        repeat_errors.lower()
        if repeat_errors[0] == 'n':
            config["repeat_errors"] = False

        highlight_errors = input("highlight missed letters ?Y/n (default Y)")
        highlight_errors += 'y'
        highlight_errors.lower()
        if highlight_errors[0] == 'n':
            config.update({"highlight_errors": False})
        shuffle_words = input("Do you want to shuffle words? ?Y/n (default Y)")
        shuffle_words += 'y'
        shuffle_words.lower()
        if shuffle_words[0] == 'n':
            config["shuffle_words"] = False
        return config
    except Exception as e:
        print(e)
        print('-----')
        print("unexpected error, using default settings . . .")
        return {
                "skip_errors": True,
                "repeat_errors": True,
                "highlight_errors": True,
                "speaker": 'alan'
            }

def intro(config):
    introduction = f"""{config}
    \t\tyou will hear some words, try to write them.

    \t\t>>   enter 'R' to repeat   <<\n\r"""
    print(introduction)
    

def highlight_error(word:str, user_input:str):
    user_input =  user_input.ljust(len(word), "*")
    for i in range(len(word)):
        if word[i] == user_input[i]: print(word[i], end="", sep="", flush=True)
        else: print(word[i].upper(), end="", flush=True)
        time.sleep(0.01)
def ask_questions(words:list[str], configs:dict):
    errors = []
    for word in words:
        speaker.say(word)
        user_input = input("-->  ").strip()
        while True:
            if user_input == 'r':
                speaker.say(word)
                user_input = input("\r-->  ").strip()
            elif user_input.lower().strip() != word.lower().strip():
                print(f"WRONG\ncorrect: {word}\nyour wrote: {user_input}")
                if configs['highlight_errors']:
                    highlight_error(word, user_input)
                print(f"\n\r".ljust(50, '-'))
                if configs["repeat_errors"] : errors.append(word)
                if configs['skip_errors']: break
                else: 
                    speaker.say(word)
                    user_input = input("-->  ").strip()
                    continue
            else:
                print("CORRECT")
                print(word.upper())
                print(f"\n\r".ljust(50, '-'))
                break
        
    if configs["repeat_errors"] and len(errors): ask_questions(errors, configs)

    print(f"\rCongratulation, you practiced {len(words)} and made {len(errors)} errors", end="")
    if len(errors):
        print("\n\nhere is a list of your errors:")
    print('\n------')
    for n, e in enumerate(errors):
        print(f"{n+1}: {e.strip()}", end='\n')
    print('------')
        

def spelling_practice():
    global speaker, words
    speaker = get_speaker('alan')
    config = get_config()
    intro(config)
    with open('./spellings.txt') as f:
        words = f.readlines()

        print("declare offset if any:")
        print("how many lines to skip from spellings.txt - press enter to skip" )
        total_lines = len(words)
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
        max_word = input("choose the number of words you wish to practice: ")
        try:
            max_word = offset + int(max_word) + 1
            if max_word >= total_lines + 1: raise ValueError
        except ValueError: max_word = total_lines + 1
        words = words[offset:max_word]
        if config['shuffle_words']: random.shuffle(words)

    ask_questions(words, config)

if __name__ == '__main__':
    spelling_practice()
