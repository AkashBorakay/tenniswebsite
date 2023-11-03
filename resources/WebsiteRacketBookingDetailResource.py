from multiprocessing import Value
from sqlalchemy.exc import SQLAlchemyError
from resources.FrameworkResource import Authorization, IsAuthenticate
from flask_restful import Resource, reqparse
from flask import request, jsonify, json
from models.FrameworkModel import *
from models.WebsiteRacketBookingDetailModel import RacketBookingDetailMasterModel
from models.WebsiteCustomerContractModel import CustomerContractMasterModel
from models.WebsiteContractMasterModel import ContractMasterModel
from datetime import datetime,date, timedelta
import datetime as pydt
from hashlib import sha256
from models.WebsiteShopTestingRacketQRCodeDetailModel import ShopTestRacketQRCodeDetailModel



class BookedCalendarDates(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            ShopTestRacketID = request.args.get('ShopTestRacketID')
            SleeveSizeID = request.args.get('SleeveSizeID')
            BookedDates = RacketBookingDetailMasterModel.GetDateToBlockCalendar(ShopTestRacketID,SleeveSizeID)
            if BookedDates:
                return jsonify([item.jsonForBookedDate() for item in BookedDates])
            else:
                return {'message':'Error While Fetching Booked Dates'}, 200  #error   
        return {'message':'token not valid'}
    
class CustomerBookedRacketCount(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            CustomerContractMasterID = request.args.get('CustomerContractMasterID')
            CustomerContractID = request.args.get('CustomerContractID')            
            TotalMaxBookedRacketCountAsPerContract = ContractMasterModel.GetCustomerContractDetail(CustomerContractMasterID) #useless take nb racket allowed
            OpenOrderCountForContract = RacketBookingDetailMasterModel.GetTotalOpenOrderCountForCustomerContract(CustomerContractID)
            if TotalMaxBookedRacketCountAsPerContract and OpenOrderCountForContract:
                return {'TotalMaxBookedRacketCountAsPerContract':TotalMaxBookedRacketCountAsPerContract,'OpenOrderCountForContract':OpenOrderCountForContract}
            else:
                return {'message':'Error While Fetching Order Count'}, 200  #error   
        return {'message':'token not valid'}
    
class CheckCountCustomerBookedRacket(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            ShopID = request.headers['ShopID']
            CustomerID = request.args.get('CustomerID')
            # CustomerContractID = request.args.get('CustomerContractID')    
            NbRacket = CustomerContractMasterModel.GetRacketContract(CustomerID, ShopID)
            if NbRacket is None:
                return {'NbRacket': 0}   
            else:
                CountBooked = RacketBookingDetailMasterModel.GetOrderCountForCustomerBetweenDates(CustomerID, ShopID)
                if CountBooked:
                    return {'NbRacket':NbRacket - CountBooked}
                else:
                    return {'NbRacket': NbRacket}, 200  #error   
        return {'message':'token not valid'}
    
class Dashboard(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                data = request.get_json()
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                ShopID = request.headers['ShopID']
                OrderStatus= data['OrderStatus'] 
                NameFilter = data['NameFilter']
                ShopOrders = RacketBookingDetailMasterModel.GetOrderListForDashBoard(ShopID,OrderStatus,Page,NameFilter)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Order List details."}, 500  #error  
            if ShopOrders:
                    return ShopOrders   
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}
    
class RacketOrderHistory(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                ShopTestRacketQRCodeDetailID = data['ShopTestRacketQRCodeDetailID']
                ShopOrders = RacketBookingDetailMasterModel.GetRacketHistoricOrders(ShopID,ShopTestRacketQRCodeDetailID,Page)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Order List details."}, 500  #error  
            if ShopOrders:
                    return ShopOrders   
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}
    
class BookedCalendarDates_V2(Resource):
    
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days+1)):
            yield start_date + timedelta(n)
    
    def get(self):
        if IsAuthenticate(request):
            ShopTestRacketID = request.args.get('ShopTestRacketID')
            SleeveSizeID = request.args.get('SleeveSizeID')
            IdenticalRacketCount = ShopTestRacketQRCodeDetailModel.CountOfIdenticalRacketWithShopTestRacketIDAndSleeveSizeID(ShopTestRacketID,SleeveSizeID)
            BookedDates = RacketBookingDetailMasterModel.GetDateToBlockCalendarAsPerShopTestRacketIDSleeveSizeIDAndDate(ShopTestRacketID,SleeveSizeID)
            BlockedDate=[]
            for bookedDates in BookedDates:
                if bookedDates.Status == 7:
                    StartDate = bookedDates.BookDate                
                    EndDate =  bookedDates.ReturnDate
                    if bookedDates.BookDate < pydt.datetime.today():
                        StartDate = pydt.datetime.today()
                    if bookedDates.ReturnDate < pydt.datetime.today():
                        EndDate = pydt.datetime.today()
                elif bookedDates.Status == 8:
                    StartDate = pydt.datetime.today()
                    EndDate = pydt.datetime.today()
                    if EndDate < bookedDates.ReturnDate:
                        EndDate = bookedDates.ReturnDate
                elif bookedDates.Status == 10:
                    StartDate = bookedDates.ActualReturnDate
                    Day = pydt.timedelta(days = 1)
                    EndDate = StartDate + Day
                bookedDates.BookDate =  StartDate.date()
                bookedDates.ReturnDate = EndDate.date()
            for data in  BookedDates :                       
                for single_date in BookedCalendarDates_V2.daterange(data.BookDate, data.ReturnDate):
                    OrderCount = 0
                    Check = True                        
                    for  MainbookedDate in BookedDates:
                        Check = True
                        if  OrderCount < IdenticalRacketCount :
                            if  MainbookedDate.BookDate <= single_date <= MainbookedDate.ReturnDate:
                                OrderCount += 1
                            else:
                                Check = False
                    if OrderCount >= IdenticalRacketCount and Check == True:
                        if single_date.strftime('%Y/%m/%d') in BlockedDate:
                            continue
                        else:
                            BlockedDate.append(single_date.strftime('%Y/%m/%d'))
            if BookedDates:
                return jsonify([blockeddate for blockeddate in BlockedDate])
            else:
                return {'message':'Error While Fetching Booked Dates'}, 200  #error   
        return {'message':'token not valid'}
    
class CustomerHistoricOrder(Resource):
        
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                CustomerID = data['CustomerID']
                CustomerHistoricOrders = RacketBookingDetailMasterModel.GetCustomerHistoricOrders(ShopID,CustomerID,Page)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Order List details."}, 500  #error  
            if CustomerHistoricOrders:
                return CustomerHistoricOrders
            else:
                return{"message" : "No historic orders found for given customer ID"} , 200  #error 
        return {'message':'token not valid'}
    
class CustomerOrder(Resource):
        
    def post(self):
            try:
                data = request.get_json()
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                CustomerID = data['CustomerID']
                CustomerHistoricOrders = RacketBookingDetailMasterModel.GetAllCustomerHistoricOrders(CustomerID,Page)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Order List details."}, 500  #error  
            if CustomerHistoricOrders:
                return CustomerHistoricOrders
            else:
                return{"message" : "No historic orders found for given customer ID"} , 200  #error 
    
class ReturnRacketViaQrCode(Resource):
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                QRCodeID = request.args.get('QRCodeID')
                Result = RacketBookingDetailMasterModel.ValidateQRcodeBooking(ShopID, QRCodeID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching QRCode details."}, 500 #error  
            if Result:
                return Result.jsonReturnScan()
            return {'message':'QR code is not existing in the database or has not left the shop'}
        return {'message':'token not valid'}
            
            
class AutoCancleCustomerOrder(Resource):
    
    def get(self):
        try:
            QRCodeDecrypted = RacketBookingDetailMasterModel.AutoCancleCustomerOrder()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching QRCode details."}, 500 #error  
        if QRCodeDecrypted == True:
            return {"message" : "Autocancellation Process Completed"}
        else:
            return {"message" : "No order found for autocancellation"}
        
class OrderStatusInArray(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                data = request.get_json()
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                ShopID = request.headers['ShopID']
                OrderStatus= data['OrderStatus'] 
                CustomerID  = data['CustomerID']
                ShopOrders = RacketBookingDetailMasterModel.GetOrderStatusInArray(ShopID,OrderStatus,Page,CustomerID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Order List details."}, 500  #error  
            if ShopOrders:
                    return ShopOrders   
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}
        
    
class QuestionBeenAsk(Resource):
    def put(self):
            try:
                data = request.get_json()
                BookingDetailID = data['BookingDetailID']
                QuestionAsk = RacketBookingDetailMasterModel.UpdateAsk(BookingDetailID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating Question details."}, 500  #error        
            if QuestionAsk:
                return  {"HasBeenAsk": QuestionAsk}
            else:
                return {"message": "An error occurred while Updating Question asking."}   
            # return json.loads('{}'), 200 #('{}', 200)
        
    def get(self):
        try:
            QuestionToAsk = RacketBookingDetailMasterModel.QuestionAllAsk()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching QRCode details."}, 500 #error  
        if QuestionToAsk is not None:
            return jsonify({"result":[item.jsonQuestion() for item in QuestionToAsk]})
        else:
            return {"message" : "No question to ask"}
        
        
class ReminderSendViaSendgrid(Resource):
    
    def get(self):
        try:
            MailToSend = RacketBookingDetailMasterModel.ReminderSendgrid()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": error}, 500 #error  
        if MailToSend:# == True:
            # return {"message" : MailToSend[0] + ', '+ MailToSend[1] +', '+ MailToSend[2] +', '+ MailToSend[3] +', '+ MailToSend[4] +', '+ MailToSend[5] +
            #         ', '+ MailToSend[6] +', '+ MailToSend[7] +', '+ MailToSend[8] +', '+ MailToSend[9]}
            return {"message" : True}
        else:
            return {"message" : "No order found for reminder"}
        
class ReminderSendgridReturn(Resource):
    
    def get(self):
        try:
            MailToSend = RacketBookingDetailMasterModel.ReminderSendgridReturn()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching QRCode details."}, 500 #error  
        if MailToSend:# == True:
            return {"message" : True}
        else:
            return {"message" : "No order found for autocancellation"}
        
        
class CancelOrder(Resource):
    
    def put(self):
        try:
            data = request.get_json()
            CustomerID = data['CustomerID']
            BookingDetailID = data['BookingDetailID']
            Status = data['Status']
            Cancelby = data['Cancelby']
            OrderCancelByAdminOrCustomer = data['OrderCancelByAdminOrCustomer']#0 if admin 1 if customer
            CancelOrders = RacketBookingDetailMasterModel.CancelCustomerOrder(CustomerID, BookingDetailID, Status, Cancelby, OrderCancelByAdminOrCustomer)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": error}, 500  #error  
        if CancelOrders:
            return CancelOrders   
        return json.loads('{}'), 200 