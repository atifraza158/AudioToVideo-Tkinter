import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
import customtkinter as ctk
# from ttkbootstrap.dialogs import
from tkinter import filedialog

def select_audio():
    global audio_file
    audio_file = filedialog.askopenfilename(initialdir=".", title="Select Audio File", filetypes=(("all files", "*.*"), ("mp3 files", "*.mp3"), ("wav files", "*.wav"), ("opus files", "*.opus")))
    print("Selected Audio File: ", audio_file)
    if audio_file:
        audio_field.delete(0, tk.END)
        audio_field.insert(tk.END, audio_file)

def select_images():
    image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.png")])
    print("Selected Image Files:", image_paths)
    
    if image_paths:
        images_field.delete(0, tk.END)
        images_field.insert(tk.END, "\n".join(image_paths))

# Main Window
window = ttk.Window(themename='solar')
window.title("Audio to Video")
window.iconbitmap("images/favicon/favicon.ico")
window.geometry('1100x700')
window.minsize(900, 600)
window.configure(bg='#C2DEDC')

# Title Here.....
title_label = ttk.Label(window, text="Audio To Video", background='#C2DEDC', foreground='#002b36')
title_label.config(font=('Arial', 25, 'bold'))
title_label.place(rely=0.1, relx=0.5, anchor='center')

# Subtitle.....
subtitle = ttk.Label(window, text='Convert Audio Files into Video With the Combinations of Images Easily', background='#C2DEDC', foreground='#002b36')
subtitle.place(rely=0.15, relx=0.5, anchor='center')

main_frame = ttk.Frame(window)
main_frame.place(relx=0.5, rely = 0.5, relheight=0.6, relwidth=0.8, anchor='center')

# Grid Configration
main_frame.columnconfigure((0,2), weight=1)
main_frame.columnconfigure(1, weight=10)
main_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1, uniform='a')

# Widgets

# 1. audio input
audio_field_text = ttk.StringVar()
images_field_text = ttk.StringVar()

audio_field = ttk.Entry(main_frame, textvariable=audio_field_text)
images_field = ttk.Entry(main_frame, textvariable=images_field_text)

# 2. labels
audio_field_label = ttk.Label(main_frame, text='Select Audio File')
images_field_label = ttk.Label(main_frame, text='Select Image Files')

# 3. select buttons
audio_select_button = ttk.Button(main_frame, text='...', command=select_audio)
images_select_button = ttk.Button(main_frame, text='...', command=select_images)

# Layout
audio_field_label.grid(row=1, column = 0, sticky='we', padx=50)
images_field_label.grid(row=2, column = 0, sticky='we', padx=50)

audio_field.grid(row=1, column = 1, sticky='we')
images_field.grid(row=2, column = 1, sticky='we')

audio_select_button.grid(row=1, column = 2, sticky='w')
images_select_button.grid(row=2, column = 2, sticky='w')

# Select images
convert_button = ttk.Button(main_frame, text='Convert Audio', width=20, command=select_audio)
convert_button.grid(row=4, column = 1, sticky='e')


window.mainloop()