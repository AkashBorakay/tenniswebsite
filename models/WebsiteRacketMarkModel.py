# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 17:11:20 2023

@author: SybilleDarbin
"""

import re
from flask.json import jsonify
from sqlalchemy.orm import query
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import func, select
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.operators import json_path_getitem_op
from db import db
from sqlalchemy.orm import backref, relationship
from models.FrameworkModel import commit, pagination,getUTCTime, save_to_db, PaginationForCustomerFilter
from datetime import datetime
from sqlalchemy.sql.elements import Null, or_, and_
from models.WebsiteCustomerModel import CustomerDetailModel
from models.WebsiteRacketMasterModel import RacketMasterModel
from hashlib import sha256


class RacketMarkModel(db.Model):
    __tablename__ = 'tp_website_mark'
    
    id = db.Column(db.Integer, primary_key=True)
    MasterRacketID = db.Column(db.Integer)
    CustomerID = db.Column(db.Integer)
    Mark = db.Column(db.Float)
    Date = db.Column(db.DateTime)
    ShopID = db.Column(db.Integer)
    Comment = db.Column(db.String(50))
    
    def __init__(self, MasterRacketID, CustomerID, Mark, ShopID, Comment):
        self.MasterRacketID = MasterRacketID
        self.CustomerID = CustomerID
        self.Mark = Mark
        self.Date = getUTCTime()
        self.ShopID = ShopID   
        self.Comment = Comment

    def json(self):
        # MasterRacket = RacketMasterModel.GetTestRacketDetail(self.MasterRacketID)    
        return {
             'CustomerID': self.CustomerID,
             'MasterRacketID' : self.MasterRacketID,
             'Mark' : self.Mark,
             'ShopID' : self.ShopID or None,
             'Comment' : self.Comment or None,
             # 'ModelDisplayName' : MasterRacket.ModelDisplayName,
             # 'Image_1' : MasterRacket.RacketImage_1,
             # 'Image_2' : MasterRacket.RacketImage_2,
             # 'Image_3' : MasterRacket.RacketImage_3,
             # 'Image_4' : MasterRacket.RacketImage_4,
        }
    
    @classmethod
    def CheckMarkByCustomerForRacketExistBeforeInsert(cls, MasterTestingRacketID, CustomerID):
        query = db.session.query(RacketMarkModel).filter(RacketMarkModel.CustomerID == CustomerID, RacketMarkModel.MasterRacketID  == MasterTestingRacketID).first()
        return query
    
    @classmethod
    def GetMarksInfo(cls):
        query = db.session.query(RacketMarkModel).all()
        return query
        
    # @classmethod
    # def GetMarksClient(cls,CustomerID,MasterRacketID):
    #     query = db.session.query(RacketMarkModel).filter(RacketMarkModel.CustomerID == CustomerID, RacketMarkModel.MasterRacketID == MasterRacketID).first()
    #     return query
    
    # @classmethod
    # def GetMarksShop(cls,ShopID,MasterRacketID):
    #     query = db.session.query(RacketMarkModel).filter(RacketMarkModel.ShopID == ShopID, RacketMarkModel.MasterRacketID == MasterRacketID, RacketMarkAvg.MasterRacketID == RacketMarkModel.MasterRacketID).first()
    #     return query
    

    @classmethod
    def UpdateGrade(cls,CustomerID, MasterRacketID, Mark, Comment):
        CheckDataBeforeUpdate = RacketMarkModel.CheckMarkByCustomerForRacketExistBeforeInsert(MasterRacketID, CustomerID)
        if CheckDataBeforeUpdate is not None:
            setattr(CheckDataBeforeUpdate, "Mark", Mark)
            setattr(CheckDataBeforeUpdate, "Comment", Comment)
            commit()
        return Mark
    
class RacketMarkAvg(db.Model):
    __tablename__ = 'tpv_website_avg_mark'
    MasterRacketID = db.Column(db.Integer, primary_key=True)
    Mark = db.Column(db.Float)
    
        
    def jsonMark(self):
        MasterRacket = RacketMasterModel.GetTestRacketDetail(self.MasterRacketID)       
        return {
             'MasterRacketID' : self.MasterRacketID,
             'Mark' : self.Mark,
        }
    
    @classmethod
    def GetMarks(cls):
        query = db.session.query(RacketMarkAvg).all()
        return query
        # return({"results":query})
    
    @classmethod
    def GetMarksMaster(cls, MasterRacketID):
        query = db.session.query(RacketMarkAvg).filter(RacketMarkAvg.MasterRacketID == MasterRacketID).first()
        return query
    