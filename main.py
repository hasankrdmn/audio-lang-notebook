from tkinter import *
from tkinter import messagebox
import sqlite3
from googletrans import Translator
import pyttsx3

def say(*arg):
    eng = pyttsx3.init()
    eng.setProperty('rate', 160)
    if arg:
        text = arg[0]
    else:
        text = translated.get('1.0','end')

    eng.say(text)
    eng.runAndWait()

def savedict():
    key = translated.get('1.0','end').lower()
    value = input_box.get().lower()
    if category == 'en2tr':
        cursor.execute("""INSERT INTO dictionary (key,value,category) VALUES (?,?,?);""", (key,value,category))
    else:
        cursor.execute("""INSERT INTO dictionary (key,value,category) VALUES (?,?,?);""", (value,key,category))
    connect.commit()

def translator():
    text = input_box.get()
    if text:
        destination = list(languages.keys())[list(languages.values()).index(clicked2.get())]
        source = list(languages.keys())[list(languages.values()).index(clicked.get())]
        translate = Translator().translate(text, destination, source)
        translated['state'] = 'normal'
        translated.delete('1.0','end')
        translated.insert(END, translate.text)
        translated['state'] = 'disabled'
        savedict_button['state'] = 'normal'
        pronounce_button['state'] = 'normal'
        global category
        category = f'{source}2{destination}'
        return
    messagebox.showerror('Error','Enter text!')

def changelang():
    dest = clicked2.get()
    src = clicked.get()
    clicked.set(dest)
    clicked2.set(src)

def seedict():
    def tell():
        try:
            say(datas[key_list.curselection()[0]][1])
        except IndexError:
            pass

    window = Toplevel(app)
    window.title('Dictionary')
    window.geometry('400x220')

    Label(window, text='Turkish').place(y=0, x=300)
    key_list = Listbox(window, selectmode='SINGLE', fg='GREEN')
    key_list.place(x=20, y=20, width=130)

    Label(window, text='English').place(y=0, x=65)
    value_list = Listbox(window, fg='BLUE')
    value_list.place(y=20, x=250, width=130)

    pronounce_button = Button(window, text='Pronounce', command=tell)
    pronounce_button.place(x=165, y=80)

    cursor.execute('SELECT * from dictionary')
    datas = cursor.fetchall()

    for data in datas:
        key_list.insert(END, data[1])
        value_list.insert(END, data[0])

    window.mainloop()

connect = sqlite3.connect('database.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS dictionary (key,value,category)""")

app = Tk()
app.title('Audio Language Notebook')
app.geometry('660x180')
app.resizable(False, False)

languages = {'en': 'English', 'tr': 'Turkish'}

input_box_label = Label(app, text='Enter text').place(x=120,y=5)
input_box = Entry(app)
input_box.place(x=50,y=30, width=200, height=20)

clicked = StringVar()
clicked.set('English')
src_lang = OptionMenu(app, clicked, *list(languages.values()))
src_lang.place(x=110, y=65, height=30)
src_lang['state'] = 'disabled'

clicked2 = StringVar()
clicked2.set('Turkish')
dest_lang = OptionMenu(app, clicked2, *list(languages.values()))
dest_lang.place(x=465, y=65, height=30)
dest_lang['state'] = 'disabled'

translated_label = Label(app, text='Translated text').place(x=465,y=5)
translated = Text(app)
translated.place(x=400,y=30, width=200, height=20)
translated['state'] = 'disabled'

change_button = Button(app, text='Change lang', command=changelang)
change_button.place(y=30, x=285, height=25)

translate_button = Button(app, text='Translate', command=translator)
translate_button.place(x=295, y=70, height=25)

savedict_button = Button(app, text='Save dictionary', command=savedict)
savedict_button.place(x=280, y=130, height=25)
savedict_button['state'] = 'disabled'

pronounce_button = Button(app, text='Pronounce', command=say)
pronounce_button.place(x=200, y=130, height=25)
pronounce_button['state'] = 'disabled'

seedict_button = Button(app, text='See dictionary', command=seedict)
seedict_button.place(x=380, y=130, height=25)

app.mainloop()
