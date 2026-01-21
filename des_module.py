# des_module.py

# -----------------------
#   DES CONSTANT TABLES
# -----------------------
IP = [
58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17,  9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
40, 8, 48, 16, 56, 24, 64, 32,
39, 7, 47, 15, 55, 23, 63, 31,
38, 6, 46, 14, 54, 22, 62, 30,
37, 5, 45, 13, 53, 21, 61, 29,
36, 4, 44, 12, 52, 20, 60, 28,
35, 3, 43, 11, 51, 19, 59, 27,
34, 2, 42, 10, 50, 18, 58, 26,
33, 1, 41,  9, 49, 17, 57, 25
]

EXPANSION = [
32, 1, 2, 3, 4, 5,
4, 5, 6, 7, 8, 9,
8, 9,10,11,12,13,
12,13,14,15,16,17,
16,17,18,19,20,21,
20,21,22,23,24,25,
24,25,26,27,28,29,
28,29,30,31,32,1
]

P_BOX = [
16,7,20,21,
29,12,28,17,
1,15,23,26,
5,18,31,10,
2,8,24,14,
32,27,3,9,
19,13,30,6,
22,11,4,25
]

# Standard DES S-boxes
SBOXES = [
[
[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
[4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
],
[
[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
[0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
],
[
[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
[13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
],
[
[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
[10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
],
[
[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
[4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
],
[
[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
[9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
],
[
[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
[1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
],
[
[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
[7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
]
]

# -----------------------
#   UTILITY FUNCTIONS
# -----------------------

def hex_to_bin(h):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)

def bin_to_hex(b):
    return hex(int(b, 2))[2:].upper()

def permute(bits, table):
    return "".join(bits[i-1] for i in table)

def xor(a, b):
    return "".join("0" if x == y else "1" for x, y in zip(a, b))

# -----------------------
#   KEY SCHEDULE
# -----------------------
PC1 = [
57,49,41,33,25,17,9,
1,58,50,42,34,26,18,
10,2,59,51,43,35,27,
19,11,3,60,52,44,36,
63,55,47,39,31,23,15,
7,62,54,46,38,30,22,
14,6,61,53,45,37,29,
21,13,5,28,20,12,4
]

PC2 = [
14,17,11,24,1,5,
3,28,15,6,21,10,
23,19,12,4,26,8,
16,7,27,20,13,2,
41,52,31,37,47,55,
30,40,51,45,33,48,
44,49,39,56,34,53,
46,42,50,36,29,32
]

SHIFT_SCHEDULE = [
1,1,2,2,2,2,2,2,
1,2,2,2,2,2,2,1
]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def generate_round_keys(key64):
    key56 = permute(key64, PC1)
    C, D = key56[:28], key56[28:]
    round_keys = []
    
    for shift in SHIFT_SCHEDULE:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        round_keys.append(permute(C + D, PC2))
    
    return round_keys

# -----------------------
#   FEISTEL FUNCTION
# -----------------------

def sbox_substitution(bits48):
    out = ""
    for i in range(8):
        block = bits48[i*6:(i+1)*6]
        row = int(block[0] + block[-1], 2)
        col = int(block[1:5], 2)
        out += bin(SBOXES[i][row][col])[2:].zfill(4)
    return out

def feistel(R, K):
    expanded = permute(R, EXPANSION)
    xored = xor(expanded, K)
    substituted = sbox_substitution(xored)
    return permute(substituted, P_BOX)

# -----------------------
#   ENCRYPT / DECRYPT
# -----------------------
def des_encrypt(plaintext_hex, key_hex):
    steps = []
    P = hex_to_bin(plaintext_hex)
    K = hex_to_bin(key_hex).zfill(64)

    steps.append("STEP 1 — Initial Permutation (IP)")
    bits = permute(P, IP)
    steps.append(f"IP Output = {bits}")

    L = bits[:32]
    R = bits[32:]

    steps.append("STEP 2 — Split into L0 and R0")
    steps.append(f"L0 = {L}")
    steps.append(f"R0 = {R}")

    round_keys = generate_round_keys(K)

    # ---------- ROUND LOOP ----------
    for i in range(16):
        steps.append("")
        steps.append(f"============= ROUND {i+1} START =============")

        # --- Feistel function breakdown ---
        steps.append(f"STEP 3.{i+1}.1 — Expand R{i}")
        ER = permute(R, EXPANSION)
        steps.append(f"E(R{i}) = {ER}")

        steps.append(f"STEP 3.{i+1}.2 — XOR with K{i+1}")
        XOR_out = xor(ER, round_keys[i])
        steps.append(f"E(R{i}) XOR K{i+1} = {XOR_out}")

        steps.append(f"STEP 3.{i+1}.3 — S-Boxes")
        S_out = sbox_substitution(XOR_out)
        steps.append(f"S-box output = {S_out}")

        steps.append(f"STEP 3.{i+1}.4 — Straight P-Box")
        f_out = permute(S_out, P_BOX)
        steps.append(f"f(R{i}, K{i+1}) = {f_out}")

        # --- MIXER ---
        steps.append(f"STEP 4 — Mixer: L{i} XOR f(R{i})")
        new_R = xor(L, f_out)
        steps.append(f"L{i} XOR f = {new_R}")

        # --- SWAPPER ---
        steps.append(f"STEP 5 — Swapper (Feistel swap):")
        steps.append(f"L{i+1} = R{i}")
        steps.append(f"R{i+1} = {new_R}")

        # Prepare next round
        L, R = R, new_R

    # ---------- Final Permutation ----------
    final = permute(R + L, FP)
    steps.append("")
    steps.append("STEP 6 — Final Permutation (FP)")
    steps.append(f"Ciphertext bits = {R+L}")
    steps.append(f"Ciphertext (hex) = {bin_to_hex(final)}")

    return bin_to_hex(final), steps

def des_decrypt(cipher_hex, key_hex):
    P = hex_to_bin(cipher_hex)
    K = hex_to_bin(key_hex).zfill(64)

    bits = permute(P, IP)
    L, R = bits[:32], bits[32:]

    round_keys = generate_round_keys(K)
    round_keys.reverse()  # use reversed keys

    for i in range(16):
        f_out = feistel(R, round_keys[i])
        L, R = R, xor(L, f_out)

    final = permute(R + L, FP)
    return bin_to_hex(final)
