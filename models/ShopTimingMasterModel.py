from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class ShopTimingMasterModel(db.Model):
    __tablename__ = 'tp_shop_timing_master'

    id = db.Column(db.Integer, primary_key=True)
    ShopID =  db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    WeekDay = db.Column(db.Integer)
    IsOpen = db.Column(db.Boolean)
    StartTime = db.Column(db.Time)
    EndTime = db.Column(db.Time)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=getUTCTime())
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)

    def __init__(self,id,ShopID,WeekDay,IsOpen,StartTime,EndTime,InsertedBy,UpdatedBy):
        
        self.id=id
        self.ShopID=ShopID
        self.WeekDay=WeekDay
        self.IsOpen=IsOpen
        self.StartTime=StartTime
        self.EndTime=EndTime
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsSystem = 0
        self.CreatedBy = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = UpdatedBy
    
    def json(self):
        return {
            'ID': self.id,
            "WeekDay": self.WeekDay,
            "IsOpen": self.IsOpen,
            "StartTime": self.StartTime and self.StartTime.strftime('%H.%M') or None, #self.StartTime.strftime('%H:%M:%S') ,
            "EndTime": self.EndTime and self.EndTime.strftime('%H.%M') or None #self.EndTime.strftime('%H:%M:%S')
            }

    @classmethod
    def GetShopTiming(cls,ShopID):
        return cls.query.filter(ShopTimingMasterModel.ShopID==ShopID,ShopTimingMasterModel.IsDeleted==0).all()

    @classmethod
    def GetShopTimingByID(cls,ShopID, ShopTimigID):
        return db.session.query(ShopTimingMasterModel).filter(ShopTimingMasterModel.id == ShopTimigID , ShopTimingMasterModel.ShopID == ShopID,ShopTimingMasterModel.IsDeleted==0).first()

    @classmethod
    def UpdateShopTimingList(cls, ShopID, data):
        query = ShopTimingMasterModel.GetShopTiming(ShopID)
        if query:                
            for NewShopTiming in data:
                for OldShopTiming in query:
                    if(OldShopTiming.id == NewShopTiming.get("ShopTimingID")):
                        for key, value in NewShopTiming.items():
                            if(key in ("StartTime", "EndTime") and value is not None):
                                value = datetime.strptime(str(value), '%H.%M') 
                            setattr(OldShopTiming, "UpdatedDate", getUTCTime())    
                            setattr(OldShopTiming, key, value)
                        break           
            commit()
        return query
    