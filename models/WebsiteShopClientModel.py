from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class CustomerShopModel(db.Model):
    __tablename__ = 'tpv_website_customer_shop'

    id = db.Column(db.Integer, primary_key=True)
    ShopID = db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    CustomerID = db.Column(db.Integer, db.ForeignKey('tp_website_customer.id'))
    
    
    def __init__(self,ShopID,CustomerID):
           self.ShopID = ShopID
           self.CustomerID = CustomerID
    
    
    def json(self):
        return {
            "CustomerID" : self.CustomerID,
            "ShopID" : self.ShopID       
        }
        
        
    @classmethod
    def GetContractList(cls, CustomerID):
        return db.session.query(CustomerShopModel).filter(CustomerShopModel.CustomerID==CustomerID).all()
    