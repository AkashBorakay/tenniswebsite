from sqlalchemy.sql.expression import select
from models.ShopMasterModel import ShopMasterModel
from db import db
from sqlalchemy.sql import func
from models.FrameworkModel import *
from datetime import datetime

class ClubMasterModel(db.Model):
    __tablename__ = 'tp_club_master'

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200))
    CourtCount = db.Column(db.Integer)
    IndoorCourtCount = db.Column(db.Integer)
    OutdoorCourtCount = db.Column(db.Integer)
    Address =  db.Column(db.String(200))
    City = db.Column(db.String(200))
    PostalCode = db.Column(db.String(50))
    StartTiming=db.Column(db.Time)
    CloseTiming=db.Column(db.Time)
    ShopID =  db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime, onupdate=getUTCTime())
    SortOrder = db.Column(db.Integer)
    IsDeleted = db.Column(db.Boolean)
    IsSystem = db.Column(db.Boolean)
    CreatedBy = db.Column(db.Integer)
    ClubFullName = db.Column(db.String(500))
    InsertedBy = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    SearchCombination = db.Column(db.String(5000))

    def __init__(self,Name,CourtCount,IndoorCourtCount,OutdoorCourtCount,Address,City,PostalCode,ShopID,StartTiming,CloseTiming,ClubFullName,InsertedBy,UpdatedBy,SearchCombination):
        self.Name = Name
        self.CourtCount= CourtCount
        self.IndoorCourtCount= IndoorCourtCount
        self.OutdoorCourtCount= OutdoorCourtCount
        self.Address= Address
        self.City = City
        self.PostalCode = PostalCode
        self.StartTiming=  StartTiming and datetime.strptime(str(StartTiming), '%H.%M') or None
        self.CloseTiming= CloseTiming and datetime.strptime(str(CloseTiming), '%H.%M') or None
        self.ShopID=ShopID
        self.IsDeleted = 0
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.SortOrder = 11
        self.IsSystem = 0
        self.CreatedBy = None
        self.ClubFullName = ClubFullName
        self.InsertedBy = InsertedBy
        self.UpdatedBy = UpdatedBy
        self.SearchCombination = SearchCombination

    def json(self):
        return {
            'ClubID': self.id,
            "Name": self.Name,
            "CourtCount": self.CourtCount,
            "IndoorCourtCount": self.IndoorCourtCount,
            "OutdoorCourtCount": self.OutdoorCourtCount,
            "Address": self.Address,
            "City": self.City,
            "PostalCode": self.PostalCode,
            "StartTiming": self.StartTiming and self.StartTiming.strftime('%H:%M') or None,
            "CloseTiming": self.CloseTiming and self.CloseTiming.strftime('%H:%M') or None,
            "ClubFullName":self.ClubFullName,
            "SortOrder":self.SortOrder
            }

    def json1(self):
        return {
            'ClubID': self.id,
            "Name": self.Name,
            "CourtCount": self.CourtCount,
            "IndoorCourtCount": self.IndoorCourtCount,
            "OutdoorCourtCount": self.OutdoorCourtCount,
            "Address": self.Address,
            "City": self.City,
            "PostalCode": self.PostalCode,
            "StartTiming": self.StartTiming and self.StartTiming.strftime('%H:%M') or None,
            "CloseTiming": self.CloseTiming and self.CloseTiming.strftime('%H:%M') or None,
            "ClubFullName":self.ClubFullName
            }   

    def jsonFilter(self):
        return {
            'ClubID': self.id,
            "Name": self.Name,
            "ClubFullName":self.ClubFullName
            }       

    @classmethod
    def GetClubList(cls):
        return db.session.query(ClubMasterModel).filter(ClubMasterModel.IsDeleted == 0).order_by(ClubMasterModel.SortOrder,ClubMasterModel.Name).all()
        # return cls.query.filter_by(IsDeleted = 0).all()
    
    @classmethod
    def GetClubMaster(cls, ClubID):
        return db.session.query(ClubMasterModel).filter(ClubMasterModel.id == ClubID, ClubMasterModel.IsDeleted == 0).first()

    @classmethod
    def UpdateClubMaster(cls, **data):
        ClubID = data.get('ClubID')
        query = ClubMasterModel.GetClubMaster(ClubID)
        # Comment below code because it create an problem while inserting due to SQL server connector which we used in app.py file for database connection.
        # if query is not None:
        #     for key, value in data.items():
        #         if(key in ("StartTiming", "CloseTiming") and value is not None):
        #             value = datetime.strptime(str(value), '%H.%M') 
        #         setattr(query, key, value)

        if query is not None:
            for key, value in data.items():
                setattr(query, key, value)
            setattr(query, "UpdatedDate", getUTCTime()) 
            commit()
        return query

    @classmethod
    def DeleteClubMaster(cls, ClubID,UpdatedBy):
        query = ClubMasterModel.GetClubMaster(ClubID)
        if query:
            # query.IsDeleted = 1,
            # query.UpdatedBy = 2
            setattr(query, "IsDeleted", 1)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "UpdatedDate", getUTCTime())
            db.session.commit()
        return query

    @classmethod
    def GetClubListAsPerSearchCriteria(cls,ShopID, SearchParameter):
        query = db.session.query(ClubMasterModel).filter(ClubMasterModel.ShopID==ShopID,ClubMasterModel.IsDeleted==0,ClubMasterModel.SearchCombination.like('%' + SearchParameter + '%')).order_by(ClubMasterModel.Name).all()    
        return query

    @classmethod
    def GetTopClubList(cls,ShopID):
        query = db.session.query(ClubMasterModel).filter(ClubMasterModel.ShopID==ShopID,ClubMasterModel.IsDeleted==0,ClubMasterModel.SortOrder.in_((1,2,3,4,5,6,7,8,9))).order_by(ClubMasterModel.SortOrder).all()   
        return query

    @classmethod
    def GetClubAllClub(cls,ShopID):
        query = db.session.query(ClubMasterModel).filter(ClubMasterModel.ShopID==ShopID,ClubMasterModel.IsDeleted==0).order_by(ClubMasterModel.Name).all()   
        return query       

    @classmethod
    def GetClubList(cls):
        ClubList = db.session.query(ClubMasterModel).filter(ClubMasterModel.IsDeleted == 0).all()
        list =[]
        for val in ([Clist.jsonFilter() for Clist in ClubList]):
            if val in list:
                continue
            else:
                list.append(val)
        return(list)