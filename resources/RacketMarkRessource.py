# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 17:07:13 2023

@author: SybilleDarbin
"""

from sqlite3 import ProgrammingError
from flask_restful import Resource, reqparse
from models.FrameworkModel import commit, save_to_db_with_flush
from models.ShopMasterModel import ShopMasterModel
from resources.FrameworkResource import Authorization,IsAuthenticate
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models.WebsiteRacketMarkModel import  RacketMarkModel, RacketMarkAvg

# from models.WebsiteRacketMasterModel import  RacketMasterModel
# from models.WebsiteShopTestingRacketModel import  ShopTestRacketModel
# from models.WebsiteShopTestingRacketQRCodeDetailModel import  ShopTestRacketQRCodeDetailModel
# from models.WebsiteQRCodeMasterModel import QRCodeMasterModel
# from models.WebsiteRacketBookingDetailModel import RacketBookingDetailMasterModel
from datetime import datetime
import datetime as pydt
import json
from sqlalchemy import true

class Racket_Marks(Resource):
    
    def put(self):
            try:
                data = request.get_json()
                CustomerID = data['CustomerID']
                MasterRacketID = data['MasterRacketID']
                Mark = data['Mark']
                Comment = data['Comment']
                UpdateMark = RacketMarkModel.UpdateGrade(CustomerID, MasterRacketID, Mark, Comment)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating Racket details."}, 500  #error        
            if UpdateMark:
                return  {"Mark": UpdateMark}
            else:
                return {"message": "No rating was save in the database"} 
            # return json.loads('{}'), 200 #('{}', 200)
        
            
    def post(self):
        data = request.get_json()
        MasterRacketID = data["MasterRacketID"]
        CustomerID = data["CustomerID"]
        check = RacketMarkModel.CheckMarkByCustomerForRacketExistBeforeInsert(MasterRacketID, CustomerID)
        if check is not None:
            return {"message": "You have already put a grade"}
        else:
            SaveMarkDetail = RacketMarkModel(**data)
            MarkID = save_to_db_with_flush(SaveMarkDetail)
            try:
                commit()
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred inserting the mark details."}, 200 #error
            return {"MarkID":   MarkID }, 201 
    
    
    def get(self):
        try:
            Mark  = RacketMarkAvg.GetMarks()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching Mark details."}, 500
        if Mark:
            return jsonify({"result":[item.jsonMark() for item in Mark]})
        return  json.loads('[]'), 200 

class Racket_Marks_Info(Resource):    
    def get(self):
        try:
            Mark  = RacketMarkModel.GetMarksInfo()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching Mark details."}, 500
        if Mark:
            return jsonify({"result":[item.json() for item in Mark]})
        return  json.loads('[]'), 200 
    # class Racket_Marks_Shop(Resource): 
    
#     def get(self):
#         if IsAuthenticate(request):
#             try:
#                 ShopID = request.headers['ShopID']
#                 RacketMasterID = request.args.get('RacketMasterID')
#                 MarkShop  = RacketMarkModel.GetMarksShop(ShopID, RacketMasterID)
#             except SQLAlchemyError as e:
#                 error = str(e.__dict__['orig'])
#                 return {"message": "An error occurred while fetching Mark details."}, 500
#             if MarkShop:
#                 return jsonify({"result":[item.json() for item in MarkShop]})
#             return  json.loads('[]'), 200 
#         return {'message':'token not valid'}
    
# class Racket_Marks_Client(Resource):
    
#     def get(self):
#             try:
#                 RacketMasterID = request.args.get('RacketMasterID')
#                 CustomerID = request.args.get("CustomerID")
#                 MarkCustomer  = RacketMarkModel.GetMarksClient(CustomerID, RacketMasterID)
#             except SQLAlchemyError as e:
#                 error = str(e.__dict__['orig'])
#                 return {"message": "An error occurred while fetching Mark details."}, 500
#             if MarkCustomer:
#                 return MarkCustomer.json()
#             return  json.loads('[]'), 200 