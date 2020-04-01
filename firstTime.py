from pymongo import MongoClient
client=MongoClient('mongodb://localhost:27017')
db=client['corona_app']
hospitals=db.hospitals

item={"number":2,
"name":"Apollo BSR Bhubaneswar",
"lat":20.2,
"long":85.8,
"total_beds":30,
"available_beds":25,
"total_ICU":10,
"available_ICU":3,
"doctors":40
}
result=hospitals.insert_one(item)
print(result)

'''
if hospitals.find_one({'name':'Anubhav'})==None:
    print(123)
else:
    print('DOD')
    '''
'''
client = MongoClient('mongodb://localhost:27017')
db = client['mydatabase']

courses=db.courses #CREATING COLLECTION OR TABLE
print(courses)
'''
'''
#INSERT 1 ITEM
course={"author":"Anubhav","name":"Python","price":120}
result=courses.insert_one(course)
print(result)

if result.acknowledged:
    print("Course added. ID is",result.inserted_id)
'''
'''
#INSERT MULTIPLE ITEMS
Carr=[{"author":"Anubhav","name":"Python","price":120},
      {"author":"Ayushman","name":"Team Building","price":120},
      {"author":"Anurag","name":"ML","price":120}]
results=courses.insert_many(Carr)
for i in results.inserted_ids:
    print(str(i))
'''
'''
#FETCH 1 ITEM
course=courses.find_one()
print(course)
'''
'''
#FETCH ALL ITEM
allcourse=courses.find()
print(allcourse)
for i in allcourse:
    print(i['author'])
'''
'''
#FILTERS
allcourse=courses.find({'author':'Anubhav',
                        'price':{'$gt':130}
                        })
print(allcourse)
for i in allcourse:
    print(i['author'])

'''
'''
#SORTING
allcourse=courses.find().sort('author',1) #1=> Ascending, -1=>Descending
#allcourse=courses.find().sort([('author',-1),('price',1)])
print(allcourse)
for i in allcourse:
    print(i['author']," - ",i['name'])
'''
'''
#LIMIT NUMBER OF ENTRIES
allcourse=courses.find().limit(3)
#allcourse=courses.find().skip(3) #Skip 3 entries and start from 4th
print(allcourse)
for i in allcourse:
    print(i['author']," - ",i['name'])
'''

















