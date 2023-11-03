from multiprocessing import Value
from models.StringerMasterModel import StringerMasterModel
from sqlalchemy.exc import SQLAlchemyError
from resources.FrameworkResource import Authorization, IsAuthenticate
from flask_restful import Resource, reqparse
from flask import request, jsonify, json
from models.FrameworkModel import *
from models.ShopMasterModel import ShopMasterModel
from models.WebsiteRoleAssignmentModel import  WebsiteRoleAssignmentModel
from models.WebsiteRoleManagementModel import  WebsiteRoleManagementModel
from models.ApplicationRoleAssignmentModel import ApplicationRoleAssignmentModel
from service.OrderMasterService import OrderMasterService
from datetime import datetime
import datetime as pydt
from hashlib import sha256


class StringerLogin(Resource):
    def post(self):
        
        data = request.get_json()
        EmailAddress= data['EmailAddress']
        Password =  data['Password']
        # EncodedPassword = sha256(Password.encode()).hexdigest()
        try:
              StringerDetail  = StringerMasterModel.GetStringerDetailForLogin(EmailAddress,Password)
              if StringerDetail:
                ShopID = StringerDetail.ShopID
                UserID = StringerDetail.id
                ShopDetail = ShopMasterModel.ShopDetail(ShopID)
                CheckEntryInRoleAssigment  = WebsiteRoleAssignmentModel.GetWebsiteRoleAssignmentMasterForStringerID(UserID)
                CheckRoleName = WebsiteRoleManagementModel.GetRoleMaster(CheckEntryInRoleAssigment.RoleID)
              else:
                return {'message': 'Login detail not found'}, 200
        except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop details."}, 200  #error
        if StringerDetail:
            if ShopDetail:
                if CheckEntryInRoleAssigment:
                    ShopID = StringerDetail.ShopID
                    StringerID = StringerDetail.id
                    StringerDetails = StringerMasterModel.GetStringer(StringerID,ShopID)
                    LastPasswordUpdatedDate = StringerDetails.PasswordUpdatedDate
                    CurrentDate=pydt.datetime.today()
                    CheckDifference = CurrentDate - LastPasswordUpdatedDate
                    if CheckDifference.days < 60:
                        return {"IsValidate":0,"StringerID" : StringerDetail.id,"StringerFirstName":StringerDetail.Name,"StringerLastName":StringerDetail.Lname,"ShopID":StringerDetail.ShopID,"ShopTokenID":ShopDetail.tokenid,"ShopName":ShopDetail.shopname,"SentEmailAddress":ShopDetail.SentEmailAddress,"RoleAssignmentID":CheckEntryInRoleAssigment.id,"UserID":CheckEntryInRoleAssigment.StringerID,"RoleID":CheckEntryInRoleAssigment.RoleID,"RoleName":CheckRoleName.RoleName}
                    elif CheckDifference.days < 90:
                        return {"IsValidate":1,"StringerID" : StringerDetail.id,"StringerFirstName":StringerDetail.Name,"StringerLastName":StringerDetail.Lname,"ShopID":StringerDetail.ShopID,"ShopTokenID":ShopDetail.tokenid,"ShopName":ShopDetail.shopname,"SentEmailAddress":ShopDetail.SentEmailAddress,"RoleAssignmentID":CheckEntryInRoleAssigment.id,"UserID":CheckEntryInRoleAssigment.StringerID,"RoleID":CheckEntryInRoleAssigment.RoleID,"RoleName":CheckRoleName.RoleName}
                    else:
                        return {"IsValidate":2,"StringerID" : StringerDetail.id,"StringerFirstName":StringerDetail.Name,"StringerLastName":StringerDetail.Lname,"ShopID":StringerDetail.ShopID,"ShopTokenID":ShopDetail.tokenid,"ShopName":ShopDetail.shopname,"SentEmailAddress":ShopDetail.SentEmailAddress,"RoleAssignmentID":CheckEntryInRoleAssigment.id,"UserID":CheckEntryInRoleAssigment.StringerID,"RoleID":CheckEntryInRoleAssigment.RoleID,"RoleName":CheckRoleName.RoleName}                    
                return {'message': 'Login detail not found'}, 200
            return {'message': 'Login detail not found'}, 200
        return {'message': 'Login detail not found'}, 200 
    
