from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource,reqparse
from flask import request,jsonify, abort,json
from models.FrameworkModel import save_to_db
from resources.FrameworkResource import Authorization, IsAuthenticate
from models.WebsiteContractMasterModel import ContractMasterModel


class ContractDetail(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                ShopContract = ContractMasterModel.GetContractList(ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop contract details."}, 200  #error
            if ShopContract:
                return jsonify({"result":[shopcontract.json() for shopcontract in ShopContract]})
            return json.loads('{}'), 200 
        return {'message':'token not valid'}
    
    def put(self):
        if IsAuthenticate(request):
            try:
                data = request.get_json()
                ShopID = request.headers['ShopID']
                ShopContract = ContractMasterModel.UpdateShopContract(ShopID,**data)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while updating Shop contract details."}, 200  #error
            if ShopContract:
                return jsonify({"ContractID": ShopContract.id})
            else:
               return {"message": "An error occurred while updating shop contract."}, 200  #error 
        return {'message':'token not valid'}
    
    def delete(self):
        if IsAuthenticate(request):
            try:
                data = request.get_json()
                ShopID = request.headers['ShopID']
                ContractID = data.get('ContractID')
                DeletedBy = data.get('DeletedBy')
                ShopContract = ContractMasterModel.DeleteShopContract(ContractID,DeletedBy,ShopID)
                if ShopContract == 1:
                    return jsonify({"ContractID": ContractID})
                else:
                   return {"message": "An error occurred while deleting shop contract may be due to wrong contract id."}, 200  #error
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while deleting Shop contract."}, 200  #error              
        return {'message':'token not valid'}
    
    def post(self): 
        if IsAuthenticate(request):
            try: 
                data = request.get_json()
                ShopID = request.headers['ShopID']
                ShopContract = ContractMasterModel(**data)
                ShopContract.ShopID = ShopID
                save_to_db(ShopContract)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while adding shop contract."}, 500  #error
            return jsonify({"ContractID": ShopContract.id})
        return {'message':'token not valid'}