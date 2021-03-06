#!/usr/bin/python3.5
import csv
import subprocess
import sys
import random
from akasztofa_fig import *


def reset_terminal():
    subprocess.call(["printf", "\033c"])


def print_toplist(name, hitted_words):
    fajl = open('toplist.txt', "r")
    top_list = fajl.read().split('\n')
    top_list = [elem.split("  ") for elem in top_list]
    top_list = top_list[:-1]
    fajl.close()
    inserted = False
    for i in range(len(top_list)):
        if hitted_words > int(top_list[i][0]):
            top_list.insert(i, [str(hitted_words), name])
            inserted = True
            break
    if not inserted:
        top_list.append([str(hitted_words), name])
    if len(top_list) > 10:
        top_list = top_list[:-1]
    print("\n   BEST PLAYERS:")
    for i in range(len(top_list)):
        print("   {:10}{}".format(top_list[i][1], top_list[i][0]))
    fajl = open('toplist.txt', 'w')
    content = ""
    for i in range(len(top_list)):
        content += "{}  {}\n".format(top_list[i][0], top_list[i][1])
    fajl.write(content)
    fajl.close()


def print_about():
    reset_terminal()
    print(logo[2], end="")     # kiírja a szabályokat és kategóriákat
    print("""
    Rules of the game:

    After you choosen a category or wrote a custom word,
    you (or the other player) have to find out the word
    by writing different letters. If the letter is in
    the word, it will be pasted to the lines.

    You have 9 lifes.
    """)


def color_green(text):
    return "\033[32m{}\033[0m".format(text)


def color_red(text):
    return "\033[31m{}\033[0m".format(text)


# beolvassa fájlt és visszaadja a kategóriákat (a sorok eleje) és a szavakat
def read_letters():
    with open('word_list.csv', 'r') as f:
        reader = csv.reader(f)
        word_list = list(reader)  # listákból álló lista
        cat_list = list()         # a kategóriák listája
        for i in range(len(word_list)):
            cat_list.append(word_list[i].pop(0))
        f.close()
        return word_list, cat_list


# beolvassa a számot, ami a kategóriát jelöli, vagy hibára fut és
# újrahívja a menu()-t
def input_numb(word):   # beolvas egy számot, vagy kilép, ha rossz az input
    numb = input("\n    Give the number of a {}: ".format(word))
    try:
        return int(numb)
    except ValueError:
        raise ValueError("Invalid input")


# értéket ad néhány változónak az elején
def init():
    life = len(figure) - 1
    hitted = list()      # eltalált lista
    bad_tips = list()    # rossz tippek lista
    return life, hitted, bad_tips


# kiválaszt egy szót a kategória (numb) alapján
def random_word(numb, word_list, cat_list):
    if numb in range(1, len(cat_list) + 1):  # ha benne van az alapkategóriákban
        the_word = random.choice(word_list[numb - 1])
        category = cat_list[numb - 1]
    if numb == -1:                         # ha teljesen random szó
        the_word = random.choice(
            word_list[random.choice(range(len(word_list)))])
        category = "RANDOM WORD OF ALL CATEGORY"
    if numb == 0:                          # játékos által megadott szó
        the_word = input("    Give the word to find out: ")
        category = "WORD FROM A PLAYER"
    return the_word, category


# bekér egy betűt tippnek, és a megfelelő listába illeszti
def tipp_f(hitted, bad_tips, life, the_word):
    tipp = input("\n\n   Write a letter: ")
    abc = ["a", "á", "b", "c", "d", "e", "é", "f", "g", "h", "i", "í",
           "j", "k", "l", "m", "n", "o", "ó", "ö", "ő", "p", "q", "r",
           "s", "t", "u", "ú", "ü", "ű", "v", "w", "x", "y", "z"]
    if tipp in abc:         # ha nem az abc-ből van megadva, nem csinál semmit
        i = 0
        bad_tip = True
        for c in the_word:  # megnézi, hogy benne van-e a szóban, ha igen, változik a hitted lista
            if tipp.upper() == c.upper():
                hitted[i] = tipp.upper()
                bad_tip = False
            i += 1
        if bad_tip:         # ha rossz a tipp, bővíti a bad_tips listát
            if tipp.upper() not in bad_tips:
                bad_tips.append(tipp.upper())
                life -= 1
    return bad_tips, life


