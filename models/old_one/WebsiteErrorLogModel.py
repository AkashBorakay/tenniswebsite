from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import select
from models.ShopMasterModel import ShopMasterModel
from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class ErrorLogModel(db.Model):
    __tablename__ = 'tp_website_Error_Log'

    id = db.Column(db.Integer, primary_key=True)
    FromAdminClient = db.Column(db.String(2000))
    BugDetail = db.Column(db.String(2000))
    ShopID =  db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=getUTCTime())
    IsDeleted = db.Column(db.Boolean)
    BugStatus = db.Column(db.Boolean)
    BugTicketStatus = db.Column(db.Boolean)
    DeviceName = db.Column(db.String(500))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    AppVersion = db.Column(db.String(2000))