import os
import tempfile
from pydub import AudioSegment
from pysndfx import AudioEffectsChain
from tkinter import Tk, Label, Button, filedialog, Scale, StringVar, Frame, messagebox

class App:
    def __init__(self, app):
        self.app = app
        self.app.title("slowed+reverb")
        self.app.iconbitmap("icon.ico")
        self.app.minsize(width=640, height=500)
        self.app.maxsize(width=640, height=500)
        #self.app.configure(background="#6622b8")
        
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
        self.slowdown = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="framerate", fg="#6622b8")
        self.slowdown.pack(side="top")

        self.reverberance = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="reverberance", fg="#6622b8")
        self.reverberance.pack(side="top")

        self.hf_damping = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="hf damping", fg="#6622b8")
        self.hf_damping.pack(side="top")

        self.room_scale = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="room scale", fg="#6622b8")
        self.room_scale.pack(side="top")

        self.stereo_depth = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="stereo depth", fg="#6622b8")
        self.stereo_depth.pack(side="top")

        self.pre_delay = Scale(self.middle_frame, orient="horizontal", from_=0, to=100, width="10", label="pre delay", fg="#6622b8")
        self.pre_delay.pack(side="top")

        #Bottom frame
        self.select_file_button = Button(self.bottom_frame, text="slowed+reverb", command=self.slowed_reverb, fg="#6622b8")
        self.select_file_button.pack(side="bottom")
        
    def select_file(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav")))
        if filepath:
            self.filepath = filepath
            self.filename.set(os.path.basename(self.filepath))
    
    def slowed_reverb(self):
        if not self.filepath:
            messagebox.showinfo("Select a file", "You must select an audio file")
        else:
            framerate = (100 - self.slowdown.get()) / 100
            audio = AudioSegment.from_file(self.filepath, format="mp3")
            
            slowed = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * framerate)})
            slowed.set_frame_rate(audio.frame_rate)
            
            with tempfile.TemporaryDirectory() as tmpwav:
                slowed.export(f"{tmpwav}\export.wav", format="wav")
                    
                os.makedirs(os.path.dirname('exported_files/'), exist_ok=True)

                fx = AudioEffectsChain().reverb(
                    reverberance=self.reverberance.get(),
                    hf_damping=self.hf_damping.get(),
                    room_scale=self.room_scale.get(),
                    stereo_depth=self.stereo_depth.get(),
                    pre_delay=self.pre_delay.get(),
                    #wet_gain=0,
                    #wet_only=False
                    )
                export_filename = os.path.splitext(self.filename.get())[0].replace(" ", "_")
                fx(f"{tmpwav}\export.wav", f"{self.export_path}/{export_filename}.wav")

if __name__ == "__main__":
    init = Tk()
    gui = App(init)
    init.mainloop()