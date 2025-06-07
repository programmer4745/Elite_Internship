import tkinter as tk
from tkinter import filedialog, messagebox
from aes_encryptor import encrypt_file, decrypt_file

def choose_file():
    filepath.set(filedialog.askopenfilename())

def encrypt_action():
    if not filepath.get() or not password.get():
        messagebox.showwarning("Input Required", "File and password are required.")
        return
    try:
        encrypt_file(filepath.get(), password.get())
        messagebox.showinfo("Success", "File encrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_action():
    if not filepath.get() or not password.get():
        messagebox.showwarning("Input Required", "File and password are required.")
        return
    try:
        decrypt_file(filepath.get(), password.get())
        messagebox.showinfo("Success", "File decrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("AES-256 File Encryptor")
app.geometry("400x200")

filepath = tk.StringVar()
password = tk.StringVar()

tk.Label(app, text="File Path").pack()
tk.Entry(app, textvariable=filepath, width=50).pack()
tk.Button(app, text="Browse", command=choose_file).pack()

tk.Label(app, text="Password").pack()
tk.Entry(app, textvariable=password, show='*', width=50).pack()

tk.Button(app, text="Encrypt", command=encrypt_action, bg="lightblue").pack(pady=5)
tk.Button(app, text="Decrypt", command=decrypt_action, bg="lightgreen").pack()

app.mainloop()
