from flask import Flask, render_template, redirect, flash, url_for, request
from forms import editHospital

app=Flask(__name__)
app.config['SECRET_KEY']="helloworld"

@app.route('/',methods=['GET','POST'])
def home():
    form=editHospital()
    if form.is_submitted():
        return render_template('dashboard.html')
    return render_template("dashboard.html",form=form)

@app.route('/newhospital/')
def normal():
    return "Direct Py Text"


if __name__=="__main__":
    app.run(debug=True)
