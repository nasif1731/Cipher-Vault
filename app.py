import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

from diffie_hellman import compute_diffie_hellman
from crypto import (
    caesar_cipher,
    vigenere_cipher,
    playfair_cipher,
    format_playfair_matrix,
    hill_cipher,
    format_matrix,
)
from aes_module import aes_encrypt_verbose, aes_decrypt_verbose
from des_module import des_encrypt, des_decrypt


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Cryptography Toolkit")
        self.root.geometry("920x700")
        self.setup_widgets()

    # -------------------------------------------------
    #                Setup Tabs
    # -------------------------------------------------
    def setup_widgets(self):
        notebook = tb.Notebook(self.root, bootstyle="primary")
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.dh_tab = tb.Frame(notebook)
        self.caesar_tab = tb.Frame(notebook)
        self.vigenere_tab = tb.Frame(notebook)
        self.playfair_tab = tb.Frame(notebook)
        self.hill_tab = tb.Frame(notebook)
        self.aes_tab = tb.Frame(notebook)
        self.des_tab = tb.Frame(notebook)

        notebook.add(self.dh_tab, text='Diffie-Hellman')
        notebook.add(self.caesar_tab, text='Caesar Cipher')
        notebook.add(self.vigenere_tab, text='Vigenère Cipher')
        notebook.add(self.playfair_tab, text='Playfair Cipher')
        notebook.add(self.hill_tab, text='Hill Cipher')
        notebook.add(self.aes_tab, text='AES-128')
        notebook.add(self.des_tab, text='DES-64')

        # Build tabs
        self.build_aes_tab()
        self.build_des_tab()
        self.build_diffie_hellman_tab()

        self.build_tab_common(self.caesar_tab, 'Caesar', 'Shift Value:', self.run_caesar)
        self.build_tab_common(self.vigenere_tab, 'Vigenère', 'Keyword:', self.run_vigenere)
        self.build_tab_common(self.playfair_tab, 'Playfair', 'Key:', self.run_playfair)
        self.build_tab_common(self.hill_tab, 'Hill', 'Key Matrix (4 values):', self.run_hill)

    # -------------------------------------------------
    #       Common Builder for Classical Ciphers
    # -------------------------------------------------
    def build_tab_common(self, frame, label, extra_field, run_func):
        tb.Label(frame, text=f"🔒 {label} Cipher", font=('Helvetica', 18, 'bold')).pack(pady=(20, 10))

        frame.plaintext = tk.StringVar()
        frame.keyfield = tk.StringVar()

        tb.Label(frame, text="Plaintext / Ciphertext:").pack(anchor='w', padx=10)
        tb.Entry(frame, textvariable=frame.plaintext, width=80, font=('Consolas', 11)).pack(padx=10, pady=5)

        tb.Label(frame, text=extra_field).pack(anchor='w', padx=10)
        tb.Entry(frame, textvariable=frame.keyfield, width=40, font=('Consolas', 11)).pack(padx=10, pady=5)

        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=15)

        tb.Button(btn_frame, text="🔐 Encrypt with Animation", bootstyle="success",
                  command=lambda: run_func(frame, encrypt=True)).pack(side='left', padx=10)

        tb.Button(btn_frame, text="🔓 Decrypt with Animation", bootstyle="warning",
                  command=lambda: run_func(frame, encrypt=False)).pack(side='left', padx=10)

        tb.Label(frame, text="Output:").pack(anchor='w', padx=10)
        frame.output_box = ScrolledText(
            frame, height=20, width=110, bg='black', fg='lime',
            font=('Courier New', 12), wrap='word'
        )
        frame.output_box.pack(padx=10, pady=10, fill='both', expand=True)
        frame.output_box.config(state='disabled')

    # -------------------------------------------------
    #                DES Tab
    # -------------------------------------------------
    def build_des_tab(self):
        frame = self.des_tab
        tb.Label(frame, text="🧱 DES Encryption/Decryption (64-bit)",
                 font=('Helvetica', 18, 'bold')).pack(pady=(20, 10))

        frame.plaintext = tk.StringVar()
        frame.keyfield = tk.StringVar()

        tb.Label(frame, text="Plaintext / Ciphertext (16 hex chars / 64-bit):").pack(anchor='w', padx=10)
        tb.Entry(frame, textvariable=frame.plaintext, width=80,
                 font=('Consolas', 11)).pack(padx=10, pady=5)

        tb.Label(frame, text="DES Key (16 hex chars / 64-bit):").pack(anchor='w', padx=10)
        tb.Entry(frame, textvariable=frame.keyfield, width=80,
                 font=('Consolas', 11)).pack(padx=10, pady=5)

        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=15)

        tb.Button(btn_frame, text="🔐 Encrypt", bootstyle="success",
                  command=lambda: self.run_des_verbose(frame, True)).pack(side='left', padx=10)
        tb.Button(btn_frame, text="🔓 Decrypt", bootstyle="warning",
                  command=lambda: self.run_des_verbose(frame, False)).pack(side='left', padx=10)

        tb.Label(frame, text="Output:").pack(anchor='w', padx=10)
        frame.output_box = ScrolledText(
            frame, height=20, width=110, bg='black', fg='yellow',
            font=('Courier New', 12), wrap='word'
        )
        frame.output_box.pack(padx=10, pady=10, fill='both', expand=True)
        frame.output_box.config(state='disabled')

    def run_des_verbose(self, frame, encrypt=True):
        try:
            text_hex = frame.plaintext.get().strip().replace(" ", "")
            key_hex = frame.keyfield.get().strip().replace(" ", "")

            if len(text_hex) != 16:
                raise ValueError("DES requires 16 hex characters (64 bits).")
            if len(key_hex) != 16:
                raise ValueError("DES key must also be 16 hex characters.")

            if encrypt:
                cipher, steps = des_encrypt(text_hex, key_hex)

                def on_done():
                    frame.output_box.config(state='normal')
                    frame.output_box.insert('end', f"\n✅ Ciphertext: {cipher}\n")
                    frame.output_box.config(state='disabled')

                self.animate_text(frame.output_box, steps, on_done, "encrypt")
            else:
                plaintext = des_decrypt(text_hex, key_hex)

                frame.output_box.config(state='normal')
                frame.output_box.delete('1.0', 'end')
                frame.output_box.insert('end', f"🔓 Plaintext: {plaintext}\n")
                frame.output_box.config(state='disabled')

        except Exception as e:
            messagebox.showerror("DES Error", str(e))

    # -------------------------------------------------
    #           Animation Handler
    # -------------------------------------------------
    def animate_text(self, text_widget, steps, final_callback, mode):
        text_widget.config(state='normal')
        text_widget.delete('1.0', 'end')
        text_widget.insert('end',
            f"{'🔐' if mode=='encrypt' else '🔓'} Starting {mode.title()}ion Steps:\n\n")
        text_widget.config(state='disabled')

        def next_step(i=0):
            if i < len(steps):
                text_widget.config(state='normal')
                text_widget.insert('end', f"🧩 Step {i+1}: {steps[i]}\n\n")
                text_widget.see('end')
                text_widget.config(state='disabled')
                text_widget.after(600, next_step, i + 1)
            else:
                final_callback()

        next_step()

    # -------------------------------------------------
    #                AES Tab
    # -------------------------------------------------
    def build_aes_tab(self):
        frame = self.aes_tab
        tb.Label(frame, text="🧊 AES-128 Encryption/Decryption",
                 font=('Helvetica', 18, 'bold')).pack(pady=(20, 10))

        frame.plaintext = tk.StringVar()
        frame.keyfield = tk.StringVar()

        tb.Label(frame, text="Plaintext / Ciphertext (Hex):").pack(anchor='w', padx=10)
        tb.Entry(frame, textvariable=frame.plaintext, width=80,
                 font=('Consolas', 11)).pack(padx=10, pady=5)

        tb.Label(frame, text="AES Key (32 hex chars):").pack(anchor='w', padx=10)
        tb.Entry(frame, textvariable=frame.keyfield, width=80,
                 font=('Consolas', 11)).pack(padx=10, pady=5)

        btn_frame = tb.Frame(frame)
        btn_frame.pack(pady=15)

        tb.Button(btn_frame, text="🔐 Encrypt", bootstyle="success",
                  command=lambda: self.run_aes_verbose(frame, True)).pack(side='left', padx=10)
        tb.Button(btn_frame, text="🔓 Decrypt", bootstyle="warning",
                  command=lambda: self.run_aes_verbose(frame, False)).pack(side='left', padx=10)

        tb.Label(frame, text="Output:").pack(anchor='w', padx=10)
        frame.output_box = ScrolledText(
            frame, height=20, width=110, bg='black', fg='cyan',
            font=('Courier New', 12), wrap='word'
        )
        frame.output_box.pack(padx=10, pady=10, fill='both', expand=True)
        frame.output_box.config(state='disabled')

    def run_aes_verbose(self, frame, encrypt=True):
        try:
            key_hex = "".join(frame.keyfield.get().split())
            if len(bytes.fromhex(key_hex)) != 16:
                raise ValueError("AES key must be 16 bytes (32 hex characters).")

            text_hex = "".join(frame.plaintext.get().split())
            if len(text_hex) != 32:
                raise ValueError("AES requires exactly 32 hex characters (128-bit block).")

            if encrypt:
                result, steps = aes_encrypt_verbose(text_hex, key_hex)

                def on_done():
                    frame.output_box.config(state='normal')
                    frame.output_box.insert('end', f"\n✅ Ciphertext: {result}\n")
                    frame.output_box.config(state='disabled')

                self.animate_text(frame.output_box, steps, on_done, "encrypt")

            else:
                result, steps = aes_decrypt_verbose(text_hex, key_hex)

                def on_done():
                    frame.output_box.config(state='normal')
                    frame.output_box.insert('end', f"\n✅ Plaintext: {result}\n")
                    frame.output_box.config(state='disabled')

                self.animate_text(frame.output_box, steps, on_done, "decrypt")

        except Exception as e:
            messagebox.showerror("AES Error", str(e))

    # -------------------------------------------------
    #             Caesar Cipher
    # -------------------------------------------------
    def run_caesar(self, frame, encrypt=True):
        try:
            text = frame.plaintext.get()
            shift = int(frame.keyfield.get())
            result = ""
            steps = []

            for c in text:
                if c.isalpha():
                    out, calc = caesar_cipher(c, shift, encrypt, True)
                    result += out
                    steps.append(calc)
                else:
                    result += c
                    steps.append(f"Non-alpha '{c}' unchanged")

            def on_done():
                reverse = ""
                for c in result:
                    if c.isalpha():
                        rc, _ = caesar_cipher(c, shift, not encrypt, True)
                        reverse += rc
                    else:
                        reverse += c

                frame.output_box.config(state='normal')
                frame.output_box.insert('end',
                    f"\nFinal: {result}\nReverse: {reverse}\n")
                frame.output_box.config(state='disabled')

            self.animate_text(frame.output_box, steps, on_done,
                              "encrypt" if encrypt else "decrypt")

        except Exception as e:
            messagebox.showerror("Caesar Error", str(e))

    # -------------------------------------------------
    #             Vigenère Cipher
    # -------------------------------------------------
    def run_vigenere(self, frame, encrypt=True):
        try:
            text = frame.plaintext.get()
            key = frame.keyfield.get()

            result, steps = vigenere_cipher(text, key, encrypt, True)

            def on_done():
                reverse, _ = vigenere_cipher(result, key, not encrypt, True)

                frame.output_box.config(state='normal')
                frame.output_box.insert('end',
                    f"\nFinal: {result}\nReverse: {reverse}\n")
                frame.output_box.config(state='disabled')

            self.animate_text(frame.output_box, steps, on_done,
                              "encrypt" if encrypt else "decrypt")

        except Exception as e:
            messagebox.showerror("Vigenère Error", str(e))

    # -------------------------------------------------
    #             Playfair Cipher
    # -------------------------------------------------
    def run_playfair(self, frame, encrypt=True):
        try:
            text = frame.plaintext.get()
            key = frame.keyfield.get()

            matrix, prepared, result, steps = playfair_cipher(
                text, key, encrypt, return_steps=True)

            _, _, reverse, _ = playfair_cipher(
                result, key, not encrypt, return_steps=True)

            def on_done():
                frame.output_box.config(state='normal')
                frame.output_box.insert('end',
                    f"\nPrepared: {prepared}\nFinal: {result}\nReverse: {reverse}\n")
                frame.output_box.insert('end', format_playfair_matrix(matrix))
                frame.output_box.config(state='disabled')

            self.animate_text(frame.output_box, steps, on_done,
                              "encrypt" if encrypt else "decrypt")

        except Exception as e:
            messagebox.showerror("Playfair Error", str(e))

    # -------------------------------------------------
    #                Hill Cipher
    # -------------------------------------------------
    def run_hill(self, frame, encrypt=True):
        try:
            text = frame.plaintext.get()
            key_list = [int(k.strip()) for k in frame.keyfield.get().split(',')]

            if len(key_list) != 4:
                raise ValueError("Hill requires exactly 4 integers.")

            K, invK, result, processed, steps = hill_cipher(
                text, key_list, 2, encrypt, return_steps=True)

            _, _, reverse, _, _ = hill_cipher(
                result, key_list, 2, not encrypt, return_steps=True)

            def on_done():
                frame.output_box.config(state='normal')
                frame.output_box.insert('end',
                    f"\nProcessed: {processed}\nFinal: {result}\nReverse: {reverse}\n")
                frame.output_box.insert('end', format_matrix(K, 'K'))
                if invK and not encrypt:
                    frame.output_box.insert('end', format_matrix(invK, 'K^-1'))
                frame.output_box.config(state='disabled')

            self.animate_text(frame.output_box, steps, on_done,
                              "encrypt" if encrypt else "decrypt")

        except Exception as e:
            messagebox.showerror("Hill Error", str(e))

    # -------------------------------------------------
    #             Diffie–Hellman
    # -------------------------------------------------
    def build_diffie_hellman_tab(self):
        frame = self.dh_tab

        tb.Label(frame, text="🔑 Diffie–Hellman Key Exchange",
                 font=('Helvetica', 18, 'bold')).pack(pady=(20, 10))

        frame.p_var = tk.StringVar()
        frame.g_var = tk.StringVar()
        frame.a_var = tk.StringVar()
        frame.b_var = tk.StringVar()

        for label, var in [
            ("Prime p:", frame.p_var),
            ("Primitive Root g:", frame.g_var),
            ("Private key a:", frame.a_var),
            ("Private key b:", frame.b_var)
        ]:
            tb.Label(frame, text=label).pack(anchor='w', padx=10)
            tb.Entry(frame, textvariable=var,
                     width=40, font=('Consolas', 11)).pack(padx=10, pady=5)

        tb.Button(frame, text="📶 Compute Shared Key",
                  bootstyle="info",
                  command=self.run_diffie_hellman).pack(pady=15)

        tb.Label(frame, text="Output:").pack(anchor='w', padx=10)
        frame.output_box = ScrolledText(
            frame, height=20, width=110, bg='black', fg='cyan',
            font=('Courier New', 12), wrap='word'
        )
        frame.output_box.pack(padx=10, pady=10, fill='both', expand=True)
        frame.output_box.config(state='disabled')

    def run_diffie_hellman(self):
        try:
            p = int(self.dh_tab.p_var.get())
            g = int(self.dh_tab.g_var.get())
            a = int(self.dh_tab.a_var.get())
            b = int(self.dh_tab.b_var.get())

            A, B, K, steps = compute_diffie_hellman(p, g, a, b)

            def on_done():
                self.dh_tab.output_box.config(state='normal')
                self.dh_tab.output_box.insert('end',
                    f"\nA (Alice): {A}\nB (Bob): {B}\nShared Key: {K}\n")
                self.dh_tab.output_box.config(state='disabled')

            self.animate_text(self.dh_tab.output_box, steps, on_done, "exchange")

        except Exception as e:
            messagebox.showerror("DH Error", str(e))


# -------------------------------------------------
#                MAIN LOOP
# -------------------------------------------------
if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = CryptoApp(root)
    root.mainloop()
