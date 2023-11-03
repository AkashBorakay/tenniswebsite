from db import db
from models.FrameworkModel import *
from sqlalchemy.orm import backref, relationship


class RacketMasterModel(db.Model):
    __tablename__ = 'tp_website_racket_master'

    id = db.Column(db.Integer, primary_key=True)
    # ShopID =  db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    Brand = db.Column(db.String(200))
    Range = db.Column(db.String(200))
    Modele = db.Column(db.String(200))
    HeadSize = db.Column(db.String(200))
    Weight = db.Column(db.Float())
    Version = db.Column(db.String(500))
    # SleeveSize = db.Column(db.String(200)) #Move to Shop Test racket QR Code detail because we have multiple test racket with different Sleev Size
    Pattern = db.Column(db.String(200))
    Technology = db.Column(db.String(2000))
    GameLevel = db.Column(db.String(200))
    #  Description = db.Column(db.String('MAX')) #Move to Shop Test racket  because description may change as per shop
    ReferenceNo = db.Column(db.String(200))
    Length = db.Column(db.String(200))
    RacketImage_1 = db.Column(db.String(2000))
    RacketImage_2 = db.Column(db.String(2000))
    RacketImage_3 = db.Column(db.String(2000))
    RacketImage_4 = db.Column(db.String(2000))
    ModelDisplayName = db.Column(db.String(2000))
    SearchCombination = db.Column(db.String(2000))
    SortOrder = db.Column(db.Integer)
    # OldPrice = db.Column(db.Float())
    # NewPrice = db.Column(db.Float())
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    DeactiveDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    IsActive = db.Column(db.Boolean) 
    Stiffness = db.Column(db.String(200))
    Balance_Unstrung = db.Column(db.String(200))
    Composition = db.Column(db.String(200))
    WeightOZ = db.Column(db.Float())
    RangeWeight = db.Column(db.String(50))
    

    # def __init__(self, Brand, Range, Modele, HeadSize,Weight,Version,Pattern,Technology,GameLevel,ReferenceNo,Length,RacketImage_1,RacketImage_2,RacketImage_3,RacketImage_4,InsertedBy,ModelDisplayName,SearchCombination,SortOrder,Stiffness,Balance_Unstrung):
        # self.SleeveSize = SleeveSize
        # self.Technology = Technology
        # self.GameLevel = GameLevel
        # self.ReferenceNo = ReferenceNo
        # self.Length = Length
        # self.IsSystem = 0
        # self.IsActive = 1
        # self.Composition = None
    def __init__(self, Brand, Range, Modele, HeadSize,Weight,WeightOZ,Version,Pattern,RacketImage_1,RacketImage_2,RacketImage_3,RacketImage_4,InsertedBy,ModelDisplayName,SearchCombination,SortOrder,Stiffness,Balance_Unstrung):
        self.Brand = Brand
        self.Range = Range
        self.Modele = Modele
        self.HeadSize = HeadSize
        self.Weight = Weight
        self.WeightOZ = WeightOZ
        self.Version = Version
        self.Pattern = Pattern
        self.RacketImage_1 = RacketImage_1
        self.RacketImage_2 = RacketImage_2
        self.RacketImage_3 = RacketImage_3
        self.RacketImage_4 = RacketImage_4
        self.InsertedBy = InsertedBy
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.ModelDisplayName =ModelDisplayName
        self.SearchCombination = SearchCombination
        if SortOrder is None:
            if 'POUCES' in Range:
                self.SortOrder = 2
            elif 'JUNIOR' in Modele:
                self.SortOrder = 2
            elif 'POUCES' in Modele:
                self.SortOrder = 2
            elif 'JUNIOR' in Range:
                self.SortOrder = 2
            else:
                self.SortOrder = 1
        else:
            self.SortOrder = SortOrder
        self.Stiffness = Stiffness
        self.Balance_Unstrung = Balance_Unstrung
        if Weight < 270:
            self.RangeWeight = "< 270 gr"
        elif Weight <= 285:
            self.RangeWeight = "De 270 à 285 gr"
        elif Weight <= 295:
            self.RangeWeight = "De 286 à 295 gr"
        elif Weight <= 305:
            self.RangeWeight = "De 296 à 305 gr"
        elif Weight <= 315:
            self.RangeWeight = "De 306 à 315 gr"
        elif Weight > 315:
            self.RangeWeight = "> 315 gr"
        
    def json(self):
        return {
                'id':self.id,
                # 'ShopID': self.ShopID,
                # 'SleeveSize':self.SleeveSize,
                # 'Technology':self.Technology, 
                # 'GameLevel':self.GameLevel,
                # 'Description':self.Description,
                # 'ReferenceNo':self.ReferenceNo,
                # 'Length':self.Length,
                # 'OldPrice':self.OldPrice, 
                # 'NewPrice':self.NewPrice,
                # 'IsActive' : self.IsActive,
                'Brand': self.Brand,
                'Range':self.Range,
                'Modele':self.Modele,
                'HeadSize':self.HeadSize, 
                'Weight':self.Weight,
                'WeightOZ':self.WeightOZ,
                'Version':self.Version,
                'Pattern':self.Pattern,
                'RacketImage_1':self.RacketImage_1, 
                'RacketImage_2':self.RacketImage_2,
                'RacketImage_3':self.RacketImage_3,
                'RacketImage_4':self.RacketImage_4,
                'ModelDisplayName':self.ModelDisplayName,
                'CreatedDate':self.CreatedDate.strftime("%Y-%m-%d"),
                'IsDeleted': self.IsDeleted,
                'Stiffness' : self.Stiffness,
                'Balance_Unstrung' : self.Balance_Unstrung
                }
    
    @classmethod
    def GetTestRacketDetail(cls,TestRacketID):
        return db.session.query(RacketMasterModel).filter(RacketMasterModel.IsDeleted == 0,RacketMasterModel.id == TestRacketID).first()
    
    @classmethod
    def CheckRacketExistOrNotBeforeInsert(cls, data):
        query = db.session.query(RacketMasterModel).filter(RacketMasterModel.IsDeleted == 0, RacketMasterModel.Brand  == data['Brand'] , RacketMasterModel.Range  == data['Range'] , RacketMasterModel.Modele  == data['Modele'], RacketMasterModel.Weight == data['Weight'], RacketMasterModel.Version == data['Version']).first()
        return query
    
    @classmethod
    def CheckRacketExistBeforeInsert(cls, MasterTestingRacketID):
        query = db.session.query(RacketMasterModel).filter(RacketMasterModel.IsDeleted == 0, RacketMasterModel.id  == MasterTestingRacketID).first()
        return query
    
    @classmethod
    def UpdateRacketMasterByAdmin(cls, data):
        TestRacketID = data.get('MasterTestingRacketID')
        TestRacketDetail = RacketMasterModel.GetTestRacketDetail(TestRacketID)
        if TestRacketDetail is not None:
            for key, value in data.items():
                setattr(TestRacketDetail, key, value)
            setattr(TestRacketDetail, "UpdatedDate", getUTCTime())
            commit()
            return TestRacketDetail
        else:
            return None    