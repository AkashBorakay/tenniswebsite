import re
from flask.json import jsonify
from sqlalchemy.orm import query
from sqlalchemy.orm.query import Query
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.operators import json_path_getitem_op
from db import db
from sqlalchemy.orm import backref, relationship
from models.FrameworkModel import commit, pagination,getUTCTime, save_to_db
from datetime import datetime, date
from sqlalchemy.sql.elements import Null, or_, and_
# from models.AgeGroupModel import AgeGroupModel
from models.ShopMasterModel import ShopMasterModel
from models.CountryMasterModel import CountryMasterModel
from models.WebsiteCustomerContractModel import CustomerContractMasterModel
from models.WebsiteContractMasterModel import ContractMasterModel
# from models.WebsiteRacketBookingDetailModel import RacketBookingDetailMasterModel
from models.FrameworkModel import pagination
from hashlib import sha256
from array import array
from models.WebsiteShopClientModel import CustomerShopModel


class CustomerDetailModel(db.Model):
    __tablename__ = 'tp_website_customer'
    
    id = db.Column(db.Integer, primary_key=True)
    Fname = db.Column(db.String(50))
    Lname = db.Column(db.String(50))
    EmailAddress = db.Column(db.String(200))
    PhoneNo = db.Column(db.String(50))
    ClubID = db.Column(db.Integer)
    ShopFavoryID = db.Column(db.Integer)
    BirthDate = db.Column(db.Date())
    EmailAddressVerified = db.Column(db.Boolean)
    IsSubscribed = db.Column(db.Boolean)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=getUTCTime())
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.String(50))
    IsCoach = db.Column(db.Boolean)
    IsGDPRAccepted = db.Column(db.Boolean)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    CustomerSearch = db.Column(db.String(500))
    IsChampion = db.Column(db.Boolean)
    CountryID = db.Column(db.Integer)
    IsCustomerCreatedFromWebsite = db.Column(db.Boolean)
    IsCorrectEmailID = db.Column(db.Boolean)
    Password = db.Column(db.String(2000))
    PasswordCreatedDate = db.Column(db.DateTime)
    PasswordUpdatedDate = db.Column(db.DateTime)
    Picture = db.Column(db.String(2000))
      
   
    def __init__(self, Fname, Lname, EmailAddress, PhoneNo, ShopFavoryID, BirthDate, CustomerSearch, CountryID, Password, InsertedBy, Picture):
        self.Fname = Fname
        self.Lname = Lname
        self.EmailAddress = EmailAddress
        self.PhoneNo = PhoneNo
        self.ShopFavoryID = ShopFavoryID
        self.ClubID = None
        self.BirthDate = BirthDate and  datetime.strptime(BirthDate, '%d/%m/%Y').date() or None
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate =  getUTCTime()#datetime.now()
        self.IsSystem = 0
        self.CreatedBy = None
        self.IsCoach = None
        self.CustomerSearch = CustomerSearch
        self.IsChampion = None
        self.CountryID = CountryID
        self.Password= Password
        self.EmailAddressVerified = False
        self.InsertedBy = InsertedBy
        self.UpdatedBy = None
        self.PasswordCreatedDate = getUTCTime()
        self.PasswordUpdatedDate = getUTCTime()
        self.Picture = Picture
        self.IsCustomerCreatedFromWebsite = True
        

    def json1(self):
        ShopDetail = ShopMasterModel.ShopDetail(self.ShopFavoryID)
        if ShopDetail:
            ShopName = ShopDetail.shopname
        else:
            ShopName = None
        CountryDetail = CountryMasterModel.GetCountryName(self.CountryID)
        if CountryDetail:
            CountryName = CountryDetail.CountryName
            CountryCode = CountryDetail.CountryCode
        else:
            CountryName = None
            CountryCode = None            
        return {
             'CustomerID': self.id,
                 'ShopFavoryID' :self.ShopFavoryID or None,
                 'ShopName' : ShopName,
                 'BirthDate' : self.BirthDate and self.BirthDate.strftime('%d/%m/%Y') or None,
                 'EmailAddressVerified' : self.EmailAddressVerified,
                 'IsGDPRAccepted' : self.IsGDPRAccepted,
                 'Fname': self.Fname,
                 'Lname': self.Lname,
                 'EmailAddress': self.EmailAddress,
                 'PhoneNo' : self.PhoneNo,
                 'IsSubscribed': self.IsSubscribed,
                 'IsDeleted':self.IsDeleted,
                 'IsCoach' : self.IsCoach,
                 'CustomerSearch' : self.CustomerSearch,
                 'IsChampion' : self.IsChampion,
                 'CountryID' : self.CountryID or None,
                 'CountryName' : CountryName,
                 'CountryCode' : CountryCode,
                 'Picture': self.Picture
        }
        
    def json(self):
        CustomerContractDetail = CustomerContractMasterModel.GetCustomerAllContracts(self.id)
        if CustomerContractDetail:
            ContractDetail =  CustomerContractDetail
        else:
            ContractDetail =  None       
        ShopDetail = ShopMasterModel.ShopDetail(self.ShopFavoryID)
        if ShopDetail:
            ShopName = ShopDetail.shopname
        else:
            ShopName = None
        CountryDetail = CountryMasterModel.GetCountryName(self.CountryID)
        if CountryDetail:
            CountryName = CountryDetail.CountryName
            CountryCode = CountryDetail.CountryCode
        else:
            CountryName = None
            CountryCode = None            
        return {
             'CustomerID': self.id,
                 'ShopFavoryID' :self.ShopFavoryID or None,
                 'ShopName' : ShopName,
                 'BirthDate' : self.BirthDate and self.BirthDate.strftime('%d/%m/%Y') or None,
                 'EmailAddressVerified' : self.EmailAddressVerified,
                 'IsGDPRAccepted' : self.IsGDPRAccepted,
                 'Fname': self.Fname,
                 'Lname': self.Lname,
                 'EmailAddress': self.EmailAddress,
                 'PhoneNo' : self.PhoneNo,
                 'IsSubscribed': self.IsSubscribed,
                 'IsDeleted':self.IsDeleted,
                 'IsCoach' : self.IsCoach,
                 'CustomerSearch' : self.CustomerSearch,
                 'IsChampion' : self.IsChampion,
                 'CountryID' : self.CountryID or None,
                 'CountryName' : CountryName,
                 'CountryCode' : CountryCode,
                 'ContractDetail' : ContractDetail or None,
                 'Picture': self.Picture
        }
        
    def CustomerDetailJson(self,ShopID):
        CustomerContractDetail = CustomerContractMasterModel.GetCustomerContractV3(self.id, ShopID)
        if CustomerContractDetail:
            ContractDetail =  CustomerContractDetail      
        else:
            ContractDetail = None
        ShopDetail = ShopMasterModel.ShopDetail(self.ShopFavoryID)
        if ShopDetail:
            ShopName = ShopDetail.shopname
        else:
            ShopName = None
        CountryDetail = CountryMasterModel.GetCountryName(self.CountryID)
        if CountryDetail:
            CountryName = CountryDetail.CountryName
            CountryCode = CountryDetail.CountryCode
        else:
            CountryName = None
            CountryCode = None            
        return {
             'CustomerID': self.id,
                 'ShopFavoryID' :self.ShopFavoryID or None,
                 'ShopName' : ShopName,
                 'BirthDate' : self.BirthDate and self.BirthDate.strftime('%d/%m/%Y') or None,
                 'EmailAddressVerified' : self.EmailAddressVerified,
                 'IsGDPRAccepted' : self.IsGDPRAccepted,
                 'Fname': self.Fname,
                 'Lname': self.Lname,
                 'EmailAddress': self.EmailAddress,
                 'PhoneNo' : self.PhoneNo,
                 'IsSubscribed': self.IsSubscribed,
                 'IsDeleted':self.IsDeleted,
                 'IsCoach' : self.IsCoach,
                 'CustomerSearch' : self.CustomerSearch,
                 'IsChampion' : self.IsChampion,
                 'CountryID' : self.CountryID or None,
                 'CountryName' : CountryName,
                 'CountryCode' : CountryCode,
                 'ContractDetail' : ContractDetail,
                 'Picture': self.Picture
        }
        
    
    @classmethod
    def GetCustomerDetailForLogin(cls,EmailAddress,Password):
        query = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.EmailAddress == EmailAddress,
                                                             CustomerDetailModel.Password == Password,
                                                             CustomerDetailModel.IsDeleted == 0).first()
        return query
    
    @classmethod
    def CheckCustomerExistOrNot(cls,EmailAddress):
        query = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.EmailAddress == EmailAddress, CustomerDetailModel.IsDeleted == 0).first()
        return query

    @classmethod
    def GetCustomerDetailUsingCustomerID(cls,CustomerID):
        query = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.id == CustomerID, CustomerDetailModel.IsDeleted == 0).first()
        return query

    @classmethod
    def UpdateCustomer(cls,**data):
        CustomerID = data.get('ID')
        BirthDate1 = data.get('BirthDate')
        BirthDate = datetime.strptime(BirthDate1, "%d/%m/%Y")
        data.pop("BirthDate")
        query = CustomerDetailModel.GetCustomerDetailUsingCustomerID(CustomerID)
        if query is not None:
            setattr(query, "UpdatedDate", getUTCTime())  
            setattr(query, "BirthDate", BirthDate)  
            for key, value in data.items():
                setattr(query, key, value) 
            commit()
        return query
    
    @classmethod
    def GetCustomerToUpdatePassword(cls,CustomerID,Password): 
        query = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.id == CustomerID,CustomerDetailModel.IsDeleted == 0,CustomerDetailModel.Password == Password).first()
        return query
    
    #2 - when new password is same as the old password saved in the db   
    # 1 - password update successfully     
    # 0 - detail not found with old Password
    @classmethod
    def UpdateCustomerPassword(cls,**data):
        CustomerID = data.get('CustomerID')
        OldPWD = data.get('OldPassword')
        NewPWD = data.get('NewPassword')
        OldPassword = sha256(OldPWD.encode()).hexdigest()
        NewPassword = sha256(NewPWD.encode()).hexdigest()
        UpdatedBy = data.get('UpdatedBy')
        query = CustomerDetailModel.GetCustomerToUpdatePassword(CustomerID,NewPassword)
        query1 = CustomerDetailModel.GetCustomerToUpdatePassword(CustomerID,OldPassword)
        if query1 is None:
            return 0
        else:
            if query is not None:
                return 2
            else:
                Password = "Password"
                Password = NewPassword
                EncodedPassword = sha256(Password.encode()).hexdigest()
                setattr(query1, "Password", EncodedPassword)
                setattr(query1, "UpdatedBy", UpdatedBy)
                setattr(query1, "PasswordUpdatedDate",getUTCTime())
                commit()
                return 1
            
    @classmethod
    def DeleteCustomer(cls, CustomerID,UpdatedBy):
        query = CustomerDetailModel.GetCustomerDetailUsingCustomerID(CustomerID)
        if query:
            setattr(query, "IsDeleted", 1)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "UpdatedDate", getUTCTime())
        commit()
        return query
    
    @classmethod
    def GetSearchCustomerForDashboard(cls,NameFilter):
        SearchParamter = (NameFilter.replace(" ","")).strip()
        return db.session.query(CustomerDetailModel).\
            filter(CustomerDetailModel.IsDeleted==0,CustomerDetailModel.CustomerSearch.like('%' + SearchParamter + '%')).all()
            
    def customer_details(ShopID,CustomerDetail = None):
        Output={}
        Output['CustomerDetail'] = CustomerDetail.CustomerDetailJson(ShopID) if CustomerDetail else None
        return Output
    
    @classmethod
    def GetAllCustomerList(cls,Page,ShopID,NameFilter):
        if NameFilter is None:
            CustomersList=[]
            CustomerData = None
            CustomersData = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.IsDeleted == 0).order_by(CustomerDetailModel.Lname).paginate(page=Page,per_page=20)
            if CustomersData:
                    for CustomerData in CustomersData.items:
                        CustomersList.append(CustomerDetailModel.customer_details(ShopID,CustomerData))
                    CustomersList= pagination(CustomersData,CustomersList)
                    return CustomersList
            else:
                return{"message" : "No customer found"}
        else:
            CustomersList=[]
            CustomerData = None
            CustomerDetail = CustomerDetailModel.GetSearchCustomerForDashboard(NameFilter)
            CustomerIDArray=[]
            if CustomerDetail is not None:
                for customerdetail in CustomerDetail:
                    CustomerIDArray.append(customerdetail.id)
            else:
                CustomersList= pagination(0,CustomersList)
                return CustomersList
            CustomersData = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.IsDeleted == 0,CustomerDetailModel.id.in_(CustomerIDArray)).order_by(CustomerDetailModel.Lname).paginate(page=Page,per_page=20)
            if CustomersData:
                    for CustomerData in CustomersData.items:
                        CustomersList.append(CustomerDetailModel.customer_details(ShopID,CustomerData))
                    CustomersList= pagination(CustomersData,CustomersList)
                    return CustomersList
            else:
                return{"message" : "No customer found"}
            
    @classmethod
    def GetAllCustomerListV2(cls,Page,ShopID,NameFilter):
        if NameFilter is None:
            CustomersList=[]
            CustomerData = None
            CustomersData = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.IsDeleted == 0, CustomerDetailModel.id == CustomerShopModel.CustomerID, 
                                                             CustomerShopModel.ShopID == ShopID).order_by(CustomerDetailModel.Lname).paginate(page=Page,per_page=20)
            if CustomersData:
                    for CustomerData in CustomersData.items:
                        CustomersList.append(CustomerDetailModel.customer_details(ShopID,CustomerData))
                    CustomersList= pagination(CustomersData,CustomersList)
                    return CustomersList
            else:
                return{"message" : "No customer found"}
        else:
            CustomersList=[]
            CustomerData = None
            CustomerDetail = CustomerDetailModel.GetSearchCustomerForDashboard(NameFilter)
            CustomerIDArray=[]
            if CustomerDetail is not None:
                for customerdetail in CustomerDetail:
                    CustomerIDArray.append(customerdetail.id)
            else:
                CustomersList= pagination(0,CustomersList)
                return CustomersList
            CustomersData = db.session.query(CustomerDetailModel).filter(CustomerDetailModel.IsDeleted == 0,CustomerDetailModel.id.in_(CustomerIDArray), 
                                                                         CustomerDetailModel.id == CustomerShopModel.CustomerID, 
                                                                         CustomerShopModel.ShopID == ShopID).order_by(CustomerDetailModel.Lname).paginate(page=Page,per_page=20)
            if CustomersData:
                    for CustomerData in CustomersData.items:
                        CustomersList.append(CustomerDetailModel.customer_details(ShopID,CustomerData))
                    CustomersList= pagination(CustomersData,CustomersList)
                    return CustomersList
            else:
                return{"message" : "No customer found"}
            
    @classmethod
    def UpdateShopPasswordThrougEmailFunctionality(cls, CustomerID, EncodedPassword):
        query = CustomerDetailModel.GetCustomerDetailUsingCustomerID(CustomerID)
        if query is not None:
            setattr(query, "Password", EncodedPassword)
            setattr(query, "PasswordUpdatedDate", getUTCTime())
            commit()
            return EncodedPassword
       