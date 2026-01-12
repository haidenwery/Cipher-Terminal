#  Copyright (C) 2026 [Haiden Wery]
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

# ------------------ #
import os
import sys
import json
import random
import base64
import time
from math import gcd
from abc import ABC, abstractmethod

# ------------------ #

STATS_FILE = "cipher_terminal_stats.json"
DICT_FILE = "dictionary.txt"  #Extra quotes 

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_stats(stats):
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print("Warning: could not save stats:", e)

# ------------------ #

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

BANNER = r"""                                                        
 _____ _     _              _____               _         _ 
|     |_|___| |_ ___ ___   |_   _|___ ___ _____|_|___ ___| |
|   --| | . |   | -_|  _|    | | | -_|  _|     | |   | .'| |
|_____|_|  _|_|_|___|_|      |_| |___|_| |_|_|_|_|_|_|__,|_|
        |_|                                                 
"""

def banner_page():
    clear_screen()
    print(BANNER)

def prompt(s="> "):
    try:
        return input(s)
    except (KeyboardInterrupt, EOFError):
        print()
        return "quit"

# ---------------------------#
class PhraseManager:
    INTERNAL_LIBRARY = [
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
        "PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS",
        "SPHINX OF BLACK QUARTZ JUDGE MY VOW",
        "KNOWLEDGE IS POWER",
        "TO BE OR NOT TO BE THAT IS THE QUESTION",
        "I THINK THEREFORE I AM",
        "ALL THAT GLITTERS IS NOT GOLD",
        "A JOURNEY OF A THOUSAND MILES BEGINS WITH A SINGLE STEP",
        "KEEP YOUR FRIENDS CLOSE AND YOUR ENEMIES CLOSER",
        "ELEMENTARY MY DEAR WATSON",
        "HOUSTON WE HAVE A PROBLEM",
        "MAY THE FORCE BE WITH YOU",
        "ET TU BRUTE",
        "CARPE DIEM SEIZE THE DAY",
        "SIC PARVIS MAGNA GREATNESS FROM SMALL BEGINNINGS",
        "THE ONLY THING WE HAVE TO FEAR IS FEAR ITSELF",
        "ASK NOT WHAT YOUR COUNTRY CAN DO FOR YOU",
        "GIVE ME LIBERTY OR GIVE ME DEATH",
        "THE UNEXAMINED LIFE IS NOT WORTH LIVING",
        "FORTUNE FAVORS THE BOLD",
        "TIME IS MONEY",
        "ACTIONS SPEAK LOUDER THAN WORDS",
        "BEAUTY IS IN THE EYE OF THE BEHOLDER",
        "BETTER LATE THAN NEVER",
        "BIRDS OF A FEATHER FLOCK TOGETHER",
        "CLEANLINESS IS NEXT TO GODLINESS",
        "DISCRETION IS THE BETTER PART OF VALOR",
        "DONT COUNT YOUR CHICKENS BEFORE THEY HATCH",
        "EASY COME EASY GO",
        "EVERY CLOUD HAS A SILVER LINING",
        "GOD HELPS THOSE WHO HELP THEMSELVES",
        "GOOD THINGS COME TO THOSE WHO WAIT",
        "HASTE MAKES WASTE",
        "IF IT AINT BROKE DONT FIX IT",
        "IGNORANCE IS BLISS",
        "IT TAKES TWO TO TANGO",
        "LOOK BEFORE YOU LEAP",
        "NECESSITY IS THE MOTHER OF INVENTION",
        "NO PAIN NO GAIN",
        "OUT OF SIGHT OUT OF MIND",
        "PRACTICE MAKES PERFECT",
        "ROME WAS NOT BUILT IN A DAY",
        "THE EARLY BIRD CATCHES THE WORM",
        "THE PEN IS MIGHTIER THAN THE SWORD",
        "TWO HEADS ARE BETTER THAN ONE",
        "WHEN IN ROME DO AS THE ROMANS DO",
        "WHERE THERE IS SMOKE THERE IS FIRE",
        "YOU CANT JUDGE A BOOK BY ITS COVER",
        "CRYPTOGRAPHY IS THE SCIENCE OF SECRETS",
        "SECURITY THROUGH OBSCURITY IS NOT SECURITY",
        "TRUST BUT VERIFY",
        "LOOSE LIPS SINK SHIPS",
        "CODE IS LAW",
        "INFORMATION WANTS TO BE FREE",
        "DEBUGGING IS TWICE AS HARD AS WRITING THE CODE"
    ]

    @staticmethod
    def get_phrase():
        phrase_pool = list(PhraseManager.INTERNAL_LIBRARY)

        if os.path.exists(DICT_FILE):
            try:
                with open(DICT_FILE, "r", encoding="utf-8") as f:
                    external_lines = [line.strip().upper() for line in f if line.strip()]
                    
                    phrase_pool.extend(external_lines)
            except Exception:
                pass

        return random.choice(phrase_pool)

