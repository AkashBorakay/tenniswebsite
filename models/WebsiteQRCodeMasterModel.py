from sqlalchemy.sql.expression import desc, null
from sqlalchemy.orm import query
from db import db
from models.FrameworkModel import *
from sqlalchemy.sql import func

class QRCodeMasterModel(db.Model):  # type: ignore
    __tablename__ = 'tp_website_qr_code_master'
    
    id = db.Column(db.Integer, primary_key=True)
    ShopID =  db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    DecryptQRCode = db.Column(db.String(1024))
    IsUsed = db.Column(db.Boolean)
    UsedDate = db.Column(db.DateTime, onupdate=func.now())
    DeactiveDate = db.Column(db.DateTime)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=func.now())
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    ActiveDate = db.Column(db.DateTime)
   

    def __init__(self, ShopID,DecryptQRCode,IsUsed,DeactiveDate,InsertedBy,UpdatedBy):
        self.ShopID = ShopID
        self.DecryptQRCode = DecryptQRCode 
        self.IsUsed = IsUsed 
        self.UsedDate = getUTCTime() 
        self.DeactiveDate = DeactiveDate 
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsSystem = 0
        self.CreatedBy = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = UpdatedBy
        self.ActiveDate = getUTCTime()

    def json(self):
        return {
        'QRCodeID': self.id,
        'ShopID': self.ShopID,
        'DecryptQRCode': self.DecryptQRCode,
        'IsUsed': self.IsUsed ,
        'UsedDate': self.UsedDate and self.UsedDate.strftime('%Y-%m-%d %H:%M:%S') or None,
        'DeactiveDate': self.DeactiveDate and self.DeactiveDate.strftime('%Y-%m-%d %H:%M:%S') or None,
        'CreatedDate': self.CreatedDate.strftime('%Y-%m-%d %H:%M:%S'),
        'UpdatedDate': self.UpdatedDate.strftime('%Y-%m-%d %H:%M:%S'),
        'ActiveDate': self.UsedDate and self.UsedDate.strftime('%Y-%m-%d %H:%M:%S') or None
        }
    
    @classmethod
    def ValidateQRcode(cls,ShopID,QRCodeDecrypted): 
        query = db.session.query(QRCodeMasterModel).filter(QRCodeMasterModel.DecryptQRCode == QRCodeDecrypted,QRCodeMasterModel.ShopID == ShopID,QRCodeMasterModel.IsDeleted == 0).first()
        return query
    
    @classmethod
    def CheckQRcode(cls,ShopID,QRCodeID): 
        query = db.session.query(QRCodeMasterModel).filter(QRCodeMasterModel.id == QRCodeID,QRCodeMasterModel.ShopID == ShopID,QRCodeMasterModel.IsDeleted == 0).first()
        return query
    
    @classmethod
    def QrCodeIsUsed(cls,ShopID, QRCodeID):
        query = QRCodeMasterModel.CheckQRcode(ShopID, QRCodeID)
        if query is not None:
            setattr(query, "UpdatedDate", getUTCTime())      
        commit()
        return query
    @classmethod
    def UpdateQRCodeStatus(cls,ShopID,QRCodeID):
        CheckDataBeforeUpdate = QRCodeMasterModel.CheckQRcode(ShopID,QRCodeID)
        if CheckDataBeforeUpdate is not None:
            CheckDataBeforeUpdate.IsUsed = 1
            CheckDataBeforeUpdate.UsedDate = getUTCTime()
            CheckDataBeforeUpdate.ActiveDate = getUTCTime()
        commit()
        return CheckDataBeforeUpdate
    
    @classmethod
    def DeactivateQRCodeDetail(cls,ShopID,QRCodeID,InsertedBy):
        CheckDataBeforeUpdate = QRCodeMasterModel.CheckQRcode(ShopID,QRCodeID)
        if CheckDataBeforeUpdate is not None:
            CheckDataBeforeUpdate.IsDeleted = 1
            CheckDataBeforeUpdate.DeactiveDate = getUTCTime()
            CheckDataBeforeUpdate.UpdatedDate = getUTCTime()
            CheckDataBeforeUpdate.UpdatedBy = InsertedBy
        commit()
        return CheckDataBeforeUpdate