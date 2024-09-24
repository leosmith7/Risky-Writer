import tkinter as tk
import time
from tkinter import messagebox

class RiskyWriter:
    def __init__(self, window):
        self.window = window
        self.window.title("Risky Writer")

        self.text_area = tk.Text(self.window, wrap="word", state=tk.DISABLED)
        self.text_area.pack(expand=True, fill="both")

        self.timer_label = tk.Label(self.window, text="Time left: 5 seconds")
        self.timer_label.pack()

        self.last_keypress_time = time.time()
        self.timer = None
        self.time_limit = 5
        self.text_cleared = False  # Flag to track if text has been cleared

        # Frame to hold the buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start Typing", command=self.start_typing)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.copy_button = tk.Button(button_frame, text="Copy Text", command=self.copy_text)
        self.copy_button.pack(side=tk.LEFT, padx=5)



    def start_typing(self):
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.bind("<KeyPress>", self.key_pressed)
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
            self.timer = self.window.after(1000, self.update_timer)
        else:
            self.clear_text()
            self.time_limit = 5
            if self.timer is not None:
                self.window.after_cancel(self.timer)
                self.timer = None

    def clear_text(self):
        if not self.text_cleared:  # Check if text has already been cleared
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Magic", "Your text has vanished! Be quicker next time.")
            self.text_cleared = True  # Set the flag to True
        self.stop_timer()
        self.text_area.config(state=tk.DISABLED)
        self.text_area.unbind("<KeyPress>")

    def stop_timer(self):
        if self.timer:
            self.window.after_cancel(self.timer)
            self.timer = None

    def copy_text(self):
        self.window.clipboard_clear()
        text_to_copy = self.text_area.get("1.0", tk.END)
        self.window.clipboard_append(text_to_copy)
        messagebox.showinfo("Copied", "Text copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RiskyWriter(root)
    root.mainloop()
