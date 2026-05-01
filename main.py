from tkinter import *
from tkinter import ttk, PhotoImage
import os

top = Tk()

top.geometry("500x425")

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
top.iconbitmap("RGB.ico")

top.title("Συνδυασμός βασικών χρωμάτων")

top.grid_columnconfigure(0, weight=1)
top.grid_columnconfigure(1, weight=1)



# ---------------------------------RED
# Label
ttk.Label(top, text="Κόκκινο").grid(column=0, row=0, columnspan=1, sticky="e")

# Slider frame
red_frame = Frame(top)
red_frame.grid(column=1, row=0, padx=5, sticky="w")

# Slider value
red_value = IntVar()

# Slider
horizontal = Scale(red_frame, from_=0, to=255, orient=HORIZONTAL, troughcolor="red", variable=red_value, showvalue=False)
horizontal.pack(side="left")

# Entry field
entry = Entry(red_frame, textvariable=red_value, width=5)
entry.pack(side="left", padx=5)



# ---------------------------------GREEN
# Label
ttk.Label(top, text="Πράσινο").grid(column=0, row=1, columnspan=1, sticky="e")

# Slider frame
green_frame = Frame(top)
green_frame.grid(column=1, row=1, padx=5, sticky="w")

# Slider value
green_value = IntVar()

# Slider
horizontal = Scale(green_frame, from_=0, to=255, orient=HORIZONTAL, troughcolor="green", variable=green_value, showvalue=False)
horizontal.pack(side="left")

# Entry field
entry = Entry(green_frame, textvariable=green_value, width=5)
entry.pack(side="left", padx=5)



# ---------------------------------BLUE
# Label
ttk.Label(top, text="Μπλε").grid(column=0, row=2, columnspan=1, sticky="e")

# Slider frame
blue_frame = Frame(top)
blue_frame.grid(column=1, row=2, padx=5, sticky="w")

# Slider value
blue_value = IntVar()

# Slider
horizontal = Scale(blue_frame, from_=0, to=255, orient=HORIZONTAL, troughcolor="blue", variable=blue_value, showvalue=False)
horizontal.pack(side="left")

# Entry field
entry = Entry(blue_frame, textvariable=blue_value, width=5)
entry.pack(side="left", padx=5)

red = red_value.get()
green = green_value.get()
blue = blue_value.get()


# ---------------------------------BOXES
# Color box frame
box_frame = ttk.Frame(top)
box_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")

# Dynamic resizing
top.rowconfigure(5, weight=1)       # Allows vertical expansion
top.columnconfigure(0, weight=1)    # Equal resizing for columns
top.columnconfigure(1, weight=1)

# Target color import
from utils import color1
tr, tg, tb = color1.red, color1.green, color1.blue

# Convert to hex format
target_hex_color = f"#{tr:02x}{tg:02x}{tb:02x}"  
input_hex_color = f"#{red:02x}{green:02x}{blue:02x}"

# Two canvases (color boxes)
right_canvas = Canvas(box_frame, bg=input_hex_color)
right_canvas.grid(row=0, column=1, sticky="nsew")

left_canvas = Canvas(box_frame, bg=target_hex_color)
left_canvas.grid(row=0, column=0, sticky="nsew")

# Canvas resize rule
box_frame.columnconfigure(0, weight=1)
box_frame.columnconfigure(1, weight=1)
box_frame.rowconfigure(0, weight=1)



# ---------------------------------CHEATBOX
def Cheat():
    global right_canvas
    red = red_value.get()
    green = green_value.get()
    blue = blue_value.get()
    input_hex_color = f"#{red:02x}{green:02x}{blue:02x}"
    right_canvas.config(bg=input_hex_color)

# Cheat button
cheat_icon = PhotoImage(file="cheat.png")
ttk.Button(top, text="Cheat", image=cheat_icon, compound="right", command=Cheat).grid(column=0, row=3, padx=5, columnspan=1, sticky="e")



# ---------------------------------SUBMIT
attempt_var = IntVar(value=1)
match_var = StringVar(value="0")
best_match = 0
best_red, best_green, best_blue = 0, 0, 0

# Submit Label (placeholder)

# Submit button
tick_icon = PhotoImage(file="tick.png")
submit_button = ttk.Button(top, text="Δοκιμή", image=tick_icon, compound="right", command=lambda: Submit())
submit_button.grid(column=0, row=4, padx=5, columnspan=1, sticky="e")

submit_label = ttk.Label(top, text=f"Προσπάθεια 0/5, καλύτερο σκορ 0% ({red},{green},{blue})")
submit_label.grid(column=1, row=4, padx=5, columnspan=1, sticky="w")

match_img = None
gameover_img = None

def Submit():
    red = red_value.get()
    green = green_value.get()
    blue = blue_value.get()
    from utils import calculate

    attempt = attempt_var.get()

    match = calculate(red, green, blue, tr, tg ,tb)

    global best_match, best_red, best_green, best_blue
    print(f"Attempt {attempt}: Match = {match}, Best Match = {best_match}")
    if match > best_match:
        best_match = match
        best_red, best_green, best_blue = red, green, blue
        match_var.set(f"{best_match}%")

        print(f"New Best Match Found! {best_match}% at ({best_red}, {best_green}, {best_blue})")


    global right_canvas
    input_hex_color = f"#{red:02x}{green:02x}{blue:02x}"
    right_canvas.config(bg=input_hex_color)

    attempt_var.set(attempt_var.get() + 1)

    submit_label.config(text=f"Προσπάθεια {attempt}/5, καλύτερο σκορ {best_match}% ({best_red}, {best_green}, {best_blue})")

    global match_img, gameover_img

    # Stop game at >=90%
    if match >= 90:
        # Disable Submit
        submit_button.config(state="disabled")
        
        # Bullseye display
        match_img = PhotoImage(file="matchy.png")
        match_label = Label(right_canvas, image=match_img)
        match_label.image = match_img  # Prevent garbage collection
        match_label.place(relx=0.5, rely=0.5, anchor="center")

    # If 5th attempt WITHOUT >=90% score
    elif attempt == 5:
        submit_button.config(state="disabled")

        # Display Nedry
        gameover_img = PhotoImage(file="gameover.png")
        gameover_label = Label(right_canvas, image=gameover_img)
        gameover_label.image = gameover_img
        gameover_label.place(relx=0.5, rely=0.5, anchor="center")



# ---------------------------------QUIT
# Quit button
ttk.Button(top, text="Quit", command=top.destroy).grid(column=1, row=6, sticky="e", padx=15, pady=5)

top.mainloop()