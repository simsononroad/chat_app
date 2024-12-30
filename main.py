from flask import Flask, request, render_template, redirect, url_for, flash, session
#import database
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = "szupertitkoskulcs"  # Ezt cseréld le egy erősebb kulcsra!

con = sqlite3.connect("data.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE login_name(id INT PRIMARY KEY ,name)")
    ins = cur.execute(f"insert into login_name (name) values ('admin')")
    con.commit()

except:
    pass



# Előre meghatározott felhasználónév és jelszó


# Főoldal (index)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    username = request.form["username"]

    cur.execute(f"select name FROM login_name")
    name = cur.fetchall()
    nevek = ""
    for names in name:
        names = names[0]
        nevek += f"{names}, "
    
    if username in nevek:
        print("nem lehet bejelentkezni")
        return redirect(url_for("index"))
    else:
        ins = cur.execute(f"insert into login_name (name) values ('{username}')")
        con.commit()
        session["user"] = username
        return redirect(url_for("chat"))





@app.route("/chat")
def chat():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    return render_template("chat.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sikeres kijelentkezés.", "success")
    return redirect(url_for("index"))




if __name__ == "__main__":
    app.run(debug=True)