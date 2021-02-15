from enum import Enum

from tkinter import *

pad = {"padx": 5, "pady": 5}

class Action(Enum):
    BURN = 1
    SAVE = 2

class App:
    def __init__(self):
        self.root = Tk()
        self.frame = LabelFrame(root, text="Youtube Music", **pad)
        self.frame.pack(**pad)

    def create_app(self):
        self._add_urls()
        self._add_actions()
        self._add_save_dir()
        self._add_submit()
        self.root.mainloop()

    def _take_action(self):
        if self.action_var.get() == Action.SAVE.value:
            song_format = "mp3"
        else:
            song_format = "wav"
        pl = YoutubePlaylist(self.urls_entry.get().strip(), "/tmp/yt")
        pl.generate_audio_medium(save_path=self.frame.filename,
                                 song_format=song_format)

    def _add_urls(self)
        # URLs
        self.urls_label = Label(self.frame, text="Enter playlist URL", **pad)
        self.urls_entry = Entry(self.frame, width=100)
        self.urls_entry.insert(0, ("ex: https://www.youtube.com/"
                                   "watch?v=jLtbFWJm9_M"))

        self.urls_label.grid(row=0, column=0)
        self.urls_entry.grid(row=0, column=1)

    def _add_actions(self):
        self.action_label = Label(self.frame,
                                  text="Burn CD(s) or save files?",
                                  **pad)
        self.action_var = IntVar()
        self.action_var.set(Action.SAVE.value)
        Radiobutton(self.frame,
                    text="Save Files",
                    variable=self.action_var,
                    value=Action.SAVE.value).grid(row=0, column=0)
        Radiobutton(self.frame,
                    text="Burn CD(s)",
                    variable=self.action_var,
                    value=Action.BURN.value).grid(row=0, column=1)

    def _add_save_dir(self):
        self.frame.filename = filedialog.askdirectory(initialdir="/tmp/yt2",
                                                      title="Where to save files")

    def _add_submit(self):
        if self.action_var.get() == Action.SAVE.value:
            text = "Save Files"
        else:
            text = "Burn CD(s)"
        footer = Button(self.frame,
                        text=text,
                        bd=1,
                        relief=SUNKEN,
                        anchor=E,
                        command=self._take_action)
        footer.grid(row=1, column=0, columnspan=3, sticky=W+E)
"""
button = Button(root, text="click me", padx=50, pady=50, command=myClick, fg="blue", bg="red")
button.pack()
root.mainloop()

# state disabled
# grid forget
"""
