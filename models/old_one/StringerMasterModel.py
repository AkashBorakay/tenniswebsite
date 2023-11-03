from datetime import datetime,timedelta
from models.FrameworkModel import commit, getUTCTime
from db import db
from importlib.machinery import SourcelessFileLoader
from sqlalchemy.sql import func
from models.WebsiteRoleAssignmentModel import  WebsiteRoleAssignmentModel
from models.ApplicationRoleAssignmentModel import  ApplicationRoleAssignmentModel
from hashlib import sha256


class StringerMasterModel(db.Model):  # type: ignore
    __tablename__ = 'tp_stringer_master'

    id=db.Column(db.Integer, primary_key=True)
    ShopID=db.Column(db.Integer,db.ForeignKey('tp_shop_master.id'))
    Name=db.Column(db.String(200))
    PhoneNumber=db.Column(db.String(50))
    StartTiming=db.Column(db.Time)
    CloseTiming=db.Column(db.Time)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime) #func.now(pytz.timezone('Europe/Amsterdam'))
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.String(50))
    Password = db.Column(db.String(1024))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    EmailAddress=db.Column(db.String(254))
    PasswordUpdatedDate = db.Column(db.DateTime)
    Lname = db.Column(db.String(200))
    AccessToApplication = db.Column(db.Boolean)
    AccessToWebsite = db.Column(db.Boolean)
    


    # def __init__(self,ShopID,Name,Lname,Age,Address,PhoneNumber,StartTiming,CloseTiming,InsertedBy,EmailAddress):
    def __init__(self, ShopID, Name, Lname, PhoneNumber, InsertedBy, EmailAddress, AccessToApplication, AccessToWebsite):
        self.ShopID=ShopID
        self.Name=Name
        self.Lname =Lname
        self.PhoneNumber=PhoneNumber
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = self.CreatedDate
        self.IsDeleted = 0
        self.IsSystem = 0
        self.CreatedBy = None
        self.Password = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = None
        self.EmailAddress = EmailAddress
        self.PasswordUpdatedDate = self.CreatedDate
        self.AccessToApplication = AccessToApplication
        self.AccessToWebsite = AccessToWebsite


    def json(self):
        RoleOfStringer = WebsiteRoleAssignmentModel.GetWebsiteRoleAssignmentMasterForStringerID(self.id)
        return {
            "StringerID":self.id,
            "FName":self.Name,
            "Lname":self.Lname,
            "PhoneNumber":self.PhoneNumber,
            "AccessToWebsite":self.AccessToWebsite,
            "AccessToApplication":self.AccessToApplication,
            "Password":self.Password,
            "EmailAddress":self.EmailAddress,
            "RoleID" : RoleOfStringer.RoleID
        }
        
    @classmethod
    def GetStringerDetailForLogin(cls,EmailAddress,Password):
        query = db.session.query(StringerMasterModel).filter(StringerMasterModel.EmailAddress == EmailAddress, 
                                                             StringerMasterModel.Password == Password, 
                                                             StringerMasterModel.IsDeleted == 0, 
                                                             StringerMasterModel.AccessToWebsite == 1).first()
        return query
    
    @classmethod
    def GetStringer(cls,StringerID, ShopID): 
        query = db.session.query(StringerMasterModel).filter(StringerMasterModel.id == StringerID, 
                                                             StringerMasterModel.ShopID == ShopID,
                                                             StringerMasterModel.IsDeleted == 0).first()
        return query
    
    @classmethod
    def CheckStringerExistOrNot(cls,EmailAddress):
        query = db.session.query(StringerMasterModel).filter(StringerMasterModel.EmailAddress == EmailAddress, StringerMasterModel.IsDeleted == 0).first()
        return query
    
    @classmethod
    def DeleteStringerMasterAndRoleAssignment(cls, StringerID, ShopID,UpdatedBy):
        query = StringerMasterModel.GetStringer(StringerID, ShopID)
        if query:
            setattr(query, "IsDeleted", 1)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "UpdatedDate", getUTCTime())
        query = WebsiteRoleAssignmentModel.GetWebsiteRoleAssignmentMasterForStringerID(StringerID)
        if query:
            setattr(query, "IsDeleted", 1)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "UpdatedDate", getUTCTime())
        query = ApplicationRoleAssignmentModel.GetShopRoleAssignmentMasterForStringerID(StringerID)
        if query:
            setattr(query, "IsDeleted", 1)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "UpdatedDate", getUTCTime())
        commit()
        return query
    
    @classmethod
    def UpdateStringerMaster(cls, NewRoleID,ShopID, **data):
        StringerID = data.get('StringerID')
        UpdatedBy  = data.get('UpdatedBy')
        query = StringerMasterModel.GetStringer(StringerID, ShopID)
        if query is not None:
            for key, value in data.items():
                setattr(query, key, value)
            setattr(query, "UpdatedDate", getUTCTime())    
        query = WebsiteRoleAssignmentModel.GetWebsiteRoleAssignmentMasterForStringerID(StringerID)
        if query:
            if query.RoleID != NewRoleID:
                setattr(query, "RoleID", NewRoleID)
                setattr(query, "UpdatedDate", getUTCTime())                    
        commit()
        return query
    
    
    @classmethod
    def GetStringerToUpdatePassword(cls,StringerID, ShopID,Password): 
        query = db.session.query(StringerMasterModel).filter(StringerMasterModel.id == StringerID, StringerMasterModel.ShopID == ShopID ,StringerMasterModel.IsDeleted == 0,StringerMasterModel.Password == Password).first()
        return query
    
    @classmethod
    def UpdateStringerPassword(cls, ShopID, **data):
        StringerID = data.get('StringerID')
        OldPWD = data.get('OldPassword')
        NewPWD = data.get('NewPassword')
        OldPassword = sha256(OldPWD.encode()).hexdigest()
        NewPassword = sha256(NewPWD.encode()).hexdigest()
        UpdatedBy = data.get('UpdatedBy')
        query = StringerMasterModel.GetStringerToUpdatePassword(StringerID, ShopID,NewPassword)
        query1 = StringerMasterModel.GetStringerToUpdatePassword(StringerID, ShopID,OldPassword)
        if query1 is None:
            return 0
        else:
            if query is not None:
                return 2
            else:
                # Password = "Password"
                # Password = NewPassword
                # EncodedPassword = sha256(Password.encode()).hexdigest()
                # setattr(query1, "Password", EncodedPassword)
                # setattr(query1, "UpdatedBy", UpdatedBy)
                # setattr(query1, "PasswordUpdatedDate",getUTCTime())
                setattr(query1, "Password", NewPassword)
                setattr(query1, "UpdatedBy", UpdatedBy)
                setattr(query1, "PasswordUpdatedDate",getUTCTime())
                commit()
                return 1
            
    @classmethod
    def GetStringerList(cls,ShopID): 
        query = db.session.query(StringerMasterModel).filter(StringerMasterModel.ShopID == ShopID,StringerMasterModel.IsDeleted == 0).order_by(StringerMasterModel.Lname).all()
        return query
    
    @classmethod
    def CreateStringerPasswordThrougEmailFunctionality(cls, StringerID,ShopID,EncodedPassword):
        query = StringerMasterModel.GetStringer(StringerID,ShopID)
        if query is not None:
            setattr(query, "Password", EncodedPassword)
            setattr(query, "CreatedDate", getUTCTime())
            setattr(query, "UpdatedDate", getUTCTime())
            commit()
            return 1

    @classmethod
    def UpdateStringerPasswordThrougEmailFunctionality(cls, StringerID, ShopID, EncodedPassword):
        query = StringerMasterModel.GetStringer(StringerID,ShopID)
        if query is not None:
            setattr(query, "Password", EncodedPassword)
            setattr(query, "PasswordUpdatedDate", getUTCTime())
            commit()
            return EncodedPassword
                    