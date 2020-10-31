from tkinter import *
import psycopg2
from PIL import ImageTk, Image
import sys


def connect():
    conn = psycopg2.connect('dbname=data user=postgres password=postgres host=127.0.0.1 port=5432')
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS data (id SERIAL PRIMARY KEY NOT NULL, ip varchar(50), ServerName varchar(50), Login varchar(50), password varchar(50), description varchar(50))')
    conn.commit()
    conn.close()


def insert(ip, ServerName, Login, password, description):
    conn = psycopg2.connect('dbname=data user=postgres password=postgres host=127.0.0.1 port=5432')
    cur = conn.cursor()
    cur.execute('INSERT INTO data (ip, ServerName, Login, password, description) VALUES(%s, %s, %s, %s, %s)',
                (ip, ServerName, Login, password, description))
    conn.commit()
    conn.close()


def view():
    conn = psycopg2.connect('dbname=data user=postgres password=postgres host=127.0.0.1 port=5432')
    cur = conn.cursor()
    cur.execute('SELECT * FROM data')
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def delete(id):
    conn = psycopg2.connect('dbname=data user=postgres password=postgres host=127.0.0.1 port=5432')
    cur = conn.cursor()
    cur.execute('DELETE FROM data WHERE id=%s', (id,))
    conn.commit()
    conn.close()


def search(ip='', ServerName='', Login='', password='', description=''):
    conn = psycopg2.connect('dbname=data user=postgres password=postgres host=127.0.0.1 port=5432')
    cur = conn.cursor()
    cur.execute('SELECT * FROM data WHERE ip=%s OR ServerName=%s OR Login=%s OR password=%s OR description=%s',
                (ip, ServerName, Login, password, description))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def get_selected_row(event):
    global selected_row
    if list1.curselection():
        index = list1.curselection()[0]
        selected_row = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_row[1])
        e2.delete(0, END)
        e2.insert(END, selected_row[2])
        e3.delete(0, END)
        e3.insert(END, selected_row[3])
        e4.delete(0, END)
        e4.insert(END, selected_row[4])
        e5.delete(0, END)
        e5.insert(END, selected_row[5])


def view_command():
    list1.delete(0, END)
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    for row in view():
        list1.insert(END, row)


def search_command():
    list1.delete(0, END)
    for row in search(ip_text.get(), server_text.get(), login_text.get(), password_text.get(), desc_text.get()):
        list1.insert(END, row)


def add_command():
    insert(ip_text.get(), server_text.get(), login_text.get(), password_text.get(), desc_text.get())
    list1.delete(0, END)
    list1.insert(END, (ip_text.get(), server_text.get(), login_text.get(), password_text.get(), desc_text.get()))


def delete_command():
    delete(selected_row[0])


def command1(event):
    if entry1.get() == $USERNAME and entry2.get() == $PASSWORD:
        win.deiconify()
        top.destroy()


def command2():
    win.deiconify()
    top.destroy()
    sys.exit()


win = Tk()
image_insert = ImageTk.PhotoImage(Image.open("{$PATH_TO_LOGO_IMAGE}"))
new_label = Label(image=image_insert)
new_label.grid(row=6, column=3)
top = Toplevel()

top.geometry('200x100')
top.title("Welcome")
top.configure(background="white")
lbl1 = Label(top, text="Username")
entry1 = Entry(top)
lbl2 = Label(top, text="Password")
entry2 = Entry(top, show="*")
button = Button(top, text="Close", command=lambda: command2())
entry2.bind('<Return>', command1)

lbl1.pack()
entry1.pack()
lbl2.pack()
entry2.pack()
button.pack()

win.wm_title('SAVE MY PASSWORDS - Admin')

l1 = Label(win, text='IP')
l1.grid(row=0, column=0)
l2 = Label(win, text='Server Name')
l2.grid(row=1, column=0)
l3 = Label(win, text='Login')
l3.grid(row=2, column=0)
l4 = Label(win, text='Password')
l4.grid(row=3, column=0)
l5 = Label(win, text='Descripiton')
l5.grid(row=4, column=0)

ip_text = StringVar()
e1 = Entry(win, textvariable=ip_text)
e1.grid(row=0, column=1)

server_text = StringVar()
e2 = Entry(win, textvariable=server_text)
e2.grid(row=1, column=1)

login_text = StringVar()
e3 = Entry(win, textvariable=login_text)
e3.grid(row=2, column=1)

password_text = StringVar()
e4 = Entry(win, textvariable=password_text)
e4.grid(row=3, column=1)

desc_text = StringVar()
e5 = Entry(win, textvariable=desc_text)
e5.grid(row=4, column=1)

list1 = Listbox(win, height=5, width=50)
list1.grid(row=5, column=0, rowspan=9, columnspan=2)

list1.bind('<<ListboxSelect>>', get_selected_row)

b1 = Button(win, text="ADD", width=10, pady=3, command=add_command)
b1.grid(row=0, column=3)

b2 = Button(win, text="Search", width=10, pady=3, command=search_command)
b2.grid(row=1, column=3)

b3 = Button(win, text="View All", width=10, pady=3, command=view_command)
b3.grid(row=2, column=3)

b4 = Button(win, text="Delete", width=10, pady=3, command=delete_command)
b4.grid(row=3, column=3)

b5 = Button(win, text="Close", width=10, pady=3, command=win.destroy)
b5.grid(row=4, column=3)

win.withdraw()
win.mainloop()