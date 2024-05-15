import basic
from tkinter import *
from ctypes import windll
from PIL import Image, ImageTk
from tkinter import filedialog

tk_title = "BelLang"

root = Tk()
root.title(tk_title)
# root.iconbitmap(tk_logo)
root.overrideredirect(True)
root.geometry('1280x720+75+75')

root.minimized = False
root.maximized = False

LGRAY = '#3e4042'
DGRAY = '#25292e'
RGRAY = '#10121f'

root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0, highlightthickness=0)


def set_appwindow(mainWindow):
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())


def minimize_me():
    root.attributes("-alpha", 0)  # so you can't see the window when is minimized
    root.minimized = True
    root.bind("<FocusOut>", deminimize)


def deminimize(event):
    root.focus()
    root.attributes("-alpha", 1)  # so you can see the window when is not minimized
    if root.minimized == True:
        root.minimized = False

    root.bind("<FocusIn>")


def maximize_me():
    if root.maximized == False:
        root.normal_size = root.geometry()
        expand_button.config(text=" 🗗 ")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.maximized = not root.maximized
        # now it's maximized

    else:  # if the window was maximized
        expand_button.config(text=" 🗖 ")
        root.geometry(root.normal_size)
        root.maximized = not root.maximized
        # now it is not maximized


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.bl')])
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            editor.insert('1.0', text)


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".bl")
    if file_path:
        text = editor.get('1.0', END)
        with open(file_path, 'w') as file:
            file.write(text)

def help_print():
    output.config(state=NORMAL)
    clear_output()
    file = open('grammar.txt', encoding="utf-8")
    help_text = file.read()
    output.insert(END, help_text)
    output.config(state=DISABLED)

close_button = Button(title_bar, text='  ×  ', command=root.destroy, bg=RGRAY, padx=2, pady=2, font=("calibri", 13),
                      bd=0, fg='white', highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me, bg=RGRAY, padx=2, pady=2, bd=0, fg='white',
                       font=("calibri", 13), highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ', command=minimize_me, bg=RGRAY, padx=2, pady=2, bd=0, fg='white',
                         font=("calibri", 13), highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY, bd=0, fg='white', font=("helvetica", 10),
                        highlightthickness=0)
tk_logo = ImageTk.PhotoImage(Image.open("logo.png"))
title_bar_ico = Label(image=tk_logo, bd=0, width=20, height=20)

# a frame for the main area of the window, this is where the actual app will go
window = Frame(root, bg=DGRAY, highlightthickness=0)

# pack the widgets
title_bar.pack(fill=X)
close_button.pack(side=RIGHT, ipadx=7, ipady=1)
expand_button.pack(side=RIGHT, ipadx=7, ipady=1)
minimize_button.pack(side=RIGHT, ipadx=7, ipady=1)
title_bar_title.pack(side=LEFT, padx=40)
title_bar_ico.place(y=7, relx=0.008)
window.pack(expand=1, fill=BOTH)  # replace this with your main Canvas/Frame/etc.


def changex_on_hovering(event):
    global close_button
    close_button['bg'] = 'red'


def returnx_to_normalstate(event):
    global close_button
    close_button['bg'] = RGRAY


def change_size_on_hovering(event):
    global expand_button
    expand_button['bg'] = LGRAY


def return_size_on_hovering(event):
    global expand_button
    expand_button['bg'] = RGRAY


def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg'] = LGRAY


def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg'] = RGRAY


def get_pos(event):
    if root.maximized == False:

        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

        def release_window(event):
            root.config(cursor="arrow")

        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
    else:
        expand_button.config(text=" 🗖 ")
        root.maximized = not root.maximized


title_bar.bind('<Button-1>', get_pos)
title_bar_title.bind('<Button-1>', get_pos)

close_button.bind('<Enter>', changex_on_hovering)
close_button.bind('<Leave>', returnx_to_normalstate)
expand_button.bind('<Enter>', change_size_on_hovering)
expand_button.bind('<Leave>', return_size_on_hovering)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)

