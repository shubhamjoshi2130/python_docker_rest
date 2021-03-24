from flask import Flask,jsonify,request
from flask_restful import Api, Resource
from pymongo import MongoClient


print(__name__)
app=Flask(__name__)
api=Api(app)


client=MongoClient("mongodb://db:27017")

db=client.aNewDB

UserNum=db["userNum"]

UserNum.insert({
    'num_of_users':0,    
})

class Visit(Resource):
    def get(self):
        prev_num=UserNum.find({})[0]['num_of_users']
        prev_num += 1
        UserNum.update({},{"$set":{"num_of_users":prev_num}})
        return str("Hello user" + str(prev_num))

class Add(Resource):

    def checkPostedData(self,postedData,functionName):
        if(functionName=="add"):
            if ('x' not in postedData) or ('y' not in postedData):
                return 301
            else:
                return 200


    def post(self):
        postedData=request.get_json()
        status_code=self.checkPostedData(postedData,"add")
        
        if status_code!=200:
            return jsonify({'Message':'An error has occured','StatusCode':301})

        x=postedData['x']
        y=postedData['y']
        x,y=int(x),int(y)

        return jsonify({'Message':x+y,'StatusCode':200})
    
api.add_resource(Add,"/add2")
api.add_resource(Visit,"/hello")

class Substract(Resource):
    pass

class Multiply(Resource):
    pass

class Divide(Resource):
    pass

if __name__=="__main__":
    app.run(host="0.0.0.0",port=80,debug=True)