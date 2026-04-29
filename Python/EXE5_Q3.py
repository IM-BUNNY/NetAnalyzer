import tkinter as tk
import math

def on_click(event):
    print("Clicked at:", event.x, event.y)

win = tk.Tk()
win.title("Indian Flag Colors")
canvas = tk.Canvas(win, width=400, height=400, bg='lightblue')
canvas.pack()


canvas.create_rectangle(50, 100, 200, 160, fill='orange', outline='')  # Saffron
canvas.create_rectangle(50, 160, 200, 220, fill='white', outline='')  # White
canvas.create_rectangle(50, 220, 200, 280, fill='green', outline='')  # Green


chakra_center_x = 125  
chakra_center_y = 190 
chakra_radius = 20


canvas.create_oval(chakra_center_x - chakra_radius, chakra_center_y - chakra_radius,
                chakra_center_x + chakra_radius, chakra_center_y + chakra_radius, outline="navy", width=2)


for i in range(24):
    angle = i * (360 / 24)  # 24 spokes at equal intervals
    x_end = chakra_center_x + chakra_radius * math.cos(math.radians(angle))
    y_end = chakra_center_y + chakra_radius * math.sin(math.radians(angle))
    canvas.create_line(chakra_center_x, chakra_center_y, x_end, y_end, fill="navy", width=1)

canvas.bind("<Button-1>", on_click)

win.mainloop()
