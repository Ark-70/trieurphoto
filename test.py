import tkinter as tk

root = tk.Tk()

img = tk.PhotoImage(file="test.png")  # reference PhotoImage in local variable
button = tk.Button(root, image=img)
button.image = img  # store a reference to the image as an attribute of the widget
button.grid()

tk.mainloop()
