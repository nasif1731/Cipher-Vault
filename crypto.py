import numpy as np

# -----------------------------
#  CAESAR CIPHER WITH STEPS
# -----------------------------
def caesar_cipher(char, shift, encrypt=True, show_steps=False):
    if not char.isalpha():
        return (char, f"Non-alpha '{char}' remains unchanged") if show_steps else char

    base = ord('A') if char.isupper() else ord('a')
    pos = ord(char) - base
    effective_shift = shift if encrypt else -shift
    new_pos = (pos + effective_shift) % 26
    shifted_char = chr(base + new_pos)

    if show_steps:
        step = (
            f"{'Encrypting' if encrypt else 'Decrypting'} '{char}': "
            f"ord={ord(char)}, pos={pos}, shift={effective_shift} → "
            f"new_pos={new_pos} → '{shifted_char}'"
        )
        return shifted_char, step

    return shifted_char


# -----------------------------
#  VIGENERE CIPHER WITH STEPS
# -----------------------------
def vigenere_cipher(text, key, encrypt=True, show_steps=False):
    key = key.upper()
    key_len = len(key)

    result = ""
    steps = []
    j = 0  # index for key

    for char in text:
        if char.isalpha():
            k = key[j % key_len]
            k_val = ord(k) - 65
            c_val = ord(char.upper()) - 65

            new_val = (c_val + k_val) % 26 if encrypt else (c_val - k_val + 26) % 26
            result_char = chr(new_val + (65 if char.isupper() else 97))

            if show_steps:
                steps.append(
                    f"{'Encrypting' if encrypt else 'Decrypting'} '{char}' with key '{k}': "
                    f"({c_val} {'+' if encrypt else '-'} {k_val}) % 26 = {new_val} → '{result_char}'"
                )

            result += result_char
            j += 1
        else:
            result += char
            if show_steps:
                steps.append(f"Non-alpha '{char}' remains unchanged")

    return (result, steps) if show_steps else result


# -----------------------------
#  PLAYFAIR CIPHER WITH STEPS
# -----------------------------
def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    seen = set()
    matrix = []

    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i * 5:(i + 1) * 5] for i in range(5)]


def locate(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return None


def playfair_prepare(text):
    text = text.upper().replace("J", "I")
    cleaned = ""

    for char in text:
        if char.isalpha():
            cleaned += char

    result = ""
    i = 0
    while i < len(cleaned):
        a = cleaned[i]
        b = cleaned[i + 1] if i + 1 < len(cleaned) else "X"

        if a == b:
            result += a + "X"
            i += 1
        else:
            result += a + b
            i += 2

    if len(result) % 2 == 1:
        result += "X"

    return result


def playfair_cipher(text, key, encrypt=True, return_steps=False):
    matrix = generate_playfair_matrix(key)
    prepared = playfair_prepare(text)
    result = ""
    steps = []

    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i + 1]
        r1, c1 = locate(matrix, a)
        r2, c2 = locate(matrix, b)

        if r1 == r2:  # same row
            new_c1 = (c1 + (1 if encrypt else -1)) % 5
            new_c2 = (c2 + (1 if encrypt else -1)) % 5
            ra, rb = matrix[r1][new_c1], matrix[r2][new_c2]
            rule = f"Row rule: shift {'right' if encrypt else 'left'}"
        elif c1 == c2:  # same column
            new_r1 = (r1 + (1 if encrypt else -1)) % 5
            new_r2 = (r2 + (1 if encrypt else -1)) % 5
            ra, rb = matrix[new_r1][c1], matrix[new_r2][c2]
            rule = f"Column rule: shift {'down' if encrypt else 'up'}"
        else:  # rectangle rule
            ra, rb = matrix[r1][c2], matrix[r2][c1]
            rule = "Rectangle rule: swap columns"

        steps.append(
            f"Digraph '{a}{b}': positions ({r1},{c1}), ({r2},{c2}) → rule applied: {rule} → '{ra}{rb}'"
        )
        result += ra + rb

    return (matrix, prepared, result, steps) if return_steps else result


def format_playfair_matrix(matrix):
    return "\n".join([" ".join(row) for row in matrix])


# -----------------------------
#  HILL CIPHER WITH STEPS (2×2)
# -----------------------------
def mod_inverse(a, m):
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


import numpy as np

def hill_cipher(text, key_list, size, encrypt=True, return_steps=False):
    K = np.array(key_list).reshape(size, size)

    # Compute determinant and modular inverse
    det = int(np.round(np.linalg.det(K))) % 26
    det_inv = mod_inverse(det, 26)

    if det_inv is None:
        raise ValueError("Key matrix is not invertible modulo 26.")

    # Store original matrix for displaying
    original_matrix = K.copy()

    # For decryption, compute inverse modulo 26
    if not encrypt:
        adj = np.round(det * np.linalg.inv(K)).astype(int) % 26
        K = (det_inv * adj) % 26  # Inverse matrix
        K = K.astype(int)

    cleaned = "".join([c.upper() for c in text if c.isalpha()])
    if len(cleaned) % size != 0:
        cleaned += "X" * (size - len(cleaned) % size)

    result = ""
    steps = []

    for i in range(0, len(cleaned), size):
        block = cleaned[i:i+size]
        vector = [ord(c) - 65 for c in block]

        multiply_steps = []
        product = []

        # Row-by-row detailed math
        for row in range(size):
            terms = []
            total = 0
            for col in range(size):
                term = K[row][col] * vector[col]
                terms.append(f"{K[row][col]}×{vector[col]}")
                total += term

            multiply_steps.append(
                f"Row {row+1}: " + " + ".join(terms) +
                f" = {total} → {total % 26}"
            )

            product.append(total % 26)

        encrypted_block = ''.join(chr(v + 65) for v in product)
        result += encrypted_block

        if encrypt:
            steps.append(
                f"Encrypting block '{block}':\n"
                f"  Vector P = {vector} from '{block}'\n"
                f"  Matrix K = {original_matrix.tolist()}\n"
                f"  Multiply (mod 26):\n    " + "\n    ".join(multiply_steps) + "\n"
                f"  Result vector = {product} → '{encrypted_block}'"
            )
        else:
            steps.append(
                f"Decrypting block '{block}':\n"
                f"  Vector C = {vector} from '{block}'\n"
                f"  Using inverse matrix K⁻¹ = {K.tolist()}\n"
                f"  Multiply (mod 26):\n    " + "\n    ".join(multiply_steps) + "\n"
                f"  Result vector = {product} → '{encrypted_block}'"
            )

    inverse_matrix = None if encrypt else K  # return inverse only during decrypt

    if return_steps:
        return original_matrix, inverse_matrix, result, cleaned, steps

    return result


def format_matrix(matrix, name):
    return f"{name} =\n" + "\n".join(str(row) for row in matrix)
