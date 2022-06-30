import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

app = tk.Tk()
app.minsize(500,250)

serial_number_label = ttk.Label(app, text="Serial Number")
serial_number_label.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)

serial_number_entry = ttk.Entry(app)
serial_number_entry.grid(column=1, row=0, sticky=tk.E, padx=10, pady=10)


# def task(label):
#     def run():
#         global i

#         value = input("")
#         label.config(text=value)
#         label.after(1000, run)
#     run()

# task(l)

app.mainloop()