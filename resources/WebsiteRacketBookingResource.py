from multiprocessing import Value
from sqlalchemy.exc import SQLAlchemyError
from resources.FrameworkResource import Authorization, IsAuthenticate
from flask_restful import Resource, reqparse
from flask import request, jsonify, json
from models.FrameworkModel import *
from models.WebsiteRacketBookingDetailModel import RacketBookingDetailMasterModel
from models.WebsiteRacketBookingModel import RacketBookingMasterModel
from models.WebsiteContractMasterModel import ContractMasterModel
from models.WebsiteQRCodeMasterModel import QRCodeMasterModel
from datetime import datetime
import datetime as pydt
from hashlib import sha256

class PlaceOrder(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                RacketBookingDetails = data['RacketBookingDetail']
                data.pop('RacketBookingDetail')
                data['ShopID']=ShopID
                RacketBookingMaster = RacketBookingMasterModel(**data)
                RacketBookingMasterID = save_to_db_with_flush(RacketBookingMaster)
                if RacketBookingMasterID:
                    for RacketBookingDetail in RacketBookingDetails:
                        RacketBookingDetail['ShopID'] = ShopID
                        RacketBookingDetail['InsertBy'] = data['InsertedBy']
                        RacketBookingDetail['CustomerID'] = data['CustomerID']
                        RacketBookingDetail['BookingID'] = RacketBookingMasterID
                        RacketBookingDetailMaster = RacketBookingDetailMasterModel(**RacketBookingDetail)
                        RacketBookingDetailMasterID = save_to_db_with_flush(RacketBookingDetailMaster)
                        if RacketBookingDetailMasterID:
                            commit()
                            if RacketBookingDetail['ShopTestRacketQRCodeDetailID'] is not None:
                                UpdateStatusOfBookedRacket = RacketBookingDetailMasterModel.UpdateStatusinRacketQRCodeDetailTable(RacketBookingDetail['ShopTestRacketQRCodeDetailID'])
                        else:
                            return {'message':'Error while inserting order detail'}, 200  #error 
                    return {'BookingID': RacketBookingMaster.id}                       
                else:
                    return {'message':'Error while inserting order detail'}, 200  #error
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while updating Customer details."}, 200  #error          
        else:
            return {'message':'token not valid'}
        
class HandOverRacketByScanningQRCode(Resource):    
    
    def put(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                HandOverRacket = RacketBookingDetailMasterModel.HandOverRacketToCustomerByScanningQRCode(ShopID,**data)
                QrCodeUsed = QRCodeMasterModel.QrCodeIsUsed(ShopID, data['QRCodeID'])
                if HandOverRacket == False:
                    return {"message":"Sleeve Size of scan racket and booked racket is different"}
                else:
                    return {"message":"ok", "BookingDetailID":HandOverRacket}
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 200  #error
        else:
            return {'message':'token not valid'}
        
class ReturnRacketToShop(Resource):
    
    def put(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                ReturnRacketToShop = RacketBookingDetailMasterModel.ReturnRacketToShop(ShopID,**data)
                QrCodeUsed = QRCodeMasterModel.QrCodeIsUsed(ShopID, data['QRCodeID'])
                if ReturnRacketToShop == False:
                    return {"message":"Sleeve Size of scan racket and booked racket is different"}
                else:
                    return {"BookingDetailID":ReturnRacketToShop}
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 200  #error
        else:
            return {'message':'token not valid'}
        
        