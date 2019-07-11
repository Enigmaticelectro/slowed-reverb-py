import os
import tempfile
from pydub import AudioSegment
from pysndfx import AudioEffectsChain
from tkinter import Tk, Label, Button, filedialog, Scale, StringVar, Frame

class App:
    def __init__(self, app):
        self.app = app
        self.app.title("slowed+reverb")
        self.app.iconbitmap("slowed_reverb.ico")
        self.app.minsize(width=640, height=500)
        self.app.maxsize(width=640, height=500)
        self.app.configure(background="#6622b8")
        
        self.top_frame = Frame(self.app)
        self.top_frame.pack(padx=20, pady=20)
        self.middle_frame = Frame(self.app)
        self.middle_frame.pack(padx=10, pady=10, expand=1)
        self.bottom_frame = Frame(self.app)
        self.bottom_frame.pack(expand=1)

        self.filepath = ""
        self.filename = StringVar(value="No file selected")
        self.export_path = "exported_files"

        #Top frame
        self.selected_file = Label(self.top_frame, textvariable=self.filename, fg="#6622b8")
        self.selected_file.pack(side="left")

        self.select_file_button = Button(self.top_frame, text="Select a file", command=self.select_file, fg="#6622b8")
        self.select_file_button.pack(side="left")
        
        #Middle frame
        self.slowdown = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="framerate:")
        self.slowdown.pack(side="top")

        self.reverberance = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="reverberance:")
        self.reverberance.pack(side="top")

        self.hf_damping = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="hf damping:")
        self.hf_damping.pack(side="top")

        self.room_scale = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="room scale:")
        self.room_scale.pack(side="top")

        self.pre_delay = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="pre delay:")
        self.pre_delay.pack(side="top")

        #Bottom frame
        self.select_file_button = Button(self.bottom_frame, text="slowed+reverb", command=self.slowed_reverb, fg="#6622b8")
        self.select_file_button.pack(side="bottom")
        
    def select_file(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("wav files", "*.wav"), ("mp3 files", "*.mp3")))
        self.filepath = filepath
        self.filename.set(os.path.basename(self.filepath))
    
    def slowed_reverb(self):
        framerate = (100 - self.slowdown.get()) / 100
        audio = AudioSegment.from_file(self.filepath)

        slowed = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * framerate)})
        slowed.set_frame_rate(audio.frame_rate)

        with tempfile.TemporaryDirectory() as tmpwav:
            slowed.export(f"{tmpwav}\export.wav", format="wav")
                
            os.makedirs(os.path.dirname('exported_files/'), exist_ok=True)

            fx = AudioEffectsChain().reverb(
                reverberance=self.reverberance.get(),
                hf_damping=self.hf_damping.get(),
                room_scale=self.room_scale.get(),
                pre_delay=self.pre_delay.get()
                )
            export_filename = os.path.splitext(self.filename.get())[0].replace(" ", "_")
            fx(f"{tmpwav}\export.wav", f"{self.export_path}/{export_filename}.wav")

if __name__ == "__main__":
    init = Tk()
    gui = App(init)
    init.mainloop()