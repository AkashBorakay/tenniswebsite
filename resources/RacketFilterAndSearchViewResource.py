from sqlite3 import ProgrammingError
from flask_restful import Resource, reqparse
from models.FrameworkModel import commit, save_to_db_with_flush
from resources.FrameworkResource import Authorization,IsAuthenticate
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models.ShopMasterModel import ShopMasterModel
from models.WebsiteRacketMasterModel import  RacketMasterModel
from models.WebsiteShopTestingRacketModel import  ShopTestRacketModel
from models.WebsiteShopTestingRacketQRCodeDetailModel import  ShopTestRacketQRCodeDetailModel
from models.WebsiteQRCodeMasterModel import QRCodeMasterModel
from models.RacketFilterAndSearchView import RacketFilterAndSearchView
from datetime import datetime
import datetime as pydt
import json
from sqlalchemy import true



class RacketFilterAccordingToSelection(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                Page = data['Page']
                DisplayCondition = data['DisplayCondition']
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                if DisplayCondition == 1:
                    RacketDetails = RacketFilterAndSearchView.SearchRacket(ShopID, Page, data)
                elif DisplayCondition == 3:
                    RacketDetails = RacketFilterAndSearchView.SearchRacketAsPerUniqueName(ShopID, Page, data)
                else:
                    RacketDetails = RacketFilterAndSearchView.RacketFilterListAccodingToSelectionForFilterData(ShopID, data,Page)
            except IsADirectoryError as e:
                error = str(e.__dict__['orig'])
                print (error)
                return {"message": "An error occurred while fetching Order List details."}, 500  #error 
            if RacketDetails:
                return RacketDetails                                                  
            return  json.loads('[]'), 200 
        return {'message':'token not valid'}
    
    