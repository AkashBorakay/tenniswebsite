from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource,reqparse
from flask import request,jsonify, abort
from models.FrameworkModel import save_to_db,save_to_db_with_flush,commit
from resources.FrameworkResource import Authorization, IsAuthenticate
from models.WebsiteCustomerModel import CustomerDetailModel
import datetime as pydt
from models.WebsiteCustomerContractModel import CustomerContractMasterModel
from models.WebsiteContractMasterModel import ContractMasterModel
import json

class CheckContractNb(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                CustomerID = request.args.get("CustomerID")
                ShopContract = CustomerContractMasterModel.CheckContractExist(CustomerID, ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 200  #error
            if ShopContract:
                return {"Nb": ShopContract}
            return {"Nb": 0}
        return {'message':'token not valid'}
    
class CheckContractActiveNb(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                CustomerID = request.args.get("CustomerID")
                ShopContract = CustomerContractMasterModel.CheckContractActive(CustomerID, ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 200  #error
            if ShopContract:
                return {"Nb": ShopContract}
            return {"Nb": 0}
        return {'message':'token not valid'}
    
class GetShopWiseCustomerContract(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                CustomerID = request.args.get("CustomerID")
                CustomerContract = CustomerContractMasterModel.GetCustomerContract(CustomerID,ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop contract details."}, 200  #error
            if CustomerContract:
                return jsonify(CustomerContract)
            return json.loads('{}'), 200 
        return {'message':'token not valid'}
    
    
class ContractCustomerDetail(Resource):
    def put(self):
        if IsAuthenticate(request):
            try:
                data = request.get_json()
                ShopID = request.headers['ShopID']
                ContractCustomerID = data["ContractCustomerID"]
                data.pop("ContractCustomerID")
                ShopContract = CustomerContractMasterModel.UpdateShopContractCustomer(ShopID, ContractCustomerID, **data)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 200  #error
            if ShopContract:
                return jsonify({"ContractID": ShopContract.id})
            else:
               return {"message": "An error occurred while updating shop contract."}, 200  #error 
        return {'message':'token not valid'}
    
    def post(self): 
        if IsAuthenticate(request):
            try: 
                data = request.get_json()
                ShopID = request.headers['ShopID']
                ShopCustomerContract = CustomerContractMasterModel(**data)
                ShopCustomerContract.ShopID = ShopID
                save_to_db(ShopCustomerContract)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 200  #error
            return jsonify({"CustomerContractID": ShopCustomerContract.id})
        return {'message':'token not valid'}
    
    
    def delete(self):
        try:
            ContractCustomerID = request.get_json().get('ContractCustomerID')
            UpdatedBy = request.get_json().get('UpdatedBy')
            EndContract = CustomerContractMasterModel.DeleteContratCustomer(ContractCustomerID, UpdatedBy)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": error}, 500 #error  
        if EndContract == True:
            return {"message" : 0}
        else:
            return {"message" : 1}
    
class GetCustomerContracts(Resource):
    
    def get(self):
            try:
                CustomerID = request.args.get("CustomerID")
                CustomerContract = CustomerContractMasterModel.GetCustomerAllContracts(CustomerID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop contract details."}, 200  #error
            if CustomerContract:
                return jsonify(CustomerContract)
            return json.loads('{}'), 200
        
        
class AutoCancelCustomerContract(Resource):
    
    def get(self):
        try:
            EndContract = CustomerContractMasterModel.AutoContractEndCustomer()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching QRCode details."}, 500 #error  
        if EndContract == True:
            return {"message" : "Autocancellation Process Completed"}
        else:
            return {"message" : "No contract ending found"}