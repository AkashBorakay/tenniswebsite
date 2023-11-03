from flask_restful import Resource, reqparse
from flask import request, jsonify, json
from models.ShopTimingMasterModel import ShopTimingMasterModel
from sqlalchemy.exc import SQLAlchemyError
from resources.FrameworkResource import Authorization, IsAuthenticate

class ShopTimingList (Resource):

    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                Shop_Timing_Master = ShopTimingMasterModel.GetShopTiming(ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop Timing details."}, 500  #error
            if Shop_Timing_Master:
                return jsonify({"result":[shop_timing_master.json() for shop_timing_master in Shop_Timing_Master]})
            return {"message": "No shop time is setup please ask Administrator to setup it for first time"}, 200 
        return {'message':'token not valid'} 

    def put(self):
         ShopTiming= None
         if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                ShopTiming = ShopTimingMasterModel.UpdateShopTimingList(ShopID, data)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while updating Shop Timings."}, 500  #error        
            if ShopTiming: 
                return  {'ShopID': ShopID}  
            return {"message": "No shop time is setup please ask Administrator to setup it for first time"}, 200
         return {'message':'token not valid'}  
