import tkinter as tk

HEIGHT = 620
WIDTH  = 1250
root = tk.Tk()

canvas = tk.Canvas(root, height= HEIGHT, width= WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = "#263D42", bd = 5) #hex teal blue
frame.place(relx = 0.5, rely= 0.01, relwidth= 1, relheight= 0.97, anchor = 'n')

TitleCard = tk.Label(frame, text = "Zombies or Flu", font = ('Courier', 18))
TitleCard.place(relx = 0.5, rely = 0.001, relwidth = 0.49, relheight  = 0.1, anchor = 'n') #header with game title

Turn = tk.Label(frame, text = 'Turn: ', font = ('Courier', 12))
Turn.place(relx = 0.75, rely = 0.001, relwidth = 0.1, relheight = 0.05) #Label for turn counter

Score = tk.Label(frame, text = 'Score: ', font = ('Courier', 12))
Score.place(relx = 0.853, rely = 0.001, relwidth = 0.1, relheight = 0.05) #Label for total score

Fear = tk.Label(frame, text = 'Fear: ', font = ('Courier', 12))
Fear.place(relx =0.75, rely = 0.055, relwidth = 0.204, relheight = 0.05) #Label for fear counter

CityFrame = tk.Frame(root, bg = 'gray', bd = 5)
CityFrame.place(relx = 0.255, rely = 0.13, relwidth = 0.725, relheight = 0.83) #Frame to hold all 9 City labels

### The 9 Neighborhoods ###
NWest = tk.Label(CityFrame, text = 'hi', bd = 5)
NWest.place(relwidth = 0.33, relheight = 0.33)

North = tk.Label(CityFrame, text = 'hi', bd = 5)
North.place(relx = 0.335, relwidth = 0.33, relheight = 0.33)

NEast = tk.Label(CityFrame, text = 'hi', bd = 5)
NEast.place(relx = 0.669, relwidth = 0.33, relheight = 0.33)

West = tk.Label(CityFrame, text = 'hi', bd = 5)
West.place(rely = 0.335, relwidth =  0.33, relheight = 0.33)

Center = tk.Label(CityFrame, text = 'hi', bd = 5)
Center.place(relx = 0.335, rely = 0.335, relwidth = 0.33, relheight = 0.33)

East = tk.Label(CityFrame, text = 'hi', bd = 5)
East.place(relx = 0.669, rely = 0.335, relwidth = 0.33, relheight = 0.33)

SWest = tk.Label(CityFrame, text = 'hi', bd = 5)
SWest.place(rely = 0.67, relwidth = 0.33, relheight = 0.33)

South = tk.Label(CityFrame, text = 'hi', bd = 5)
South.place(relx = 0.335, rely = 0.67, relwidth = 0.33, relheight = 0.33)

SEast = tk.Label(CityFrame, text = 'hi', bd = 5)
SEast.place(relx = 0.669, rely = 0.67, relwidth = 0.33, relheight = 0.33)

DeployFrame = tk.Label(frame, bg = 'gray', bd = 5)
DeployFrame.place(relwidth= 0.25, relheight= 0.99) #frame to hold the 25 Deployment buttons

###The 25 Buttons ###
NoDeploy = tk.Button(DeployFrame, text = "No Depoloyment", font = ('Courier', 7))
NoDeploy.place(relwidth = 1)

QuarantineOpen = tk.Button(DeployFrame, text = "Quarantine Open", font = ('Courier', 7))
QuarantineOpen.place(rely = 0.04, relwidth = 1)

QuarantineFenced = tk.Button(DeployFrame, text = "Quarantine Fenced", font = ('Courier', 7))
QuarantineFenced.place(rely = 0.08, relwidth = 1)

BiteCenterDisinfect = tk.Button(DeployFrame, text = "Bite Center Disinfect", font = ('Courier', 7))
BiteCenterDisinfect.place(rely = 0.12, relwidth = 1)

BiteCenterAmputate = tk.Button(DeployFrame, text = "Bite Center Amputate", font = ('Courier', 7))
BiteCenterAmputate.place(rely = 0.16, relwidth = 1)

ZCureFDA = tk.Button(DeployFrame, text = "Z Cure (FDA)", font = ('Courier', 7))
ZCureFDA.place(rely = 0.2, relwidth = 1)

ZCureEXP = tk.Button(DeployFrame, text = "Z Cure (EXP)", font = ('Courier', 7))
ZCureEXP.place(rely = 0.24, relwidth = 1)

FluVaccOpt = tk.Button(DeployFrame, text = "Flu Vaccine (Optional)", font = ('Courier', 7))
FluVaccOpt.place(rely = 0.28, relwidth = 1)

FluVaccMan = tk.Button(DeployFrame, text = "Flu Vaccine (Mandatory)", font = ('Courier', 7))
FluVaccMan.place(rely = 0.32, relwidth = 1)

KilnOVersight = tk.Button(DeployFrame, text = "Kiln (Oversight)", font = ('Courier', 7))
KilnOVersight.place(rely = 0.36, relwidth = 1)

KilnNoQ = tk.Button(DeployFrame, text = "Kiln (No Questions)", font = ('Courier', 7))
KilnNoQ.place(rely = 0.4, relwidth = 1)

BroadcastDontPanic = tk.Button(DeployFrame, text = "Broadcast Dont Panic", font = ('Courier', 7))
BroadcastDontPanic.place(rely = 0.44, relwidth = 1)



root.mainloop()