class StringerRegister(Resource):
    def post(self):
        if IsAuthenticate(request):
            ShopID = request.headers['ShopID']
            data = request.get_json()
            RoleID = data['RoleID']
            InsertedBy = data['InsertedBy']
            try:
                StringerDetail  = StringerMasterModel.CheckStringerExistOrNot(data['EmailAddress'])
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop details."}, 200  #error
            if StringerDetail:
                return {'message': 'Stringer Email ID already register with us'}, 200
            else:
                try:
                    data.pop('RoleID')
                    data['ShopID'] = ShopID
                    SaveStringerDetail = StringerMasterModel(**data)
                    StringerID = save_to_db_with_flush(SaveStringerDetail)
                    if StringerID:
                        WebsiteRoleAssingment = WebsiteRoleAssignmentModel(StringerID, RoleID, InsertedBy)
                        ApplicationRoleAssingment = ApplicationRoleAssignmentModel(StringerID, 2, InsertedBy)
                        WebsiteRoleAssingmentID = save_to_db_with_flush(WebsiteRoleAssingment)
                        ApplicationRoleAssingmentID = save_to_db_with_flush(ApplicationRoleAssingment)
                        if WebsiteRoleAssingmentID and ApplicationRoleAssingmentID:
                            try:
                                commit()
                                OrderMasterService.EmailForPasswordCreationForStringer(StringerID, data['Name'], data['Lname'], data['EmailAddress'], ShopID)
                                return {"StringerID": StringerID}, 201
                            except SQLAlchemyError as e:
                                error = str(e.__dict__['orig'])
                                return {"message": e}, 200 #error  
                        else:
                            return {"message": "An error occurred inserting the stringer details."}, 200 #error
                    else:
                        return {"message": "An error occurred inserting the stringer details."}, 200 #error
                except SQLAlchemyError as e:
                    error = str(e.__dict__['orig'])
                    return {"message": e}, 200 #error
        return {'message':'token not valid'}
    
    def delete(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                StringerID = request.get_json().get('StringerID')
                UpdatedBy = request.get_json().get('UpdatedBy')
                StringerDetail = StringerMasterModel.DeleteStringerMasterAndRoleAssignment(StringerID,ShopID,UpdatedBy)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while deleting Stringer details."}, 500  #error        
            if StringerDetail: 
                return  {'StringerID': StringerDetail.UserID},200  
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}
    
    def put(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                NewRoleID = data['RoleID']
                data.pop('RoleID')
                StringerDetails = StringerMasterModel.UpdateStringerMaster(NewRoleID['RoleID'],ShopID, **data)
            except SQLAlchemyError as e:    
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating Stringer details."}, 500  #error        
            if StringerDetails:
                return  {"StringerID" :StringerDetails.id}
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}
    
class StringerPasswordUpdate(Resource):
    
    def put(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                StringerDetails = StringerMasterModel.UpdateStringerPassword(ShopID, **data)
            except SQLAlchemyError as e:    
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while Updating Stringer details."}, 500  #error        
            return {'Output':StringerDetails}
        return {'message':'token not valid'} 
    
class StringerList(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                StringerMaster = StringerMasterModel.GetStringerList(ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Stringer details."}, 500
            if StringerMaster:
                return jsonify({"result":[stringerlist.json() for stringerlist in StringerMaster]})
            return  json.loads('[]'), 200 
        return {'message':'token not valid'}
    
        
class GetDataForForgotPasswordStringer(Resource):
    
    def post(self):
        try:
            ShopID = request.headers['ShopID']
            data = request.get_json()
            EmailAddress = data['EmailAddress']
            CheckEmailExistOrNotForStringer = StringerMasterModel.CheckStringerExistOrNot(EmailAddress)
            if CheckEmailExistOrNotForStringer:
                StringerName = CheckEmailExistOrNotForStringer.Name +' '+CheckEmailExistOrNotForStringer.Lname
                StringerEmail = CheckEmailExistOrNotForStringer.EmailAddress
                StringerID = CheckEmailExistOrNotForStringer.id
                ResetPasswordLink = "https://testracketwebsite.azurewebsites.net/api/V1/UpdatePasswordStringer?StringerID=" + str(StringerID) + "&" + "ShopID=" + str(ShopID)
                return {"Result" : 1,"StringerName":StringerName,"StringerEmail":StringerEmail,"StringerID":StringerID,"ResetPasswordLink":ResetPasswordLink} #Customer Found with Given Email ID   
            else:
                return {"Result" : 0} #Customer Not Found with Given Email ID               
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching customer detail."}, 200  #error