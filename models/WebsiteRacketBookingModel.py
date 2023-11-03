from operator import and_
from sqlalchemy.orm import query, relationship
import datetime as pydt
from db import db
from models.FrameworkModel import *
from sqlalchemy.sql import func
from sqlalchemy.orm import backref, relationship
from flask import request, jsonify, json
from datetime import datetime,timedelta
from sqlalchemy import cast,Date

class RacketBookingMasterModel(db.Model):
    __tablename__ = 'tp_website_racket_booking'
    
    id = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer)
    ShopID =  db.Column(db.Integer)
    Comment = db.Column(db.String(2000))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    CancelBy = db.Column(db.Integer)
    IsDeleted = db.Column(db.Boolean)
    
    
    def __init__(self, ShopID,CustomerID,InsertedBy):
        self.ShopID = ShopID
        self.CustomerID = CustomerID
        self.Comment = None
        self.IsDeleted = 0
        self.InsertedBy = InsertedBy
        self.UpdatedBy = None 
        self.CancelBy = None   