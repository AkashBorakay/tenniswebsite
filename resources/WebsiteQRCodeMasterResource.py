# -*- coding: utf-8 -*-

from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource,reqparse
from flask import request,jsonify, abort
from models.FrameworkModel import save_to_db
from resources.FrameworkResource import Authorization, IsAuthenticate
from models.WebsiteQRCodeMasterModel import QRCodeMasterModel

import json

# class CheckQRCode(Resource):
         
#     def get(self):
#         if IsAuthenticate(request):
#             try:
#                 QRCodeID = request.args.get('QRCodeID')
#                 ShopID = request.headers['ShopID']
#                 QRCodeDecrypted  = QRCodeMasterModel.CheckQRcode(ShopID,QRCodeID)
#             except SQLAlchemyError as e:
#                 error = str(e.__dict__['orig'])
#                 return {"message": "An error occurred while fetching QRCode details."}, 500  #error  
#             if QRCodeDecrypted:
#                 return QRCodeDecrypted.json()
#             return {'message':'QRCode not found'}
#         return {'message':'token not valid'}
    
    
class CheckQRCodeDecrypted(Resource):
         
    def get(self):
        if IsAuthenticate(request):
            try:
                DecryptQRCode = request.args.get('DecryptQRCode')
                ShopID = request.headers['ShopID']
                QRCodeDecrypted  = QRCodeMasterModel.ValidateQRcode(ShopID, DecryptQRCode)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching QRCode details."}, 500  #error  
            if QRCodeDecrypted:
                return QRCodeDecrypted.json()
            return {'message':'QRCode not found'}
        return {'message':'token not valid'}