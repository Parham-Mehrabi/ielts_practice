from vocabs import vocab_practice
from spelling import spelling_practice
from constants import APP_VERSION, APP_NAME

def menu():
    print(APP_NAME, APP_VERSION)
    user_input = input("""
        SELECT EITHER SPELLING OR VOCABULARY PRACTICE:
        1) SPELLING
        2) VOCABULARY \n\r--> """)
    try:
        user_input = int(user_input)
    except ValueError:
        return menu()
    if user_input == 1: return spelling_practice()
    elif user_input == 2: return vocab_practice(), 
    else: return print("Invalid. choose either '1' or '2' "), menu()
    


if __name__ == '__main__':
    menu()