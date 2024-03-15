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



class App(ctk.CTk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(900, 600)
        self.configure(bg='#C2DEDC')
        self._set_appearance_mode('light')

        self.nav_bar = NavBar(self)
        self.main_menu = MainMenu(self)

        self.mainloop()



class NavBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=("#51829B", "#51829B"))
        self.place(x = 0, y = 0, relwidth=1, relheight=0.1)

        # Widgets
        heading = ctk.CTkLabel(self, text="Audio To Video", font=("uber move", 22, 'bold'))
        login_button = ctk.CTkButton(self, text="Login", fg_color="#EADFB4", height=50, text_color="black", hover_color="#EABBB4", font=("uber move", 18, 'bold'))

        # Layout
        heading.pack(side='left', padx=20)
        login_button.pack(side = 'right', padx = 20, )


class MainMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.place(x = 0, rely = 0.1, relwidth=1, relheight=0.9)
        self.create_widgets()

    def create_widgets(self):
        global status_label, images_field, audio_field
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=10)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')

        # Widgets
        audio_field_text = ttk.StringVar()
        images_field_text = ttk.StringVar()
        audio_field = ctk.CTkEntry(self, textvariable=audio_field_text)
        images_field = ctk.CTkEntry(self, textvariable=images_field_text)
        audio_field_label = ctk.CTkLabel(self, text='Select Audio File', font=('uber move', 16))
        images_field_label = ctk.CTkLabel(self, text='Select Image Files', font=('uber move', 16))
        audio_select_button = ctk.CTkButton(self, text='...', text_color="black", hover_color="#EABBB4", font=("uber move", 18, 'bold'),fg_color="#EADFB4", command=self.select_audio)
        images_select_button = ctk.CTkButton(self, text='...', text_color="black", hover_color="#EABBB4", font=("uber move", 18, 'bold'),fg_color="#EADFB4", command=self.select_images)
        convert_button = ctk.CTkButton(self, text='Convert And Save', width=20, fg_color="#EADFB4", height=50, text_color="black", hover_color="#EABBB4", font=("uber move", 18, 'bold'), command=lambda: self.convert_audio_to_video(progress_var))
        progress_var = tk.DoubleVar()
        status_label = ctk.CTkLabel(self, text="", text_color='black', font=("uber move", 14), corner_radius=20, padx = 10)
        # progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate", variable=progress_var)


        # Layout
        audio_field_label.grid(row=1, column=0, sticky='we', padx=50)
        images_field_label.grid(row=2, column=0, sticky='we', padx=50)
        audio_field.grid(row=1, column=1, sticky='we', ipady = 15)
        images_field.grid(row=2, column=1, sticky='we', ipady = 15)
        audio_select_button.grid(row=1, column=2, sticky='w', ipady = 15)
        images_select_button.grid(row=2, column=2, sticky='w', ipady = 15)
        convert_button.grid(row=3, column=1, columnspan = 2, sticky='e', padx = 50)
        # progress_bar.grid(row=5, column=1, sticky='ew')
        # status_label.grid(row=5, column=0, sticky='nsew')
        status_label.place(relx=0.01, rely=0.9, anchor='w', relheight=0.1,)

        # Bind Convert Audio button to conversion function
        # convert_button.config()

    def select_audio(self):
        global audio_file
        audio_file = filedialog.askopenfilename(initialdir=".", title="Select Audio File", filetypes=(("Audio files", "*.mp3;*.wav;*.opus"), ("All files", "*.*")))
        print("Selected Audio File:", audio_file)
        if audio_file:
            audio_field.delete(0, tk.END)
            audio_field.insert(tk.END, audio_file)

    def select_images(self):
        image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg;*.png")])
        print("Selected Image Files:", image_paths)
        if image_paths:
            images_field.delete(0, tk.END)
            images_field.insert(tk.END, "\n".join(image_paths))

    def convert_audio_to_video(self, progress_var):
            global audio_field, images_field

            # Update label text to indicate the video creation process has started
            status_label.configure(text="We are Creating Video, Be Patient Don't Close the application", bg_color="#FFEECC")

            audio = audio_field.get()
            images = images_field.get()

            if audio == '' or images == '':
                status_label.configure(text="")
                showinfo("Insertion Error", "Fill all the fields")
            else:
                def _convert():
                    # Access progress_var from the outer function's scope
                    nonlocal progress_var
                    progress_var = progress_var  # This line may not be necessary, but ensures proper scoping
                    temp_dir = "temp_images"
                    os.makedirs(temp_dir, exist_ok=True)
                    images = images_field.get().split("\n")
                    for i, img_path in enumerate(images):
                        shutil.copy(img_path, os.path.join(temp_dir, f"image_{i}.png"))

                    # Resize and convert images to RGB format
                    for img_path in images:
                        img = Image.open(img_path)
                        img = img.resize((1280, 720))
                        img = img.convert("RGB")
                        img.save(img_path)

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
                            # Update label text to indicate the video creation process has completed successfully
                            status_label.configure(text="Video is Created Successfully", bg_color="lightgreen")
                        except Exception as e:
                            print("An error occurred:", e)
                        finally:
                            shutil.rmtree(temp_dir)
                            # Reset the label text after completion or in case of an error
                            status_label.configure(text="Video is Created Successfully", bg_color="lightgreen")

                    # Update progress variable
                    progress_var.set(100)

                thread = Thread(target=_convert)
                thread.start()


class MyBarLogger(ProgressBarLogger):
    def callback(self, **changes):
        for (parameter, value) in changes.items():
            print('Parameter %s is now %s' % (parameter, value))

    def bars_callback(self, bar, attr, value, old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100
        print(bar, attr, percentage)
        # Update progress bar value on the GUI
        # progress_bar['value'] = percentage



App("Audio to Video", (1100, 700))