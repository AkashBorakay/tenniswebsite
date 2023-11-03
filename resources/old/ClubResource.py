# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:14:09 2023

@author: SybilleDarbin
"""

from flask_restful import Resource,reqparse
from models.FrameworkModel import save_to_db
from models.ClubMasterModel import ClubMasterModel
from flask import request, jsonify, json
from sqlalchemy.exc import SQLAlchemyError

class ClubList(Resource):
         
    def get(self):
        try:
            Club  = ClubMasterModel.GetClubList()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"message": "An error occurred while fetching Country list."}, 500  #error        
        return jsonify([Clist for Clist in Club])
