from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource,reqparse
from flask import request,jsonify, abort
from models.FrameworkModel import save_to_db
from resources.FrameworkResource import Authorization, IsAuthenticate
from models.RacketStatusMasterModel import RacketStatusMasterModel

import json

class RacketStatusMaster(Resource):
         
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                RacketStatusMaster  = RacketStatusMasterModel.GetRacketStatusMaster(ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Racket Status details."}, 500  #error  
            if RacketStatusMaster:
                return jsonify([racketstatus.json() for racketstatus in RacketStatusMaster])
            return json.loads('{}'), 200 
        return {'message':'token not valid'}

    def post(self):
        if IsAuthenticate(request):
            data = request.get_json()
            RacketStatusMaster = RacketStatusMasterModel(**data)
            try:
                save_to_db(RacketStatusMaster)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred inserting the Racket Status details."}, 500 #error
            return RacketStatusMaster.json()
        return {'message':'token not valid'}