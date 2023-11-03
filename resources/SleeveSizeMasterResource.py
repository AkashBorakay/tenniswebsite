from flask_restful import Resource, reqparse
from flask import request, jsonify, json
from models.SleeveSizeMasterModel import SleeveSizeMasterModel
from sqlalchemy.exc import SQLAlchemyError
#from models.ShopMasterModel import ShopMasterModel
from resources.FrameworkResource import Authorization, IsAuthenticate



class SleeveSizeList(Resource):
    def get(self):
        if IsAuthenticate(request):
            try:
                SleeveSizeList = SleeveSizeMasterModel.GetSleeveSizeList()
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 500  #error        
            return jsonify([sleevesizelist.json() for sleevesizelist in SleeveSizeList])
        return {'message':'token not valid'}   