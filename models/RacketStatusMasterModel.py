from db import db
from models.FrameworkModel import getUTCTime
from sqlalchemy.orm import relationship

class RacketStatusMasterModel(db.Model):
    __tablename__ = 'tp_racket_status_master'
    
    id = db.Column(db.Integer, primary_key=True)
    ShopID = db.Column(db.Integer)
    Status = db.Column(db.String(200))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    
    
    def __init__(self, ShopID, Status,InsertedBy,UpdatedBy):
        self.ShopID = ShopID
        self.Status = Status 
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate =  getUTCTime()
        self.IsSystem = 0
        self.CreatedBy = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = UpdatedBy


    def json(self):
        return {
             'RacketStatusID': self.id,
                 'ShopID' :self.ShopID,
                 'Status' : self.Status
        }

    @classmethod
    def GetRacketStatusMaster(cls,ShopID):
        query = db.session.query(RacketStatusMasterModel).filter(RacketStatusMasterModel.ShopID == ShopID,RacketStatusMasterModel.IsDeleted == 0).all()
        return query

    @classmethod
    def GetRacketNewRacketStatus(cls,NewStatusID,ShopID):
        query = db.session.query(RacketStatusMasterModel).filter(RacketStatusMasterModel.id == NewStatusID,RacketStatusMasterModel.ShopID == ShopID,RacketStatusMasterModel.IsDeleted == 0).first()
        return query    
