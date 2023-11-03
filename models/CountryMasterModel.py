from sqlalchemy.sql.expression import select
from models.ShopMasterModel import ShopMasterModel
from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class CountryMasterModel(db.Model):
    __tablename__ = 'tp_country_master'

    id = db.Column(db.Integer, primary_key=True)
    CountryName = db.Column(db.String(200))
    CountryTelCode = db.Column(db.String(200))
    CountryCode = db.Column(db.String(200))
    Currency = db.Column(db.String(200))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=getUTCTime())
    SortOrder = db.Column(db.Integer)
    IsDeleted = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    EN = db.Column(db.String(2000))
    FR = db.Column(db.String(2000))

    def json(self):
        return {
            'CountryID': self.id,
            "CountryName": self.CountryName,
            "CountryCode": self.CountryCode,
            "EN" : self.EN,
            "FR" : self.FR,            
            }

    @classmethod
    def GetCountryList(cls,language):
        try:
            query = db.session.query(getattr(CountryMasterModel,language),getattr(CountryMasterModel,"CountryCode"),getattr(CountryMasterModel,"id")).filter(CountryMasterModel.IsDeleted == 0).order_by(CountryMasterModel.SortOrder).all()
        except AttributeError as e:
            query = db.session.query(getattr(CountryMasterModel,"EN"),getattr(CountryMasterModel,"CountryCode"),getattr(CountryMasterModel,"id")).filter(CountryMasterModel.IsDeleted == 0).order_by(CountryMasterModel.SortOrder).all()
        return query
            
    @classmethod
    def GetCountryName(cls,CountryID):
        return db.session.query(CountryMasterModel).filter(CountryMasterModel.id == CountryID,CountryMasterModel.IsDeleted == 0).first()
    
    @classmethod
    def GetAllCountryName(cls):
        CountryList = db.session.query(CountryMasterModel).filter(CountryMasterModel.IsDeleted == 0).all()
        list =[]
        for val in ([countrylist.json() for countrylist in CountryList]):
            if val in list:
                continue
            else:
                list.append(val)
        return(list)