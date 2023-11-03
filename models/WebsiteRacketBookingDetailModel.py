from operator import and_, or_
from sqlalchemy.orm import query, relationship
import datetime as pydt
from db import db
from models.FrameworkModel import *
from sqlalchemy.sql import func
from sqlalchemy.orm import backref, relationship
from flask import request, jsonify, json
from datetime import datetime,timedelta
from sqlalchemy import cast,Date
from models.WebsiteShopTestingRacketQRCodeDetailModel import ShopTestRacketQRCodeDetailModel
from models.WebsiteCustomerModel import CustomerDetailModel
from models.WebsiteContractMasterModel import ContractMasterModel
from models.WebsiteShopTestingRacketModel import ShopTestRacketModel
from models.SleeveSizeMasterModel import SleeveSizeMasterModel
from models.WebsiteCustomerContractModel import CustomerContractMasterModel
from models.WebsiteQRCodeMasterModel import QRCodeMasterModel
from models.ShopMasterModel import ShopMasterModel
from models.RacketStatusMasterModel import RacketStatusMasterModel
from models.WebsiteRacketMasterModel import RacketMasterModel
# from service.OrderMasterService import OrderMasterService

class RacketBookingDetailMasterModel(db.Model):
    __tablename__ = 'tp_website_racket_booking_detail'
    
    id = db.Column(db.Integer, primary_key=True)
    BookingID = db.Column(db.Integer)
    CustomerID = db.Column(db.Integer)
    ShopID =  db.Column(db.Integer)
    CustomerContractID =  db.Column(db.Integer)
    ShopTestRacketID = db.Column(db.Integer)
    ShopTestRacketQRCodeDetailID = db.Column(db.Integer)
    Comment = db.Column(db.String(2000))
    Status = db.Column(db.Integer)
    BookDate = db.Column(db.DateTime)
    ReturnDate = db.Column(db.DateTime)
    ActualReturnDate = db.Column(db.DateTime)
    CancelDate = db.Column(db.DateTime)
    NeedToRepair = db.Column(db.Boolean)
    LatePrice = db.Column(db.Float())
    ContractPrice = db.Column(db.Float())
    CreatedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)
    IsDeleted = db.Column(db.Boolean)
    OrderByAdminOrCustomer = db.Column(db.Integer)
    InsertBy = db.Column(db.Integer)
    OrderCancelByAdminOrCustomer = db.Column(db.Integer)
    Cancelby = db.Column(db.Integer)
    OrderUpdatedByAdminOrCustomer = db.Column(db.Integer)
    UpdatedBy = db.Column(db.Integer)
    IsLate = db.Column(db.Boolean)
    OrderPlaceFrom = db.Column(db.Integer)
    SleeveSizeID = db.Column(db.Integer)
    IsCancel = db.Column(db.Boolean)
    AskRating = db.Column(db.Boolean)
    
    def __init__(self, BookingID,CustomerID,ShopID,InsertBy,CustomerContractID,ShopTestRacketID,ShopTestRacketQRCodeDetailID,Comment,Status,BookDate,ReturnDate,ContractPrice,OrderByAdminOrCustomer,OrderPlaceFrom,SleeveSizeID):
        self.BookingID = BookingID
        self.CustomerID = CustomerID
        self.ShopID =  ShopID
        self.CustomerContractID =  CustomerContractID
        self.ShopTestRacketID = ShopTestRacketID
        self.ShopTestRacketQRCodeDetailID = ShopTestRacketQRCodeDetailID
        self.Comment = Comment
        self.Status = Status
        self.BookDate = BookDate
        self.ReturnDate = ReturnDate
        self.ActualReturnDate = None
        self.NeedToRepair = False
        self.LatePrice = None
        self.ContractPrice = ContractPrice
        self.CreatedDate = getUTCTime()
        self.UpdatedDate = getUTCTime()
        self.IsDeleted = 0
        self.OrderByAdminOrCustomer = OrderByAdminOrCustomer
        self.InsertBy = InsertBy
        self.OrderCancelByAdminOrCustomer = None
        self.Cancelby = None
        self.OrderUpdatedByAdminOrCustomer = None
        self.UpdatedBy = None
        self.IsLate = False
        self.OrderPlaceFrom = OrderPlaceFrom
        self.SleeveSizeID = SleeveSizeID
        self.CancelDate = None
        self.IsCancel = False
        self.AskRating = False
    
    def jsonForBookedDate(self):
        return {
            "BookDate" : self.BookDate and self.BookDate.strftime('%d/%m/%Y') or None,
            "ReturnDate" : self.ReturnDate and self.ReturnDate.strftime('%d/%m/%Y') or None
        }
        
    def json(self):
        if self.Status == 7:
            DateDifference = (datetime.strptime((self.BookDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((getUTCTime().strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        else:
            DateDifference = (datetime.strptime((self.ReturnDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((getUTCTime().strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        SleeveSize = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(self.SleeveSizeID)
        if (self.Status == 7) | (self.Status == 8):
            RangeBooked = (datetime.strptime((self.ReturnDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((self.BookDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        elif (self.Status == 9) | (self.Status == 10):
            RangeBooked = (datetime.strptime((self.ActualReturnDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((self.BookDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        else:
            RangeBooked = (datetime.strptime((self.ReturnDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((getUTCTime().strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        return {
            "BookingDetailID" : self.id,
            "BookingID" : self.BookingID,
            "CustomerID" : self.CustomerID,
            "ShopID" : self.ShopID,
            "CustomerContractID" : self.CustomerContractID,
            "ShopTestRacketID" : self.ShopTestRacketID,
            "ShopTestRacketQRCodeDetailID" : self.ShopTestRacketQRCodeDetailID,
            "Comment" : self.Comment,
            "Status" : self.Status,
            "BookDate" : self.BookDate and self.BookDate.strftime('%Y-%m-%d') or None,
            "ReturnDate" : self.ReturnDate and self.ReturnDate.strftime('%Y-%m-%d') or None,
            "ActualReturnDate" : self.ActualReturnDate and self.ActualReturnDate.strftime('%Y-%m-%d') or None,
            "CancelDate" : self.CancelDate and self.CancelDate.strftime('%Y-%m-%d') or None,
            "NeedToRepair" : self.NeedToRepair,
            "CreatedDate" : self.CreatedDate.strftime("%Y-%m-%d"),
            "UpdatedDate" : self.UpdatedDate.strftime("%Y-%m-%d"),
            "OrderByAdminOrCustomer" : self.OrderByAdminOrCustomer,
            "InsertBy": self.InsertBy,
            "OrderCancelByAdminOrCustomer": self.OrderCancelByAdminOrCustomer,
            "Cancelby": self.Cancelby,
            "OrderUpdatedByAdminOrCustomer": self.OrderUpdatedByAdminOrCustomer,
            "UpdatedBy": self.UpdatedBy,
            "IsLate" : self.IsLate,
            "OrderPlaceFrom" : self.OrderPlaceFrom,
            "SleeveSizeID" : self.SleeveSizeID,
            "SleeveSizeName" : SleeveSize,
            "DateDifference" : DateDifference,
            "RangeBooked" : RangeBooked,
            "IsCancel": self.IsCancel,
            "AskRating": self.AskRating
        }
        
    def jsonReturnScan(self):
        if (self.Status == 7) | (self.Status == 8):
            RangeBooked = (datetime.strptime((self.ReturnDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((self.BookDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        elif (self.Status == 9) | (self.Status == 10):
             RangeBooked = (datetime.strptime((self.ActualReturnDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((self.BookDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        else:
             RangeBooked = (datetime.strptime((self.ReturnDate.strftime('%Y-%m-%d')),'%Y-%m-%d').date() - datetime.strptime((getUTCTime().strftime('%Y-%m-%d')),'%Y-%m-%d').date()).days
        SleeveSize = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(self.SleeveSizeID)
        if self.ShopTestRacketQRCodeDetailID:
            RacketValue = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(self.ShopTestRacketQRCodeDetailID)
        StatusName = RacketStatusMasterModel.GetRacketNewRacketStatus(RacketValue.RacketStatusID, self.ShopID)
        StatusNewName = RacketStatusMasterModel.GetRacketNewRacketStatus(RacketValue.RacketNewStatusID, self.ShopID)
        return {
            "BookingDetailID" : self.id,
            "BookingID" : self.BookingID,
            "CustomerID" : self.CustomerID,
            "ShopID" : self.ShopID,
            "CustomerContractID" : self.CustomerContractID,
            "ShopTestRacketID" : self.ShopTestRacketID,
            "ShopTestRacketQRCodeDetailID" : self.ShopTestRacketQRCodeDetailID,
            "Status" : self.Status,
            "BookDate" : self.BookDate and self.BookDate.strftime('%Y-%m-%d') or None,
            "ReturnDate" : self.ReturnDate and self.ReturnDate.strftime('%Y-%m-%d') or None,
            "ActualReturnDate" : self.ActualReturnDate and self.ActualReturnDate.strftime('%Y-%m-%d') or None,
            "CancelDate" : self.CancelDate and self.CancelDate.strftime('%Y-%m-%d') or None,
            "NeedToRepair" : self.NeedToRepair,
            "OrderByAdminOrCustomer" : self.OrderByAdminOrCustomer,
            "InsertBy": self.InsertBy,
            "OrderCancelByAdminOrCustomer": self.OrderCancelByAdminOrCustomer,
            "Cancelby": self.Cancelby,
            "OrderUpdatedByAdminOrCustomer": self.OrderUpdatedByAdminOrCustomer,
            "UpdatedBy": self.UpdatedBy,
            "IsLate" : self.IsLate,
            "IsDeleted" : self.IsDeleted,
            "OrderPlaceFrom" : self.OrderPlaceFrom,
            "SleeveSizeID" : self.SleeveSizeID,
            "SleeveSizeName" : SleeveSize,
            "QrCodeID" : RacketValue.QRCodeID,
            "UniqueRacketName" : RacketValue.UniqueRacketName,
            "RacketStatusID" : RacketValue.RacketStatusID,
            "RacketNewStatusID" : RacketValue.RacketNewStatusID,
            "RangeBooked" : RangeBooked,
            "MasterTestingRacketID" : RacketValue.MasterTestingRacketID,
            "RacketStatus" : StatusName.Status,
            "RacketNewStatus" : StatusNewName.Status,
            "IsCancel": self.IsCancel,
            "AskRating": self.AskRating
            }
    
    def jsonQuestion(self):
        RacketValue = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetailOrder(self.ShopTestRacketQRCodeDetailID)
        return {
            "BookingDetailID" : self.id,
            "CustomerID" : self.CustomerID,
            "ShopID" : self.ShopID,
            "Status" : self.Status,
            "ActualReturnDate" : self.ActualReturnDate and self.ActualReturnDate.strftime('%Y-%m-%d') or None,
            "MasterTestingRacketID" : RacketValue.MasterTestingRacketID,
            "AskRating": self.AskRating
            }
    
    
    @classmethod
    def GetDateToBlockCalendar(cls,ShopTestRacketID,SleeveSizeID):
        StatusArray = [7,8]
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0,RacketBookingDetailMasterModel.Status.in_(StatusArray),RacketBookingDetailMasterModel.ShopTestRacketID == ShopTestRacketID,RacketBookingDetailMasterModel.SleeveSizeID  == SleeveSizeID).all()
    
    @classmethod
    def GetTotalOpenOrderCountForCustomerContract(cls,CustomerContractID):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0,RacketBookingDetailMasterModel.Status.in_([7,8]),RacketBookingDetailMasterModel.CustomerContractID == CustomerContractID).count()
    
    @classmethod
    def GetOrderCountForCustomerBetweenDates(cls,CustomerID, ShopID):
        query = db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0,RacketBookingDetailMasterModel.Status.in_([7,8]), RacketBookingDetailMasterModel.CustomerID == CustomerID,
                                                                       RacketBookingDetailMasterModel.ShopID == ShopID).count()
        return query
    # (RacketBookingDetailMasterModel.BookDate <= StartDate) and (StartDate <= RacketBookingDetailMasterModel.ReturnDate)) or ((RacketBookingDetailMasterModel.BookDate <= EndDate) and (EndDate <= RacketBookingDetailMasterModel.ReturnDate)
    @classmethod
    def GetOrderDetail(cls, ShopID, CustomerID, BookingDetailID):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,RacketBookingDetailMasterModel.CustomerID == CustomerID,RacketBookingDetailMasterModel.id == BookingDetailID,RacketBookingDetailMasterModel.IsDeleted == 0 ).first()
    
    @classmethod
    def GetOrderDetailByCustomerIDAndBookingDetailID(cls, CustomerID, BookingDetailID):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.CustomerID == CustomerID, RacketBookingDetailMasterModel.id == BookingDetailID, RacketBookingDetailMasterModel.IsDeleted == 0).first()
    
    @classmethod
    def HandOverRacketToCustomerByScanningQRCode(cls, ShopID, **data):
        CustomerID = data.get('CustomerID')
        BookingDetailID  = data.get('BookingDetailID')
        QRCodeID = data.get('QRCodeID')
        ShopTestRacketQRCodeDetailID = data.get('ShopTestRacketQRCodeDetailID')
        UpdatedBy = data.get('UpdatedBy')
        SleeveSizeIDAndShopTestRacketID = ShopTestRacketQRCodeDetailModel.GetSleeveSizeIDForRacket(ShopTestRacketQRCodeDetailID)
        if data.get('SleeveSizeID') == SleeveSizeIDAndShopTestRacketID['SleeveSizeID'] and data.get('ShopTestRacket') == SleeveSizeIDAndShopTestRacketID['ShopTestRacketID']:            
            query = RacketBookingDetailMasterModel.GetOrderDetail(ShopID, CustomerID, BookingDetailID)
            if query is not None:
                for key, value in data.items():
                    setattr(query, key, value)
                setattr(query, "Status", 8)
                setattr(query, "IsLate", False)
                setattr(query, "NeedToRepair", False)
                setattr(query, "UpdatedDate", getUTCTime())
            query = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(ShopTestRacketQRCodeDetailID)
            if query is not None:
                setattr(query, "IsRacketTakenByCustomer", True)
                setattr(query, "NeedToRepair", False)
                setattr(query, "UpdatedDate", getUTCTime())
                setattr(query, "UpdatedBy", UpdatedBy)               
            commit()
            return BookingDetailID
        else:
            return False
        
    @classmethod
    def UpdateStatusinRacketQRCodeDetailTable(cls,ShopTestRacketQRCodeDetailID):
        query = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(ShopTestRacketQRCodeDetailID)
        if query is not None:
            setattr(query, "IsRacketTakenByCustomer", True)
            setattr(query, "NeedToRepair", False)
            setattr(query, "UpdatedDate", getUTCTime())       
        commit()
        return query
    
    @classmethod
    def ReturnRacketToShop(cls, ShopID, **data):
        CustomerID = data.get('CustomerID')
        BookingDetailID  = data.get('BookingDetailID')
        UpdatedBy = data.get('UpdatedBy')
        ActualReturnDate = data.get('ActualReturnDate') 
        NeedToRepair = data.get('NeedToRepair')    
        IsLate =  data.get('IsLate')
        RacketNewStatusID = data.get("RacketNewStatusID")
        QRCodeID = data.get('QRCodeID')
        IsCancel =  data.get('IsCancel')
        if QRCodeID:
            ShopTestRacketQRCodeDetailID = ShopTestRacketQRCodeDetailModel.GetShopTestRacketAsPerQrCodeID(QRCodeID)
        else:
            ShopTestRacketQRCodeDetailID = data.get('ShopTestRacketQRCodeDetailID')
        query = RacketBookingDetailMasterModel.GetOrderDetail(ShopID, CustomerID, BookingDetailID)
        if query is not None:
            if NeedToRepair == True and IsCancel == False:
                setattr(query, "Status", 10)
            elif NeedToRepair == False and IsCancel == True:
                setattr(query, "Status", 12)
                setattr(query, "Cancelby", UpdatedBy)
                setattr(query, "CancelDate", getUTCTime())
            else:
                setattr(query, "Status", 9)  
            setattr(query, "IsLate", IsLate)
            
            if ActualReturnDate is None:
                setattr(query, "ActualReturnDate", getUTCTime())
            setattr(query, "NeedToRepair", NeedToRepair)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "IsCancel", IsCancel)
        query = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(ShopTestRacketQRCodeDetailID)
        if query is not None:
            setattr(query, "IsRacketTakenByCustomer", False)
            setattr(query, "UpdatedDate", getUTCTime())  
            setattr(query, "NeedToRepair", NeedToRepair)
            setattr(query, "UpdatedBy", UpdatedBy)
            setattr(query, "RacketNewStatusID", RacketNewStatusID)
            setattr(query, "IsCancel", IsCancel)
        commit()
        return BookingDetailID
    
    @classmethod
    def CheckQRCodeOrder(cls, ShopID, OldShopTestRacketQRCodeDetailID):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopTestRacketQRCodeDetailID == OldShopTestRacketQRCodeDetailID,RacketBookingDetailMasterModel.IsDeleted == 0,RacketBookingDetailMasterModel.Status.in_([7,8]),RacketBookingDetailMasterModel.ShopID == ShopID).first()
    
    @classmethod
    def GetDepartureOrderList(cls, ShopID,OrderStatus,Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
             RacketBookingDetailMasterModel.Status==OrderStatus).\
        order_by(RacketBookingDetailMasterModel.BookDate).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetRacketTakenByCustomerOrderList(cls, ShopID,OrderStatus,Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
             RacketBookingDetailMasterModel.Status==OrderStatus).\
        order_by(RacketBookingDetailMasterModel.UpdatedDate).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetReturnOrderList(cls, ShopID,OrderStatus,Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,RacketBookingDetailMasterModel.IsDeleted == 0,\
             RacketBookingDetailMasterModel.Status==OrderStatus).\
        order_by(RacketBookingDetailMasterModel.ActualReturnDate).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetOrderList(cls, ShopID,OrderStatus,Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
             RacketBookingDetailMasterModel.Status==OrderStatus).\
        order_by(RacketBookingDetailMasterModel.ActualReturnDate).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetRepairOrderRacketList(cls, ShopID,OrderStatus,Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
             RacketBookingDetailMasterModel.Status==OrderStatus).\
        order_by(RacketBookingDetailMasterModel.ActualReturnDate).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetOrderByRacketIDAndShopID(cls, ShopID, ShopTestRacketQRCodeDetailID, Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
             RacketBookingDetailMasterModel.ShopTestRacketQRCodeDetailID == ShopTestRacketQRCodeDetailID).\
        order_by(RacketBookingDetailMasterModel.ActualReturnDate).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetAllOrdersAsPerStatus(cls, ShopID,OrderStatus,Page,CustomerIDs):
        if OrderStatus == 7:            
            return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
                RacketBookingDetailMasterModel.Status==OrderStatus,RacketBookingDetailMasterModel.CustomerID.in_(CustomerIDs)).\
            order_by(RacketBookingDetailMasterModel.BookDate).paginate(page=Page,per_page=20)
        elif OrderStatus == 8:
            return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
                RacketBookingDetailMasterModel.Status==OrderStatus,RacketBookingDetailMasterModel.CustomerID.in_(CustomerIDs)).\
            order_by(RacketBookingDetailMasterModel.UpdatedDate).paginate(page=Page,per_page=20)
        elif OrderStatus == 9:
            return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
                RacketBookingDetailMasterModel.Status==OrderStatus,RacketBookingDetailMasterModel.CustomerID.in_(CustomerIDs)).\
            order_by(RacketBookingDetailMasterModel.ActualReturnDate).paginate(page=Page,per_page=20)
        elif OrderStatus == 10:
            return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
                RacketBookingDetailMasterModel.Status==OrderStatus,RacketBookingDetailMasterModel.CustomerID.in_(CustomerIDs)).\
            order_by(RacketBookingDetailMasterModel.ActualReturnDate).paginate(page=Page,per_page=20)
            
    @classmethod
    def GetLateOrderCountTillToday(cls, ShopID):
        CurrentDate=pydt.datetime.today()
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID, RacketBookingDetailMasterModel.Status == 7,cast(RacketBookingDetailMasterModel.BookDate, Date) < cast(CurrentDate, Date)).count()
        
    def order_details(ShopID,CustomerDetail = None,ContractDetail = None,RacketDetail = None,OrderDetail = None, BookRacketQRCodeDetail = None):
        Output={}
        Output['CustomerDetail'] = CustomerDetail.json1() if CustomerDetail else None
        Output['ContractDetail'] = ContractDetail.json(ShopID)  if ContractDetail else None
        Output['RacketDetail'] = RacketDetail.jsonForDashboard() if RacketDetail else None
        Output['OrderDetail'] = OrderDetail.json() if OrderDetail else None
        Output['BookRacketQRCodeDetail'] = BookRacketQRCodeDetail.json(ShopID) if BookRacketQRCodeDetail else None
        return Output
    
    def customer_historic_order_details(ShopID,ContractDetail = None,RacketDetail = None,OrderDetail = None, BookRacketQRCodeDetail = None,ShopDetail = None):
        Output={}
        Output['ShopDetail'] = ShopDetail.json() if ShopID else None
        Output['ContractDetail'] = ContractDetail.json(ShopID)  if ContractDetail else None
        Output['RacketDetail'] = RacketDetail.jsonForDashboard() if RacketDetail else None
        Output['OrderDetail'] = OrderDetail.json() if OrderDetail else None
        Output['BookRacketQRCodeDetail'] = BookRacketQRCodeDetail.json(ShopID) if BookRacketQRCodeDetail else None
        return Output
    
    @classmethod
    def GetOrderListForDashBoard(cls,ShopID,OrderStatus,Page,NameFilter):
        if NameFilter is None:
            OrderList=[]
            BookRacketQRCodeDetail = OrderDetail = RacketDetail = CustomerDetail = ContractDetail = None
            if OrderStatus == 7:
                Orders = RacketBookingDetailMasterModel.GetDepartureOrderList(ShopID,OrderStatus,Page)
            elif OrderStatus == 8:
                Orders = RacketBookingDetailMasterModel.GetRacketTakenByCustomerOrderList(ShopID,OrderStatus,Page)
            elif OrderStatus == 9:
                Orders = RacketBookingDetailMasterModel.GetReturnOrderList(ShopID,OrderStatus,Page)
            elif OrderStatus == 10:
                Orders = RacketBookingDetailMasterModel.GetRepairOrderRacketList(ShopID,OrderStatus,Page)
            elif OrderStatus == 11:
                Orders = RacketBookingDetailMasterModel.GetReturnOrderList(ShopID,OrderStatus,Page)
            elif OrderStatus == 12:
                Orders = RacketBookingDetailMasterModel.GetReturnOrderList(ShopID,OrderStatus,Page)
            elif OrderStatus == 13:
                Orders = RacketBookingDetailMasterModel.GetReturnOrderList(ShopID,OrderStatus,Page)
            if Orders:
                for order in Orders.items:
                    CustomerDetail  = CustomerDetailModel.GetCustomerDetailUsingCustomerID(order.CustomerID)
                    ContractDetail = CustomerContractMasterModel.GetCustomerContractForDashboard(order.CustomerID)
                    RacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(order.ShopTestRacketID,order.ShopID)
                    OrderDetail = RacketBookingDetailMasterModel.GetOrderDetail(order.ShopID,order.CustomerID,order.id)
                    BookRacketQRCodeDetail = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(order.ShopTestRacketQRCodeDetailID)
                    if CustomerDetail and ContractDetail and RacketDetail and OrderDetail and BookRacketQRCodeDetail:
                        OrderList.append(RacketBookingDetailMasterModel.order_details(ShopID,CustomerDetail,ContractDetail,RacketDetail,OrderDetail,BookRacketQRCodeDetail))
                    else:                        
                        if CustomerDetail and ContractDetail and RacketDetail and OrderDetail:
                            OrderList.append(RacketBookingDetailMasterModel.order_details(ShopID,CustomerDetail,ContractDetail,RacketDetail,OrderDetail,BookRacketQRCodeDetail))
                OrderList= PaginationForOrderDashboard(Orders,OrderList)
                return OrderList
        else:
            OrderList=[]
            BookRacketQRCodeDetail = OrderDetail = RacketDetail = CustomerDetail = ContractDetail = None
            CustomerDetail = CustomerDetailModel.GetSearchCustomerForDashboard(NameFilter)
            CustomerIDArray=[]
            if CustomerDetail is not None:
                for customerdetail in CustomerDetail:
                    CustomerIDArray.append(customerdetail.id)
            else:
                OrderList= PaginationForOrderDashboardWithOutResult(0,OrderList)
                return OrderList
            Orders = RacketBookingDetailMasterModel.GetAllOrdersAsPerStatus(ShopID,OrderStatus,Page,CustomerIDArray)
            if Orders:
                for order in Orders.items:
                    CustomerDetail  = CustomerDetailModel.GetCustomerDetailUsingCustomerID(order.CustomerID)
                    ContractDetail = CustomerContractMasterModel.GetCustomerContractForDashboard(order.CustomerID)
                    RacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(order.ShopTestRacketID,order.ShopID)
                    OrderDetail = RacketBookingDetailMasterModel.GetOrderDetail(order.ShopID,order.CustomerID,order.id)
                    BookRacketQRCodeDetail = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(order.ShopTestRacketQRCodeDetailID)
                    if CustomerDetail and ContractDetail and RacketDetail and OrderDetail and BookRacketQRCodeDetail:
                        OrderList.append(RacketBookingDetailMasterModel.order_details(ShopID,CustomerDetail,ContractDetail,RacketDetail,OrderDetail,BookRacketQRCodeDetail))
                    else:
                        if CustomerDetail and ContractDetail and RacketDetail and OrderDetail:
                            OrderList.append(RacketBookingDetailMasterModel.order_details(ShopID,CustomerDetail,ContractDetail,RacketDetail,OrderDetail,BookRacketQRCodeDetail))
                OrderList= PaginationForOrderDashboard(Orders,OrderList)
                return OrderList             
            else:
                return{"message" : "No order found"}
            
    @classmethod
    def GetRacketHistoricOrders(cls, ShopID, ShopTestRacketQRCodeDetailID, Page):
        OrderList=[]
        Orders = RacketBookingDetailMasterModel.GetOrderByRacketIDAndShopID(ShopID, ShopTestRacketQRCodeDetailID, Page)
        if Orders:
            for order in Orders.items:
                CustomerDetail  = CustomerDetailModel.GetCustomerDetailUsingCustomerID(order.CustomerID)
                ContractDetail = CustomerContractMasterModel.GetCustomerContractForDashboard(order.CustomerID)
                RacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(order.ShopTestRacketID, order.ShopID)
                OrderDetail = RacketBookingDetailMasterModel.GetOrderDetail(order.ShopID,order.CustomerID,order.id)
                BookRacketQRCodeDetail = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(order.ShopTestRacketQRCodeDetailID)
                if CustomerDetail and ContractDetail and RacketDetail and OrderDetail and BookRacketQRCodeDetail:
                    OrderList.append(RacketBookingDetailMasterModel.order_details(ShopID, CustomerDetail, ContractDetail, RacketDetail, OrderDetail, BookRacketQRCodeDetail))
                else:
                    return{"message" : "Some details are not fetched"} , 200  #error  
            OrderList = pagination(Orders, OrderList)
            return OrderList             
        else:
            return{"message" : "No order found"}
        
    @classmethod
    def GetDateToBlockCalendarAsPerShopTestRacketIDSleeveSizeIDAndDate(cls,ShopTestRacketID,SleeveSizeID):
        StatusArray = [7,8,10]
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0,RacketBookingDetailMasterModel.Status.in_(StatusArray),RacketBookingDetailMasterModel.ShopTestRacketID == ShopTestRacketID,RacketBookingDetailMasterModel.SleeveSizeID  == SleeveSizeID).all()
    
    @classmethod
    def GetOrderByCustomerIDAndShopID(cls, ShopID,CustomerID,Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
             RacketBookingDetailMasterModel.CustomerID==CustomerID).\
        order_by(RacketBookingDetailMasterModel.id).paginate(page=Page,per_page=20)
    
    @classmethod
    def GetCustomerHistoricOrders(cls,ShopID,CustomerID,Page):
        OrderList=[]
        Orders = RacketBookingDetailMasterModel.GetOrderByCustomerIDAndShopID(ShopID, CustomerID, Page)
        if Orders:
            for order in Orders.items:
                ContractDetail = CustomerContractMasterModel.GetCustomerContractForDashboard(order.CustomerID)
                RacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(order.ShopTestRacketID,order.ShopID)
                OrderDetail = RacketBookingDetailMasterModel.GetOrderDetail(order.ShopID,order.CustomerID,order.id)
                BookRacketQRCodeDetail = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(order.ShopTestRacketQRCodeDetailID)
                ShopDetail = ShopMasterModel.ShopDetail(OrderDetail.ShopID)
                if ContractDetail and RacketDetail and OrderDetail:
                    OrderList.append(RacketBookingDetailMasterModel.customer_historic_order_details(ShopID,ContractDetail,RacketDetail,OrderDetail,BookRacketQRCodeDetail, ShopDetail))
                else:
                    return{"message" : "No historic orders found for given customer ID"} , 200  #error  
            OrderList= pagination(Orders,OrderList)
            return OrderList             
        else:
            return{"message" : "No historic orders found for given customer ID"}, 200  #error 
        
    @classmethod
    def GetOrderByCustomerID(cls, CustomerID,Page):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.CustomerID == CustomerID).order_by(RacketBookingDetailMasterModel.id).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetAllCustomerHistoricOrders(cls,CustomerID, Page):
        OrderList=[]
        Orders = RacketBookingDetailMasterModel.GetOrderByCustomerID(CustomerID, Page)
        if Orders:
            for order in Orders.items:
                ContractDetail = CustomerContractMasterModel.GetCustomerContractForDashboard(order.CustomerID)
                RacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopTestRacketID(order.ShopTestRacketID)
                OrderDetail = RacketBookingDetailMasterModel.GetOrderDetailByCustomerIDAndBookingDetailID(order.CustomerID, order.id)
                BookRacketQRCodeDetail = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(order.ShopTestRacketQRCodeDetailID)
                ShopID = OrderDetail.ShopID
                ShopDetail = ShopMasterModel.ShopDetail(OrderDetail.ShopID)
                if RacketDetail and OrderDetail:
                    OrderList.append(RacketBookingDetailMasterModel.customer_historic_order_details(ShopID, ContractDetail, RacketDetail, OrderDetail, BookRacketQRCodeDetail, ShopDetail))
                else:
                    return{"message" : "No historic orders found for given customer ID"} , 200  #error  
            OrderList= pagination(Orders,OrderList)
            return OrderList             
        else:
            return{"message" : "No historic orders found for given customer ID"}, 200  #error
        
    @classmethod
    def ValidateQRcodeBooking(cls,ShopID,QRCodeID):
        query = db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopTestRacketQRCodeDetailID == ShopTestRacketQRCodeDetailModel.id,
                                                                        ShopTestRacketQRCodeDetailModel.QRCodeID == QRCodeID,
                                                                        RacketBookingDetailMasterModel.ShopID == ShopID, 
                                                                        RacketBookingDetailMasterModel.Status == 8, 
                                                                        ShopTestRacketQRCodeDetailModel.IsRacketTakenByCustomer == 1,
                                                                        ShopTestRacketQRCodeDetailModel.IsDeleted == 0).first()
        return query
                                                                        # QRCodeMasterModel.DecryptQRCode == QRCodeDecrypted, 
    
    @classmethod
    def AutoCancleCustomerOrder(cls):
        CurrentDate=pydt.datetime.today()
        AllDataOfStatus7 = db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0, RacketBookingDetailMasterModel.Status == 7,cast(RacketBookingDetailMasterModel.BookDate, Date) < cast(CurrentDate, Date)).all()
        if AllDataOfStatus7:
            for Data in AllDataOfStatus7:
                setattr(Data, "IsCancel", True)  
                setattr(Data, "CancelDate", getUTCTime())  
                setattr(Data, "Status", 13)
                commit()
                CustomerDetail = CustomerDetailModel.GetCustomerDetailUsingCustomerID(Data.CustomerID)
                CustomerName = CustomerDetail.Fname +' '+ CustomerDetail.Lname
                CustomerEmailID = CustomerDetail.EmailAddress
                ShopTestRacket = ShopTestRacketModel.GetShopRacketDetailByShopTestRacketID(Data.ShopTestRacketID)
                RacketDetail = RacketMasterModel.GetTestRacketDetail(ShopTestRacket.MasterTestingRacketID)
                RacketName = RacketDetail.Brand +' '+ RacketDetail.Range +' '+ RacketDetail.Modele + '(' +str(RacketDetail.Weight) +')'
                BookedDate = Data.BookDate
                ShopDetail = ShopMasterModel.ShopDetail(Data.ShopID)
                OrderMasterService.EmailForAutoCancelOrder(CustomerName,CustomerEmailID,RacketName,BookedDate,ShopDetail)
            return True
        else:
            return {"message" : "No order found for autocancellation"}, 200  #error
        
    @classmethod
    def GetOrderListOnBasisOfStatus(cls, ShopID,OrderStatus,Page,CustomerID):
        return db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.ShopID == ShopID,\
             RacketBookingDetailMasterModel.Status.in_(OrderStatus),RacketBookingDetailMasterModel.CustomerID == CustomerID).\
        order_by(RacketBookingDetailMasterModel.BookDate).paginate(page=Page,per_page=20)
        
    @classmethod
    def GetOrderStatusInArray(cls,ShopID,OrderStatus,Page,CustomerID):
        OrderList=[]
        BookRacketQRCodeDetail = OrderDetail = RacketDetail = CustomerDetail = ContractDetail = None
        if OrderStatus:
            Orders = RacketBookingDetailMasterModel.GetOrderListOnBasisOfStatus(ShopID,OrderStatus,Page,CustomerID)
        else:
            Orders = RacketBookingDetailMasterModel.GetOrderByCustomerIDAndShopID(ShopID,CustomerID,Page)
        if Orders:
            for order in Orders.items:
                CustomerDetail  = CustomerDetailModel.GetCustomerDetailUsingCustomerID(order.CustomerID)
                ContractDetail = CustomerContractMasterModel.GetCustomerContractForDashboard(order.CustomerID)
                RacketDetail = ShopTestRacketModel.GetShopRacketDetailByShopIDAndShopTestRacketID(order.ShopTestRacketID,order.ShopID)
                OrderDetail = RacketBookingDetailMasterModel.GetOrderDetail(order.ShopID,order.CustomerID,order.id)
                BookRacketQRCodeDetail = ShopTestRacketQRCodeDetailModel.GetShopTestRacketQRCodeDetail(order.ShopTestRacketQRCodeDetailID)
                if CustomerDetail and ContractDetail and RacketDetail and OrderDetail and BookRacketQRCodeDetail:
                    OrderList.append(RacketBookingDetailMasterModel.order_details(ShopID,CustomerDetail,ContractDetail,RacketDetail,OrderDetail,BookRacketQRCodeDetail))
                else:
                    if CustomerDetail and ContractDetail and RacketDetail and OrderDetail:
                        OrderList.append(RacketBookingDetailMasterModel.order_details(ShopID,CustomerDetail,ContractDetail,RacketDetail,OrderDetail,BookRacketQRCodeDetail))
            OrderList = PaginationForOrderDashboard(Orders, OrderList)
            return OrderList
                # if OrderStatus == 7:
                #     Counter1 = RacketBookingDetailMasterModel.GetLateOrderCountTillToday(ShopID) #OrderLate
                #     Counter2 = RacketBookingDetailMasterModel.GetRemainingOrderCountForToday(ShopID) #OrderRemainingToday
                #     Counter3 = RacketBookingDetailMasterModel.GetOrderCountForTomorrow(ShopID) #OrderOfTomorrow
                #     Counter4 = RacketBookingDetailMasterModel.GetOrderCountOfTheDayAfterTomorrow(ShopID) #OrderOfTheDayAfterTomorrow
                #     Counter5 = RacketBookingDetailMasterModel.GetCompletedOrderCountForToday(ShopID) #OrderCompleted 
                #     OrderList= PaginationForOrderDashboard(Orders,OrderList,Counter1,Counter2,Counter3,Counter4,Counter5)
                #     return OrderList
                
    @classmethod
    def QuestionAsk(cls, BookingDetailID):
        query = db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.id == BookingDetailID, 
                                                                        or_(RacketBookingDetailMasterModel.Status == 9, RacketBookingDetailMasterModel.Status == 10),
                                                                        RacketBookingDetailMasterModel.AskRating == 0, 
                                                                        RacketBookingDetailMasterModel.IsDeleted == 0).first()
        return query
    @classmethod
    def QuestionAllAsk(cls):
        query = db.session.query(RacketBookingDetailMasterModel).filter(or_(RacketBookingDetailMasterModel.Status == 10, RacketBookingDetailMasterModel.Status == 9),
                                                                        RacketBookingDetailMasterModel.AskRating == 0, 
                                                                        RacketBookingDetailMasterModel.IsDeleted == 0).all()
        return query

    @classmethod
    def UpdateAsk(cls, BookingDetailID):
        CheckDataBeforeUpdate = RacketBookingDetailMasterModel.QuestionAsk(BookingDetailID)
        if CheckDataBeforeUpdate is not None:
            setattr(CheckDataBeforeUpdate, "AskRating", True)
            commit()
            return True
        return False
    
    #sendgrid reminder
    @classmethod
    def ReminderSendgrid(cls):
        CurrentDate=pydt.datetime.today()
        Subject = "N'oubliez pas de récuperer la raquette de test"
        OrderToReming = db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0, RacketBookingDetailMasterModel.Status == 7,cast(RacketBookingDetailMasterModel.BookDate, Date) == cast(CurrentDate, Date), cast(RacketBookingDetailMasterModel.CreatedDate, Date) < cast(CurrentDate, Date)).all()
        if OrderToReming:
            for Data in OrderToReming:
                CustomerDetail = CustomerDetailModel.GetCustomerDetailUsingCustomerID(Data.CustomerID)
                CustomerName = CustomerDetail.Fname +' '+ CustomerDetail.Lname
                CustomerEmailID = CustomerDetail.EmailAddress
                ShopTestRacket = ShopTestRacketModel.GetShopRacketDetailByShopTestRacketID(Data.ShopTestRacketID)
                RacketDetail = RacketMasterModel.GetTestRacketDetail(ShopTestRacket.MasterTestingRacketID)
                RacketName = RacketDetail.ModelDisplayName
                PictureRacket = RacketDetail.RacketImage_1
                OrderID = Data.id
                OrderID = str(OrderID)
                BookedDate = Data.BookDate.strftime('%d/%m/%Y')
                BookedDate = str(BookedDate)
                ReturnDate = Data.ReturnDate.strftime('%d/%m/%Y')
                ReturnDate = str(ReturnDate)
                ShopDetail = ShopMasterModel.ShopDetail(Data.ShopID)
                ShopAddress = ShopDetail.ShopAddress
                ShopName = ShopDetail.shopname
                SleeveSize = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(Data.SleeveSizeID)
                del ShopDetail
                # order = [CustomerName, CustomerEmailID, OrderID, RacketName, PictureRacket, ShopAddress, ShopName, SleeveSize, BookedDate, ReturnDate]
                # return order
                OrderMasterService.SendReminder(Subject, CustomerName, CustomerEmailID, OrderID, RacketName, PictureRacket, ShopAddress, ShopName, SleeveSize, BookedDate, ReturnDate)
                return True
        else:
            return {"message" : "No order to send reminder"}, 200  #error
    
    @classmethod
    def ReminderSendgridReturn(cls):
        CurrentDate=pydt.datetime.today()
        Subject = "N'oubliez pas de rapporter la raquette de test"
        OrderToReming = db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0, RacketBookingDetailMasterModel.Status == 8,cast(RacketBookingDetailMasterModel.ReturnDate, Date) == cast(CurrentDate, Date)).all()
        if OrderToReming:
            for Data in OrderToReming:
                CustomerDetail = CustomerDetailModel.GetCustomerDetailUsingCustomerID(Data.CustomerID)
                CustomerName = CustomerDetail.Fname +' '+ CustomerDetail.Lname
                CustomerEmailID = CustomerDetail.EmailAddress
                ShopTestRacket = ShopTestRacketModel.GetShopRacketDetailByShopTestRacketID(Data.ShopTestRacketID)
                RacketDetail = RacketMasterModel.GetTestRacketDetail(ShopTestRacket.MasterTestingRacketID)
                RacketName = RacketDetail.ModelDisplayName
                PictureRacket = RacketDetail.RacketImage_1
                OrderID = Data.id
                OrderID = str(OrderID)
                BookedDate = Data.BookDate.strftime('%d/%m/%Y')
                BookedDate = str(BookedDate)
                ReturnDate = Data.ReturnDate.strftime('%d/%m/%Y')
                ReturnDate = str(ReturnDate)
                ShopDetail = ShopMasterModel.ShopDetail(Data.ShopID)
                ShopAddress = ShopDetail.ShopAddress
                ShopName = ShopDetail.shopname
                SleeveSize = SleeveSizeMasterModel.GetSleeveSizeAccordingToID(Data.SleeveSizeID)
                del ShopDetail
                OrderMasterService.SendReminder(Subject, CustomerName, CustomerEmailID, OrderID, RacketName, PictureRacket, ShopAddress, ShopName, SleeveSize, BookedDate, ReturnDate)
                return True
        else:
            return {"message" : "No order to send reminder"}, 200  #error
        
            
    @classmethod
    def CancelCustomerOrder(cls, CustomerID, BookingDetailID, Status, OrderCancelByAdminOrCustomer, Cancelby):
        query = db.session.query(RacketBookingDetailMasterModel).filter(RacketBookingDetailMasterModel.IsDeleted == 0, RacketBookingDetailMasterModel.Status == 7, 
                                                                                   RacketBookingDetailMasterModel.CustomerID == CustomerID, RacketBookingDetailMasterModel.id == BookingDetailID).first()
        
        if query:
            setattr(query, "IsCancel", True)  
            setattr(query, "CancelDate", getUTCTime())  
            setattr(query, "Status", Status)
            setattr(query, "OrderCancelByAdminOrCustomer", OrderCancelByAdminOrCustomer)
            setattr(query, "Cancelby", Cancelby)
            commit()
            return {"message" : "La commande a été annulé"}
        else:
            return {"message" : "La commande n'a pas été trouvé"}, 200  #error