# resize the window width
resizex_widget = Frame(window, bg=DGRAY, cursor='sb_h_double_arrow')
resizex_widget.pack(side=RIGHT, ipadx=2, fill=Y)


def resizex(event):
    xwin = root.winfo_x()
    difference = (event.x_root - xwin) - root.winfo_width()

    if root.winfo_width() > 150:  # 150 is the minimum width for the window
        try:
            root.geometry(f"{root.winfo_width() + difference}x{root.winfo_height()}")
        except:
            pass
    else:
        if difference > 0:  # so the window can't be too small (150x150)
            try:
                root.geometry(f"{root.winfo_width() + difference}x{root.winfo_height()}")
            except:
                pass

    resizex_widget.config(bg=DGRAY)


resizex_widget.bind("<B1-Motion>", resizex)

# resize the window height
resizey_widget = Frame(window, bg=DGRAY, cursor='sb_v_double_arrow')
resizey_widget.pack(side=BOTTOM, ipadx=2, fill=X)


def resizey(event):
    ywin = root.winfo_y()
    difference = (event.y_root - ywin) - root.winfo_height()

    if root.winfo_height() > 150:  # 150 is the minimum height for the window
        try:
            root.geometry(f"{root.winfo_width()}x{root.winfo_height() + difference}")
        except:
            pass
    else:
        if difference > 0:  # so the window can't be too small (150x150)
            try:
                root.geometry(f"{root.winfo_width()}x{root.winfo_height() + difference}")
            except:
                pass

    resizex_widget.config(bg=DGRAY)


resizey_widget.bind("<B1-Motion>", resizey)

root.after(10, lambda: set_appwindow(root))  # to see the icon on the task bar

# Поле ввода текста
editor = Text(font="Arial 14", bg="#212120", fg="White", bd=0, state=NORMAL)
editor.focus_set()
editor.place(y=35, relwidth=1, relheight=0.62222)

# # Поле вывода текста
output = Text(font="Arial 14", bg="#333331", fg="White", bd=0, state=DISABLED)
output.place(rely=0.67, relwidth=1, relheight=0.33333)


# help button
help_button = Button(text="Дапамога", font="Arial 12", fg="WHITE", activeforeground="WHITE", bg=RGRAY, bd=0,
                     activebackground=LGRAY, cursor='hand2', pady=4, command=help_print)
help_button.place(relx=0.1)

button_op = Button(text="Адкрыць файл", font="Arial 12", fg="WHITE", activeforeground="WHITE", bg=RGRAY, bd=0,
                     activebackground=LGRAY, cursor='hand2', pady=4, command=open_file)
button_op.place(relx=0.17)

save_button = Button(text="Захаваць файл", font="Arial 12", fg="WHITE", activeforeground="WHITE", bg=RGRAY, bd=0,
                     activebackground=LGRAY, cursor='hand2', pady=4, command=save_file)
save_button.place(relx=0.27)

# # Ввод текста
def get_text1(event):
    output.config(state=NORMAL)
    clear_output()
    text = editor.get("1.0", END)
    result, error = basic.run("<праграмма>", text)
    if error:
        output.insert(END, error.as_string() + '\n')
    elif result:
        strok = "\n".join(str(x) for x in result.elements if x is not None)
        output.insert(END, strok)
        output.insert(END, '\n')
    output.config(state=DISABLED)


def get_text2():
    output.config(state=NORMAL)
    clear_output()
    text = editor.get("1.0", END)
    result, error = basic.run("<праграмма>", text)
    if error:
        output.insert(END, error.as_string() + '\n')
    elif result:
        output.insert(END, result)
        output.insert(END, '\n')
    output.config(state=DISABLED)


def clear_output():
    output.delete("1.0", END)


def clear_output_event(event):
    output.delete("1.0", END)


editor.bind('<F10>', clear_output_event)
editor.bind('<F10>', get_text1)

# start button
image = ImageTk.PhotoImage(file="start_button.png")
start_button = Button(image=image, bg=RGRAY, bd=0, activebackground=LGRAY, cursor='hand2', height=33, width=33,
                      command=get_text2)
start_button.place(relx=0.8)

# ===================================================================================================

root.mainloop()
