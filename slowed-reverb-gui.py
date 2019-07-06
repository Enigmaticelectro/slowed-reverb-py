from tkinter import Tk, Label, Button, filedialog

class App:
    def __init__(self, app):
        self.app = app
        app.title("slowed+reverb")

        self.file = ""

        self.select_file_button = Button(app, text="Select file", command=self.select_file)
        self.select_file_button.pack()

    def select_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("wav files", "*.wav"), ("mp3 files", "*.mp3")))
        self.file = filename

if __name__ == "__main__":
    init = Tk()
    gui = App(init)
    init.mainloop()