# import the standard GUI library
import tkinter as tk
# create a window
window = tk.Tk()
# initialise window's size
main_frame = tk.Frame(width=640, height=360, master=window, bg="red")
main_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

greeting = tk.Label(text="Hello, Tkinter", master=main_frame)
greeting.pack()
window.mainloop()