from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from test import getmail
from model import Todo

import imaplib
import email
from email.header import decode_header
import webbrowser
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/getmails")
def getmails():
    return getmail()

@app.route("/read")
def read():
    alltodo = Todo.query.all()
    return render_template("myTodo.html", alltodo = alltodo)

@app.route("/update/<int:sno>", methods = ['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter(sno == sno).first()
    if(request.method == "POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter(sno == sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo);
        db.session.commit();
        return redirect('/')
    return render_template("update.html", todo = todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter(sno == sno).first()
    db.session.delete(todo)
    db.session.commit();
    return redirect('/read')

@app.route("/", methods = ['GET', 'POST'])
def create():
    if(request.method =="POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo);
        db.session.commit();
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True,port = 8000)