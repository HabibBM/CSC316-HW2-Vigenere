def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('a')
            new_char = chr((ord(ch) - base + shift) % 26 + base)
            result += new_char
            key_index += 1
        else:
            result += ch
    return result


def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('a')
            new_char = chr((ord(ch) - base - shift) % 26 + base)
            result += new_char
            key_index += 1
        else:
            result += ch
    return result


def key_to_order(num_key):
    pairs = []
    for position, digit in enumerate(num_key):
        pairs.append((int(digit), position))
    pairs.sort()
    order = [position for (digit, position) in pairs]
    return order


def column_encrypt(text, num_key):
    cols = len(num_key)
    while len(text) % cols != 0:
        text += "X"

    grid = []
    for i in range(0, len(text), cols):
        grid.append(list(text[i:i + cols]))

    order = key_to_order(num_key)

    result = ""
    for col in order:
        for row in grid:
            result += row[col]
    return result


def column_decrypt(text, num_key):
    cols = len(num_key)
    rows = len(text) // cols
    order = key_to_order(num_key)

    grid = [["" for _ in range(cols)] for _ in range(rows)]

    index = 0
    for col in order:
        for row in range(rows):
            grid[row][col] = text[index]
            index += 1

    result = ""
    for row in grid:
        result += "".join(row)
    return result


def row_encrypt(text, num_key):
    rows_count = len(num_key)
    while len(text) % rows_count != 0:
        text += "X"

    row_length = len(text) // rows_count
    rows = []
    for i in range(0, len(text), row_length):
        rows.append(text[i:i + row_length])

    order = key_to_order(num_key)

    result = ""
    for r in order:
        result += rows[r]
    return result


def row_decrypt(text, num_key):
    rows_count = len(num_key)
    row_length = len(text) // rows_count
    order = key_to_order(num_key)

    scrambled_rows = []
    for i in range(0, len(text), row_length):
        scrambled_rows.append(text[i:i + row_length])

    original_rows = ["" for _ in range(rows_count)]
    for position, r in enumerate(order):
        original_rows[r] = scrambled_rows[position]

    return "".join(original_rows)


def encrypt(text, vig_key, col_key, row_key):
    block = len(col_key) * len(row_key)
    while len(text) % block != 0:
        text += "X"

    step1 = vigenere_encrypt(text, vig_key)
    step2 = column_encrypt(step1, col_key)
    step3 = row_encrypt(step2, row_key)
    return step1, step2, step3


def decrypt(text, vig_key, col_key, row_key):
    step1 = row_decrypt(text, row_key)
    step2 = column_decrypt(step1, col_key)
    step3 = vigenere_decrypt(step2, vig_key)
    return step3


def main():
    print("=== Vigenere Cipher with Row & Column Permutations ===")
    print("1) Encrypt")
    print("2) Decrypt")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        text = input("Enter the plaintext: ")
        vig_key = input("Enter the Vigenere keyword (letters): ").strip()
        col_key = input("Enter the column permutation key (digits, e.g. 3142): ").strip()
        row_key = input("Enter the row permutation key (digits, e.g. 231): ").strip()

        s1, s2, s3 = encrypt(text, vig_key, col_key, row_key)
        print("\n--- Steps ---")
        print("After Vigenere:          ", s1)
        print("After column permutation:", s2)
        print("Final ciphertext:        ", s3)
        print("\nCopy this ciphertext to decrypt it back:")
        print(s3)

    elif choice == "2":
        text = input("Enter the ciphertext: ")
        vig_key = input("Enter the Vigenere keyword (letters): ").strip()
        col_key = input("Enter the column permutation key (digits, e.g. 3142): ").strip()
        row_key = input("Enter the row permutation key (digits, e.g. 231): ").strip()

        original = decrypt(text, vig_key, col_key, row_key)
        print("\nDecrypted text:")
        print(original)
        print("\n(Note: there may be some extra X letters at the end from padding.)")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
