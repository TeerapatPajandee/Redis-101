import os
import json
import redis
from flask import Flask,request,jsonify

app = Flask(__name__)
db=redis.StrictRedis(
        host='10.100.2.136',
        port=6379,
        password='KAKhif54289',
        decode_responses=True
    )

# Get Show All #
@app.route('/' , methods = ['GET']) 
def GetAllKey():
    key = db.keys()
    print(key)
    allkeys = []
    for r in key :
        allkeys.append(db.hgetall(r))
    return jsonify(allkeys)

# Get Only One #
@app.route('/<Key>' , methods=['GET'])
def GetSingelKey(Key):
    SingleKey = db.hgetall(Key)
    if(SingleKey):
        return SingleKey
    else:
        return "Key : "+Key+" is not found"

# Insert #
@app.route('/insert' , methods=['POST'])
def CreateData():
    id        = request.json['id']
    TypeCard  = request.json['TypeCard']
    CodeStart = request.json['CodeStart']
    CodeEnd   = request.json['CodeEnd']
    User = {"id":id, "TypeCard":TypeCard , "CodeStart":CodeStart , "CodeEnd":CodeEnd}
    db.hmset(id,User)
    return "Create Success"

# Update #
@app.route('/update/<Key>' , methods=['PUT'])
def UpdateData(Key):
    if(db.keys(Key)):
        TypeCard  = request.json['TypeCard']
        CodeStart = request.json['CodeStart']
        CodeEnd   = request.json['CodeEnd']
        ID = {"TypeCard":TypeCard , "CodeStart":CodeStart , "CodeEnd":CodeEnd}
        db.hmset(Key,ID)
        return "Update Success"
    else :
        return "Update fail, Key : "+Key+" is not found"

# Delete #
@app.route('/del/<Key>' , methods=['DELETE'])
def DeleteData(Key):
    db.delete(Key)
    return "Delete Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
