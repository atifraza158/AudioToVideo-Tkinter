import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
# from tkinter import ttk
import os
import shutil
from moviepy import editor
from threading import Thread
from tkinter.messagebox import showinfo
from proglog import ProgressBarLogger
from PIL import Image
import customtkinter as ctk


# Main window
window = ctk.CTk()
window.title("Audio to Video Converter")
window.geometry('1100x700')
window.minsize(900, 600)
window.configure(bg='#C2DEDC')
window._set_appearance_mode('light')

nav_bar = ctk.CTkFrame(window, fg_color=("#51829B", "#51829B"))
nav_bar.place(x = 0, y = 0, relwidth=1, relheight=0.1)

main_menu = ctk.CTkFrame(window)
main_menu.place(x = 0, rely = 0.1, relwidth=1, relheight=0.9)

# -------------- COMPONENTS OF NAVIGATION BAR --------------------
heading = ctk.CTkLabel(nav_bar, text="Audio To Video", font=("uber move", 22, 'bold'))
heading.pack(side='left', padx=20)

login_button = ctk.CTkButton(nav_bar, text="Login", fg_color="#EADFB4", height=50, text_color="black", hover_color="#EABBB4", font=("uber move", 18, 'bold'))
login_button.pack(side = 'right', padx = 20, )



# ---------------- Main Menu Compnents 
# Grid Configuration
main_menu.columnconfigure((0,1,2), weight=1, uniform='a')
main_menu.rowconfigure((0,1,2,3,4,5,6), weight=1, uniform='a')




window.mainloop()