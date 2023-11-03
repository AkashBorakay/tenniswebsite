from db import db
from models.FrameworkModel import *


class ShopMasterModel(db.Model):    # type: ignore
    __tablename__ = 'tp_shop_master'

    id = db.Column(db.Integer, primary_key=True)
    shopname = db.Column(db.String(50))
    ShopAddress = db.Column(db.String(2000))
    ShopShortAddress = db.Column(db.String(2000))
    ShopPhoneNumber = db.Column(db.String(100))
    password = db.Column(db.String(50))
    tokenid = db.Column(db.String(200))
    IsDeleted = db.Column(db.Boolean)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    SentEmailAddress = db.Column(db.String(500))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    ShopEmailAddress = db.Column(db.String(500))
    PasswordUpdatedDate = db.Column(db.DateTime)
    Longitude = db.Column(db.String(254))
    Latitude = db.Column(db.String(254))
    ShopLogoForMap = db.Column(db.String(2000))
    ShopLogo = db.Column(db.String(2000))
    
    
   


    def __init__(self, ID, shopname, password, tokenid,InsertedBy,UpdatedBy):
        self.shopname = shopname
        self.password = password
        self.tokenid = tokenid
        self.ID = ID
        self.isDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsSystem = 0
        self.CreatedBy = None
        self.InsertedBy = InsertedBy
        self.UpdatedBy = UpdatedBy
        self.PasswordUpdatedDate = getUTCTime()
        

    def json(self):
        return {'ShopID':self.id,
                'tokenid': self.tokenid,
                'ShopName': self.shopname,
                'ShopAddress':self.ShopAddress,
                'ShopShortAddress':self.ShopShortAddress,
                'ShopEmailAddress':self.ShopEmailAddress,
                'ShopPhoneNumber':self.ShopPhoneNumber, 
                'Longitude':float(self.Longitude),
                'Latitude':float(self.Latitude),
                'ShopLogoForMap' : self.ShopLogoForMap,
                'ShopLogo' : self.ShopLogo
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def Auth(cls,ShopID,TokenID):
        query = db.session.query(ShopMasterModel).filter(ShopMasterModel.tokenid == TokenID,ShopMasterModel.id == ShopID,ShopMasterModel.IsDeleted == 0).first()
        return query

    @classmethod
    def GetAllShop(cls):
        return db.session.query(ShopMasterModel).filter(ShopMasterModel.IsDeleted == 0).order_by(ShopMasterModel.shopname).all()
    
    @classmethod
    def ShopDetail(cls,ShopID):
        return db.session.query(ShopMasterModel).filter(ShopMasterModel.IsDeleted == 0,ShopMasterModel.id == ShopID).first()
    
    @classmethod
    def ShopDetailUsingShopIDAndAuthorizationToken(cls,ShopID,Authorization):
        return db.session.query(ShopMasterModel).filter(ShopMasterModel.IsDeleted == 0,ShopMasterModel.id == ShopID,ShopMasterModel.tokenid == Authorization).first()