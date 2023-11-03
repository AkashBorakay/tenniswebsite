# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 15:43:53 2023

@author: SybilleDarbin
"""

from multiprocessing import Value
from sqlalchemy.exc import SQLAlchemyError
from resources.FrameworkResource import Authorization, IsAuthenticate
from flask_restful import Resource, reqparse
from flask import request, jsonify, json
from models.FrameworkModel import *
from models.Cancel_OrderModel import  CancelMasterView
from datetime import datetime
import datetime as pydt
from hashlib import sha256


class CustomerCancelAuto(Resource):
    
    def post(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                data = request.get_json()
                Page = data['Page']
                Page = 1 if Page is None else int(Page)
                NameFilter = data['NameFilter']
                CustomerDetails  = CancelMasterView.GetAllcancel(Page, ShopID, NameFilter)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": error}, 500  #error        
            if CustomerDetails:                
                return  CustomerDetails,200  
            return json.loads('{}'), 200 #('{}', 200)
        return {'message':'token not valid'}