from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *

class AgeGroupModel(db.Model):
    __tablename__ = 'tp_age_group'

    id = db.Column(db.Integer, primary_key=True)
    AgeGroup = db.Column(db.Integer)
    SortOrder = db.Column(db.Integer)	
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=func.now())
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)

    def __init__(self, AgeGroup,InsertedBy,UpdatedBy):
        self.AgeGroup = AgeGroup
        self.SortOrder = None
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsSystem = 0
        self.CreatedBy = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = UpdatedBy
    
    def json(self):
        return {'AgeGroupID': self.id, "AgeGroup": self.AgeGroup}

    @classmethod
    def GetAgeGroupList(cls):
        return cls.query.filter_by(IsDeleted = 0).all()
    
    @classmethod
    def GetAgeGroupNameByID(cls, AgeGroupID):
        return db.session.query(AgeGroupModel).filter(AgeGroupModel.id == AgeGroupID,AgeGroupModel.IsDeleted == 0).first()