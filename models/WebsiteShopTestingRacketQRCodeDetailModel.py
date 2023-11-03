from db import db
from models.FrameworkModel import *
from sqlalchemy.sql.expression import outerjoin,join
from sqlalchemy.orm import backref, relationship
from flask import request,jsonify, abort
from models.SleeveSizeMasterModel import SleeveSizeMasterModel
from models.WebsiteQRCodeMasterModel import QRCodeMasterModel



class ShopTestRacketQRCodeDetailModel(db.Model):
    __tablename__ = 'tp_website_shop_testing_racket_QRCode_detail'

    id = db.Column(db.Integer, primary_key=True)
    MasterTestingRacketID = db.Column(db.Integer)
    QRCodeID = db.Column(db.Integer)
    UniqueRacketName = db.Column(db.String(2000))
    Comment = db.Column(db.String(2000))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    DeactiveDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    IsActive = db.Column(db.Boolean) 
    ShopTestRacketID = db.Column(db.Integer)
    RacketStatusID = db.Column(db.Integer)
    RacketNewStatusID = db.Column(db.Integer)
    SleeveSizeID = db.Column(db.Integer)
    NeedToRepair = db.Column(db.Boolean)
    IsRacketTakenByCustomer = db.Column(db.Boolean)

    def __init__(self,ShopTestRacketID,MasterTestingRacketID, QRCodeID, UniqueRacketName, InsertedBy,RacketStatusID,SleeveSizeID,RacketNewStatusID):
        self.ShopTestRacketID = ShopTestRacketID
        self.MasterTestingRacketID = MasterTestingRacketID
        self.QRCodeID = QRCodeID
        self.UniqueRacketName = UniqueRacketName
        self.InsertedBy = InsertedBy
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.DeactiveDate = None
        self.IsActive = 1
        self.IsDeleted = 0
        self.RacketStatusID = RacketStatusID
        self.SleeveSizeID = SleeveSizeID
        self.NeedToRepair = 0
        self.IsRacketTakenByCustomer = 0
        self.RacketNewStatusID = RacketNewStatusID
        
    def json(self,ShopID):
        SleeveSizeName = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(self.SleeveSizeID)
        QRCodeName = QRCodeMasterModel.CheckQRcode(ShopID,self.QRCodeID)
        return{
            'ShopTestRacketQRCodeDetailID':self.id,
            'MasterTestingRacketID' : self.MasterTestingRacketID,
            'QRCodeID' : self.QRCodeID,
            'QRCodeName' : QRCodeName.DecryptQRCode,
            'QRDate' : QRCodeName.UsedDate.strftime('%Y-%m-%d'),
            'UniqueRacketName' : self.UniqueRacketName,
            'ShopTestRacketID' : self.ShopTestRacketID,
            'RacketStatusID' : self.RacketStatusID,
            'RacketNewStatusID' : self.RacketNewStatusID,
            'SleeveSizeID' : self.SleeveSizeID,
            'SleeveSizeName' : SleeveSizeName,
            'NeedToRepair' : self.NeedToRepair,
            'IsRacketTakenByCustomer' : self.IsRacketTakenByCustomer     
        }        
    
    def jsonMessageQr(self,ShopID):
        QRCodeName = QRCodeMasterModel.CheckQRcode(ShopID, self.QRCodeID)
        if (QRCodeName.IsUsed == 1) & (self.IsRacketTakenByCustomer == 0) & (self.NeedToRepair == 0):
            Message = 0
        elif (QRCodeName.IsUsed == 1) & (self.IsRacketTakenByCustomer == 0) & (self.NeedToRepair == 1) :
            Message = 3
        elif (QRCodeName.IsUsed == 1) & (self.IsRacketTakenByCustomer == 1) :
            Message = 1
        elif QRCodeName.IsUsed == 0:
            Message = 2
        return{  
            'Message': Message,
            'ShopTestRacketQRCodeDetailID':self.id,
            'NomRaquette':self.UniqueRacketName,
            'QrCodeID': self.QRCodeID
        }
    
    def SleeveSize(self, ShopID):
        SleeveSizeName = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(self.SleeveSizeID)
        SleeveSizeNameShort = SleeveSizeMasterModel.GetSleeveSizeAccordingToIDName(self.SleeveSizeID)
        QRCodeName = QRCodeMasterModel.CheckQRcode(ShopID, self.QRCodeID)
        return{
            'SleeveSizeID':self.SleeveSizeID,
            'SleeveSizeName' : SleeveSizeName,
            'SleeveSizeShortName' : SleeveSizeNameShort,
            'UniqueRacketName' : self.UniqueRacketName,
            'QRCodeID' : self.QRCodeID,
            'QrDate':QRCodeName.UsedDate.strftime('%Y-%m-%d'),
            'WebsiteShopTestRacketQRCodeDetailID' : self.id
        }
    
    def SleeveSize2(self):
        SleeveSizeName = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(self.SleeveSizeID)
        SleeveSizeNameShort = SleeveSizeMasterModel.GetSleeveSizeAccordingToIDName(self.SleeveSizeID)
        return{
            'SleeveSizeID':self.SleeveSizeID,
            'SleeveSizeShortName' : SleeveSizeNameShort,
            'SleeveSizeName' : SleeveSizeName
        }
        
    def SleeveSizeForCustomer(self):
        SleeveSizeName = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(self.SleeveSizeID)
        return{
            'SleeveSizeID':self.SleeveSizeID,
            'SleeveSizeName' : SleeveSizeName
        }
        
    @classmethod
    def GetRacketList(cls,ShopTestingRacketID, SleeveSizeID):
        query = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.SleeveSizeID == SleeveSizeID, ShopTestRacketQRCodeDetailModel.ShopTestRacketID == ShopTestingRacketID, ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        return query
        
    @classmethod
    def GetSleeveSizeForRacket(cls,ShopTestingRacketID, ShopID):
        SleeveSizeDetail = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.ShopTestRacketID == ShopTestingRacketID, ShopTestRacketQRCodeDetailModel.IsDeleted == 0)
        list =[]
        for val in ([item.SleeveSize(ShopID) for item in SleeveSizeDetail]):
            if val in list:
                continue
            else:
                list.append(val)
        return(list)
        
    @classmethod
    def GetSleeveSizeForRacket2(cls,ShopTestingRacketID):
        SleeveSizeDetail = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.ShopTestRacketID == ShopTestingRacketID, ShopTestRacketQRCodeDetailModel.IsDeleted == 0)
        list =[]
        for val in ([sleevesizedetail.SleeveSize2() for sleevesizedetail in SleeveSizeDetail]):
            if val in list:
                continue
            else:
                list.append(val)
        return(list)
    
    @classmethod
    def GetSleeveSizeListForFitler(cls,ShopTestRacketIDList):
        SleeveSizeDetail = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.ShopTestRacketID.in_(ShopTestRacketIDList), ShopTestRacketQRCodeDetailModel.IsDeleted == 0)
        list =[]
        for val in ([sleevesizedetail.SleeveSize() for sleevesizedetail in SleeveSizeDetail]):
            if val in list:
                continue
            else:
                list.append(val)
        return(list)
    
    @classmethod
    def GetSleeveSizeListOfFitlerForCustomer(cls,ShopTestRacketIDList):
        SleeveSizeDetail = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.ShopTestRacketID.in_(ShopTestRacketIDList), ShopTestRacketQRCodeDetailModel.IsDeleted == 0)
        list =[]
        for val in ([sleevesizedetail.SleeveSizeForCustomer() for sleevesizedetail in SleeveSizeDetail]):
            if val in list:
                continue
            else:
                list.append(val)
        return(list)
    
    
    @classmethod
    def GetShopTestRacketQRCodeDetail(cls,ShopTestRacketQRCodeDetailID):
        return db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.id == ShopTestRacketQRCodeDetailID,
                                                                        ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        
    @classmethod
    def GetShopTestRacketQRCodeDetailOrder(cls,ShopTestRacketQRCodeDetailID):
        return db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.id == ShopTestRacketQRCodeDetailID).first()
    @classmethod
    def GetSleeveSizeIDForRacket(cls,ShopTestRacketQRCodeDetailID):
        query = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.id == ShopTestRacketQRCodeDetailID,ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        if query is not None:
            return {"SleeveSizeID":query.SleeveSizeID,"ShopTestRacketID":query.ShopTestRacketID}
        else:
            return None
        
    @classmethod
    def DisableOldShopTestRacketQRCodeID(cls,OldShopTestRacketQRCodeDetailID,InsertedBy):
        CheckDataBeforeUpdate = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(OldShopTestRacketQRCodeDetailID)
        if CheckDataBeforeUpdate is not None:
            CheckDataBeforeUpdate.IsDeleted = 1
            CheckDataBeforeUpdate.DeactiveDate = getUTCTime()
            CheckDataBeforeUpdate.UpdatedBy = InsertedBy
            CheckDataBeforeUpdate.IsRacketTakenByCustomer = 0
        commit()
        if CheckDataBeforeUpdate is not None:
            return CheckDataBeforeUpdate.QRCodeID
        else:
            return None
        
    @classmethod
    def CountOfIdenticalShopTestRacket(cls,ShopTestRacketID):
        return db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.ShopTestRacketID == ShopTestRacketID,ShopTestRacketQRCodeDetailModel.IsDeleted == 0).count()
    
    @classmethod
    def GetShopTestRacketAsPerQrCodeID(cls,QRCodeID):
        query = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.QRCodeID == QRCodeID,ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        if query is not None:
            return query.id
        else:
            return None
        
    @classmethod
    def GetSleeveSizeAsPerShopTestRacketAsPerQrCodeID(cls, id, ShopID):
        SleeveSizeID = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.id == id, ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        SleeveSizeDetail = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(SleeveSizeID.SleeveSizeID)
        QRCodeName = QRCodeMasterModel.CheckQRcode(ShopID, SleeveSizeID.QRCodeID)
        if SleeveSizeID is not None:
            return {"SleeveSizeID":SleeveSizeID.SleeveSizeID, "SleeveSizeName":SleeveSizeDetail,
                    "UniqueRacketName":SleeveSizeID.UniqueRacketName, "QRCodeID":SleeveSizeID.QRCodeID,
                    'QrDate':QRCodeName.UsedDate.strftime('%Y-%m-%d'),
                    "WebsiteShopTestRacketQRCodeDetailID":SleeveSizeID.id, "RacketStatusID":SleeveSizeID.RacketStatusID,
                    "RacketNewStatusID":SleeveSizeID.RacketNewStatusID}
        else:
            return None
        
    @classmethod
    def CountOfIdenticalRacketWithShopTestRacketIDAndSleeveSizeID(cls,ShopTestRacketID,SleeveSizeID):
        return db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.ShopTestRacketID == ShopTestRacketID,ShopTestRacketQRCodeDetailModel.SleeveSizeID == SleeveSizeID,ShopTestRacketQRCodeDetailModel.IsDeleted == 0).count()
    
    
    @classmethod
    def ValidateQRcodeMessage(cls,ShopID, QRCodeDecrypted): 
        query = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.QRCodeID == QRCodeMasterModel.id,
                                                                         QRCodeMasterModel.DecryptQRCode == QRCodeDecrypted,
                                                                         QRCodeMasterModel.ShopID == ShopID,
                                                                         QRCodeMasterModel.IsDeleted == 0,
                                                                         ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        return query
    
    
    @classmethod
    def CheckQR_RacketAvailable(cls,ShopID, QRCodeID, ShopTestRacketQRCodeDetailID): 
        query = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.id == ShopTestRacketQRCodeDetailID,
                                                                         ShopTestRacketQRCodeDetailModel.QRCodeID == QRCodeID,
                                                                         ShopTestRacketQRCodeDetailModel.IsRacketTakenByCustomer == 0,
                                                                         ShopTestRacketQRCodeDetailModel.QRCodeID == QRCodeMasterModel.id,
                                                                         QRCodeMasterModel.ShopID == ShopID,
                                                                         QRCodeMasterModel.IsUsed == 1,
                                                                         QRCodeMasterModel.IsDeleted == 0).first()
        return query
    
    @classmethod
    def Get_Qr_Racket_Info(cls,ShopID,QRCodeID): 
        query = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.QRCodeID == QRCodeID,
                                                                         QRCodeMasterModel.id == QRCodeID,
                                                                         QRCodeMasterModel.ShopID == ShopID).first()
        return query
    
    @classmethod
    def Update_Stat(cls, RacketNewStatusID, StringerID, ShopTestRacketQRCodeDetailID):
        query = db.session.query(ShopTestRacketQRCodeDetailModel).filter(ShopTestRacketQRCodeDetailModel.id == ShopTestRacketQRCodeDetailID,
                                                                        ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        if query is not None:
            setattr(query, "UpdatedDate", getUTCTime())  
            setattr(query, "UpdatedBy", StringerID)
            setattr(query, "RacketNewStatusID", RacketNewStatusID)
            commit()
            return True
        return False