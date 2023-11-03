from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class ShopHolidayModel(db.Model):

    __tablename__="tp_shop_holiday_master"

    id=db.Column(db.Integer, primary_key=True) 
    ShopID =  db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    HolidayName = db.Column(db.String(200))
    HolidayDate = db.Column(db.Date)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=func.now())
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)

    def __init__(self,HolidayName,HolidayDate,InsertedBy): 
        self.HolidayName=HolidayName
        self.HolidayDate=datetime.strptime(HolidayDate, '%Y-%m-%d').date()
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsSystem = 0
        self.CreatedBy = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = None
    
    def json(self):
        return {
            "HolidayID" : self.id,
            "HolidayName" : self.HolidayName,
            "HolidayDate" : self.HolidayDate.strftime("%Y-%m-%d")
        }
    
    @classmethod
    def GetHolidayList(cls,shopID):
        return db.session.query(ShopHolidayModel).filter(ShopHolidayModel.ShopID==shopID,ShopHolidayModel.IsDeleted==0).order_by(ShopHolidayModel.HolidayDate).all()
        # return cls.query.filter(ShopHolidayModel.ShopID==shopID,ShopHolidayModel.IsDeleted==0).all()

    @classmethod
    def GetShopHoliday(cls, ShopHolidayID):
         return db.session.query(ShopHolidayModel).filter(ShopHolidayModel.id == ShopHolidayID, ShopHolidayModel.IsDeleted == 0).first()

    @classmethod
    def UpdateShopHoliday(cls,**data):
        ShopHolidayID = data.get('ShopHolidayID')
        query = ShopHolidayModel.GetShopHoliday(ShopHolidayID)
        if query is not None:
            for key, value in data.items():
                setattr(query, key, value)
                setattr(query, "UpdatedDate", getUTCTime())        
            commit()
        return query

    @classmethod
    def DeleteShopHoliday(cls, ShopHolidayID,UpdatedBy):
        query = ShopHolidayModel.GetShopHoliday(ShopHolidayID)
        if query:
            setattr(query, "IsDeleted", 1)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "UpdatedDate", getUTCTime())
            db.session.commit()
            # query.IsDeleted = 1
            # commit()
        return query