from flask import Flask, render_template, redirect, flash, url_for, request
from forms import editHospital
from pymongo import MongoClient

client=MongoClient('mongodb://localhost:27017')
db=client['corona_app']
global hospitals
hospitals=db.hospitals
global allhopitals

app=Flask(__name__)
app.config['SECRET_KEY']="helloworld"

@app.route('/',methods=['GET','POST'])
def home():
    info=""
    allhopitals=hospitals.find()
    if request.method=="POST":
        try:
            
            hosid=int(request.form['hospnumber'])
            
            totalbeds=int(request.form['totalbeds'])
            availablebeds=int(request.form['availablebeds'])
            totalICU=int(request.form['totalICU'])
            availableICU=int(request.form['availableICU'])
            totdocs=int(request.form['totdocs'])
            
            updations={
                "total_beds":totalbeds,
                "available_beds":availablebeds,
                "total_ICU":totalICU,
                "available_ICU":availableICU,
                "doctors":totdocs
            }

            newvalues = { "$set": updations}
            hospitals.update_one({'number':hosid}, newvalues)
            allhopitals=hospitals.find()
            return render_template("dashboard.html",info=allhopitals)
        except:
            return "Galti"
    return render_template("dashboard.html",info=allhopitals)


@app.route('/new/',methods=['GET','POST'])
def newHospital():
    return render_template("facility.html")

@app.route('/processing/',methods=['GET','POST'])
def process():
    if request.method=="POST":
        case=0
        try:
            hospname=str(request.form['addfac'])
            if ("'" in hospname or '"' in hospname):
                throw
            case=1
            lat=float(request.form['lat'])
            lat=round(lat,4)
            long=float(request.form['long'])
            long=round(long,4)
            case=2
            totbeds=int(request.form['addtotalbeds'])
            availablebeds=int(request.form['addavailablebeds'])
            icubeds=int(request.form['addtotalICU'])
            availableicubeds=int(request.form['addavailableICU'])
            doctors=int(request.form['addtotdocs'])
            case=3
            allhopitals=hospitals.find().sort('number',-1).limit(1)
            for i in allhopitals:
                Num=i['number']+1
            item={"number":Num,
            "name":hospname,
            "lat":lat,
            "long":long,
            "total_beds":totbeds,
            "available_beds":availablebeds,
            "total_ICU":icubeds,
            "available_ICU":availableicubeds,
            "doctors":doctors
            }
            result=hospitals.insert_one(item)
            allhopitals=hospitals.find()
            return render_template("dashboard.html",info=allhopitals)
        except:
            message="An error was encountered. Please try again." 
            if case==0:
                message="The Facility Name entered is not valid. Please try again."
            if case==1:
                message="The Latitude and Longitude coordinates entered is/are not valid. Please try again."
            if case==2:
                message="One or more fields entered were not acceptable. Please try again."
            return render_template("facility.html", msg=message)
    else:
        return newHospital()

if __name__=="__main__":
    app.run(debug=True)
