from datetime import datetime
from flask import Flask, render_template, request, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,BooleanField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_bootstrap import Bootstrap

import tempfile
from flask import send_file
import re
app = Flask(__name__)
app.config['SECRET_KEY']="codename47"
app.debug=True
class ChatForm(FlaskForm):
    content=TextAreaField("Content",validators=[DataRequired(message="This field is required"),Length(min=0,message=None)])
    submit=SubmitField("Submit")
global rolls


@app.route("/", methods=["GET","POST"])
def home():
    form = ChatForm()
    if form.validate_on_submit():
        data=form.content.data
        global rolls
        rolls=sorted(list(set(re.findall("(1604-[0-9]+-[0-9]+-[0-9]+)", data))))
        global fh
        fh=tempfile.NamedTemporaryFile(mode="w+")
        for roll in rolls:
            print(roll)
            fh.write(roll+"\n")
    
        
        return render_template("rolls.html", rolls=rolls)
    else: 
       return  render_template("index.html",form = form)
# for home page
@app.route("/download", methods=["GET","POST"])
def download():
    fh=open("roll_list.txt","w")
    for roll in rolls:
        print(roll)
        fh.write((roll+"\n"))
    
    fh.flush()
    return send_file("roll_list.txt", as_attachment=True)





if __name__=="__main__":
    app.run()