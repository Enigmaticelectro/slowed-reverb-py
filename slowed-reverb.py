from tkinter import Tk, Label, Button, filedialog, Scale
from pydub import AudioSegment
import os

class App:
    def __init__(self, app):
        self.app = app
        app.title("slowed+reverb")

        self.file = ""
        self.export_path = "output"

        self.select_file_button = Button(app, text="Select file", command=self.select_file)
        self.select_file_button.pack()

        self.select_file_button = Button(app, text="slowed+reverb", command=self.slowed_reverb)
        self.select_file_button.pack()
        
        self.slowdown = Scale(app, orient="horizontal", from_=0, to=100, label="slow down:")
        self.slowdown.pack()
        
    def select_file(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("wav files", "*.wav"), ("mp3 files", "*.mp3")))
        self.file = filepath
    
    def slowed_reverb(self):
        framerate = (100 - self.slowdown.get()) / 100
        audio = AudioSegment.from_file(self.file)

        slowed = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * framerate)})
        slowed.set_frame_rate(audio.frame_rate)
        slowed.export(f"{self.export_path}/{os.path.basename(self.file)}", format="mp3")


if __name__ == "__main__":
    init = Tk()
    gui = App(init)
    init.mainloop()