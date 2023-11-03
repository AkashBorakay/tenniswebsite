from db import db
import datetime as pydt
from sqlalchemy.sql import func
from models.FrameworkModel import *
from sqlalchemy import cast,Date
from datetime import datetime
from models.WebsiteContractMasterModel import ContractMasterModel
from models.ShopMasterModel import ShopMasterModel

class CustomerContractMasterModel(db.Model):
    __tablename__ = 'tp_website_customer_contract'

    id = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('tp_website_customer.id'))
    ContractID = db.Column(db.Integer, db.ForeignKey('tp_website_contract_master.id'))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    DeactiveDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    IsActive = db.Column(db.Boolean)
    CreditCardPrintDate = db.Column(db.DateTime)
    EndingContractDate = db.Column(db.DateTime)
    NbRacketAllowed = db.Column(db.SmallInteger)
    
    
    def __init__(self, CustomerID, ContractID, InsertedBy, CreditCardPrintDate, EndingContractDate, NbRacketAllowed):
           self.CustomerID = CustomerID
           self.ContractID = ContractID
           self.CreatedDate = getUTCTime()
           self.UpdatedDate = getUTCTime()
           self.DeactiveDate = None
           self.IsDeleted = False
           self.InsertedBy = InsertedBy
           self.UpdatedBy = None
           self.IsActive = False
           self.CreditCardPrintDate = CreditCardPrintDate and  datetime.strptime(CreditCardPrintDate, '%d/%m/%Y') or None
           self.EndingContractDate = EndingContractDate and  datetime.strptime(EndingContractDate, '%d/%m/%Y') or None
           self.NbRacketAllowed = NbRacketAllowed
           
    def json(self,ShopID):
        ContractDetail = ContractMasterModel.GetContract(self.ContractID,ShopID)
        ShopDetail = ShopMasterModel.ShopDetail(ShopID)
        if ContractDetail:
            output = {
            'CustomerContractID' : self.id,
            'MasterContractID': self.ContractID,
            'IsDeleted': self.IsDeleted,
            'CreditCardPrintDate': self.CreditCardPrintDate and self.CreditCardPrintDate.strftime('%Y-%m-%d') or None,
            'EndingContractDate': self.EndingContractDate and self.EndingContractDate.strftime('%Y-%m-%d') or None,
            'NbRacketAllowed': self.NbRacketAllowed,
            'ContractName' :  ContractDetail.ContractName,
            'Charge' : ContractDetail.Charge,
            'DurationOfContractInMonth' : ContractDetail.DurationOfContractInMonth,
            'DurationBetween2BookingInDays' : ContractDetail.DurationBetween2BookingInDays,
            'MinimumDurationOfBookingRacket' : ContractDetail.MinimumDurationOfBookingRacket,
            'MiximumDurationOfBookingRacket' : ContractDetail.MiximumDurationOfBookingRacket,
            'ShopID' : ShopDetail.id,
            'ShopName' : ShopDetail.shopname,
            'ShopLogo' : ShopDetail.ShopLogo
            }
            return output
        else:
            return {'ContractDetail' : None}
        
    def JsonToGetAllCustomerContracts(self):
        ContractDetail = ContractMasterModel.GetContractForCustomer(self.ContractID)
        ShopDetail = ShopMasterModel.ShopDetail(ContractDetail.ShopID)
        if self.EndingContractDate is not None:
            RemainingTime = (datetime.strptime((self.EndingContractDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((getUTCTime().strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        else:
            RemainingTime = None
        if ContractDetail:
            output = {
            'CustomerContractID' : self.id,
            'MasterContractID': self.ContractID,
            'IsDeleted': self.IsDeleted,
            'CreditCardPrintDate': self.CreditCardPrintDate and self.CreditCardPrintDate.strftime('%Y-%m-%d') or None,
            'EndingContractDate': self.EndingContractDate and self.EndingContractDate.strftime('%Y-%m-%d') or None,
            'NbRacketAllowed': self.NbRacketAllowed,
            'ContractName' :  ContractDetail.ContractName,
            'Charge' : ContractDetail.Charge,
            'DurationOfContractInMonth' : ContractDetail.DurationOfContractInMonth,
            'MaxiumBookRacket' : ContractDetail.MaxiumBookRacket,
            'DurationBetween2BookingInDays' : ContractDetail.DurationBetween2BookingInDays,
            'MinimumDurationOfBookingRacket' : ContractDetail.MinimumDurationOfBookingRacket,
            'MiximumDurationOfBookingRacket' : ContractDetail.MiximumDurationOfBookingRacket,
            'ShopID' : ShopDetail.id,
            'ShopName' : ShopDetail.shopname,
            'TimeRemainingContract': RemainingTime,
            'ShopLogo' : ShopDetail.ShopLogo
            }
            return output
        else:
            return {'ContractDetail' : None}
            
        
    @classmethod
    def GetLastCustomerContract(cls, CustomerID, ShopID):
        Query = db.session.query(ContractMasterModel).filter(ContractMasterModel.id == CustomerContractMasterModel.ContractID, CustomerContractMasterModel.CustomerID == CustomerID, 
                                                             CustomerContractMasterModel.IsDeleted == 0, ContractMasterModel.ShopID == ShopID).order_by(CustomerContractMasterModel.CreatedDate.desc()).first()
        return Query.ContractName
    
    @classmethod
    def GetCustomerContract(cls,CustomerID,ShopID):
        Query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.CustomerID == CustomerID, CustomerContractMasterModel.IsDeleted == 0).all()
        AllContract = [query.json(ShopID) for query in Query]
        return AllContract
    
    @classmethod
    def GetCustomerContractV3(cls, CustomerID, ShopID):
        Query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.CustomerID == CustomerID, CustomerContractMasterModel.IsDeleted == 0, 
                                                                     CustomerContractMasterModel.ContractID == ContractMasterModel.id, ContractMasterModel.ShopID == ShopID).all()
        AllContract = [query.json(ShopID) for query in Query]
        return AllContract
        
    @classmethod
    def GetCustomerContractForDashboard(cls,CustomerID):
        Query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.CustomerID == CustomerID,CustomerContractMasterModel.IsDeleted == 0).first()
        return Query
    
    @classmethod
    def CheckContractExist(cls,CustomerID, ShopID):
        Query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.CustomerID == CustomerID,
                                                                     CustomerContractMasterModel.ContractID == ContractMasterModel.id, ContractMasterModel.ShopID == ShopID).count()
        return Query
    
    @classmethod
    def CheckContractActive(cls,CustomerID, ShopID):
        Query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.CustomerID == CustomerID, CustomerContractMasterModel.IsDeleted == 0,
                                                                     CustomerContractMasterModel.ContractID == ContractMasterModel.id, ContractMasterModel.ShopID == ShopID).count()
        return Query
    @classmethod
    def GetCustomerAllContracts(cls,CustomerID):
        Query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.CustomerID == CustomerID,CustomerContractMasterModel.IsDeleted == 0).all()
        AllContract = [query.JsonToGetAllCustomerContracts() for query in Query]
        return AllContract
    
    @classmethod
    def GetCustomerContractV2(cls,ContractCustomerID, ShopID):
        return db.session.query(CustomerContractMasterModel).filter(ContractMasterModel.id == CustomerContractMasterModel.ContractID, 
                                                                    CustomerContractMasterModel.id == ContractCustomerID, CustomerContractMasterModel.IsDeleted == 0,
                                                                    ContractMasterModel.ShopID == ShopID).first()
    
    @classmethod
    def GetRacketContract(cls,CustomerID, ShopID):
        Query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.ContractID == ContractMasterModel.id, 
                                                                    CustomerContractMasterModel.CustomerID == CustomerID, CustomerContractMasterModel.IsDeleted == 0,
                                                                    ContractMasterModel.ShopID == ShopID).first()
        return Query.NbRacketAllowed
    
    @classmethod
    def UpdateShopContractCustomer(cls,ShopID, ContractCustomerID,**data):
        EndingContractDate1 = data.get('EndingContractDate')
        EndingContractDate = datetime.strptime(EndingContractDate1, "%d/%m/%Y")
        CreditCardPrintDate1 = data.get('CreditCardPrintDate')
        CreditCardPrintDate = datetime.strptime(CreditCardPrintDate1, "%d/%m/%Y")
        NbRacketAllowed = data.get('NbRacketAllowed')
        UpdatedBy = data.get('UpdatedBy')
        ContractID = data.get('ContractID')
        query = CustomerContractMasterModel.GetCustomerContractV2(ContractCustomerID, ShopID)
        if query is not None:
            setattr(query, 'EndingContractDate', EndingContractDate)
            setattr(query, 'CreditCardPrintDate', CreditCardPrintDate)
            setattr(query, 'NbRacketAllowed', NbRacketAllowed)
            setattr(query, 'ContractID', ContractID)
            setattr(query, 'UpdatedBy', UpdatedBy)
            setattr(query, "UpdatedDate", getUTCTime())        
            commit()
        del EndingContractDate1, EndingContractDate, CreditCardPrintDate1, CreditCardPrintDate, NbRacketAllowed, UpdatedBy
        return query
    
    
    @classmethod
    def DeleteContratCustomer(cls, ContractCustomerID, UpdatedBy):
        query = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.id == ContractCustomerID).first()
        if query:
            setattr(query, "IsDeleted", True)  
            setattr(query, "DeactiveDate", getUTCTime())  
            setattr(query, "UpdatedBy", UpdatedBy)  
            commit()
            return True
        else:
            return {"message" : "No order found for autocancellation"}, 200  #error
        
    @classmethod
    def AutoContractEndCustomer(cls):
        CurrentDate=pydt.datetime.today()
        AllDataOfStatus7 = db.session.query(CustomerContractMasterModel).filter(CustomerContractMasterModel.IsDeleted == 0,
                                                                                cast(CustomerContractMasterModel.EndingContractDate, Date) < cast(CurrentDate, Date)).all()
        if AllDataOfStatus7:
            for Data in AllDataOfStatus7:
                setattr(Data, "IsDeleted", True)  
                setattr(Data, "DeactiveDate", getUTCTime())  
                commit()
            return True
        else:
            return {"message" : "No order found for autocancellation"}, 200  #error