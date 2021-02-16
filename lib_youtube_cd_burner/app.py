from enum import Enum

from tkinter import *
import tkinter as tk
from tkinter import filedialog

from .youtube_playlist import YoutubePlaylist

pad = {"padx": 30, "pady": 30}

class Action(Enum):
    BURN = 1
    SAVE = 2

class Language(Enum):
    ENGLISH = "English"
    RUSSIAN = "русский"

class App:
    def __init__(self):
        self.filename=None
        self.root = Tk()
        self.root.tk.call('tk', 'scaling', 10.0)
        self.root.option_add('*Font', 'Times 30')
        self.root.title("")
        self.frame = LabelFrame(self.root, text="", **pad)
        self.frame.pack(**pad)

    def create_app(self):
        self._add_languages()
        self._add_urls()
        self._add_actions()
        self._add_save_dir()
        self._add_submit()
        self._update_text()
        self.root.mainloop()

###############
### Actions ###
###############
    def _take_action(self):
        self.status_bar = Label(self.frame,
                                text=self.status_dl_text,
                                bd=1,
                                relief=SUNKEN,
                                bg="yellow")
        self.status_bar.grid(row=6, columnspan=2, sticky=W+E, **pad)

        if self.action_var.get() == Action.SAVE.value:
            song_format = "mp3"
        else:
            song_format = "wav"
        self.root.update_idletasks()
        self.root.update()
        pl = YoutubePlaylist([self.urls_entry.get().strip()], "/tmp/yt")
        filename = self.filename if self.file_shown else None
        pl.generate_audio_medium(save_path=self.filename,
                                 song_format=song_format)
        self.status_bar["text"] = self.status_done_text
        self.status_bar["bg"] = "green"
        self.root.update_idletasks()
        self.root.update()

    def _browse_files(self):
        kwargs = {"initialdir": "/tmp/yt2",
                  "title": self.select_folder_text}
        self.filename = filedialog.askdirectory(**kwargs)
        self.file_label_entry.delete(0, END)
        self.file_label_entry.insert(0, self.filename)
        self.file_shown = True

    def _remove_browse_files(self):
        self.file_label_entry.grid_forget()
        self.file_button.grid_forget()
        self._update_text()
        self.file_shown = False

    def _add_browse_files(self, submit_text_update=True):
        self.file_label_entry.grid(row=3, column=1, **pad)
        self.file_button.grid(row=3, column=0, **pad)
        if submit_text_update:
            self._update_text()
        self.file_shown = True

    def _update_text(self, *args):
        self.root.title(self.root_text)
        self.frame["text"] = self.root_text
        self.save_files_button["text"] = self.save_files_text
        self.burn_cds_button["text"] = self.burn_cds_text
        self.urls_label["text"] = self.enter_url_text
        self.file_button["text"] = self.select_folder_text
        self.submit["text"] = self.submit_text

##############
### Format ###
##############

    def _add_languages(self):
        self.language_var = StringVar()
        self.language_var.set(Language.ENGLISH.value)
        OptionMenu(self.frame,
                   self.language_var,
                   Language.ENGLISH.value,
                   Language.RUSSIAN.value,
                   command=self._update_text).grid(row=0, column=0, **pad)


    def _add_actions(self):
        self.action_var = IntVar()
        self.action_var.set(Action.SAVE.value)
        self.save_files_button = Radiobutton(self.frame,
                                             text="",
                                             variable=self.action_var,
                                             value=Action.SAVE.value,
                                             command=self._add_browse_files
                                             )
        self.save_files_button.grid(row=0, column=1, sticky="W", **pad)
        self.burn_cds_button = Radiobutton(self.frame,
                                           text="",
                                           variable=self.action_var,
                                           value=Action.BURN.value,
                                           command=self._remove_browse_files
                                           )
        self.burn_cds_button.grid(row=1, column=1, stick="W", **pad)


    def _add_urls(self):
        # URLs
        self.urls_label = Label(self.frame,
                                text=self.enter_url_text,
                                **pad)
        self.urls_entry = Entry(self.frame, width=50)
        #self.urls_entry.insert(0, ("ex: https://www.youtube.com/"
        #                           "watch?v=jLtbFWJm9_M"))

        self.urls_label.grid(row=2, column=0, **pad)
        self.urls_entry.grid(row=2, column=1, **pad)

    def _add_save_dir(self):
        self.file_label_entry = Entry(self.frame, width=50)
        self.file_button = Button(self.frame,
                                  text=self.select_folder_text,
                                  bd=1,
                                  command=self._browse_files)
        self._add_browse_files(submit_text_update=False)

    def _add_submit(self):
        # https://stackoverflow.com/a/1918054/8903959
        self.submit = Button(self.frame,
                             text=self.submit_text,
                             bd=1,
                             #relief=SUNKEN,
                             #anchor=E,
                             command=self._take_action)
        self.submit.grid(row=4, column=0, columnspan=3, sticky=W+E, **pad)

#############
### Texts ###
#############

    @property
    def submit_text(self):
        if self.action_var.get() == Action.SAVE.value:
            return self.select_folder_text
        else:
            return self.burn_cds_text

    @property
    def root_text(self):
        if self.language_var.get() == Language.ENGLISH.value:
            return "Youtube Music"
        elif self.language_var.get() == Language.RUSSIAN.value:
            return "музыка на YouTube"

    @property
    def select_folder_text(self):
        if self.language_var.get() == Language.ENGLISH.value:
            return "Select save folder"
        elif self.language_var.get() == Language.RUSSIAN.value:
            return "выберите папку для сохранения"

    @property
    def burn_cds_text(self):
        if self.language_var.get() == Language.ENGLISH.value:
            return "Burn CD(s)"
        elif self.language_var.get() == Language.RUSSIAN.value:
            return "записывать компакт-диски"

    @property
    def enter_url_text(self):
        if self.language_var.get() == Language.ENGLISH.value:
            return "Enter (playlist) URL"
        elif self.language_var.get() == Language.RUSSIAN.value:
            return "Введите (плейлист) URL"

    @property
    def save_files_text(self):
        if self.language_var.get() == Language.ENGLISH.value:
            return "Save file(s)"
        elif self.language_var.get() == Language.RUSSIAN.value:
            return "Сохранить файлы"

    @property
    def status_dl_text(self):
        if self.language_var.get() == Language.ENGLISH.value:
            return "Downloading..."
        elif self.language_var.get() == Language.RUSSIAN.value:
            return "скачивание"

    @property
    def status_done_text(self):
        if self.language_var.get() == Language.ENGLISH.value:
            return "Done!"
        elif self.language_var.get() == Language.RUSSIAN.value:
            return "сделано!"



"""
button = Button(root, text="click me", padx=50, pady=50, command=myClick, fg="blue", bg="red")
button.pack()
root.mainloop()

# state disabled
# grid forget
"""
