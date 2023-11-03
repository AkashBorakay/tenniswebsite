from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *

class SleeveSizeMasterModel(db.Model):
    __tablename__ = 'tp_website_SleeveSize_master'

    id = db.Column(db.Integer, primary_key=True)
    SleeveSize = db.Column(db.String(50))
    SleeveSizeShort = db.Column(db.String(50))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=func.now())
    IsDeleted = db.Column(db.Boolean)
    UpdatedBy = db.Column(db.Integer)

    def __init__(self, id, SleeveSize, SleeveSizeShort, UpdatedBy):
        self.id=id
        self.SleeveSize = SleeveSize
        self.SleeveSizeShort = SleeveSizeShort
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.UpdatedBy = UpdatedBy
    
    def json(self):
        return {'SleeveSizeID': self.id, "SleeveSize": self.SleeveSize, "SleeveSizeShortName": self.SleeveSizeShort}

    @classmethod
    def GetSleeveSizeList(cls):
        return cls.query.filter_by(IsDeleted = 0).all()
    
    @classmethod
    def GetSleeveSizeAccordingToID(cls,SleeveSizeID):
        query = db.session.query(SleeveSizeMasterModel).filter(SleeveSizeMasterModel.id == SleeveSizeID).first()
        if query is not None:
            return query.SleeveSize
        else:
            return None
        
    @classmethod
    def GetSleeveSizeAccordingToIDName(cls,SleeveSizeID):
        query = db.session.query(SleeveSizeMasterModel).filter(SleeveSizeMasterModel.id == SleeveSizeID).first()
        if query is not None:
            return query.SleeveSizeShort
        else:
            return None