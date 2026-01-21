# 🔐 Cipher-Vault: The Cryptography Playground

**From Caesar to AES: Experience the evolution of secret messaging.**  
*A complete Python suite for encrypting, decrypting, and exchanging keys using classic and modern algorithms.*

---

## 🧐 What is this?

This isn't just a script; it's a time machine for Information Security.

**Cipher-Vault** brings together the history of cryptography into a single, interactive application. Whether you want to shift letters like a Roman General (Caesar Cipher), swap bits like a 70s IBM engineer (DES), or secure data like a modern bank (AES), this project has you covered.

It features a **Gradio Web Interface** (`app.py`) that lets you visualize inputs, keys, and ciphertext outputs in real-time.

---

## ⚔️ Features Arsenal

We have implemented a wide range of cryptographic techniques across different modules:

### 🏛️ Classical Ciphers (`crypto.py`)

The OG methods. Simple, historical, and fun to break.

* **Caesar Cipher:** The classic shift.
* **Vigenère Cipher:** The polyalphabetic upgrade.
* **Playfair Cipher:** The diagrammatic digram approach.
* **Rail Fence & Row Transposition:** Scrambling positions, not just values.

### 🛡️ Modern Encryption

The heavy hitters used in real-world security.

* **AES (Advanced Encryption Standard):** The gold standard of symmetric encryption (`aes_module.py`).
* **DES (Data Encryption Standard):** The ancestor of modern block ciphers (`des_module.py`).

### 🤝 Key Exchange

* **Diffie-Hellman:** A secure method for two parties to agree on a secret key over an insecure channel (`diffie_hellman.py`).

---

## 🚀 Quick Start

**1. Clone the Vault**

```bash
git clone https://github.com/your-username/cipher-vault.git
cd cipher-vault
```

**2. Install Dependencies**

```bash
# We need pycryptodome for the modern math and Gradio for the UI
pip install pycryptodome gradio
```

**3. Run the Interface**  
Fire up the web app to interact with all algorithms in one place.

```bash
python app.py
```

👉 **Open your browser at:** `http://127.0.0.1:7860`

---

## 🧠 Under the Hood

Here is how the project is structured:

| File | Purpose |
| --- | --- |
| **`app.py`** | The **Gradio** frontend. It acts as the central hub, routing user inputs to the correct algorithm module. |
| **`crypto.py`** | Contains pure Python implementations of **Classical Ciphers** (Caesar, Playfair, Rail Fence, etc.). |
| **`aes_module.py`** | Handles **AES-128** encryption and decryption, managing padding and block modes. |
| **`des_module.py`** | Implements the **DES** algorithm, demonstrating the Feistel network structure. |
| **`diffie_hellman.py`** | Simulates the **DH Key Exchange**, generating public/private keys and computing the shared secret. |

---

## 📸 Example Usage

**Scenario: Diffie-Hellman Key Exchange**

1. **Alice** generates a Private Key and Public Key.
2. **Bob** generates a Private Key and Public Key.
3. They swap Public Keys.
4. The app calculates the **Shared Secret** ensuring secure communication.

**Scenario: AES Encryption**

* **Input:** "Secret Message"
* **Key:** "MySuperSecretKey"
* **Output (Hex):** `A3 F2 91 ...`

---

## 📜 Credits

* Developed by **[Your Name]**
* **Tech Stack:** Python, Gradio, PyCryptodome

---

**🔒 Keep your secrets safe.**  
*Star this repo if you learned something new about crypto!*
