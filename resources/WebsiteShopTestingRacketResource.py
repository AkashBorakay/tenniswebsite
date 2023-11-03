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
from models.WebsiteRacketBookingDetailModel import RacketBookingDetailMasterModel
from datetime import datetime
import datetime as pydt
import json
from sqlalchemy import true


# class AllTestRacketForShop(Resource):
    
#     def get(self):
#         if IsAuthenticate(request):
#             try:
#                 ShopID = request.headers['ShopID']
#                 ShopTestingRackets = ShopTestRacketModel.GetAllTestingRacketForShop(ShopID)
#             except SQLAlchemyError as e:    
#                 error = str(e.__dict__['orig'])
#                 return {"message": "An error occurred while fetching all testing racket for shop."}, 200  #error
#             if ShopTestingRackets:
#                 return jsonify([item.json(ShopID) for item in ShopTestingRackets])
#             else:
#                 return {'message':'problem while fetching all testing racket for shop.'}
#         return {'message':'token not valid'}
    
class RacketDetail(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            data = request.get_json()
            ShopID = request.headers['ShopID']
            QRCodeID = data["QRCodeID"]
            InsertedBy = data["InsertedBy"]
            UniqueRacketName = data["UniqueRacketName"]
            RacketStatusID = data["RacketStatusID"]
            RacketNewStatusID = data["RacketNewStatusID"]
            SleeveSizeID = data["SleeveSizeID"]
            Description = data["Description"]
            OldPrice = data["OldPrice"]
            NewPrice = data["NewPrice"]
            RacketRentalDays = data["RacketRentalDays"]
            try:
                CheckRacketIsExistOrNot = RacketMasterModel.CheckRacketExistOrNotBeforeInsert(data)
                if CheckRacketIsExistOrNot is None:
                    data.pop('QRCodeID')
                    data.pop('UniqueRacketName')
                    data.pop('RacketStatusID')
                    data.pop('RacketNewStatusID')
                    data.pop('SleeveSizeID')
                    data.pop('Description')
                    data.pop('OldPrice')
                    data.pop('NewPrice')
                    data.pop('RacketRentalDays')
                    RacketDetail = RacketMasterModel(**data)
                    RacketID=save_to_db_with_flush(RacketDetail)
                    if RacketID:
                        ShopTestRacketData=ShopTestRacketModel(ShopID,RacketID,InsertedBy,Description,OldPrice,RacketRentalDays,NewPrice)
                        ShopTestRacketID=save_to_db_with_flush(ShopTestRacketData)
                        if ShopTestRacketID:
                            ShopTestRacketQRCodeDetail=ShopTestRacketQRCodeDetailModel(ShopTestRacketID,RacketID,QRCodeID,UniqueRacketName,InsertedBy,RacketStatusID,SleeveSizeID,RacketNewStatusID)
                            ShopTestRacketQRCodeDetailID=save_to_db_with_flush(ShopTestRacketQRCodeDetail)
                            if ShopTestRacketQRCodeDetailID:
                                commit()
                                MarkQRCodeAsUsed = QRCodeMasterModel.UpdateQRCodeStatus(ShopID,QRCodeID)
                                return {'RacketID':RacketID,'ShopTestRacketID' : ShopTestRacketID,'ShopTestRacketQRCodeDetailID':ShopTestRacketQRCodeDetailID}
                            else:
                                return {'Message':'Error While Inserting Data'}
                        else:
                            return {'Message':'Error While Inserting Data'}
                    else:
                        return {'Message':'Error While Inserting Data'}
                else:
                    CheckRacketAddedForShopOrNot = ShopTestRacketModel.GetRacketByMasterRacketID(CheckRacketIsExistOrNot.id,ShopID)
                    if CheckRacketAddedForShopOrNot is None:
                        ShopTestRacketData=ShopTestRacketModel(ShopID,CheckRacketIsExistOrNot.id,InsertedBy,Description,OldPrice,RacketRentalDays,NewPrice)
                        ShopTestRacketID=save_to_db_with_flush(ShopTestRacketData)
                        if ShopTestRacketID:
                            ShopTestRacketQRCodeDetail=ShopTestRacketQRCodeDetailModel(ShopTestRacketID,CheckRacketIsExistOrNot.id,QRCodeID,UniqueRacketName,InsertedBy,RacketStatusID,SleeveSizeID,RacketNewStatusID)
                            ShopTestRacketQRCodeDetailID=save_to_db_with_flush(ShopTestRacketQRCodeDetail)
                            if ShopTestRacketQRCodeDetailID:
                                commit()
                                MarkQRCodeAsUsed = QRCodeMasterModel.UpdateQRCodeStatus(ShopID,QRCodeID)
                                return {'RacketID':CheckRacketIsExistOrNot.id,'ShopTestRacketID' : ShopTestRacketID,'ShopTestRacketQRCodeDetailID':ShopTestRacketQRCodeDetailID}
                            else:
                                return {'Message':'Error While Inserting Data'}
                        else:
                            return {'Message':'Error While Inserting Data'}
                    else:
                        ShopTestRacketQRCodeDetail=ShopTestRacketQRCodeDetailModel(CheckRacketAddedForShopOrNot.id,CheckRacketIsExistOrNot.id,QRCodeID,UniqueRacketName,InsertedBy,RacketStatusID,SleeveSizeID,RacketNewStatusID)
                        ShopTestRacketQRCodeDetailID=save_to_db_with_flush(ShopTestRacketQRCodeDetail)
                        if ShopTestRacketQRCodeDetailID:
                            commit()
                            MarkQRCodeAsUsed = QRCodeMasterModel.UpdateQRCodeStatus(ShopID,QRCodeID)
                            return {'RacketID':CheckRacketIsExistOrNot.id,'ShopTestRacketID' : CheckRacketAddedForShopOrNot.id,'ShopTestRacketQRCodeDetailID':ShopTestRacketQRCodeDetailID}
                        else:
                            return {'Message':'Error While Inserting Data'}                        
            except SQLAlchemyError  as e:
                    error = str(e.__dict__['orig'])
                    return {"message": "An error occurred while inserting the Racket details."}, 200 #error   
        return {'message':'token not valid'}
    
    def put(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                ShopTestRacketDetail = data['ShopTestRacket']
                ShopTestRacketQRCodeIDDetail = data['ShopTestRacketQRCodeDetail']
                ShopTestRacketUpdate = ShopTestRacketModel.UpdateShopTestRacket(ShopID,ShopTestRacketDetail,ShopTestRacketQRCodeIDDetail)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating Racket details."}, 500  #error        
            if ShopTestRacketUpdate:
                return  ShopTestRacketUpdate
            else:
                {"message": "An error occurred while Updating Shop Test Racket Detail."}, 500  #error      
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'} 
    
    def delete(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                UpdatedBy = data['UpdatedBy']
                ShopTestRacketQRCodeDetailID = data['ShopTestRacketQRCodeDetailID']
                CheckOrderIsOpenOrNotForTheQRCode = RacketBookingDetailMasterModel.CheckQRCodeOrder(ShopID,ShopTestRacketQRCodeDetailID)
                if CheckOrderIsOpenOrNotForTheQRCode:
                    return {"message": "An Order is open or advance booked for this Racket so kindly first modify or cancel order"}
                else:
                    DeleteRacket = ShopTestRacketModel.DeleteShopTestRacket(ShopID,ShopTestRacketQRCodeDetailID,UpdatedBy)            
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while deleting Racket details."}, 500  #error        
            if DeleteRacket != 0:
                return  DeleteRacket
            else:
                {"message": "An error occurred while deleting Shop Test Racket Detail."}, 500  #error      
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}   
    
class GetRacketDetailAsPerUniqueValues(Resource):
        
    def post(self):
        if IsAuthenticate(request):
            data = request.get_json()
            ShopID = request.headers['ShopID']
            try:
                CheckRacketIsExistOrNot = RacketMasterModel.CheckRacketExistOrNotBeforeInsert(data)
                if CheckRacketIsExistOrNot:
                    return jsonify(CheckRacketIsExistOrNot.json())
                else:
                    return {"message": "No Detail Found"}                       
            except SQLAlchemyError  as e:
                    error = str(e.__dict__['orig'])
                    return {"message": "An error occurred while inserting the Racket details."}, 200 #error   
        return {'message':'token not valid'}
    
# class AssingNewQRCodeToExistingRacket(Resource):
    
#     def post(self):
#         if IsAuthenticate(request):
#             data = request.get_json()
#             ShopID = request.headers['ShopID']
#             QRCodeID = data["QRCodeID"]
#             InsertedBy = data["InsertedBy"]
#             UniqueRacketName = data["UniqueRacketName"]
#             RacketStatusID = data["RacketStatusID"]
#             RacketNewStatusID = data["RacketNewStatusID"]
#             SleeveSizeID = data["SleeveSizeID"]
#             Description = data["Description"]
#             OldPrice = data["OldPrice"]
#             NewPrice = data["NewPrice"]
#             OldShopTestRacketQRCodeDetailID = data["OldShopTestRacketQRCodeDetailID"]
#             RacketRentalDays = data["RacketRentalDays"]
#             try:
#                 CheckOrderIsOpenOrNotForTheQRCode = RacketBookingDetailMasterModel.CheckQRCodeOrder(ShopID,OldShopTestRacketQRCodeDetailID)
#                 if CheckOrderIsOpenOrNotForTheQRCode:
#                     return {"message": "An Order is open or advance booked for this Racket so kindly first modify or cancel order"}
#                 else:
#                     CheckRacketIsExistOrNot = RacketMasterModel.CheckRacketExistOrNotBeforeInsert(data)
#                     if CheckRacketIsExistOrNot is None:
#                         data.pop('QRCodeID')
#                         data.pop('UniqueRacketName')
#                         data.pop('RacketStatusID')
#                         data.pop('RacketNewStatusID')
#                         data.pop('SleeveSizeID')
#                         data.pop('Description')
#                         data.pop('OldShopTestRacketQRCodeDetailID')
#                         data.pop('OldPrice')
#                         data.pop('NewPrice')
#                         data.pop('RacketRentalDays')
#                         RacketDetail = RacketMasterModel(**data)
#                         RacketID=save_to_db_with_flush(RacketDetail)
#                         if RacketID:
#                             ShopTestRacketData=ShopTestRacketModel(ShopID,RacketID,InsertedBy,Description,OldPrice,RacketRentalDays,NewPrice)
#                             ShopTestRacketID=save_to_db_with_flush(ShopTestRacketData)
#                             if ShopTestRacketID:
#                                 ShopTestRacketQRCodeDetail=ShopTestRacketQRCodeDetailModel(ShopTestRacketID,RacketID,QRCodeID,UniqueRacketName,InsertedBy,RacketStatusID,SleeveSizeID,RacketNewStatusID)
#                                 ShopTestRacketQRCodeDetailID=save_to_db_with_flush(ShopTestRacketQRCodeDetail)
#                                 if ShopTestRacketQRCodeDetailID:
#                                     commit()
#                                     MarkQRCodeAsUsed = QRCodeMasterModel.UpdateQRCodeStatus(ShopID,QRCodeID)
#                                     GetQRCodeIDWhichWeNeedToDisable = ShopTestRacketQRCodeDetailModel.DisableOldShopTestRacketQRCodeID(OldShopTestRacketQRCodeDetailID,InsertedBy)
#                                     DisableOldQRCode = QRCodeMasterModel.DeactivateQRCodeDetail(ShopID,GetQRCodeIDWhichWeNeedToDisable,InsertedBy) 
#                                     return {'RacketID':RacketID,'ShopTestRacketID' : ShopTestRacketID,'ShopTestRacketQRCodeDetailID':ShopTestRacketQRCodeDetailID}
#                                 else:
#                                     return {'Message':'Error While Inserting Data'}
#                             else:
#                                 return {'Message':'Error While Inserting Data'}
#                         else:
#                             return {'Message':'Error While Inserting Data'}
#                     else:
#                         CheckRacketAddedForShopOrNot = ShopTestRacketModel.GetRacketByMasterRacketID(CheckRacketIsExistOrNot.id,ShopID)
#                         if CheckRacketAddedForShopOrNot is None:
#                             ShopTestRacketData=ShopTestRacketModel(ShopID,CheckRacketIsExistOrNot.id,InsertedBy,Description,OldPrice,RacketRentalDays,NewPrice)
#                             ShopTestRacketID=save_to_db_with_flush(ShopTestRacketData)
#                             if ShopTestRacketID:
#                                 ShopTestRacketQRCodeDetail=ShopTestRacketQRCodeDetailModel(ShopTestRacketID,CheckRacketIsExistOrNot.id,QRCodeID,UniqueRacketName,InsertedBy,RacketStatusID,SleeveSizeID,RacketNewStatusID)
#                                 ShopTestRacketQRCodeDetailID=save_to_db_with_flush(ShopTestRacketQRCodeDetail)
#                                 if ShopTestRacketQRCodeDetailID:
#                                     commit()
#                                     MarkQRCodeAsUsed = QRCodeMasterModel.UpdateQRCodeStatus(ShopID,QRCodeID)
#                                     GetQRCodeIDWhichWeNeedToDisable = ShopTestRacketQRCodeDetailModel.DisableOldShopTestRacketQRCodeID(OldShopTestRacketQRCodeDetailID,InsertedBy)
#                                     DisableOldQRCode = QRCodeMasterModel.DeactivateQRCodeDetail(ShopID,GetQRCodeIDWhichWeNeedToDisable,InsertedBy) 
#                                     return {'RacketID':CheckRacketIsExistOrNot.id,'ShopTestRacketID' : ShopTestRacketID,'ShopTestRacketQRCodeDetailID':ShopTestRacketQRCodeDetailID}
#                                 else:
#                                     return {'Message':'Error While Inserting Data'}
#                             else:
#                                 return {'Message':'Error While Inserting Data'}
#                         else:
#                             ShopTestRacketQRCodeDetail=ShopTestRacketQRCodeDetailModel(CheckRacketAddedForShopOrNot.id,CheckRacketIsExistOrNot.id,QRCodeID,UniqueRacketName,InsertedBy,RacketStatusID,SleeveSizeID,RacketNewStatusID)
#                             ShopTestRacketQRCodeDetailID=save_to_db_with_flush(ShopTestRacketQRCodeDetail)
#                             if ShopTestRacketQRCodeDetailID:
#                                 commit()
#                                 MarkQRCodeAsUsed = QRCodeMasterModel.UpdateQRCodeStatus(ShopID,QRCodeID)
#                                 GetQRCodeIDWhichWeNeedToDisable = ShopTestRacketQRCodeDetailModel.DisableOldShopTestRacketQRCodeID(OldShopTestRacketQRCodeDetailID,InsertedBy)
#                                 DisableOldQRCode = QRCodeMasterModel.DeactivateQRCodeDetail(ShopID,GetQRCodeIDWhichWeNeedToDisable,InsertedBy)                            
#                                 return {'RacketID':CheckRacketIsExistOrNot.id,'ShopTestRacketID' : CheckRacketAddedForShopOrNot.id,'ShopTestRacketQRCodeDetailID':ShopTestRacketQRCodeDetailID}
#                             else:
#                                 return {'Message':'Error While Inserting Data'}                        
#             except SQLAlchemyError  as e:
#                     error = str(e.__dict__['orig'])
#                     return {"message": "An error occurred while inserting the Racket details."}, 200 #error   
#         return {'message':'token not valid'}
class AssingNewQRCode(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            data = request.get_json()
            ShopID = request.headers['ShopID']
            QRCodeID = data["QRCodeID"]
            OldShopTestRacketQRCodeDetailID = data["OldShopTestRacketQRCodeDetailID"]
            InsertedBy = data["InsertedBy"]
            OldQRCodeID = data["OldQRCodeID"]
            try:
                CheckQrRacketAvailable = ShopTestRacketQRCodeDetailModel.CheckQR_RacketAvailable(ShopID, OldQRCodeID, OldShopTestRacketQRCodeDetailID)
                if CheckQrRacketAvailable is None:
                    return {"message": "An Order is open for this Racket so kindly first modify "}
                else:
                    #get all information to duplicates
                    GetRacket = ShopTestRacketQRCodeDetailModel.Get_Qr_Racket_Info(ShopID, OldQRCodeID)     
                    if GetRacket:
                        #Create the duplicates
                        #check master table if racket master exist
                        CheckRacketIsExistOrNot = RacketMasterModel.CheckRacketExistBeforeInsert(GetRacket.MasterTestingRacketID)
                        if CheckRacketIsExistOrNot is not None:
                            #check master table if racket master exist with shop info
                            CheckRacketAddedForShopOrNot = ShopTestRacketModel.GetRacketByMasterRacketID(CheckRacketIsExistOrNot.id, ShopID)
                            if CheckRacketAddedForShopOrNot is not None:
                                ShopTestRacketQRCodeDetail = ShopTestRacketQRCodeDetailModel(CheckRacketAddedForShopOrNot.id, CheckRacketIsExistOrNot.id, QRCodeID, 
                                                                                             GetRacket.UniqueRacketName, InsertedBy, GetRacket.RacketStatusID, GetRacket.SleeveSizeID, GetRacket.RacketNewStatusID)
                                ShopTestRacketQRCodeDetailID=save_to_db_with_flush(ShopTestRacketQRCodeDetail)
                                if ShopTestRacketQRCodeDetailID:
                                    commit()
                                    MarkQRCodeAsUsed = QRCodeMasterModel.UpdateQRCodeStatus(ShopID,QRCodeID)
                                    #update the data for qr to del
                                    QrCodeUpdate = QRCodeMasterModel.DeactivateQRCodeDetail(ShopID, OldQRCodeID, InsertedBy)
                                    #update the data for ShopTestRacketQRDetailID to del
                                    ShopTestRacketQRDetailUpdate = ShopTestRacketQRCodeDetailModel.DisableOldShopTestRacketQRCodeID(OldShopTestRacketQRCodeDetailID, InsertedBy)   
                                    return {'RacketID':CheckRacketIsExistOrNot.id,'ShopTestRacketID' : CheckRacketAddedForShopOrNot.id,'ShopTestRacketQRCodeDetailID':ShopTestRacketQRCodeDetailID}
                                else:
                                    return {'Message':'Error While Inserting Data'}        
                            else:
                                return {'message':'step1'}
                        else:
                            return {'message':'step2'}
                    else:
                        return {'message':'step3'}
                                
            except SQLAlchemyError  as e:
                    error = str(e.__dict__['orig'])
                    return {"message": error}, 200 #error   
        else :
            return {'message':'token not valid'}
    
class RacketDataBySuperAdmin(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            data = request.get_json()
            ShopID = request.headers['ShopID']
            InsertedBy = data["InsertedBy"]
            Description = data["Description"]
            OldPrice = data["OldPrice"]
            NewPrice = data["NewPrice"]
            RacketRentalDays = data["RacketRentalDays"]
            try:
                CheckRacketIsExistOrNot = RacketMasterModel.CheckRacketExistOrNotBeforeInsert(data)
                if CheckRacketIsExistOrNot is None:
                    data.pop('Description')
                    data.pop('NewPrice')
                    data.pop('OldPrice')
                    data.pop('RacketRentalDays')
                    RacketDetail = RacketMasterModel(**data)
                    RacketID=save_to_db_with_flush(RacketDetail)
                    if RacketID:
                        ShopTestRacketData=ShopTestRacketModel(ShopID,RacketID,InsertedBy,Description,OldPrice,RacketRentalDays,NewPrice)
                        ShopTestRacketID=save_to_db_with_flush(ShopTestRacketData)
                        if ShopTestRacketID:
                            commit()
                            return {'RacketID':RacketID,'ShopTestRacketID' : ShopTestRacketID}
                        else:
                            return {'Message':'Error While Inserting Data'}
                    else:
                        return {'Message':'Error While Inserting Data'}
                else:
                    CheckRacketAddedForShopOrNot = ShopTestRacketModel.GetRacketByMasterRacketID(CheckRacketIsExistOrNot.id,ShopID)
                    if CheckRacketAddedForShopOrNot is None:
                        ShopTestRacketData=ShopTestRacketModel(ShopID,CheckRacketIsExistOrNot.id,InsertedBy,Description,OldPrice,RacketRentalDays,NewPrice)
                        ShopTestRacketID=save_to_db_with_flush(ShopTestRacketData)
                        if ShopTestRacketID:
                            commit()
                            return {'RacketID':CheckRacketIsExistOrNot.id,'ShopTestRacketID' : ShopTestRacketID}
                        else:
                            return {'Message':'Error While Inserting Data'} 
                    else:
                        return {'Message':'Data already available in database'}                       
            except SQLAlchemyError  as e:
                    error = str(e.__dict__['orig'])
                    return {"message": "An error occurred while inserting the Racket details."}, 200 #error   
        return {'message':'token not valid'}
    
    def delete(self):
        if IsAuthenticate(request):
            data = request.get_json()
            ShopID = request.headers['ShopID']
            UpdatedBy = data["UpdatedBy"]
            ShopTestRacketID = data["ShopTestRacketID"]
            try:                
                ShopTestRacketDetail = ShopTestRacketModel.DeleteShopTestRacketBySuperAdmin(ShopID,UpdatedBy,ShopTestRacketID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while deleting shop test racket"},200   #error        
            if ShopTestRacketDetail: 
                return  {'ShopTestRacketID': ShopTestRacketDetail.id},200  
            else:
                return {"Message":"No racket found using given shop test racket ID"},200 
        return {'message':'token not valid'}
    
    
    def put(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                UpdatedBy = data["UpdatedBy"]
                Description = data["Description"]
                OldPrice = data["OldPrice"]
                NewPrice = data["NewPrice"]
                RacketRentalDays = data["RacketRentalDays"]
                MasterTestingRacketID = data["MasterTestingRacketID"]
                ShopTestingRacketid = data["ShopTestingRacketid"]
                data.pop('Description')
                data.pop('NewPrice')
                data.pop('OldPrice')
                data.pop('RacketRentalDays')
                data.pop('ShopTestingRacketid')
                RacketMasterDataUpdate = RacketMasterModel.UpdateRacketMasterByAdmin(data)
                CheckRacketAddedForShopOrNot = ShopTestRacketModel.GetRacketByMasterRacketID(MasterTestingRacketID, ShopID)
                if CheckRacketAddedForShopOrNot is None:
                    ShopTestRacketData=ShopTestRacketModel(ShopID, MasterTestingRacketID, UpdatedBy, Description, OldPrice, RacketRentalDays, NewPrice)
                    ShopTestRacketID=save_to_db_with_flush(ShopTestRacketData)
                    if ShopTestRacketID:
                        commit()
                        ShopTestingRacketid = ShopTestRacketID
                RacketShopDataUpdate = ShopTestRacketModel.UpdateShopTestRacketMasterByAdmin(ShopTestingRacketid,ShopID,Description,OldPrice,NewPrice,RacketRentalDays,UpdatedBy)
            except SQLAlchemyError as e:    
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating racket master data"}, 200
            if RacketMasterDataUpdate and RacketShopDataUpdate:
                return {'MasterTestingRacketID':RacketMasterDataUpdate.id,'RacketShopDataUpdate':RacketShopDataUpdate.id}
            else:
                {"message": "An error occurred while Updating racket master data"}, 200                
        return {'message':'token not valid'} 
    
class GetRacketDataBySuperAdmin(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            ShopID = request.headers['ShopID']
            data = request.get_json()
            NameFilter = data['NameFilter']
            Page = data['Page']
            Page = 1 if Page is None else int(Page)
            try:                
                ShopTestRacketDetail = ShopTestRacketModel.GetAllTestingRacketOfShopForAdmin(ShopID,Page,NameFilter)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching shop test racket"},200   #error        
            if ShopTestRacketDetail: 
                return ShopTestRacketDetail
                # return jsonify([shoptestingracket.jsonForDashboard() for shoptestingracket in ShopTestRacketDetail])
            else:
                return {"Message":"An error occurred while fetching shop test racket"},200 
        return {'message':'token not valid'}
            
            

class CheckQRCodeMessage(Resource):
         
    def get(self):
        if IsAuthenticate(request):
            try:
                QRCodeDecrypted = request.args.get('QRCodeDecrypted')
                ShopID = request.headers['ShopID']
                QRCodeDecrypted  = ShopTestRacketQRCodeDetailModel.ValidateQRcodeMessage(ShopID, QRCodeDecrypted)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching QRCode details."}, 500  #error  
            if QRCodeDecrypted:
                return QRCodeDecrypted.jsonMessageQr(ShopID)
            return {'message':'QRCode not found'}
        return {'message':'token not valid'}
    
class RacketStatus(Resource):
     def put(self):
         if IsAuthenticate(request):
            try:
                 data = request.get_json()
                 ShopTestRacketQRCodeDetailID = data["ShopTestRacketQRCodeDetailID"]
                 StringerID = data["StringerID"]
                 RacketNewStatusID = data["RacketNewStatusID"]                
                 query = ShopTestRacketQRCodeDetailModel.Update_Stat(RacketNewStatusID, StringerID, ShopTestRacketQRCodeDetailID)
            except SQLAlchemyError as e:    
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating racket master data"}, 200
            if query:
                return {'message': query}
            else:
                return {"message": "query is empty"}, 200                
         return {'message':'token not valid'} 