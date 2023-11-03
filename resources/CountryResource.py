# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:50:39 2023

@author: SybilleDarbin
"""

# -*- coding: utf-8 -*-

from flask_restful import Resource,reqparse
from models.FrameworkModel import save_to_db
from models.CountryMasterModel import CountryMasterModel
from flask import request, jsonify, json
from sqlalchemy.exc import SQLAlchemyError

class CountryList(Resource):
         
    def get(self):
        Country  = CountryMasterModel.GetAllCountryName()
        try:
            Country  = CountryMasterModel.GetAllCountryName()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching Country list."}, 500  #error        
        return jsonify([Clist for Clist in Country])
