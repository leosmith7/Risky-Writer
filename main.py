import tkinter as tk
import time
from tkinter import messagebox

class RiskyWriter:
    def __init__(self, window):
        self.window = window
        self.window.title("Risky Writer")

        self.text_area = tk.Text(self.window, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        self.timer_label = tk.Label(self.window, text="Time left: 5 seconds")
        self.timer_label.pack()

        self.last_keypress_time = time.time()
        self.timer = None
        self.time_limit = 6

        self.start_button = tk.Button(self.window, text="Start Typing", command=self.start_typing)
        self.start_button.pack()

        self.text_area.bind("<KeyPress>", self.key_pressed)

    def start_typing(self):
        self.text_area.focus()
        self.last_keypress_time = time.time()
        if self.timer is None:
            self.start_timer()

    def key_pressed(self, event):
        self.last_keypress_time = time.time()
        if self.timer is None:
            self.start_timer()

    def start_timer(self):
        self.update_timer()
        self.window.after(1000, self.check_time)

    def check_time(self):
        self.timer = time.time()
        if self.timer - self.last_keypress_time >= self.time_limit:
            self.clear_text()
        else:
            self.timer = self.window.after(1000, self.check_time)

    def update_timer(self):
        remaining_time = self.time_limit - (time.time() - self.last_keypress_time)
        if remaining_time > 0:
            self.timer_label.config(text=f"Time left: {int(remaining_time)} seconds")
            self.window.after(1000, self.update_timer)
        else:
            self.clear_text()

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        messagebox.showinfo("Magic", "Your text has vanished! Be quicker next time.")
        self.stop_timer()

    def stop_timer(self):
        if self.timer:
            self.window.after_cancel(self.timer)
            self.timer = None

if __name__ == "__main__":
    root = tk.Tk()
    app = RiskyWriter(root)
    root.mainloop()
