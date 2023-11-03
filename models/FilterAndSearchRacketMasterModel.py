from models.FrameworkModel import pagination
from db import db
# from sqlalchemy.sql.expression import desc
from models.WebsiteShopTestingRacketQRCodeDetailModel import ShopTestRacketQRCodeDetailModel
    
# !!! part racket master 
class RacketMasterFilterView(db.Model):
    __tablename__ = 'tpv_RacketMasterFilter_1'
    ShopTestRacketID = db.Column(db.Integer)
    MasterTestingRacketID = db.Column(db.Integer, primary_key=True)
    ShopID = db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    Brand = db.Column(db.String(200))
    Range = db.Column(db.String(200))
    Modele = db.Column(db.String(200))
    HeadSize = db.Column(db.String(200))
    Version = db.Column(db.String(500))
    Weight = db.Column(db.Float())
    WeightOZ = db.Column(db.Float())
    Pattern = db.Column(db.String(200))
    Stiffness = db.Column(db.String(200))
    Balance_Unstrung = db.Column(db.String(200))
    RacketImage_1 = db.Column(db.String(2000))
    RacketImage_2 = db.Column(db.String(2000))
    RacketImage_3 = db.Column(db.String(2000))
    RacketImage_4 = db.Column(db.String(2000))
    ModelDisplayName = db.Column(db.String(2000))
    SearchCombination = db.Column(db.String(2000))
    Description = db.Column(db.String(5000))
    OldPrice = db.Column(db.Float())
    NewPrice = db.Column(db.Float())
    RacketRentalDays = db.Column(db.Integer)


    def json(self):
        SleeveSize = ShopTestRacketQRCodeDetailModel.GetSleeveSizeForRacket(self.ShopTestRacketID, self.ShopID)
        return {'ShopTestRacketID':self.ShopTestRacketID,
                'ShopID': self.ShopID,
                'RacketMasterID': self.MasterTestingRacketID,
                'Brand':self.Brand,
                'Range':self.Range, 
                'Modele':self.Modele, 
                'Weight':self.Weight,
                'WeightOZ':self.WeightOZ,
                'Version' : self.Version,              
                'RacketImage_1':self.RacketImage_1,
                'RacketImage_2':self.RacketImage_2, 
                'RacketImage_3':self.RacketImage_3, 
                'RacketImage_4':self.RacketImage_4,         
                'Pattern':self.Pattern,       
                'HeadSize':self.HeadSize,      
                'Stiffness' : self.Stiffness,
                'Balance_Unstrung' : self.Balance_Unstrung,   
                'ModelDisplayName' : self.ModelDisplayName,      
                'Description':self.Description,
                'OldPrice' : self.OldPrice,
                'NewPrice' : self.NewPrice,
                'RacketRentalDays': self.RacketRentalDays               
                }
                
    def jsonBrand(self):
        return {
        'Brand': self.Brand,
        }
        
    def jsonModel(self):
        return {
        'Model' : self.Modele
        }

    def jsonRange(self):
        return {
        'Range': self.Range
        }
        
    def jsonVersion(self):
        return {
        'Version': self.Version
        }
    
    def jsonWeight(self): 
        return {
        'Weight': self.Weight
        }         
        
    @classmethod
    def RacketFilterListAccodingToSelectionForFilterData(cls,ShopID, data, Page):            
        query =  db.session.query(RacketMasterFilterView).filter(RacketMasterFilterView.ShopID == ShopID)

        if data['SearchParameter']:
            SearchPara = (data['SearchParameter'].replace(" ","")).strip()
            query = query.filter(*[RacketMasterFilterView.SearchCombination.like( '%' + SearchPara + '%' )]) 
        
        if data['Brand'] is not None:
            Brand = data['Brand'].split(",")
            query = query.filter( RacketMasterFilterView.Brand.in_(Brand))
        if data['Range'] is not None:
            Range = data['Range'].split(",")
            query = query.filter(RacketMasterFilterView.Range.in_(Range))
        if data['Model'] is not None:
            Model = data['Model'].split(",")
            query = query.filter(RacketMasterFilterView.Modele.in_(Model))
        if data['Version'] is not None:
            Version = data['Version'].split(",")
            query = query.filter(RacketMasterFilterView.Version.in_(Version))
        if data['Weight'] is not None:
            Weight = data['Weight'].split(",")
            query = query.filter(RacketMasterFilterView.Weight.in_(Weight))
            
        if data['OutputVariable'] == 1:
            query = query.order_by(RacketMasterFilterView.Brand).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonBrand() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 2:
            query = query.order_by(RacketMasterFilterView.Range).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonRange() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 3:
            query = query.order_by(RacketMasterFilterView.Modele).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonModel() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 4:
            query = query.order_by(RacketMasterFilterView.Version).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonVersion() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 5:
            query = query.order_by(RacketMasterFilterView.Weight).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonWeight() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 7 :
            query = query.order_by(RacketMasterFilterView.ModelDisplayName).paginate(page=Page,per_page=20)
            RacketDetails =[item.json() for item in query.items]
            output= pagination(query,RacketDetails)
            return output
        
    @classmethod
    def SearchRacket(cls, ShopID, Page, data):
        query =  db.session.query(RacketMasterFilterView).filter(RacketMasterFilterView.ShopID == ShopID)

        if data['SearchParameter']:
            SearchPara = (data['SearchParameter'].replace(" ","")).strip()
            query = query.filter(*[RacketMasterFilterView.SearchCombination.like( '%' + SearchPara + '%' )]) 
        if data['Brand']:
            Brand = data['Brand'].split(",")
            query = query.filter( RacketMasterFilterView.Brand.in_(Brand))
        if data['Range']:
            Range = data['Range'].split(",")
            query = query.filter( RacketMasterFilterView.Range.in_(Range))
        if data['Model']:
            Model = data['Model'].split(",")         
            query = query.filter( RacketMasterFilterView.Modele.in_(Model))

        query = query.paginate(page=Page,per_page=20)
        RacketDetails = [item.json() for item in query.items]
        output= pagination(query,RacketDetails)
        return output

    @classmethod
    def GetShopRacketDetailAsPerShopTestRacketID(cls,ShopTestRacketID):
        return db.session.query(RacketMasterFilterView).filter(RacketMasterFilterView.ShopTestRacketID == ShopTestRacketID).first()
    