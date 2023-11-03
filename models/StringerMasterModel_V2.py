from datetime import datetime,timedelta
from models.FrameworkModel import commit, getUTCTime
from db import db
from importlib.machinery import SourcelessFileLoader
from sqlalchemy.sql import func
# from models.WebsiteRoleAssignmentModel import  WebsiteRoleAssignmentModel
# from models.ApplicationRoleAssignmentModel import  ApplicationRoleAssignmentModel
from hashlib import sha256


class StringerMasterModel(db.Model):  # type: ignore
    __tablename__ = 'tp_website_stringer_master'

    id=db.Column(db.Integer, primary_key=True)
    ShopID=db.Column(db.Integer,db.ForeignKey('tp_shop_master.id'))
    Name=db.Column(db.String(200))
    Lname = db.Column(db.String(200))
    EmailAddress=db.Column(db.String(254))
    PhoneNumber=db.Column(db.String(50))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime) #func.now(pytz.timezone('Europe/Amsterdam'))
    PasswordUpdatedDate = db.Column(db.DateTime)
    LastConnection = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    Password = db.Column(db.String(1024))
    CreatedBy = db.Column(db.String(50))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    AccessToApplication = db.Column(db.Boolean)
    AccessToWebsite = db.Column(db.Boolean)
    RoleID = db.Column(db.Integer)
    
    def __init__(self, ShopID, Name, Lname, PhoneNumber, InsertedBy, EmailAddress, AccessToApplication, AccessToWebsite, RoleID):
        self.ShopID=ShopID
        self.Name=Name
        self.Lname =Lname
        self.PhoneNumber=PhoneNumber
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = self.CreatedDate
        self.IsDeleted = 0
        self.CreatedBy = None
        self.Password = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = None
        self.EmailAddress = EmailAddress
        self.PasswordUpdatedDate = self.CreatedDate
        self.AccessToApplication = AccessToApplication
        self.AccessToWebsite = AccessToWebsite
        self.RoleID = RoleID

    def json(self):
        return {
            "StringerID":self.id,
            "FName":self.Name,
            "Lname":self.Lname,
            "PhoneNumber":self.PhoneNumber,
            "AccessToWebsite":self.AccessToWebsite,
            "AccessToApplication":self.AccessToApplication,
            "Password":self.Password,
            "EmailAddress":self.EmailAddress,
            "RoleID" : self.RoleID,
            "DateAccess":self.LastConnection,
            "DatePwd":self.PasswordUpdatedDate
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
        # query = WebsiteRoleAssignmentModel.GetWebsiteRoleAssignmentMasterForStringerID(StringerID)
        # if query:
        #     setattr(query, "IsDeleted", 1)
        #     setattr(query, "UpdatedBy", UpdatedBy)
        #     setattr(query, "UpdatedDate", getUTCTime())
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
        # query = WebsiteRoleAssignmentModel.GetWebsiteRoleAssignmentMasterForStringerID(StringerID)
        # if query:
        #     if query.RoleID != NewRoleID:
        #         setattr(query, "RoleID", NewRoleID)
        #         setattr(query, "UpdatedDate", getUTCTime())                    
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
                    
    @classmethod
    def ConnectionLast(cls, NewRoleID,ShopID, **data):
        StringerID = data.get('StringerID')
        query = StringerMasterModel.GetStringer(StringerID, ShopID)
        if query is not None:
            setattr(query, "LastConnection", getUTCTime())                        
        commit()
        return query
    
    @classmethod
    def GetShopRoleAssignmentMasterForStringerID(cls, StringerID):
        return db.session.query(StringerMasterModel).filter(StringerMasterModel.id == StringerID, StringerMasterModel.IsDeleted == 0).first()   
    