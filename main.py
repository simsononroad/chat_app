from flask import Flask, request, render_template, redirect, url_for, flash, session
#import database
import hashlib
import sqlite3
from form import belepes
from google_keys import *
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment
import requests

GOOGLE_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

app = Flask(__name__)
app.secret_key = "szupertitkoskulcs"  # Ezt cseréld le egy erősebb kulcsra!

con = sqlite3.connect("data.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE login_name(id INT PRIMARY KEY ,name)")
    cur.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY AUTOINCREMENT, message, sender)")
    ins = cur.execute(f"insert into login_name (name) values ('admin')")
    con.commit()

except:
    pass



# Előre meghatározott felhasználónév és jelszó


# Főoldal (index)
@app.route("/")
def index():
    form = belepes()
    return render_template("index.html", site_key=GOOGLE_RECAPTCHA_SITE_KEY, form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = belepes()
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    username = request.form["username"]


    if form.validate_on_submit():
        secret_response = request.form["g-recaptcha-response"]
        verify_response = requests.post(url=f"{GOOGLE_VERIFY_URL}?secret={GOOGLE_RECAPTCHA_SECRET_KEY}&response={secret_response}").json
        print(verify_response)
    cur.execute(f"select name FROM login_name")
    name = cur.fetchall()
    nevek = ""
    for names in name:
        names = names[0]
        nevek += f"{names}, "
    
    if username in nevek:
        print("nem lehet bejelentkezni")
        error = "Van már ilyen nevű felhasználó"
        return redirect(url_for("index"))
    else:
        ins = cur.execute(f"insert into login_name (name) values ('{username}')")
        con.commit()
        session["user"] = username
        return redirect(url_for("chat"))





@app.route("/chat")
def chat():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    
    cur.execute(f"select message, sender FROM messages")
    uzenetek = cur.fetchall()
    uzenet_n = ""
    for i in uzenetek:
        message1 = i[0]
        kuldo1 = i[1]
        uzenet_n += f"{kuldo1}: {message1} <br>"


    return render_template("chat.html", user=session["user"], uzenet_n=uzenet_n)
    
    


@app.route("/send_message", methods=["POST"])
def send_message():
    kuldo = session["user"]
    uzenet = request.form["message_html"]
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    ins = cur.execute(f"insert into messages (message, sender) values ('{uzenet}', '{kuldo}')")
    con.commit()
    return redirect(url_for("chat"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sikeres kijelentkezés.", "success")
    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(debug=True)