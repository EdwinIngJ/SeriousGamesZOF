import tkinter as tk
from tkinter import font

HEIGHT = 620
WIDTH  = 1250
root = tk.Tk()

canvas = tk.Canvas(root, height= HEIGHT, width= WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = "#263D42", bd = 5) #hex teal blue
frame.place(relx = 0.5, rely= 0.01, relwidth= 1, relheight= 0.97, anchor = 'n')

label = tk.Label(frame, text = '"Deployment lablels go here"', font = ('Courier', 15))
label.place(relwidth= 0.33, relheight= 0.8)

root.mainloop()
