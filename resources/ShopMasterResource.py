from flask_restful import Resource, reqparse
from models.ShopMasterModel import ShopMasterModel
from resources.FrameworkResource import Authorization,IsAuthenticate
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
# from models.WebsiteRoleAssignmentModel import  WebsiteRoleAssignmentModel
from datetime import datetime
import datetime as pydt
import json


class AllShopList(Resource):
    
    def get(self):
        try:
            ShopList = ShopMasterModel.GetAllShop()
        except SQLAlchemyError as e:    
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching all shop details."}, 500  #error
        if ShopList:
            return jsonify([shoplist.json() for shoplist in ShopList])
        else:
            return {'message':'problem while fetch all shop list'}
        
class GetShop(Resource):
    
    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                Authorization = request.headers['Authorization']
                ShopDetail = ShopMasterModel.ShopDetailUsingShopIDAndAuthorizationToken(ShopID,Authorization)
            except SQLAlchemyError as e:    
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching shop details."}, 500  #error
            if ShopDetail:
                return ShopDetail.json()
            else:
                return {'message':'problem while fetch shop list'}
        return {'message':'token not valid'}
    