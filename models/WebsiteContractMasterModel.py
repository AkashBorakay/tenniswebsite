from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class ContractMasterModel(db.Model):
    __tablename__ = 'tp_website_contract_master'

    id = db.Column(db.Integer, primary_key=True)
    ShopID = db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    ContractName = db.Column(db.String(2000))
    Charge = db.Column(db.Float())
    DurationOfContractInDays  = db.Column(db.Integer)
    DurationOfContractInMonth = db.Column(db.Integer)
    DurationOfContractInYears = db.Column(db.Integer)
    MaxiumBookRacket = db.Column(db.Integer)
    DurationBetween2BookingInDays = db.Column(db.Integer)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    DeactiveDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    DeletedBy = db.Column(db.Integer)
    IsActive = db.Column(db.Boolean)
    MinimumDurationOfBookingRacket = db.Column(db.Integer)
    MiximumDurationOfBookingRacket = db.Column(db.Integer)
    
    
    def __init__(self,Charge,ContractName,DurationBetween2BookingInDays,DurationOfContractInMonth,MaxiumBookRacket,MinimumDurationOfBookingRacket,MiximumDurationOfBookingRacket,InsertedBy):
           self.Charge = Charge
           self.ContractName = ContractName
           self.DurationBetween2BookingInDays = DurationBetween2BookingInDays
           self.DurationOfContractInMonth = DurationOfContractInMonth
           self.MaxiumBookRacket = MaxiumBookRacket
           self.MinimumDurationOfBookingRacket = MinimumDurationOfBookingRacket
           self.MiximumDurationOfBookingRacket = MiximumDurationOfBookingRacket
           self.InsertedBy = InsertedBy
           self.CreatedDate = getUTCTime()
           self.UpdatedBy = None
           self.UpdatedDate = None
           self.DeletedBy = None
           self.DeactiveDate = None
           self.IsDeleted = 0
           self.IsActive = 1
    
    
    def json(self):
        return {
            "ContractID" : self.id,
            "ShopID" : self.ShopID,
            "ContractName" : self.ContractName,
            "Charge":self.Charge,
            "DurationOfContractInMonth" : self.DurationOfContractInMonth,
            "MaxiumBookRacket":self.MaxiumBookRacket,
            "DurationBetween2BookingInDays":self.DurationBetween2BookingInDays,
            "MinimumDurationOfBookingRacket":self.MinimumDurationOfBookingRacket,
            "MiximumDurationOfBookingRacket":self.MiximumDurationOfBookingRacket            
        }
        
    
    @classmethod
    def GetCustomerContractDetail(cls,CustomerContractMasterID):
        query = db.session.query(ContractMasterModel).filter(ContractMasterModel.id == CustomerContractMasterID, ContractMasterModel.IsDeleted == 0).first()
        if query is not None:
            return query.MaxiumBookRacket
        else:
            return None
        
    
    @classmethod
    def GetContractList(cls,shopID):
        return db.session.query(ContractMasterModel).filter(ContractMasterModel.ShopID==shopID,ContractMasterModel.IsDeleted==0).all()
    
    @classmethod
    def GetContract(cls, ContractID, ShopID):
        return db.session.query(ContractMasterModel).filter(ContractMasterModel.ShopID == ShopID, ContractMasterModel.id == ContractID, ContractMasterModel.IsDeleted == 0).first()
    
    @classmethod
    def GetContractForCustomer(cls,ContractID):
        return db.session.query(ContractMasterModel).filter(ContractMasterModel.id==ContractID).first()
    
    @classmethod
    def UpdateShopContract(cls,ShopID,**data):
        ContractID = data.get('ContractID')
        query = ContractMasterModel.GetContract(ContractID,ShopID)
        if query is not None:
            for key, value in data.items():
                setattr(query, key, value)
                setattr(query, "UpdatedDate", getUTCTime())        
            commit()
        return query
    
    @classmethod
    def DeleteShopContract(cls, ContractID,DeletedBy,ShopID):
        query = ContractMasterModel.GetContract(ContractID,ShopID)
        if query:
            setattr(query, "IsDeleted", 1)
            setattr(query, "DeletedBy", DeletedBy)
            setattr(query, "DeactiveDate", getUTCTime())
            db.session.commit()
            return 1
        return 0