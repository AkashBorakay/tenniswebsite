from sqlalchemy.sql.expression import select
from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime
from models.WebsiteRoleManagementModel_V2 import WebsiteRoleManagementModel

class WebsiteRoleAssignmentModel(db.Model):
    __tablename__ = 'tp_website_role_assignment'

    id = db.Column(db.Integer, primary_key=True)
    StringerID = db.Column(db.Integer, db.ForeignKey('tp_website_stringer_master.id'))
    RoleID = db.Column(db.Integer, db.ForeignKey('tp_website_role_master.id'))
    CreatedDate = db.Column(db.Date)
    UpdatedDate = db.Column(db.Date)
    IsDeleted = db.Column(db.Boolean)
    IsSystem =  db.Column(db.Boolean)
    CreatedBy = db.Column(db.String(200))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)


    def __init__(self,StringerID,RoleID,InsertedBy):
        self.StringerID = StringerID
        self.RoleID = RoleID
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsDeleted = 0
        self.IsSystem = None
        self.CreatedBy = 1
        self.InsertedBy = InsertedBy
        self.UpdatedBy = None

    def json(self):
        return {
            'UserID': self.StringerID,
            'RoleID': self.RoleID,
            "CreatedDate": self.CreatedDate,
            "UpdatedDate": self.UpdatedDate,
            "IsDeleted": self.IsDeleted,
            "IsSystem": self.IsSystem,
            "CreatedBy": self.CreatedBy,
            "InsertedBy": self.InsertedBy,
            "UpdatedBy": self.UpdatedBy
            }

    @classmethod
    def GetShopRoleAssignmentList(cls):
        return db.session.query(WebsiteRoleAssignmentModel).filter(WebsiteRoleAssignmentModel.IsDeleted == 0).all()

    @classmethod
    def GetShopRoleAssignmentMasterForRoleID(cls, RoleID):
        return db.session.query(WebsiteRoleAssignmentModel).filter(WebsiteRoleAssignmentModel.RoleID == RoleID, WebsiteRoleAssignmentModel.IsDeleted == 0).first()

    @classmethod
    def GetWebsiteRoleAssignmentMasterForStringerID(cls, StringerID):
        return db.session.query(WebsiteRoleAssignmentModel).filter(WebsiteRoleAssignmentModel.StringerID == StringerID,WebsiteRoleAssignmentModel.IsDeleted == 0).first()  

