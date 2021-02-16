from enum import Enum

from tkinter import *
from tkinter import filedialog

pad = {"padx": 5, "pady": 5}

class Action(Enum):
    BURN = 1
    SAVE = 2

class Language(Enum):
    ENGLISH = 1
    RUSSIAN = 2

class App:
    def __init__(self):
        self.texts = []
        self.root = Tk()
        self.root_text = StringVar()
        self.root.title(self.root_text.get())
        self.frame = LabelFrame(self.root, text=self.root_text.get(), **pad)
        self.frame.pack(**pad)

    def create_app(self):
        self.burn_cds_text = StringVar()
        self.save_files_text = StringVar()
        self._add_languages()
        self._add_urls()
        self._add_actions()
        self._add_save_dir()
        self._add_submit()
        self._change_language()
        self.root.mainloop()

###############
### Actions ###
###############
    def _take_action(self):
        if self.action_var.get() == Action.SAVE.value:
            song_format = "mp3"
        else:
            song_format = "wav"
        pl = YoutubePlaylist(self.urls_entry.get().strip(), "/tmp/yt")
        pl.generate_audio_medium(save_path=self.frame.filename,
                                 song_format=song_format)

    def _browse_files(self):
        kwargs = {"initialdir": "/tmp/yt2",
                  "title": self.select_folder.text.get()}
        filename = filedialog.askdirectory(**kwargs)
        self.file_label_entry.delete(0, END)
        self.file_label_entry.insert(0, filename)

    def _remove_browse_files(self):
        self.file_label_entry.grid_forget()
        self.file_button.grid_forget()
        self.submit_text.set("Burn CD(s)")

    def _add_browse_files(self, submit_text_update=True):
        self.file_label_entry.grid(row=2, column=1)
        self.file_button.grid(row=2, column=0)
        if submit_text_update:
            self.submit_text.set("Save File(s)")

    def _change_language(self):
        if self.language_var == Language.ENGLISH:
            self._add_english_text()
        elif self.language_var == Language.RUSSIAN:
            self._add_russian_text()

    def _add_english_text(self):
        self.root.text.set("Youtube Music")
        self.select_folder_text.set("Select save folder")
        self.burn_cds_text.set("Burn CD(s)")
        self.save_files_text.set("Save File(s)")
        self.enter_url_text.set("Enter (playlist) URL:")
        self.root.title(self.root_text.get())
        self.frame["text"] = self.root_text.get()

    def _add_russian_text(self):
        pass

##############
### Format ###
##############

    def _add_languages(self):
        self.language_var = IntVar()
        self.language_var.set(Language.ENGLISH.value)
        Radiobutton(self.frame,
                    text="English",
                    variable=self.language_var,
                    value=Language.ENGLISH.value,
                    command=self._change_language).grid(row=0, column=0)
        Radiobutton(self.frame,
                    text="русский",
                    variable=self.language_var,
                    value=Language.RUSSIAN.value,
                    command=self._change_language).grid(row=0, column=1)


    def _add_actions(self):
        self.action_var = IntVar()
        self.action_var.set(Action.SAVE.value)
        Radiobutton(self.frame,
                    textvariable=self.save_files_text,
                    variable=self.action_var,
                    value=Action.SAVE.value,
                    command=self._add_browse_files).grid(row=1, column=0)
        Radiobutton(self.frame,
                    textvariable=self.burn_cds_text,
                    variable=self.action_var,
                    value=Action.BURN.value,
                    command=self._remove_browse_files).grid(row=1, column=1)


    def _add_urls(self):
        self.enter_url_text = StringVar()
        # URLs
        self.urls_label = Label(self.frame,
                                textvariable=self.enter_url_text,
                                **pad)
        self.urls_entry = Entry(self.frame, width=50)
        #self.urls_entry.insert(0, ("ex: https://www.youtube.com/"
        #                           "watch?v=jLtbFWJm9_M"))

        self.urls_label.grid(row=1, column=0)
        self.urls_entry.grid(row=1, column=1)

    def _add_save_dir(self):
        self.select_folder_text = StringVar()
        self.file_label_entry = Entry(self.frame, width=50)
        self.file_button = Button(self.frame,
                                  textvariable=self.select_folder_text,
                                  bd=1,
                                  command=self._browse_files)
        self._add_browse_files(submit_text_update=False)

    def _add_submit(self):
        if self.action_var.get() == Action.SAVE.value:
            text = self.save_files_text.get()
        else:
            text = self.burn_cds_text.get()
        # https://stackoverflow.com/a/1918054/8903959
        self.submit_text = StringVar()
        self.submit_text.set(text)
        footer = Button(self.frame,
                        textvariable=self.submit_text,
                        bd=1,
                        #relief=SUNKEN,
                        #anchor=E,
                        command=self._take_action)
        footer.grid(row=4, column=0, columnspan=3, sticky=W+E)

"""
button = Button(root, text="click me", padx=50, pady=50, command=myClick, fg="blue", bg="red")
button.pack()
root.mainloop()

# state disabled
# grid forget
"""