# ------------------ #

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def sanitize_letters(s):
    return "".join(ch for ch in s.upper() if ch.isalpha())

def preserve_nonletters(s):
    return "".join(ch.upper() if ch.isalpha() else ch for ch in s)

def modinv(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("No modular inverse")

# ------------------ #

class Cipher(ABC):
    def __init__(self, name, key_desc):
        self.name = name
        self.key_desc = key_desc

    @abstractmethod
    def encrypt(self, text, key):
        pass

    @abstractmethod
    def decrypt(self, text, key):
        pass

    @abstractmethod
    def generate_key(self):
        """Returns a valid random key for this cipher."""
        pass

    def format_key(self, key):
        """Returns a string representation of the key for display."""
        return str(key)

# ------------------ #

class Caesar(Cipher):
    def __init__(self): super().__init__("Caesar", "Shift (1-25)")

    def encrypt(self, text, shift):
        s = preserve_nonletters(text)
        out = []
        r = shift % 26
        for ch in s:
            if ch.isalpha():
                out.append(ALPHABET[(ALPHABET.index(ch) + r) % 26])
            else:
                out.append(ch)
        return "".join(out)

    def decrypt(self, text, shift):
        return self.encrypt(text, -shift)

    def generate_key(self): return random.randint(1, 25)


class ROT13(Cipher):
    def __init__(self): super().__init__("ROT13", "None")

    def encrypt(self, text, key=None):
        return Caesar().encrypt(text, 13)

    def decrypt(self, text, key=None): return self.encrypt(text)
    def generate_key(self): return None


class Atbash(Cipher):
    def __init__(self): super().__init__("Atbash", "None")

    def encrypt(self, text, key=None):
        _ATBASH = {a: b for a, b in zip(ALPHABET, reversed(ALPHABET))}
        s = preserve_nonletters(text)
        return "".join(_ATBASH[ch] if ch.isalpha() else ch for ch in s)

    def decrypt(self, text, key=None): return self.encrypt(text)
    def generate_key(self): return None


class Vigenere(Cipher):
    def __init__(self): super().__init__("Vigenere", "Keyword")

    def _keystream(self, key, length):
        k = sanitize_letters(key)
        if not k: raise ValueError("Key must contain letters")
        return (k * ((length // len(k)) + 1))[:length]

    def encrypt(self, text, key):
        seq = preserve_nonletters(text)
        ks = self._keystream(key, len([c for c in seq if c.isalpha()]))
        out = []
        ki = 0
        for ch in seq:
            if ch.isalpha():
                shift = ALPHABET.index(ks[ki])
                out.append(ALPHABET[(ALPHABET.index(ch) + shift) % 26])
                ki += 1
            else:
                out.append(ch)
        return "".join(out)

    def decrypt(self, text, key):
        seq = preserve_nonletters(text)
        ks = self._keystream(key, len([c for c in seq if c.isalpha()]))
        out = []
        ki = 0
        for ch in seq:
            if ch.isalpha():
                shift = ALPHABET.index(ks[ki])
                out.append(ALPHABET[(ALPHABET.index(ch) - shift) % 26])
                ki += 1
            else:
                out.append(ch)
        return "".join(out)

    def generate_key(self):
        return ''.join(random.choice(ALPHABET) for _ in range(random.randint(3, 8)))


class Affine(Cipher):
    def __init__(self): super().__init__("Affine", "Pair (a, b)")

    def encrypt(self, text, key):
        a, b = key
        s = preserve_nonletters(text)
        out = []
        for ch in s:
            if ch.isalpha():
                x = ALPHABET.index(ch)
                out.append(ALPHABET[(a * x + b) % 26])
            else:
                out.append(ch)
        return "".join(out)

    def decrypt(self, text, key):
        a, b = key
        try:
            a_inv = modinv(a, 26)
        except ValueError:
            return "[Error: Key 'a' has no modular inverse]"
        s = preserve_nonletters(text)
        out = []
        for ch in s:
            if ch.isalpha():
                y = ALPHABET.index(ch)
                out.append(ALPHABET[(a_inv * (y - b)) % 26])
            else:
                out.append(ch)
        return "".join(out)

    def generate_key(self):
        coprimes = [x for x in range(1, 26) if gcd(x, 26) == 1]
        return (random.choice(coprimes), random.randint(0, 25))

    def format_key(self, key): return f"a={key[0]}, b={key[1]}"


class RailFence(Cipher):
    def __init__(self): super().__init__("Rail Fence", "Rails (int)")

    def encrypt(self, text, rails):
        s = sanitize_letters(text)
        if rails <= 1: return s
        fence = ['' for _ in range(rails)]
        row, direction = 0, 1
        for ch in s:
            fence[row] += ch
            row += direction
            if row == rails - 1 or row == 0: direction *= -1
        return ''.join(fence)

    def decrypt(self, text, rails):
        s = sanitize_letters(text)
        if rails <= 1: return s
        pattern = []
        row, direction = 0, 1
        for _ in s:
            pattern.append(row)
            row += direction
            if row == rails - 1 or row == 0: direction *= -1

        rows = {r: [] for r in range(rails)}
        idx = 0
        for r in range(rails):
            cnt = pattern.count(r)
            rows[r] = list(s[idx:idx+cnt])
            idx += cnt

        pointers = {r:0 for r in range(rails)}
        out = []
        for r in pattern:
            out.append(rows[r][pointers[r]])
            pointers[r] += 1
        return ''.join(out)

    def generate_key(self): return random.randint(2, 6)


class Substitution(Cipher):
    def __init__(self): super().__init__("Substitution", "Map (26 chars)")

    def encrypt(self, text, keymap):
        s = preserve_nonletters(text)
        return "".join(keymap.get(ch, ch) for ch in s)

    def decrypt(self, text, keymap):
        inv = {v: k for k, v in keymap.items()}
        s = preserve_nonletters(text)
        return "".join(inv.get(ch, ch) for ch in s)

    def generate_key(self):
        shuffled = list(ALPHABET)
        random.shuffle(shuffled)
        return dict(zip(ALPHABET, shuffled))

    def format_key(self, key):
        demo = "".join([key[c] for c in ALPHABET[:10]])
        return f"{demo}..."


class Hill(Cipher):
    def __init__(self): super().__init__("Hill (2x2)", "Matrix [a,b,c,d]")

    def matrix_det_inv(self, matrix):
        a,b = matrix[0]
        c,d = matrix[1]
        det = (a*d - b*c) % 26
        try:
            invdet = modinv(det, 26)
        except ValueError:
            raise ValueError("Matrix not invertible")
        return [[(d * invdet) % 26, ((-b) * invdet) % 26],
                [((-c) * invdet) % 26, (a * invdet) % 26]]

    def encrypt(self, text, matrix):
        s = sanitize_letters(text)
        if len(s) % 2 == 1: s += 'X'
        out = []
        for i in range(0, len(s), 2):
            v0, v1 = ALPHABET.index(s[i]), ALPHABET.index(s[i+1])
            c0 = (matrix[0][0]*v0 + matrix[0][1]*v1) % 26
            c1 = (matrix[1][0]*v0 + matrix[1][1]*v1) % 26
            out.append(ALPHABET[c0] + ALPHABET[c1])
        return ''.join(out)

    def decrypt(self, text, matrix):
        inv = self.matrix_det_inv(matrix)
        s = sanitize_letters(text)
        out = []
        for i in range(0, len(s), 2):
            v0 = ALPHABET.index(s[i])
            v1 = ALPHABET.index(s[i+1]) if i+1 < len(s) else 0
            p0 = (inv[0][0]*v0 + inv[0][1]*v1) % 26
            p1 = (inv[1][0]*v0 + inv[1][1]*v1) % 26
            out.append(ALPHABET[p0] + ALPHABET[p1])
        return ''.join(out)

    def generate_key(self):
        while True:
            a,b,c,d = [random.randint(0,25) for _ in range(4)]
            det = (a*d - b*c) % 26
            if gcd(det, 26) == 1:
                return [[a,b],[c,d]]

    def format_key(self, key): return f"{key[0]},{key[1]}"

class Base64Cipher(Cipher):
    def __init__(self): super().__init__("Base64", "None")
    def encrypt(self, text, key=None): return base64.b64encode(text.encode('utf-8')).decode('ascii')
    def decrypt(self, text, key=None):
        try: return base64.b64decode(text.encode('ascii')).decode('utf-8')
        except: return "[Invalid Base64]"
    def generate_key(self): return None

CIPHER_REGISTRY = [
    Caesar(),
    ROT13(),
    Atbash(),
    Vigenere(),
    Affine(),
    Substitution(),
    RailFence(),
    Hill(),
    Base64Cipher()
]

# ------------------ #

def ensure_user(stats, user):
    if user not in stats:
        stats[user] = {"total_attempts": 0, "total_correct": 0, "total_hints": 0, "ciphers": {}}

def ensure_cipher_entry(stats, user, cipher_name):
    ensure_user(stats, user)
    if cipher_name not in stats[user]["ciphers"]:
        stats[user]["ciphers"][cipher_name] = {
            "attempts": 0, "correct": 0, "hints": 0, "fastest": None, "longest": None
        }

def record_attempt(stats, user, cipher_name, correct, hints_used, elapsed_seconds):
    ensure_cipher_entry(stats, user, cipher_name)
    stats[user]["total_attempts"] += 1
    stats[user]["total_hints"] += hints_used
    if correct: stats[user]["total_correct"] += 1

    c = stats[user]["ciphers"][cipher_name]
    c["attempts"] += 1
    c["hints"] += hints_used
    if correct: c["correct"] += 1

    if elapsed_seconds is not None and correct:
        if c["fastest"] is None or elapsed_seconds < c["fastest"]:
            c["fastest"] = elapsed_seconds
        if c["longest"] is None or elapsed_seconds > c["longest"]:
            c["longest"] = elapsed_seconds
    save_stats(stats)

# ------------------ #
def give_hint(expected, reveal=3):
    s = sanitize_letters(expected)
    if not s: return "(no hint available)"
    reveal = min(reveal, len(s))
    return f"Hint: starts with '{s[:reveal]}...'"

def practice_mode(stats, user, cipher):
    banner_page()
    print(f"Practice: {cipher.name}")
    print("Type 'hint' for a clue, 'skip' to pass, 'quit' to exit.")

    while True:
        phrase = PhraseManager.get_phrase()
        is_encode = random.choice([True, False])
        key = cipher.generate_key()

        try:
            if is_encode:
                prompt_text = f"Encode this using {cipher.name}"
                challenge_text = phrase
                target_display = cipher.encrypt(phrase, key)
                comparison_target = sanitize_letters(target_display)
                display_key = cipher.format_key(key) if key is not None else "N/A"
            else:
                prompt_text = f"Decode this from {cipher.name}"
                challenge_text = cipher.encrypt(phrase, key)
                target_display = phrase 
                comparison_target = sanitize_letters(phrase)
                display_key = cipher.format_key(key) if key is not None else "N/A"

            print(f"\n{prompt_text}")
            print(f"Text: {challenge_text}")

            start_t = time.time()
            hints = 0

            while True:
                ans = prompt("Your Answer: ").strip()
                if ans.lower() == "quit": return

                if ans.lower() == "skip":
                    print(f"Skipped. The answer was: {target_display}")
                    break

                if ans.lower() == "hint":
                    print(give_hint(comparison_target))
                    hints += 1
                    continue

                elapsed = time.time() - start_t
                user_clean = sanitize_letters(ans)
                correct = (user_clean == comparison_target)

                if correct:
                    record_attempt(stats, user, cipher.name, True, hints, elapsed)
                    print(f"Correct! ({elapsed:.2f}s)")
                    break 
                else:
                    record_attempt(stats, user, cipher.name, False, hints, elapsed)
                    print("Incorrect.")
                    retry = prompt("Try again? (Y/n): ").lower()
                    if retry == 'n':
                        print(f"The answer was: {target_display}")
                        break

            if prompt("Next? (Enter to continue, 'q' to quit): ").lower() == 'q':
                return

        except Exception as e:
            print(f"Error generating puzzle: {e}")
            break

def input_mode(stats, user, cipher):
    banner_page()
    print(f"Input Mode: {cipher.name}")
    print(f"Key Format: {cipher.key_desc}")
    print("Enter 'random' for a random key where applicable.")

    while True:
        msg = prompt("\nEnter message (or 'quit'): ")
        if msg.lower() in ("quit", ""): return

        key = None
        if cipher.key_desc != "None":
            k_in = prompt(f"Enter Key ({cipher.key_desc}): ").strip()
            if k_in.lower() == "random":
                key = cipher.generate_key()
                print(f"Using random key: {cipher.format_key(key)}")
            else:
                try:
                    if "int" in cipher.key_desc or "Shift" in cipher.key_desc:
                        key = int(k_in)
                    elif "Pair" in cipher.key_desc: # Affine
                        parts = k_in.replace(',',' ').split()
                        key = (int(parts[0]), int(parts[1]))
                    elif "Matrix" in cipher.key_desc:
                        parts = k_in.replace(',',' ').split()
                        key = [[int(parts[0]), int(parts[1])], [int(parts[2]), int(parts[3])]]
                    elif "Map" in cipher.key_desc:
                        if len(k_in) != 26: raise ValueError
                        key = {ALPHABET[i]: k_in.upper()[i] for i in range(26)}
                    else:
                        key = k_in
                except:
                    print("Invalid key format.")
                    continue

        mode = prompt("Encode (e) or Decode (d)? ").lower()
        try:
            if mode.startswith('d'):
                res = cipher.decrypt(msg, key)
            else:
                res = cipher.encrypt(msg, key)
            print(f"Result:\n{res}")
        except Exception as e:
            print(f"Error: {e}")

# ------------------ #
def show_stats(stats, user):
    banner_page()
    ensure_user(stats, user)
    u = stats[user]
    print(f"\nStats for {user}")
    print(f"Total Attempts: {u['total_attempts']} | Accuracy: {(u['total_correct']/(u['total_attempts'] or 1))*100:.1f}%")

    print("\n" + "="*75)
    print(f"{'Cipher':<15} | {'Score':<10} | {'Fastest':<10} | {'Hints'}")
    print("-" * 75)

    for c_name, data in u["ciphers"].items():
        score = f"{data['correct']}/{data['attempts']}"
        fast = f"{data['fastest']:.2f}s" if data['fastest'] else "--"
        print(f"{c_name:<15} | {score:<10} | {fast:<10} | {data['hints']}")
    print("="*75 + "\n")
    prompt("Enter to continue...")

def main():
    stats = load_stats()
    current_user = None

    while True:
        banner_page()
        if current_user: print(f"Logged in as: {current_user}")
        print("1. Login")
        print("2. Ciphers")
        print("3. Stats")
        print("4. About")
        print("5. Quit")

        choice = prompt("Select: ").strip().lower()

        if choice == "1":
            u = prompt("Username: ").strip()
            if u:
                current_user = u
                ensure_user(stats, current_user)

        elif choice == "2":
            if not current_user:
                print("Login first!"); time.sleep(1); continue

            while True:
                banner_page()
                for i, c in enumerate(CIPHER_REGISTRY):
                    print(f"{i+1}. {c.name}")
                print("B. Back")

                sel = prompt("Choice: ").lower()
                if sel == 'b': 
                    banner_page()
                    break
                if sel.isdigit() and 1 <= int(sel) <= len(CIPHER_REGISTRY):
                    cipher = CIPHER_REGISTRY[int(sel)-1]
                    banner_page()
                    print(f"Cipher: {cipher.name}")
                    print("1. Practice\n2. Input Mode")
                    sub = prompt("Mode: ")
                    if sub == "1": practice_mode(stats, current_user, cipher)
                    elif sub == "2": input_mode(stats, current_user, cipher)

        elif choice == "3":
            if current_user: show_stats(stats, current_user)
            else: print("Login first!")

        elif choice == "4":
            banner_page()
            print("--- Cipher Terminal v1.0 ---")
            print("This is Version 1.0 of a hobby project to practice and learn cryptography better. \nIn the future, more ciphers will be added as well as bug fixes, updated systems and UI, redesigns, and more. ")
            prompt("Enter to continue...")

        elif choice in ("5", "quit"):
            save_stats(stats)
            sys.exit()

if __name__ == "__main__":

    main()
