from sqlalchemy.sql.expression import select
from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class ApplicationRoleAssignmentModel(db.Model):
    __tablename__ = 'tp_role_assignment'

    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer)
    RoleID = db.Column(db.Integer)
    CreatedDate = db.Column(db.Date)
    UpdatedDate = db.Column(db.Date)
    IsDeleted = db.Column(db.Boolean)
    IsSystem =  db.Column(db.Boolean)
    CreatedBy = db.Column(db.String(200))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)


    def __init__(self,UserID,RoleID,InsertedBy):
        self.UserID = UserID
        self.RoleID = RoleID
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsDeleted = 0
        self.IsSystem = None
        self.CreatedBy = 1
        self.InsertedBy = InsertedBy
        self.UpdatedBy = None
        
    @classmethod
    def GetShopRoleAssignmentMasterForStringerID(cls, StringerID):
        return db.session.query(ApplicationRoleAssignmentModel).filter(ApplicationRoleAssignmentModel.UserID == StringerID,ApplicationRoleAssignmentModel.IsDeleted == 0,ApplicationRoleAssignmentModel.RoleID != 1).first()    