# sets the menu screen and asks the game mode
def menu_mode(name=[]):
    while True:
        print_about()
        print("    GAME MODES:")
        print("    1 - NORMAL")
        print("    2 - ARCADE")
        print("    3 - ")

        try:
            numb = input_numb("mode")
            if numb in [1, 2, 3]:
                if numb == 2:
                    name.append(input("    Please give your name: "))
                return numb       # bekéri a választott kategória számát
        except ValueError:
            continue


# sets the menu screen and asks the category
def menu_cat(mode, name=""):
    life_left = len(figure) - 1
    hitted_words = 0
    while True:
        life, hitted, bad_tips = init()
        life = life_left
        life += 3
        if life > len(figure) - 1:
            life = len(figure) - 1
        word_list, cat_list = read_letters()
        print_about()
        print("   CATEGORIES:""")
        print("   -1 - A RANDOM WORD OF ALL CATEGORY")
        print("    0 - A WORD GIVEN BY A PLAYER")
        i = 1
        for elem in cat_list:
            print("{:5} - {}".format(i, elem))
            i += 1

        try:
            if mode == 2: 
                numb = -1
            else:
                numb = input_numb("category")       # bekéri a választott kategória számát
            if numb not in range(-1, len(cat_list) + 1):
                continue
        except ValueError:
            continue
        the_word, category = random_word(numb, word_list, cat_list)     # választ egy szót

        for c in the_word:        # felépíti a hitted listát
            if c == '-':
                hitted.append("-")
            elif c == ' ':
                hitted.append(" ")
            else:
                hitted.append("_")

        life_left, hitted_words = game_menu(the_word, life, hitted, bad_tips, category, mode, hitted_words, name)


# itt folyik a játék, itt rajzolódik az akasztófa
def game_menu(the_word, life, hitted, bad_tips, category, mode, hitted_words, name):

    while life > 0 and "_" in hitted:
        reset_terminal()

        print(figure[9 - life], "\n")
        print("   YOU HAVE TO FIND OUT A(N) " + category + "\n")
        print("   Number of solved words: ", hitted_words, "\n\n\n", end="   ")

        for i in range(
                len(the_word)):      # writing the lines and hitted letters
            if the_word[i] != " " and the_word[i] != "-":
                print("_{}_".format(hitted[i] if hitted[i] == "_" else color_green(hitted[i])), end=" ")
            else:
                print(" " + hitted[i] + " ", end=" ")

        print("\n\n   BAD TIPS:", end=" ")
        for i in bad_tips:
            print(color_red(i), end=" ")

        bad_tips, life = tipp_f(hitted, bad_tips, life, the_word)

    if life == 0:
        reset_terminal()
        print(figure[9 - life])
        print("   YOU'RE HANGED, BASTARD!" + "\n\n" +
              "   YOU SHOULD FIND OUT THIS:", the_word, "\n")
        if mode == 2:
            print("   Number of solved words: ", hitted_words)
            print_toplist(name, hitted_words)
            sys.exit()

    if life > 0:
        reset_terminal()
        print(figure[9 - life])
        print("   YOU WON!!!", "\n\n", "  THE WORD:", the_word)

    if mode == 2:
        hitted_words += 1
        return life, hitted_words
    else:
        new_game = input("\n   Do yo try again [y/n]? ")
        if new_game in ["y", "Y"]:
            return None
        else:
            print("\n   Thanks the game! Bye...")
            sys.exit()


# lejátsza az intrót és meghívja a menu()-t
def main():
    try:
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=60))
        intro(logo)
        name = []
        while True:
            mode = menu_mode(name)
            if mode != 2:
                name = [""]
            menu_cat(mode, name[0])
    except KeyboardInterrupt:
        print("\n   You exited the game!")
        sys.exit()


if __name__ == "__main__":
    main()
