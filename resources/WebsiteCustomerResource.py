from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource,reqparse
from flask import request, jsonify, abort
from models.FrameworkModel import save_to_db,save_to_db_with_flush,commit
from resources.FrameworkResource import Authorization, IsAuthenticate
import datetime as pydt
from models.WebsiteCustomerContractModel import CustomerContractMasterModel
from models.WebsiteCustomerModel import CustomerDetailModel
from service.OrderMasterService import OrderMasterService
import json
from hashlib import sha256
import os

# class CustomerLogin(Resource):
         
#     def post(self):
#         data = request.get_json()
#         EmailAddress= data['EmailAddress']
#         Password =  data['Password']
#         try:
#             CustomerDetail  = CustomerDetailModel.GetCustomerDetailForLogin(EmailAddress,Password)
#         except SQLAlchemyError as e:
#             error = str(e.__dict__['orig'])
#             return {"message": "An error occurred while fetching Shop details."}, 200  #error
#         if CustomerDetail:
#             # CustomerContractList = CustomerContractMasterModel.GetCustomerContract(CustomerDetail.id)
#             LastPasswordUpdatedDate = CustomerDetail.PasswordUpdatedDate
#             CurrentDate=pydt.datetime.today()
#             CheckDifference = CurrentDate - LastPasswordUpdatedDate
#             if CheckDifference.days < 60:
#                 return {"IsValidate":0,
#                     "CustomerID" : CustomerDetail.id,
#                     "Fname" : CustomerDetail.Fname,
#                     "Lname" : CustomerDetail.Lname,
#                     "EmailAddress" : CustomerDetail.EmailAddress,
#                     "PhoneNo" : CustomerDetail.PhoneNo,
#                     "ShopFavoryID" : CustomerDetail.ShopFavoryID,
#                     "ClubID" : CustomerDetail.ClubID,
#                     "BirthDate" : CustomerDetail.BirthDate,
#                     "EmailAddressVerified" : CustomerDetail.EmailAddressVerified,
#                     "IsSubscribed" : CustomerDetail.IsSubscribed,
#                     "IsCoach" : CustomerDetail.IsCoach,
#                     "IsGDPRAccepted" : CustomerDetail.IsGDPRAccepted,
#                     "IsChampion" : CustomerDetail.IsChampion,
#                     "CountryID" : CustomerDetail.CountryID,
#                     "IsCustomerCreatedFromWebsite" : CustomerDetail.IsCustomerCreatedFromWebsite,
#                     "IsCorrectEmailID" : CustomerDetail.IsCorrectEmailID,
#                     "Password" : CustomerDetail.Password,
#                     'Picture': CustomerDetail.Picture
#                     }
#                     # "CustomerContractList":CustomerContractList}     
#             elif CheckDifference.days < 90:
#                 return {"IsValidate":1,
#                     "CustomerID" : CustomerDetail.id,
#                     "Fname" : CustomerDetail.Fname,
#                     "Lname" : CustomerDetail.Lname,
#                     "EmailAddress" : CustomerDetail.EmailAddress,
#                     "PhoneNo" : CustomerDetail.PhoneNo,
#                     "ShopFavoryID" : CustomerDetail.ShopFavoryID,
#                     "ClubID" : CustomerDetail.ClubID,
#                     "BirthDate" : CustomerDetail.BirthDate,
#                     "EmailAddressVerified" : CustomerDetail.EmailAddressVerified,
#                     "IsSubscribed" : CustomerDetail.IsSubscribed,
#                     "IsCoach" : CustomerDetail.IsCoach,
#                     "IsGDPRAccepted" : CustomerDetail.IsGDPRAccepted,
#                     "IsChampion" : CustomerDetail.IsChampion,
#                     "CountryID" : CustomerDetail.CountryID,
#                     "IsCustomerCreatedFromWebsite" : CustomerDetail.IsCustomerCreatedFromWebsite,
#                     "IsCorrectEmailID" : CustomerDetail.IsCorrectEmailID,
#                     "Password" : CustomerDetail.Password,
#                     'Picture': CustomerDetail.Picture
#                     }
#                     # "CustomerContractList":CustomerContractList} 
#             else:
#                 return {"IsValidate":2,
#                     "CustomerID" : CustomerDetail.id,
#                     "Fname" : CustomerDetail.Fname,
#                     "Lname" : CustomerDetail.Lname,
#                     "EmailAddress" : CustomerDetail.EmailAddress,
#                     "PhoneNo" : CustomerDetail.PhoneNo,
#                     "ShopFavoryID" : CustomerDetail.ShopFavoryID,
#                     "ClubID" : CustomerDetail.ClubID,
#                     "BirthDate" : CustomerDetail.BirthDate,
#                     "EmailAddressVerified" : CustomerDetail.EmailAddressVerified,
#                     "IsSubscribed" : CustomerDetail.IsSubscribed,
#                     "IsCoach" : CustomerDetail.IsCoach,
#                     "IsGDPRAccepted" : CustomerDetail.IsGDPRAccepted,
#                     "IsChampion" : CustomerDetail.IsChampion,
#                     "CountryID" : CustomerDetail.CountryID,
#                     "IsCustomerCreatedFromWebsite" : CustomerDetail.IsCustomerCreatedFromWebsite,
#                     "IsCorrectEmailID" : CustomerDetail.IsCorrectEmailID,
#                     "Password" : CustomerDetail.Password,
#                     'Picture': CustomerDetail.Picture
#                     }
#                     # "CustomerContractList":CustomerContractList}                   
#         return {'message': 'Login detail not found'}, 200
    
