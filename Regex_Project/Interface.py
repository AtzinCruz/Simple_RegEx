from tkinter import *
from tkinter import filedialog, ttk, messagebox
from Main import RegEx


regex = RegEx()

root = Tk()
root.title("ReGex")
root.geometry("1000x600")

query = StringVar()

def upload_file():
    file = filedialog.askopenfilename()
    if file != '':
        regex.set_path(file)
        print(regex.text)
        text.delete("1.0", END)
        text.insert('1.0', regex.text)

    else:
        messagebox.showwarning("No file", "The file was not correctly upload")


def upload_query():
    query.set(query_input.get())
    print(query_input.get())
    label.config(text=f"Indexes: {str(regex.query_management(query.get()))}")
    if 'fr' in str(query.get()):
        messagebox.showinfo("Exito", "El archivo ha sido modificado")
        regex.set_text()
        text.delete("1.0", END)
        text.insert('1.0', regex.text)

def clear():
    query_input.delete(0, END)


menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label='Upload file', command=upload_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Input
menu_frame = Frame(root)
query_label = Label(menu_frame, text="Insert query: ", font=("Helvetica", 10))
query_label.grid(row=0, column=0)
query_input = Entry(menu_frame, font=("Helvetica", 10), width=70)
query_input.grid(row=0, column=1)
query_button = Button(menu_frame, text="Upload query", command=upload_query)
query_button.grid(row=0, column=4, padx=15)
clear_button = Button(menu_frame, text="Clear", command=clear)
clear_button.grid(row=0, column=5)
menu_frame.pack()

# text frame
text = Text(root, wrap=WORD)
text.pack(fill=BOTH, expand=True, padx=15, pady=15)

#Matches frame
label = Label(root, text='Indexes: []', wraplength=1000)
label.pack(fill=BOTH, expand=True, padx=5, pady=5)

root.mainloop()





