from hashlib import sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource,reqparse
from flask import request,jsonify, abort
from models.FrameworkModel import save_to_db,save_to_db_with_flush,commit
from resources.FrameworkResource import Authorization, IsAuthenticate
from models.WebsiteCustomerModel import CustomerDetailModel
import datetime as pydt
from models.ShopMasterModel import ShopMasterModel
from models.WebsiteRoleAssignmentModel import  WebsiteRoleAssignmentModel
from models.WebsiteRoleManagementModel import  WebsiteRoleManagementModel
from models.ApplicationRoleAssignmentModel import ApplicationRoleAssignmentModel
from models.StringerMasterModel import StringerMasterModel
from models.WebsiteCustomerContractModel import CustomerContractMasterModel
import json

class CommanLogin(Resource):
    
    def post(self):        
        data = request.get_json()
        EmailAddress= data['EmailAddress']
        Password =  data['Password']
        AdminOrClient =  data['AdminOrClient']
        EncodedPassword = sha256(Password.encode()).hexdigest()
        try:
            if AdminOrClient == 0:
                StringerDetail  = StringerMasterModel.GetStringerDetailForLogin(EmailAddress,EncodedPassword)
                if StringerDetail:
                    ShopID = StringerDetail.ShopID
                    StringerID = StringerDetail.id
                    # ShopDetail = ShopMasterModel.ShopDetail(ShopID)
                    CheckEntryInRoleAssigment  = WebsiteRoleAssignmentModel.GetWebsiteRoleAssignmentMasterForStringerID(StringerID)
                    CheckRoleName = WebsiteRoleManagementModel.GetRoleMaster(CheckEntryInRoleAssigment.RoleID)
                    if CheckEntryInRoleAssigment:
                        ShopID = StringerDetail.ShopID
                        StringerID = StringerDetail.id
                        StringerDetails = StringerMasterModel.GetStringer(StringerID,ShopID)
                        LastPasswordUpdatedDate = StringerDetails.PasswordUpdatedDate
                        CurrentDate=pydt.datetime.today()
                        CheckDifference = CurrentDate - LastPasswordUpdatedDate
                        if CheckDifference.days < 60:
                            IsValidate = 0
                        elif CheckDifference.days < 90:
                            IsValidate = 1
                        else:
                            IsValidate = 2
                        return {"message":IsValidate, "StringerID" : StringerDetail.id, "StringerName":StringerDetail.Name, "StringerLastName":StringerDetail.Lname, 
                                "EmailAddress" : StringerDetail.EmailAddress, "ShopID":StringerDetail.ShopID,
                                "RoleAssignmentID":CheckEntryInRoleAssigment.id, "RoleID":CheckEntryInRoleAssigment.RoleID, "IsCustomer":False}
                else:
                    return {'message': 3}, 200
                return {'message': 3}, 200
            elif AdminOrClient == 1:
                CustomerDetail  = CustomerDetailModel.GetCustomerDetailForLogin(EmailAddress, EncodedPassword)
                if CustomerDetail:
                    LastPasswordUpdatedDate = CustomerDetail.PasswordUpdatedDate
                    CurrentDate = pydt.datetime.today()
                    CheckDifference = CurrentDate - LastPasswordUpdatedDate
                    if CheckDifference.days < 60:
                        IsValidate = 0
                    elif CheckDifference.days < 90:
                        IsValidate = 1
                    else:
                        IsValidate = 2

                    return {"message":IsValidate, "CustomerID" : CustomerDetail.id, "Fname" : CustomerDetail.Fname, "Lname" : CustomerDetail.Lname,
                            "EmailAddress" : CustomerDetail.EmailAddress, "PhoneNo" : CustomerDetail.PhoneNo, "ShopFavoryID" : CustomerDetail.ShopFavoryID,
                            "BirthDate" : CustomerDetail.BirthDate.strftime('%d/%m/%Y'), "CountryID" : CustomerDetail.CountryID,
                            "Password" : CustomerDetail.Password, "IsCustomer":True} 
                else:
                    return {'message': 3}, 200
            
            else:
                return {'message': 3}, 200
        except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop details."}, 200  #error
        
    
    
    
    