import customtkinter
import sqlite3



con = sqlite3.connect("data.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE login_name(id INT PRIMARY KEY ,name)")
    cur.execute("CREATE TABLE messages(message, sender)")
    ins = cur.execute(f"insert into login_name (name) values ('admin')")
    con.commit()

except:
    pass


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

login_page = customtkinter.CTk()  # create CTk window like you do with the Tk window
login_page.geometry("400x240")

window = customtkinter.CTk()
window.geometry("700x600")
window.title("New window")
def login_pages():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    username = user.get()
    cur.execute(f"select name FROM login_name")
    name = cur.fetchall()
    nevek = ""
    for names in name:
        names = names[0]
        nevek += f"{names}, "

    if username in nevek:
        print("nem lehet bejelentkezni")
        error = "Van már ilyen nevű felhasználó"
    else:
        ins = cur.execute(f"insert into login_name (name) values ('{username}')")
        con.commit()
        open_chat = customtkinter.CTkButton(master=login_page, text="Belépés a csevegésbe!", command=lambda: chat(login_page))
        open_chat.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

uzenet_n = ""
def chat(master):
    global uzenet_n
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    
    message = customtkinter.CTkEntry(window, placeholder_text="Üzenet")
    message.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
    
    clear_all = customtkinter.CTkButton(master=window, text="torol", command=lambda: send_message(message))
    clear_all.place(relx=0.10, rely=0.1, anchor=customtkinter.CENTER)
    
    button = customtkinter.CTkButton(master=window, text="Kuldes", command=delete_all)
    button.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
    
    cur.execute(f"select message, sender FROM messages")
    uzenetek = cur.fetchall()
    
    for i in uzenetek:
        message1 = i[0]
        kuldo1 = i[1]
        uzenet_n += f"{kuldo1}: {message1} \n"
    label = customtkinter.CTkLabel(master=window, text=uzenet_n)
    label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    while True:
        window.update()
        window.mainloop()
    

def delete_all():
    global uzenet_n
    uzenet_n = ""

def send_message(text):
    kuldo = user.get()
    uzenet = text.get()
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    ins = cur.execute(f"insert into messages (message, sender) values ('{uzenet}', '{kuldo}')")
    con.commit()
    refresh = 1
    window.update()    
    chat(login_page)

user = customtkinter.CTkEntry(login_page, placeholder_text="Felhasználónév")
user.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=login_page, text="Belépés", command=login_pages)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)



# Use CTkButton instead of tkinter Button



login_page.mainloop()