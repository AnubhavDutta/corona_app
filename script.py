from flask import Flask, render_template, redirect, flash, url_for, request
from pymongo import MongoClient
import math

client=MongoClient('mongodb://localhost:27017')
db=client['corona_app']
global hospitals
hospitals=db.hospitals
global allhopitals

app=Flask(__name__)

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
            pw=str(request.form['pw'])
            
            updations={
                "total_beds":totalbeds,
                "available_beds":availablebeds,
                "total_ICU":totalICU,
                "available_ICU":availableICU,
                "doctors":totdocs
            }
            allhopitals=hospitals.find({'number':hosid}).limit(1)
            if(allhopitals[0]['key']!=pw):
                allhopitals=hospitals.find()
                return render_template("dashboard.html",info=allhopitals)
            newvalues = { "$set": updations}
            hospitals.update_one({'number':hosid}, newvalues)
            allhopitals=hospitals.find()
            return render_template("dashboard.html",info=allhopitals)
        except:
            allhopitals=hospitals.find()
            return render_template("dashboard.html",info=allhopitals)
    return render_template("dashboard.html",info=allhopitals)


@app.route('/new/',methods=['GET','POST'])
def newHospital():
    return render_template("facility.html")

def distance(lat1, lat2,long1,long2):
    ang1=abs(lat1-lat2)
    ang2=abs(long1-long2)
    return math.sqrt((ang1**2)+(ang2**2))

@app.route('/nearby/',methods=['GET','POST'])
def nearby():
    if request.method=="POST":
        lat=float(request.form['lat'])
        lat=round(lat,4)
        long=float(request.form['long'])
        long=round(long,4)
        myhopitals=hospitals.find()
        allhopitals=[]
        for i in myhopitals:
            i['distance']=distance(lat, i['lat'] , long , i['long'])
            allhopitals=allhopitals+[i]
        result=[]
        for g in range(5):
            index=0
            minPoint=float('inf')
            minInd=0
            minItem=None
            for i in allhopitals:
                if( i['distance'] < minPoint and i['available_beds']>0 ):
                    minPoint=i['distance']
                    minItem=i
                    minInd=index
                index+=1
            allhopitals=list(allhopitals)
            del allhopitals[minInd]
            result=result+[minItem]
            if(len(allhopitals)<1):
                break
        return render_template("dashboard.html",info=result, near=True)
    else:
        allhopitals=hospitals.find()
        return render_template("dashboard.html",info=allhopitals)

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
            pw=str(request.form['mykey'])
            
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
            "doctors":doctors,
            "key":pw
            }
            result=hospitals.insert_one(item)
            allhopitals=hospitals.find()
            return render_template("dashboard.html",info=allhopitals)
        except:
            message="An error was encountered. Please try again." 
            if case==0:
                message="The Facility Name entered is not valid. Please try again."
            elif case==1:
                message="The Latitude and Longitude coordinates entered is/are not valid. Please try again."
            elif case==2:
                message="One or more fields entered were not acceptable. Please try again."
            elif (case==3):
                message="There is something wrong at our end. Try again after sometime."
            return render_template("facility.html", msg=message)
    else:
        return newHospital()

@app.route('/show/')
def show():
    myhopitals=hospitals.find()
    allhopitals=[]
    for i in myhopitals:
        allhopitals = allhopitals + [i]
    return render_template("showcase.html", info=allhopitals)

if __name__=="__main__":
    app.run(debug=False)