import random

print("Welcome to Hangman Game")

words = ["python", "java", "computer", "science", "artificial" ,"intelligence"]

hang_art = {
    0:("  ",
       "  ",
       "  "),
    1:(" o ",
       "  ",
       "  "),
    2:(" o ",
       " | ",
       "  "),
    3:(" o ",
       "/| ",
       "  "),
    4:(" o ",
       "/|\\ ",
       "  "),
    5:(" o ",
       "/|\\",
       "/ "),
    6:(" o ",
       "/|\\ ",
       "/ \\")                          
}

def display_hangman(wrong_guess):
    print("**********")
    for line in hang_art[wrong_guess]:
        print(line)
    print("**********")    

def display_hint(hint):
    print(" ".join(hint))

def display_answer(answer):
    print(" ".join(answer))
    

def main():
    answer = random.choice(words)
    hint = ["_"] * len(answer)
    wrong_guess = 0
    letters_guessed = set()
    is_running = True

    while is_running:
        display_hangman(wrong_guess)
        display_hint(hint)
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a valid input")
            continue
        elif guess in letters_guessed:
            print("You have already guessed that letter")
        else:
            letters_guessed.add(guess)    
        

        if guess in answer:
          for i in range(len(answer)):
              if guess == answer[i]:
                 hint[i] = guess
        else:
            wrong_guess += 1

        if "_" not in hint:
            display_answer(answer)
            print("You won!")
            is_running = False
        elif wrong_guess == len(hang_art)-1:
            display_hangman(wrong_guess)
            print("You Lost!")
            display_answer(answer)
            is_running = False
               




if __name__ == "__main__":
    main()