from models.FrameworkModel import pagination
from db import db
from sqlalchemy.sql.expression import desc
from models.WebsiteShopTestingRacketQRCodeDetailModel import ShopTestRacketQRCodeDetailModel



class RacketFilterAndSearchView(db.Model):
    __tablename__ = 'tpv_webiste_shop_test_racket'
    
    ShopTestRacketID = db.Column(db.Integer, primary_key=True)
    ShopID = db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    # MasterTestingRacketID = db.Column(db.Integer)
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    DeactiveDate = db.Column(db.DateTime)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    IsDeleted = db.Column(db.Boolean)
    RacketMasterID = db.Column(db.Integer)
    Brand = db.Column(db.String(200))
    Range = db.Column(db.String(200))
    Modele = db.Column(db.String(200))
    Weight = db.Column(db.Float())
    Version = db.Column(db.String(500))
    HeadSize = db.Column(db.String(200))
    # SleeveSize = db.Column(db.String(200))
    GameLevel = db.Column(db.String(200))
    Description = db.Column(db.String(5000))
    RacketImage_1 = db.Column(db.String(2000))
    RacketImage_2 = db.Column(db.String(2000))
    RacketImage_3 = db.Column(db.String(2000))
    RacketImage_4 = db.Column(db.String(2000))
    ModelDisplayName = db.Column(db.String(2000))
    OldPrice = db.Column(db.Float())
    NewPrice = db.Column(db.Float())
    SortOrder = db.Column(db.Integer)
    Pattern = db.Column(db.String(200))
    Stiffness = db.Column(db.String(200))
    Balance_Unstrung = db.Column(db.String(200))
    SearchCombination = db.Column(db.String(2000))
    RacketRentalDays = db.Column(db.Integer)
    
    def json(self):
        SleeveSize = ShopTestRacketQRCodeDetailModel.GetSleeveSizeForRacket(self.ShopTestRacketID, self.ShopID)
        return {'ShopTestRacketID':self.ShopTestRacketID,
                'ShopID': self.ShopID,
                'RacketMasterID': self.RacketMasterID,
                'Brand':self.Brand,
                'Range':self.Range, 
                'Modele':self.Modele, 
                'Weight':self.Weight,
                'Version' : self.Version,                
                'HeadSize':self.HeadSize,
                'Pattern':self.Pattern,             
                'Description':self.Description,
                'ModelDisplayName' : self.ModelDisplayName,               
                'RacketImage_1':self.RacketImage_1,
                'RacketImage_2':self.RacketImage_2, 
                'RacketImage_3':self.RacketImage_3, 
                'RacketImage_4':self.RacketImage_4, 
                'OldPrice' : self.OldPrice,
                'NewPrice' : self.NewPrice,
                'Stiffness' : self.Stiffness,
                'Balance_Unstrung' : self.Balance_Unstrung,
                'RacketRentalDays': self.RacketRentalDays,
                'SleeveSizeList' : SleeveSize                
                }
        
    def JsonToGetDataAsPerUniqueRacketName(self, ShopID):
        SleeveSize = ShopTestRacketQRCodeDetailModel.GetSleeveSizeAsPerShopTestRacketAsPerQrCodeID(self.id, ShopID)
        ShopTestRacketDetail = RacketFilterAndSearchView.GetShopRacketDetailAsPerShopTestRacketID(self.ShopTestRacketID)
        return {
                'ShopTestRacketID':self.ShopTestRacketID,
                'ShopID': ShopTestRacketDetail.ShopID,
                'RacketMasterID':  ShopTestRacketDetail.RacketMasterID,
                'Brand': ShopTestRacketDetail.Brand,
                'Range': ShopTestRacketDetail.Range, 
                'Modele': ShopTestRacketDetail.Modele, 
                'Weight': ShopTestRacketDetail.Weight,
                'Version' : ShopTestRacketDetail.Version,                
                'HeadSize': ShopTestRacketDetail.HeadSize,
                'Pattern': ShopTestRacketDetail.Pattern,           
                'Description': ShopTestRacketDetail.Description,
                'ModelDisplayName' : ShopTestRacketDetail.ModelDisplayName,               
                'RacketImage_1': ShopTestRacketDetail.RacketImage_1,
                'RacketImage_2': ShopTestRacketDetail.RacketImage_2, 
                'RacketImage_3': ShopTestRacketDetail.RacketImage_3, 
                'RacketImage_4': ShopTestRacketDetail.RacketImage_4, 
                'OldPrice' : ShopTestRacketDetail.OldPrice,
                'NewPrice' : ShopTestRacketDetail.NewPrice,
                'Stiffness' : ShopTestRacketDetail.Stiffness,
                'Balance_Unstrung' : ShopTestRacketDetail.Balance_Unstrung,
                'RacketRentalDays': ShopTestRacketDetail.RacketRentalDays,
                'SleeveSizeID' : SleeveSize['SleeveSizeID'],  
                'SleeveSizeName' : SleeveSize['SleeveSizeName'], 
                'UniqueRacketName' : SleeveSize['UniqueRacketName'],
                'QRCodeID' : SleeveSize['QRCodeID'],
                'QrDate' : SleeveSize['QrDate'],
                'RacketStatusID' : SleeveSize['RacketStatusID'], 
                'RacketNewStatusID' : SleeveSize['RacketNewStatusID'], 
                'WebsiteShopTestRacketQRCodeDetailID' : SleeveSize['WebsiteShopTestRacketQRCodeDetailID']               
                }
        
    @classmethod
    def SearchRacket(cls, ShopID, Page, data):
        query =  db.session.query(RacketFilterAndSearchView).filter(RacketFilterAndSearchView.IsDeleted == 0,RacketFilterAndSearchView.ShopID == ShopID)
        if data['SearchParameter']:
            SearchPara = (data['SearchParameter'].replace(" ","")).strip()
            query = query.filter(*[RacketFilterAndSearchView.SearchCombination.like( '%' + SearchPara + '%' )]) 
        if data['Brand']:
            query = query.filter( RacketFilterAndSearchView.Brand == data['Brand'])
        if data['Range']:
            query = query.filter( RacketFilterAndSearchView.Range == data['Range'])
        if data['Model']:            
            query = query.filter( RacketFilterAndSearchView.Modele == data['Model'])
        query = query.order_by(RacketFilterAndSearchView.SortOrder).paginate(page=Page,per_page=20)
        RacketDetails = [item.json() for item in query.items]
        output= pagination(query,RacketDetails)
        return output
    
    @classmethod
    def RacketFilterListAccodingToSelectionForFilterData(cls,ShopID,data,Page):
        if data['SleeveSize'] is not None:
            query = db.session.query(RacketFilterAndSearchView).filter(RacketFilterAndSearchView.IsDeleted == 0,RacketFilterAndSearchView.ShopID == ShopID,ShopTestRacketQRCodeDetailModel.SleeveSizeID==data['SleeveSize'], ShopTestRacketQRCodeDetailModel.IsDeleted==0).\
                join(ShopTestRacketQRCodeDetailModel,RacketFilterAndSearchView.ShopTestRacketID==ShopTestRacketQRCodeDetailModel.ShopTestRacketID,isouter=True)
        else:
            query = db.session.query(RacketFilterAndSearchView).filter(RacketFilterAndSearchView.IsDeleted == 0,RacketFilterAndSearchView.ShopID == ShopID)  
        if data['OutputVariable'] == 7 :
            query = query.order_by(RacketFilterAndSearchView.SortOrder,RacketFilterAndSearchView.ShopTestRacketID).paginate(page=Page,per_page=20)
            RacketDetails =[item.json() for item in query.items]
            output= pagination(query,RacketDetails)
            return output   
    
    @classmethod
    def SearchRacketAsPerUniqueName(cls, ShopID, Page, data):
        RacketList=[]
        if data['SearchParameter']:            
            query = db.session.query(RacketFilterAndSearchView,ShopTestRacketQRCodeDetailModel).filter(RacketFilterAndSearchView.IsDeleted == 0,RacketFilterAndSearchView.ShopID == ShopID,ShopTestRacketQRCodeDetailModel.UniqueRacketName.like( '%' + data['SearchParameter'] + '%' ), ShopTestRacketQRCodeDetailModel.IsDeleted==0).\
                    join(ShopTestRacketQRCodeDetailModel,RacketFilterAndSearchView.ShopTestRacketID==ShopTestRacketQRCodeDetailModel.ShopTestRacketID,isouter=True)
        else:
            query = db.session.query(RacketFilterAndSearchView,ShopTestRacketQRCodeDetailModel).filter(RacketFilterAndSearchView.IsDeleted == 0,RacketFilterAndSearchView.ShopID == ShopID, ShopTestRacketQRCodeDetailModel.IsDeleted==0).\
                    join(ShopTestRacketQRCodeDetailModel,RacketFilterAndSearchView.ShopTestRacketID==ShopTestRacketQRCodeDetailModel.ShopTestRacketID,isouter=True)
        query = query.order_by(RacketFilterAndSearchView.SortOrder).paginate(page=Page,per_page=20)
        for item in query.items:
            ShopTestRacketQRCodeDetailModelData = item[1]
            ShopTestQRCodeRacketDetails = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(ShopTestRacketQRCodeDetailModelData.id)
            RacketList.append(RacketFilterAndSearchView.JsonToGetDataAsPerUniqueRacketName(ShopTestQRCodeRacketDetails, ShopID))
        output= pagination(query,RacketList)
        return output 
    
    @classmethod
    def GetShopRacketDetailAsPerShopTestRacketID(cls,ShopTestRacketID):
        return db.session.query(RacketFilterAndSearchView).filter(RacketFilterAndSearchView.ShopTestRacketID == ShopTestRacketID, ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
