from db import db
from models.FrameworkModel import *
from models.WebsiteRacketMasterModel import RacketMasterModel
from models.WebsiteShopTestingRacketQRCodeDetailModel  import ShopTestRacketQRCodeDetailModel
# from models.RacketFilterAndSearchView  import RacketFilterAndSearchViewl
from models.FilterAndSearchRacketModel  import RacketTestingFilterView
from models.FilterAndSearchRacketMasterModel  import RacketMasterFilterView
from sqlalchemy.sql.expression import outerjoin,join
from sqlalchemy.orm import backref, relationship
import json
from flask import request, jsonify



class ShopTestRacketModel(db.Model):
    __tablename__ = 'tp_website_shop_testing_racket'

    id = db.Column(db.Integer, primary_key=True)
    ShopID =  db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    MasterTestingRacketID = db.Column(db.Integer, db.ForeignKey('tp_website_racket_master.id'))
    Comment = db.Column(db.String(2000))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    DeactiveDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    IsActive = db.Column(db.Boolean) 
    Description = db.Column(db.String(5000))
    OldPrice = db.Column(db.Float())
    NewPrice = db.Column(db.Float())
    RacketRentalDays = db.Column(db.Integer)
    

    def __init__(self, ShopID, MasterTestingRacketID,  InsertedBy,Description,OldPrice,RacketRentalDays,NewPrice):
        self.ShopID = ShopID
        self.MasterTestingRacketID = MasterTestingRacketID
        self.InsertedBy = InsertedBy
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.DeactiveDate = None
        self.IsActive = 1
        self.IsDeleted = 0
        self.Description = Description
        self.OldPrice = OldPrice
        self.NewPrice = NewPrice
        self.NewPrice = None
        self.UpdatedBy = None
        self.RacketRentalDays = RacketRentalDays
        
    def json(self, ShopID):
        TestRacket = RacketMasterModel.GetTestRacketDetail(self.MasterTestingRacketID)
        SleeveSize = ShopTestRacketQRCodeDetailModel.GetSleeveSizeForRacket(self.id, ShopID)
        return {
                'ShopTestingRacketid':self.id,
                'ShopID': self.ShopID,
                'MasterTestingRacketID': self.MasterTestingRacketID,
                'IsDeleted': self.IsDeleted,
                'CreatedDate':self.CreatedDate.strftime("%Y-%m-%d"),
                'Brand': TestRacket.Brand,
                'Range':TestRacket.Range,
                'Modele':TestRacket.Modele,
                'HeadSize':TestRacket.HeadSize, 
                'Weight':TestRacket.Weight,
                'WeightOZ':TestRacket.WeightOZ,
                'Version':TestRacket.Version,
                # 'SleeveSize':TestRacket.SleeveSize,
                'Pattern':TestRacket.Pattern,
                'Description':self.Description,
                'RacketImage_1':TestRacket.RacketImage_1, 
                'RacketImage_2':TestRacket.RacketImage_2,
                'RacketImage_3':TestRacket.RacketImage_3,
                'RacketImage_4':TestRacket.RacketImage_4,
                'ModelDisplayName':TestRacket.ModelDisplayName,
                'OldPrice':self.OldPrice, 
                'NewPrice':self.NewPrice,
                'Stiffness':TestRacket.Stiffness, 
                'Balance_Unstrung':TestRacket.Balance_Unstrung,
                'SleeveSizeList' : SleeveSize,
                'RacketRentalDays':self.RacketRentalDays
                }
         
    def jsonForDashboard(self):
        TestRacket = RacketMasterModel.GetTestRacketDetail(self.MasterTestingRacketID)
        return {
                'ShopTestingRacketid':self.id,
                'ShopID': self.ShopID,
                'MasterTestingRacketID': self.MasterTestingRacketID,
                'IsDeleted':self.IsDeleted,
                'CreatedDate':self.CreatedDate.strftime("%Y-%m-%d"),
                'Brand': TestRacket.Brand,
                'Range':TestRacket.Range,
                'Modele':TestRacket.Modele,
                'HeadSize':TestRacket.HeadSize, 
                'Weight':TestRacket.Weight,
                'WeightOZ':TestRacket.WeightOZ,
                'Version':TestRacket.Version,
                # 'SleeveSize':TestRacket.SleeveSize,
                'Pattern':TestRacket.Pattern,
                'Technology':TestRacket.Technology, 
                'GameLevel':TestRacket.GameLevel,
                'Description':self.Description,
                'ReferenceNo':TestRacket.ReferenceNo,
                'Length':TestRacket.Length,
                'RacketImage_1':TestRacket.RacketImage_1, 
                'RacketImage_2':TestRacket.RacketImage_2,
                'RacketImage_3':TestRacket.RacketImage_3,
                'RacketImage_4':TestRacket.RacketImage_4,
                'ModelDisplayName':TestRacket.ModelDisplayName,
                'OldPrice':self.OldPrice, 
                'NewPrice':self.NewPrice,
                'Stiffness':TestRacket.Stiffness, 
                'Balance_Unstrung':TestRacket.Balance_Unstrung,
                'RacketRentalDays' : self.RacketRentalDays
                }
        
        
    @classmethod
    def GetAllTestingRacketForShop(cls,ShopID):
        return db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.IsDeleted == 0,
                                                            ShopTestRacketModel.ShopID == ShopID).all()
    
    @classmethod
    def GetRacketByMasterRacketID(cls,MasterTestingRacketID,ShopID):
        return db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.IsDeleted == 0,ShopTestRacketModel.MasterTestingRacketID == MasterTestingRacketID,
                                                            ShopTestRacketModel.ShopID == ShopID).first()
    
    @classmethod
    def GetShopRacketDetailByShopIDAndShopTestRacketID(cls,ShopTestRacketID,ShopID):
        return db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.id == ShopTestRacketID,
                                                            ShopTestRacketModel.ShopID == ShopID).first()
    
    @classmethod
    def GetShopRacketDetailByShopTestRacketID(cls,ShopTestRacketID):
        return db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.id == ShopTestRacketID).first()
    
    @classmethod
    def UpdateShopTestRacket(cls, ShopID, ShopTestRacketDetail,ShopTestRacketQRCodeIDDetail):
        ShopTestRacketQRCodeDetailID = ShopTestRacketQRCodeIDDetail.get('ShopTestRacketQRCodeDetailID')
        ShopTestRacketID = ShopTestRacketDetail.get('ShopTestRacketID')
        query1 = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(ShopTestRacketID, ShopID)
        if query1 is not None:
            for key, value in ShopTestRacketDetail.items():
                setattr(query1, key, value)
            setattr(query1, "UpdatedDate", getUTCTime())
        query2 = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(ShopTestRacketQRCodeDetailID)
        if query2 is not None:
            for key, value in ShopTestRacketQRCodeIDDetail.items():
                setattr(query2, key, value)
            setattr(query2, "UpdatedDate", getUTCTime())               
        commit()
        return {"RacketMaterID":query1.MasterTestingRacketID,"ShopTestRacketID" :query1.id,"ShopTestRacketQRCodeDetailID":query2.id}
    
    @classmethod
    def DeleteShopTestRacket(cls, ShopID, ShopTestRacketQRCodeDetailID, UpdatedBy):
        GetRacketDetail = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(ShopTestRacketQRCodeDetailID)
        if GetRacketDetail:
            ShopTestRacketID = GetRacketDetail.id
            CheckTotalIdenticalRacket = ShopTestRacketQRCodeDetailModel.CountOfIdenticalShopTestRacket(ShopTestRacketID)
            if CheckTotalIdenticalRacket > 1:
                setattr(GetRacketDetail, "UpdatedBy", UpdatedBy)
                setattr(GetRacketDetail, "UpdatedDate", getUTCTime())
                setattr(GetRacketDetail, "IsDeleted", 1)          
            else:
                if GetRacketDetail is not None:
                    setattr(GetRacketDetail, "UpdatedBy", UpdatedBy)
                    setattr(GetRacketDetail, "UpdatedDate", getUTCTime())
                    setattr(GetRacketDetail, "IsDeleted", 1)
                GetShopTestRacet = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(ShopTestRacketID,ShopID)
                if GetShopTestRacet is not None:
                    setattr(GetShopTestRacet, "UpdatedBy", UpdatedBy)
                    setattr(GetShopTestRacet, "DeactiveDate", getUTCTime())
                    setattr(GetShopTestRacet, "IsDeleted", 1)
            commit()
            if GetRacketDetail:
                return {"ShopTestRacketQRCodeDetailID":GetRacketDetail.id}
            else:
                return 0
            
    @classmethod
    def DeleteShopTestRacketBySuperAdmin(cls, ShopID, UpdatedBy, ShopTestRacketID):
        ShopRacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(ShopTestRacketID,ShopID)
        if ShopRacketDetail:
            setattr(ShopRacketDetail, "UpdatedBy", UpdatedBy)
            setattr(ShopRacketDetail, "UpdatedDate", getUTCTime())
            setattr(ShopRacketDetail, "DeactiveDate", getUTCTime())
            setattr(ShopRacketDetail, "IsDeleted", 1)          
        else:
            return None
        commit()
        return ShopRacketDetail
    
    @classmethod
    def UpdateShopTestRacketMasterByAdmin(cls, ShopTestingRacketid,ShopID,Description,OldPrice,NewPrice,RacketRentalDays,UpdatedBy):
        ShopTestingRacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(ShopTestingRacketid,ShopID)
        if ShopTestingRacketDetail is not None:
            setattr(ShopTestingRacketDetail, "Description", Description)
            setattr(ShopTestingRacketDetail, "OldPrice", OldPrice)
            setattr(ShopTestingRacketDetail, "NewPrice", NewPrice)
            setattr(ShopTestingRacketDetail, "RacketRentalDays", RacketRentalDays)
            setattr(ShopTestingRacketDetail, "UpdatedBy", UpdatedBy)
            setattr(ShopTestingRacketDetail, "UpdatedDate", getUTCTime())
            commit()
            return ShopTestingRacketDetail
        else:
            return None 
        
    def racket_details(ShopTestRacket = None):
        Output={}
        Output = ShopTestRacket.jsonForDashboard() if ShopTestRacket else None
        return Output
        
        
    # @classmethod
    # def GetAllTestingRacketOfShopForAdmin(cls,ShopID,Page,NameFilter):
    #     if NameFilter == None:
    #         RacketList = []
    #         ShopTestRacket = None
    #         ShopTestRackets = db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.IsDeleted == 0,ShopTestRacketModel.ShopID == ShopID).order_by(ShopTestRacketModel.id).paginate(page=Page,per_page=20)
    #         if ShopTestRackets:
    #             for ShopTestRacket in ShopTestRackets.items:
    #                 RacketList.append(ShopTestRacketModel.racket_details(ShopTestRacket))
    #             ShopRacketList = PaginationForOrderDashboard(ShopTestRackets,RacketList)
    #             return ShopRacketList
    #         else:
    #             return {"message": "No test racket found for shop"}
    #     else:
    #         RacketList = []
    #         ShopTestRacket = None
    #         RacketDataFromView =  db.session.query(RacketFilterAndSearchView).filter(RacketFilterAndSearchView.IsDeleted == 0,RacketFilterAndSearchView.ShopID == ShopID)
    #         SearchPara = (NameFilter.replace(" ","")).strip()
    #         FilterData = RacketDataFromView.filter(*[RacketFilterAndSearchView.SearchCombination.like( '%' + SearchPara + '%' )])
    #         MasterTestRacketID = []
    #         if FilterData is not None:
    #             for data in FilterData:
    #                 MasterTestRacketID.append(data.RacketMasterID)
    #         else:
    #             return {"message": "No test racket found for shop"}                
    #         ShopTestRackets = db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.IsDeleted == 0,ShopTestRacketModel.ShopID == ShopID,ShopTestRacketModel.MasterTestingRacketID.in_(MasterTestRacketID)).order_by(ShopTestRacketModel.id).paginate(page=Page,per_page=20)
    #         if ShopTestRackets:
    #             for ShopTestRacket in ShopTestRackets.items:
    #                 RacketList.append(ShopTestRacketModel.racket_details(ShopTestRacket))
    #             ShopRacketList = PaginationForOrderDashboard(ShopTestRackets,RacketList)
    #             return ShopRacketList
    #         else:
    #             return {"message": "No test racket found for shop"}
                    
            
    @classmethod
    def GetAllTestingRacketOfShopForAdmin(cls,ShopID,Page,NameFilter):
        if NameFilter == None:
            RacketList = []
            ShopTestRacket = None
            ShopTestRackets = db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.IsDeleted == 0,ShopTestRacketModel.ShopID == ShopID).order_by(ShopTestRacketModel.id).paginate(page=Page,per_page=20)
            if ShopTestRackets:
                for ShopTestRacket in ShopTestRackets.items:
                    RacketList.append(ShopTestRacketModel.racket_details(ShopTestRacket))
                ShopRacketList = PaginationForOrderDashboard(ShopTestRackets,RacketList)
                return ShopRacketList
            else:
                return {"message": "No test racket found for shop"}
        else:
            RacketList = []
            ShopTestRacket = None
            RacketDataFromView =  db.session.query(RacketMasterFilterView).filter(RacketMasterFilterView.ShopID == ShopID)
            SearchPara = (NameFilter.replace(" ","")).strip()
            FilterData = RacketDataFromView.filter(*[RacketMasterFilterView.SearchCombination.like( '%' + SearchPara + '%' )])
            MasterTestRacketID = []
            if FilterData is not None:
                for data in FilterData:
                    MasterTestRacketID.append(data.MasterTestingRacketID)
            else:
                return {"message": "No test racket found for shop"}                
            ShopTestRackets = db.session.query(ShopTestRacketModel).filter(ShopTestRacketModel.IsDeleted == 0,ShopTestRacketModel.ShopID == ShopID,ShopTestRacketModel.MasterTestingRacketID.in_(MasterTestRacketID)).order_by(ShopTestRacketModel.id).paginate(page=Page,per_page=20)
            if ShopTestRackets:
                for ShopTestRacket in ShopTestRackets.items:
                    RacketList.append(ShopTestRacketModel.racket_details(ShopTestRacket))
                ShopRacketList = PaginationForOrderDashboard(ShopTestRackets,RacketList)
                return ShopRacketList
            else:
                return {"message": "No test racket found for shop"}