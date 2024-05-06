import basicbellang
from tkinter import *
from tkinter import ttk

text_full = ""

root = Tk()
root.geometry("1280x720")
root.title("Belvim")
root.iconbitmap(default="logo.ico")
root.resizable(False, False)


# Toolbar

def open_help():
    window = Tk()
    window.title("Дапамога")
    window.geometry("500x500")
    file_gr = open('grammar.txt', encoding="utf-8")
    grammar = file_gr.read()
    label = ttk.Label(window, text=grammar, font="Arial 10")
    label.pack(anchor="nw", expand=1)


main_menu = Menu()
main_menu.add_cascade(label="File")
main_menu.add_cascade(label="Дапамога", command=open_help)

root.config(menu=main_menu)

# Поле ввода текста
editor = Text(font="Arial 14",  bg="#212120", fg="White", bd=0)
editor.place(anchor="nw", width=1264, height=480)

editor_scroll = ttk.Scrollbar(orient="vertical", command=editor.yview)
editor_scroll.place(x=1264, height=480)

# Поле вывода текста
output = Text(font="Arial 14", bg="#333331", fg="White", bd=0, state=DISABLED)
output.place(y=480, width=1264, height=240)

output_scroll = ttk.Scrollbar(orient="vertical", command=output.yview)
output_scroll.place(x=1264, y=480, height=240)


# Ввод текста
def get_text(event):
    output.config(state=NORMAL)
    delete()
    global text_full
    text_full = [x for x in editor.get("1.0", END).split('\n') if x]
    for line in text_full:
        result, error = basicbellang.run("<праграмма>", line)
        if error:
            output.insert(END, error.as_string() + '\n')
        elif result:
            output.insert(END,  result)
            output.insert(END, '\n')
    output.config(state=DISABLED)


def delete():
    output.delete("1.0", END)


editor.bind('<Return>', delete)
editor.bind('<Return>', get_text)

root.mainloop()

# file = open('code.txt', encoding="utf-8")
# text_full = file.read().split('\n')

# for line in text_full:
#     result, error = basicbellang.run("<праграмма>", line)

# while True:
#     text = str(input("BELLANG>>> "))
#
#     result, error = basicbellang.run("<праграмма>", text)
#
#     if error:
#         print(error.as_string())
#     elif result:
#         print(result)
