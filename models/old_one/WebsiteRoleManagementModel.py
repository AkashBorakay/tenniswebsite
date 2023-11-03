from sqlalchemy.sql.expression import select
from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class WebsiteRoleManagementModel(db.Model):
    __tablename__ = 'tp_shop_role_management'

    id = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(200))
    CreatedDate = db.Column(db.Date)
    UpdatedDate = db.Column(db.Date)
    IsDeleted = db.Column(db.Boolean)
    IsSystem =  db.Column(db.Boolean)
    CreatedBy = db.Column(db.String(200))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)


    def __init__(self,RoleName,InsertedBy,UpdatedBy):
        self.RoleName = RoleName
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsDeleted = 0
        self.IsSystem = None
        self.CreatedBy = 1
        self.InsertedBy = InsertedBy
        self.UpdatedBy = UpdatedBy

    def json(self):
        return {
            'RoleName': self.RoleName
            }

    @classmethod
    def GetRoleList(cls):
        return db.session.query(WebsiteRoleManagementModel).filter(WebsiteRoleManagementModel.IsDeleted == 0).all()

    @classmethod
    def GetRoleMaster(cls, RoleID):
        return db.session.query(WebsiteRoleManagementModel).filter(WebsiteRoleManagementModel.id == RoleID, WebsiteRoleManagementModel.IsDeleted == 0).first()

    @classmethod
    def UpdateRole(cls, **data):
        RoleID = data.get('RoleID')
        query = WebsiteRoleManagementModel.GetRoleMaster(RoleID)

        if query is not None:
            for key, value in data.items(): 
                setattr(query, key, value)
            setattr(query, "UpdatedDate", getUTCTime())
            commit()
        return query

    @classmethod
    def DeleteRoleMaster(cls, RoleID):
        query = WebsiteRoleManagementModel.GetRoleMaster(RoleID)
        if query:
            query.IsDeleted = 1
            commit()
        return query

