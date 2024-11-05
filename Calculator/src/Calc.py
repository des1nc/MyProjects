import tkinter as tk
import math
from tkinter import ttk

def add_to_display(number):
    display.insert(tk.END, number)

def clear_display():
    display.delete(0, tk.END)

def calculate():
    try:
        expression = display.get()
        if "sin" in expression:
            angle = float(expression.split("sin")[1])
            result = str(math.sin(angle))
        elif "cos" in expression:
            angle = float(expression.split("cos")[1])
            result = str(math.cos(angle))
        elif "tan" in expression:
            angle = float(expression.split("tan")[1])
            result = str(math.tan(angle))
        else:
            result = str(eval(expression))
        clear_display()
        add_to_display(result)
    except Exception:
        clear_display()
        add_to_display("Ошибка")

root = tk.Tk()
root.title("Calc. by AmUkSpace")
root.configure(background='black')

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

display = ttk.Entry(mainframe, justify="right")
display.grid(column=0, row=0, columnspan=4, padx=5, pady=5, sticky="NSEW")

button_1 = ttk.Button(mainframe, text="1", command=lambda: add_to_display("1"))
button_1.grid(column=0, row=1, padx=5, pady=5)

button_2 = ttk.Button(mainframe, text="2", command=lambda: add_to_display("2"))
button_2.grid(column=1, row=1, padx=5, pady=5)

button_3 = ttk.Button(mainframe, text="3", command=lambda: add_to_display("3"))
button_3.grid(column=2, row=1, padx=5, pady=5)

button_add = ttk.Button(mainframe, text="+", command=lambda: add_to_display("+"))
button_add.grid(column=3, row=1, padx=5, pady=5)

button_4 = ttk.Button(mainframe, text="4", command=lambda: add_to_display("4"))
button_4.grid(column=0, row=2, padx=5, pady=5)

button_5 = ttk.Button(mainframe, text="5", command=lambda: add_to_display("5"))
button_5.grid(column=1, row=2, padx=5, pady=5)

button_6 = ttk.Button(mainframe, text="6", command=lambda: add_to_display("6"))
button_6.grid(column=2, row=2, padx=5, pady=5)

button_subtract = ttk.Button(mainframe, text="-", command=lambda: add_to_display("-"))
button_subtract.grid(column=3, row=2, padx=5, pady=5)

button_7 = ttk.Button(mainframe, text="7", command=lambda: add_to_display("7"))
button_7.grid(column=0, row=3, padx=5, pady=5)

button_8 = ttk.Button(mainframe, text="8", command=lambda: add_to_display("8"))
button_8.grid(column=1, row=3, padx=5, pady=5)

button_9 = ttk.Button(mainframe, text="9", command=lambda: add_to_display("9"))
button_9.grid(column=2, row=3, padx=5, pady=5)

button_multiply = ttk.Button(mainframe, text="*", command=lambda: add_to_display("*"))
button_multiply.grid(column=3, row=3, padx=5, pady=5)

button_clear = ttk.Button(mainframe, text="C", command=clear_display)
button_clear.grid(column=0, row=4, padx=5, pady=5)

button_0 = ttk.Button(mainframe, text="0", command=lambda: add_to_display("0"))
button_0.grid(column=1, row=4, padx=5, pady=5)

button_decimal = ttk.Button(mainframe, text=".", command=lambda: add_to_display("."))
button_decimal.grid(column=2, row=4, padx=5, pady=5)

button_divide = ttk.Button(mainframe, text="/", command=lambda: add_to_display("/"))
button_divide.grid(column=3, row=4, padx=5, pady=5)

button_equals = ttk.Button(mainframe, text="=", command=calculate)
button_equals.grid(column=0, row=5, columnspan=4, padx=5, pady=5, sticky="NSEW")

for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

root.mainloop()