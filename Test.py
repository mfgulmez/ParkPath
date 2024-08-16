import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.configure("RoundedFrame.TFrame", borderwidth=5, relief="ridge", corner=10)

rounded_frame = ttk.Frame(root, style="RoundedFrame.TFrame")
rounded_frame.pack(padx=20, pady=20)

label = tk.Label(rounded_frame, text="Bu bir yuvarlatılmış çerçeve!")
label.pack()

root.mainloop()
