# -*- coding: utf-8 -*-

from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource,reqparse
from flask import request,jsonify, abort
from models.FrameworkModel import save_to_db
from resources.FrameworkResource import Authorization, IsAuthenticate
from models.WebsiteRoleManagementModel_V2 import WebsiteRoleManagementModel

import json

class RoleDetail(Resource):
         
    def get(self):
        if IsAuthenticate(request):
            try:
                # ShopID = request.headers['ShopID']
                GetRoleList  = WebsiteRoleManagementModel.GetRoleList()
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching role list "}, 200  #error  
            if GetRoleList:
                return jsonify([Role.json() for Role in GetRoleList])
            return {'message':'Role not found'}
        return {'message':'token not valid'}