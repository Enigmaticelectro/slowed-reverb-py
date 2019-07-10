import os
import tempfile
from pydub import AudioSegment
from pysndfx import AudioEffectsChain
from tkinter import Tk, Label, Button, filedialog, Scale

class App:
    def __init__(self, app):
        self.app = app
        app.title("slowed+reverb")

        self.file = ""
        self.export_path = "exported_files"

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
        filename = os.path.splitext(os.path.basename(self.file))[0]

        slowed = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * framerate)})
        slowed.set_frame_rate(audio.frame_rate)

        with tempfile.TemporaryDirectory() as tmpwav:
            slowed.export(f"{tmpwav}\{filename}.wav", format="wav")
                
            os.makedirs(os.path.dirname('exported_files/'), exist_ok=True)

            fx = AudioEffectsChain().reverb(reverberance=25, hf_damping=35, room_scale=100, pre_delay=5)
            fx(f"{tmpwav}\{filename}.wav", f"{self.export_path}/{filename}.wav")

if __name__ == "__main__":
    init = Tk()
    gui = App(init)
    init.mainloop()