import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter import ttk as tkk
import os
import shutil
from moviepy import editor
from threading import Thread
from tkinter.messagebox import showinfo
from proglog import ProgressBarLogger

class MyBarLogger(ProgressBarLogger):
    def callback(self, **changes):
        for (parameter, value) in changes.items():
            print('Parameter %s is now %s' % (parameter, value))

    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100
        print(bar, attr, percentage)
        # Update progress bar value on the GUI
        progress_bar['value'] = percentage

def select_audio():
    global audio_file
    audio_file = filedialog.askopenfilename(initialdir=".", title="Select Audio File", filetypes=(("Audio files", "*.mp3;*.wav;*.opus"), ("All files", "*.*")))
    print("Selected Audio File:", audio_file)
    if audio_file:
        audio_field.delete(0, tk.END)
        audio_field.insert(tk.END, audio_file)

def select_images():
    image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.png")])
    print("Selected Image Files:", image_paths)
    if image_paths:
        images_field.delete(0, tk.END)
        images_field.insert(tk.END, "\n".join(image_paths))

def convert_audio_to_video(progress_var):
    global audio_field, images_field
    audio = audio_field.get()
    images = images_field.get()

    if audio == '' or images == '':
        showinfo("Insertion Error", "Fill all the fields")
    else:
        def _convert(progress_var, progress_bar):
            temp_dir = "temp_images"
            os.makedirs(temp_dir, exist_ok=True)
            images = images_field.get().split("\n")
            for i, img_path in enumerate(images):
                shutil.copy(img_path, os.path.join(temp_dir, f"image_{i}.png"))

            audio_clip = editor.AudioFileClip(audio_file)
            image_files = sorted(os.listdir(temp_dir))
            image_clips = [editor.ImageClip(os.path.join(temp_dir, img)).set_duration(audio_clip.duration) for img in image_files]

            video_clip = editor.concatenate_videoclips(image_clips, method="compose")
            video_clip = video_clip.set_audio(audio_clip)

            output_file = filedialog.asksaveasfilename(initialdir=".", title="Save Video As", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
            if output_file and not output_file.endswith(".mp4"):
                output_file += ".mp4"

            if output_file:
                try:
                    logger = MyBarLogger()
                    video_clip.write_videofile(output_file, codec="libx264", fps=24, logger=logger)
                    print("Video successfully created.")
                except Exception as e:
                    print("An error occurred:", e)

            shutil.rmtree(temp_dir)

            # Update progress variable
            progress_var.set(100)

        thread = Thread(target=_convert, args=(progress_var, progress_bar))
        thread.start()

# Main window
window = ttk.Window(themename='solar')
window.title("Audio to Video Converter")
window.geometry('1100x700')
window.minsize(900, 600)
window.configure(bg='#C2DEDC')

# Title
title_label = ttk.Label(window, text="Audio To Video", background='#C2DEDC', foreground='#002b36')
title_label.config(font=('Arial', 25, 'bold'))
title_label.place(rely=0.1, relx=0.5, anchor='center')

# Subtitle
subtitle = ttk.Label(window, text='Convert Audio Files into Video With the Combinations of Images Easily', background='#C2DEDC', foreground='#002b36')
subtitle.place(rely=0.15, relx=0.5, anchor='center')

main_frame = ttk.Frame(window)
main_frame.place(relx=0.5, rely=0.5, relheight=0.6, relwidth=0.8, anchor='center')

# Grid Configuration
main_frame.columnconfigure((0, 2), weight=1)
main_frame.columnconfigure(1, weight=10)
main_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')

# Widgets
audio_field_text = ttk.StringVar()
images_field_text = ttk.StringVar()
audio_field = ttk.Entry(main_frame, textvariable=audio_field_text)
images_field = ttk.Entry(main_frame, textvariable=images_field_text)
audio_field_label = ttk.Label(main_frame, text='Select Audio File')
images_field_label = ttk.Label(main_frame, text='Select Image Files')
audio_select_button = ttk.Button(main_frame, text='...', command=select_audio)
images_select_button = ttk.Button(main_frame, text='...', command=select_images)
convert_button = ttk.Button(main_frame, text='Convert And Save', width=20)
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate", variable=progress_var)

# Layout
audio_field_label.grid(row=1, column=0, sticky='we', padx=50)
images_field_label.grid(row=2, column=0, sticky='we', padx=50)
audio_field.grid(row=1, column=1, sticky='we')
images_field.grid(row=2, column=1, sticky='we')
audio_select_button.grid(row=1, column=2, sticky='w')
images_select_button.grid(row=2, column=2, sticky='w')
convert_button.grid(row=4, column=1, sticky='e')
progress_bar.grid(row=5, column=1, sticky='ew')

# Bind Convert Audio button to conversion function
convert_button.config(command=lambda: convert_audio_to_video(progress_var))

window.mainloop()
