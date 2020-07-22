import tkinter as tk

HEIGHT = 620
WIDTH  = 1250
root = tk.Tk()

canvas = tk.Canvas(root, height= HEIGHT, width= WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = "#263D42", bd = 5) #hex teal blue
frame.place(relx = 0.5, rely= 0.01, relwidth= 1, relheight= 0.97, anchor = 'n')

label = tk.Label(frame, text = '"Deployment lablels go here"', font = ('Courier', 15))
label.place(relwidth= 0.25, relheight= 0.95)

TitleCard = tk.Label(frame, text = "Zombies or Flu", font = ('Courier', 18))
TitleCard.place(relx = 0.5, rely = 0.001, relwidth = 0.49, relheight  = 0.1, anchor = 'n')

Turn = tk.Label(frame, text = 'Turn: ', font = ('Courier', 12))
Turn.place(relx = 0.75, rely = 0.001, relwidth = 0.1, relheight = 0.05)

Score = tk.Label(frame, text = 'Score: ', font = ('Courier', 12))
Score.place(relx = 0.86, rely = 0.001, relwidth = 0.1, relheight = 0.05)

root.mainloop()
