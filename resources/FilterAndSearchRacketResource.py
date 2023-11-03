# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:19:58 2023

@author: SybilleDarbin
"""

from sqlite3 import ProgrammingError
from flask_restful import Resource, reqparse
from models.FrameworkModel import commit, save_to_db_with_flush
from models.ShopMasterModel import ShopMasterModel
from resources.FrameworkResource import Authorization,IsAuthenticate
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models.WebsiteRacketMasterModel import  RacketMasterModel
from models.WebsiteShopTestingRacketModel import  ShopTestRacketModel
from models.WebsiteShopTestingRacketQRCodeDetailModel import  ShopTestRacketQRCodeDetailModel
from models.WebsiteQRCodeMasterModel import QRCodeMasterModel
from models.FilterAndSearchRacketModel import RacketTestingFilterView
from models.FilterAndSearchRacketMasterModel import RacketMasterFilterView
from datetime import datetime#, date
import datetime as pydt
import json
from sqlalchemy import true

# today = date.today()

class RacketTestingFilter(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                Page = data['Page']
                DisplayCondition = data['DisplayCondition']
                OutputVariable = data['OutputVariable']
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                if DisplayCondition == 1:
                    RacketDetails = RacketTestingFilterView.SearchRacket(ShopID, Page, data)
                else:
                    RacketDetails = RacketTestingFilterView.RacketFilterListAccodingToSelectionForFilterData(ShopID, data,Page)
            except SyntaxError as e:
                error = str(e.__dict__['orig'])
                print (error)
                return {"message": "An error occurred while fetching Order List details."}, 500  #error 
            if RacketDetails:
                if DisplayCondition == 1:
                    return RacketDetails
                else:
                    if OutputVariable == 1:
                        return RacketDetails    
                    if OutputVariable == 2:
                        return RacketDetails        
                    if OutputVariable == 3:
                        return RacketDetails     
                    if OutputVariable == 4:
                        return RacketDetails     
                    if OutputVariable == 5:
                        return RacketDetails    
                    if OutputVariable == 7:
                        return RacketDetails
            return  json.loads('[]'), 200 
        return {'message':'token not valid'}
    
        
class RacketMasterFilter(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                Page = data['Page']
                DisplayCondition = data['DisplayCondition']
                OutputVariable = data['OutputVariable']
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                if DisplayCondition == 1:
                    RacketDetails = RacketMasterFilterView.SearchRacket(ShopID, Page, data)
                else:
                    RacketDetails = RacketMasterFilterView.RacketFilterListAccodingToSelectionForFilterData(ShopID, data, Page)
            except SyntaxError as e:
                error = str(e.__dict__['orig'])
                print (error)
                return {"message": "An error occurred while fetching Order List details."}, 500  #error 
            if RacketDetails:
                if DisplayCondition == 1:
                    return RacketDetails
                else:
                    if OutputVariable == 1:
                        return RacketDetails    
                    if OutputVariable == 2:
                        return RacketDetails        
                    if OutputVariable == 3:
                        return RacketDetails     
                    if OutputVariable == 4:
                        return RacketDetails     
                    if OutputVariable == 5:
                        return RacketDetails    
                    if OutputVariable == 7:
                        return RacketDetails
            return  json.loads('[]'), 200 
        return {'message':'token not valid'}
    
