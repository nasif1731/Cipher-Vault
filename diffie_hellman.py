from math import gcd

def is_primitive_root(g, p):
    """Check if g is a primitive root modulo p"""
    required_set = set()
    for i in range(1, p):
        required_set.add(pow(g, i, p))
    return len(required_set) == p - 1

def compute_diffie_hellman(p, g, a, b):
    steps = []

    steps.append(f"Step 1: Public Prime (p): {p}")
    steps.append(f"Step 2: Primitive Root (g): {g}")

    # Check if g is a primitive root modulo p
    if not is_primitive_root(g, p):
        steps.append(f"⚠️ Warning: {g} is not a primitive root modulo {p}. Choose a valid generator.")
        return None, None, None, steps

    steps.append(f"Step 3: Alice's Private Key (a): {a}")
    steps.append(f"Step 4: Bob's Private Key (b): {b}")

    # Step 5-6: Compute public keys
    A = pow(g, a, p)
    B = pow(g, b, p)
    steps.append(f"Step 5: Alice computes A = g^a mod p = {g}^{a} mod {p} = {A}")
    steps.append(f"Step 6: Bob computes B = g^b mod p = {g}^{b} mod {p} = {B}")

    # Step 7-8: Exchange public keys
    steps.append(f"Step 7: 🔁 Alice sends A = {A} to Bob")
    steps.append(f"Step 8: 🔁 Bob sends B = {B} to Alice")

    # Step 9-10: Compute shared secret key
    K1 = pow(B, a, p)  # Alice computes
    K2 = pow(A, b, p)  # Bob computes
    steps.append(f"Step 9: Alice computes K = B^a mod p = {B}^{a} mod {p} = {K1}")
    steps.append(f"Step 10: Bob computes K = A^b mod p = {A}^{b} mod {p} = {K2}")

    # Step 11: Final shared key confirmation
    if K1 == K2:
        shared_key = K1
        steps.append(f"Step 11: ✅ Shared Secret Key: {shared_key}")
    else:
        shared_key = None
        steps.append("Step 11: ❌ Error: Keys do not match — check inputs!")

    return A, B, shared_key, steps
