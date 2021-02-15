from tkinter import *

root = Tk()

e = Entry(root, width=50)
e.pack()
e.insert(0, "Enter your name")
#e.delete(0, END)
e.get()

frame = LabelFrame(root, text="Myframe", padx=5, pady=5)
frame.pack(padx=5, pady=5)

def popup():
    messagebox.showinfo("This is my popop", "hello")
Button(root, text="popup", command=popup).pack()

root.filename = filedialog.askdirectory(initialdir="/tmp/", title="select a folder to save in", filetypes="", initialfile="")

mylbal = Label(root, text=root.filename).pack()

# Burn CD or save files
exr = StrVar()
ext.set("2") # default?
ext.get()
Radiobutton(root, text="option1", variable=ext, value="wav").pack()



# other attrs
# columnspan
# state=DISABLED

#grid_forget()?


footer = Label(root, text="footer", bd=1, relief=SUNKEN, anchor=E)
footer.grid(row=2, column=0, columnspan=3, sticky=W+E)

# Define labels
urls = Label(root, text="Input URLs")
download_path = Label(root, text="download path")

urls.grid(row=0, column=0)
download_path.grid(row=5, column=0)

def myClick():
    mylabel = Label(root, text="CLICKED")
    mylabel.pack()

button = Button(root, text="click me", padx=50, pady=50, command=myClick, fg="blue", bg="red")
button.pack()
root.mainloop()
