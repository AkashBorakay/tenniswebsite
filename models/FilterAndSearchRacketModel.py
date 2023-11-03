from models.FrameworkModel import pagination
from db import db
# from sqlalchemy.sql.expression import desc
from models.WebsiteShopTestingRacketQRCodeDetailModel import ShopTestRacketQRCodeDetailModel
# from models.WebsiteShopTestingRacketModel import  ShopTestRacketModel


class RacketTestingFilterView(db.Model):
    __tablename__ = 'tpv_RacketTestingFilter'
    ShopTestRacketID = db.Column(db.Integer, primary_key=True)
    SleeveSizeID = db.Column(db.Integer)
    MasterTestingRacketID = db.Column(db.Integer)
    ShopID = db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    Brand = db.Column(db.String(200))
    Range = db.Column(db.String(200))
    Modele = db.Column(db.String(200))
    Version = db.Column(db.String(500))
    Weight = db.Column(db.Float())
    WeightOZ = db.Column(db.Float())
    HeadSize = db.Column(db.String(200))
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
    NbRacket = db.Column(db.Integer)
    Nb_NA = db.Column(db.Integer)
    
    def json(self):
        SleeveSize = ShopTestRacketQRCodeDetailModel.GetSleeveSizeForRacket(self.ShopTestRacketID)
        if self.NbRacket - self.Nb_NA == 0:
            Available = False
        else:
            Available = True
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
                'RacketRentalDays': self.RacketRentalDays,
                'Qty_Racket': self.NbRacket,
                'Qty_NA_Racket': self.Nb_NA,
                'Available': Available,
                'SleeveSizeList' : SleeveSize                
                }
    
    def json2(self):
        SleeveSize = ShopTestRacketQRCodeDetailModel.GetSleeveSizeForRacket2(self.ShopTestRacketID)
        if self.NbRacket - self.Nb_NA == 0:
            Available = False
        else:
            Available = True
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
                'RacketRentalDays': self.RacketRentalDays,
                'Qty_Racket': self.NbRacket,
                'Qty_NA_Racket': self.Nb_NA,
                'Available': Available,
                'SleeveSizeList' : SleeveSize                
                }
    # def jsonInfo(self):
    #     SleeveSize = ShopTestRacketQRCodeDetailModel.GetSleeveSizeAsPerShopTestRacketAsPerQrCodeID(self.id)
    #     ShopTestRacketDetail = RacketTestingFilterView.GetShopRacketDetailAsPerShopTestRacketID(self.ShopTestRacketID)
    #     return {
    #             'ShopTestRacketID':self.ShopTestRacketID,
    #             'ShopID': ShopTestRacketDetail.ShopID,
    #             'RacketMasterID':  ShopTestRacketDetail.MasterTestingRacketID,
    #             'Brand': ShopTestRacketDetail.Brand,
    #             'Range': ShopTestRacketDetail.Range, 
    #             'Modele': ShopTestRacketDetail.Modele, 
    #             'Weight': ShopTestRacketDetail.Weight,
    #             'Version' : ShopTestRacketDetail.Version,                
    #             'HeadSize': ShopTestRacketDetail.HeadSize,
    #             'Pattern': ShopTestRacketDetail.Pattern,           
    #             'Description': ShopTestRacketDetail.Description,
    #             'ModelDisplayName' : ShopTestRacketDetail.ModelDisplayName,               
    #             'RacketImage_1': ShopTestRacketDetail.RacketImage_1,
    #             'RacketImage_2': ShopTestRacketDetail.RacketImage_2, 
    #             'RacketImage_3': ShopTestRacketDetail.RacketImage_3, 
    #             'RacketImage_4': ShopTestRacketDetail.RacketImage_4, 
    #             'OldPrice' : ShopTestRacketDetail.OldPrice,
    #             'NewPrice' : ShopTestRacketDetail.NewPrice,
    #             'Stiffness' : ShopTestRacketDetail.Stiffness,
    #             'Balance_Unstrung' : ShopTestRacketDetail.Balance_Unstrung,
    #             'RacketRentalDays': ShopTestRacketDetail.RacketRentalDays,
    #             'SleeveSizeID' : SleeveSize['SleeveSizeID'],  
    #             'SleeveSizeName' : SleeveSize['SleeveSizeName'], 
    #             'UniqueRacketName' : SleeveSize['UniqueRacketName'],
    #             'QRCodeID' : SleeveSize['QRCodeID'],
    #             'RacketStatusID' : SleeveSize['RacketStatusID'], 
    #             'RacketNewStatusID' : SleeveSize['RacketNewStatusID'], 
    #             'WebsiteShopTestRacketQRCodeDetailID' : SleeveSize['WebsiteShopTestRacketQRCodeDetailID']    
    #             }
                
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
    
    def jsonWeight(self): # use below for racket filter according to selection API
        return {
        'Weight': self.Weight,
        }         
       
    @classmethod
    # def RacketFilterListAccodingToSelectionForFilterData_V2(cls,ShopID,data,Page):
    def RacketFilterListAccodingToSelectionForFilterData(cls, ShopID, data, Page):            
        query = db.session.query(RacketTestingFilterView).filter(RacketTestingFilterView.ShopID == ShopID)
        
        if data['Brand'] is not None:
            Brand = data['Brand'].split(",")
            query = query.filter( RacketTestingFilterView.Brand.in_(Brand))
        if data['Range'] is not None:
            Range = data['Range'].split(",")
            query = query.filter(RacketTestingFilterView.Range.in_(Range))
        if data['Model'] is not None:
            Model = data['Model'].split(",")
            query = query.filter(RacketTestingFilterView.Modele.in_(Model))
        if data['Version'] is not None:
            Version = data['Version'].split(",")
            query = query.filter(RacketTestingFilterView.Version.in_(Version))
        if data['Weight'] is not None:
            Weight = data['Weight'].split(",")
            query = query.filter(RacketTestingFilterView.Weight.in_(Weight))
            
        if data['OutputVariable'] == 1:
            query = query.order_by(RacketTestingFilterView.Brand).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonBrand() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 2:
            query = query.order_by(RacketTestingFilterView.Range).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonRange() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 3:
            query = query.order_by(RacketTestingFilterView.Modele).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonModel() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 4:
            query = query.order_by(RacketTestingFilterView.Version).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonVersion() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 5:
            query = query.order_by(RacketTestingFilterView.Weight).paginate(page=Page,per_page=20)
            RacketDetails = []
            for val in ([item.jsonWeight() for item in query.items]):
                if val in RacketDetails:
                    continue
                else:
                    RacketDetails.append(val)
            return({"results":RacketDetails})
        if data['OutputVariable'] == 7 :
            query = query.order_by(RacketTestingFilterView.ShopTestRacketID).paginate(page=Page,per_page=20)
            RacketDetails = [item.json2() for item in query.items]
            output= pagination(query,RacketDetails)
            return output
        
        
    @classmethod
    def RacketFilterList_model(cls,ShopID, Page):            
        query = db.session.query(RacketTestingFilterView).filter(RacketTestingFilterView.ShopID == ShopID)
        query = query.order_by(RacketTestingFilterView.ShopTestRacketID).paginate(page=Page,per_page=20)
        RacketDetails =[item.jsonInfo() for item in query.items]
        output= pagination(query,RacketDetails)
        return output
        
    @classmethod
    # def SearchRacket_V2(cls, ShopID, Page, data):
    def SearchRacket(cls, ShopID, Page, data):
        query =  db.session.query(RacketTestingFilterView).filter(RacketTestingFilterView.ShopID == ShopID)

        if data['SearchParameter']:
            SearchPara = (data['SearchParameter'].replace(" ","")).strip()
            query = query.filter(*[RacketTestingFilterView.SearchCombination.like( '%' + SearchPara + '%' )]) 
        if data['Brand']:
            Brand = data['Brand'].split(",")
            query = query.filter( RacketTestingFilterView.Brand.in_(Brand))
        if data['Range']:
            Range = data['Range'].split(",")
            query = query.filter( RacketTestingFilterView.Range.in_(Range))
        if data['Model']:
            Model = data['Model'].split(",")         
            query = query.filter( RacketTestingFilterView.Modele.in_(Model))

        query = query.paginate(page=Page,per_page=20)
        RacketDetails = [item.json() for item in query.items]
        output= pagination(query,RacketDetails)
        return output

    @classmethod
    def GetShopRacketDetailAsPerShopTestRacketID(cls,ShopTestRacketID):
        return db.session.query(RacketTestingFilterView).filter(RacketTestingFilterView.ShopTestRacketID == ShopTestRacketID).first()
   