class CustomerInfo(Resource):
    
    def get(self):
            try:
                CustomerID = request.args.get("CustomerID")
                CustomerDetail  = CustomerDetailModel.GetCustomerDetailUsingCustomerID(CustomerID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching customer details."}, 500  #error        
            if CustomerDetail:                
                return  CustomerDetail.json(),200  
            return json.loads('{}'), 200 #('{}', 200)
    
             
class CheckCustomer(Resource):
    def get(self):
            try:
                Email = request.args.get("EmailAddress")
                CustomerDetail  = CustomerDetailModel.CheckCustomerExistOrNot(Email)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching customer details."}, 500  #error        
            if CustomerDetail:                
                return  {"message": 0, "CustomerID": CustomerDetail.id}    
            else:
                return  {"message": 1}
        
class CustomerDetail(Resource):
         
    def post(self):
        data = request.get_json()
        NormalPassword = data["Password"]
        EncryptedPassword = sha256(NormalPassword.encode()).hexdigest()     
        try:
            CustomerDetail  = CustomerDetailModel.CheckCustomerExistOrNot(data['EmailAddress'])
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching Shop details."}, 200  #error
        if CustomerDetail:
            return {'message': 'Email ID already register with us'}, 200
        else:
            data.pop('Password')
            data['Password'] = EncryptedPassword
            SaveCustomerDetail = CustomerDetailModel(**data)
            CustomerID = save_to_db_with_flush(SaveCustomerDetail)
            
            # ShopCustomerContract = CustomerContractMasterModel(CustomerID, **data)
            # save_to_db(ShopCustomerContract)
            try:
                commit()
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred inserting the customer details."}, 200 #error
            return {"CustomerID":   CustomerID, "message" : "ok" }, 201 
        
        
    def put(self):
            try:
                data = request.get_json()
                CustomerDetails = CustomerDetailModel.UpdateCustomer(**data)
            except SQLAlchemyError as e:    
                error = str(e.__dict__['orig'])
                return {"message": error}, 200  #error        
            if CustomerDetails:
                return  {"CustomerID" :CustomerDetails.id}
            return json.loads('{}'), 200 #('{}', 200)
    
    
    def delete(self):
            try:
                CustomerID = request.get_json().get('CustomerID')
                UpdatedBy = request.get_json().get('UpdatedBy')
                CustomerDetail = CustomerDetailModel.DeleteCustomer(CustomerID,UpdatedBy)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while deleting customer details."}, 500  #error        
            if CustomerDetail: 
                return  {'CustomerID': CustomerDetail.id},200  
            return json.loads('{}'), 200 #('{}', 200)
    
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                CustomerID = request.args.get("CustomerID")
                CustomerDetail  = CustomerDetailModel.GetCustomerDetailUsingCustomerID(CustomerID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching customer details."}, 500  #error        
            if CustomerDetail:                
                return  CustomerDetail.CustomerDetailJson(ShopID),200  
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}
    
class CustomerPasswordUpdate(Resource):
        
    def put(self):
            try:
                data = request.get_json()
                CustomerDetails = CustomerDetailModel.UpdateCustomerPassword(**data)
            except SQLAlchemyError as e:    
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating customer details."}, 200  #error        
            return {'Output':CustomerDetails}
    
# class CustomerList(Resource):
    
#     def post(self):
#         if IsAuthenticate(request):
#             try:
#                 ShopID = request.headers['ShopID']
#                 data = request.get_json()
#                 Page = data['Page']
#                 Page = 1 if Page is None else int(Page)
#                 NameFilter = data['NameFilter']
#                 CustomerDetails  = CustomerDetailModel.GetAllCustomerList(Page,ShopID,NameFilter)
#             except SQLAlchemyError as e:
#                 error = str(e.__dict__['orig'])
#                 return {"message": "An error occurred while deleting customer details."}, 500  #error        
#             if CustomerDetail:                
#                 return  CustomerDetails,200  
#             return json.loads('{}'), 200 #('{}', 200)
#         return {'message':'token not valid'}
     
class CustomerListV2(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                NameFilter = data['NameFilter']
                CustomerDetails  = CustomerDetailModel.GetAllCustomerListV2(Page,ShopID,NameFilter)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while deleting customer details."}, 500  #error        
            if CustomerDetail:                
                return  CustomerDetails,200  
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}
# class ForgotPassword(Resource):#use sendgrid instead
    
#     def post(self):
#         try:
#             data = request.get_json()
#             EmailAddress = data['EmailAddress']
#             CheckEmailExistOrNotForCustomer = CustomerDetailModel.CheckCustomerExistOrNot(EmailAddress)
#             if CheckEmailExistOrNotForCustomer:
#                 CustomerName = CheckEmailExistOrNotForCustomer.Fname +' '+CheckEmailExistOrNotForCustomer.Lname
#                 CustomerEmail = CheckEmailExistOrNotForCustomer.EmailAddress
#                 CustomerID = CheckEmailExistOrNotForCustomer.id
#                 Lien = "https://testracketwebsite.azurewebsites.net/api/V1/UpdatePassword?CustomerID=" + str(CustomerID)
#                 OrderMasterService.EmailForForgotPassword(CustomerName,CustomerEmail,CustomerID)
#                 return {"Result" : 1} #EMail Sent
#             else:
#                 return {"Result" : 0} #EMail Not Sent               
#         except SQLAlchemyError as e:
#             error = str(e.__dict__['orig'])
#             return {"message": error}, 200  #error
            # return {"message": "An error occurred while sending password reset notification email."}, 200  #error
        
class GetDataForForgotPassword(Resource):
    
    def post(self):
        try:
            data = request.get_json()
            EmailAddress = data['EmailAddress']
            CheckEmailExistOrNotForStringer = CustomerDetailModel.CheckCustomerExistOrNot(EmailAddress)
            if CheckEmailExistOrNotForStringer:
                CustomerName = CheckEmailExistOrNotForStringer.Fname +' '+CheckEmailExistOrNotForStringer.Lname
                CustomerEmail = CheckEmailExistOrNotForStringer.EmailAddress
                CustomerID = CheckEmailExistOrNotForStringer.id
                # ResetPasswordLink = "https://testracketwebsite.azurewebsites.net/api/V1/UpdatePassword?CustomerID=" + str(CustomerID)
                ResetPasswordLink = os.environ.get('AzureAppServiceURL_Websiste') + "/api/V1/UpdatePassword?CustomerID=" + str(CustomerID)
                return {"Result" : 1,"CustomerName":CustomerName,"CustomerEmail":CustomerEmail,"CustomerID":CustomerID,"ResetPasswordLink":ResetPasswordLink} #Customer Found with Given Email ID   
            else:
                return {"Result" : 0} #Customer Not Found with Given Email ID               
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching customer detail."}, 200  #error
        
        
        
class CustomerRegisterFromAdmin(Resource):
    def post(self):
            data = request.get_json()
            InsertedBy = data['InsertedBy']
            try:
                CustomerDetail  = CustomerDetailModel.CheckCustomerExistOrNot(data['EmailAddress'])
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop details."}, 200  #error
            if CustomerDetail:
                return {'message': 'Customer Email ID already register with us'}, 200
            else:
                try:
                    SaveCustomerDetail = CustomerDetailModel(**data)
                    CustomerID = save_to_db_with_flush(SaveCustomerDetail)
                    if CustomerID:
                        try:
                            commit()
                            OrderMasterService.EmailForPasswordCreationForCustomer(CustomerID, data['Fname'], data['Lname'], data['EmailAddress'])
                            return {"CustomerID":   CustomerID }, 201
                        except SQLAlchemyError as e:
                            error = str(e.__dict__['orig'])
                            return {"message": e}, 200 #error  
                    else:
                        return {"message": "An error occurred inserting the stringer details."}, 200 #error
                except SQLAlchemyError as e:
                    error = str(e.__dict__['orig'])
                    return {"message": e}, 200 #error
                
    