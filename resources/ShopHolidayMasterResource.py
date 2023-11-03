from models.FrameworkModel import commit, save_to_db, save_to_db_with_flush
from flask_restful import Resource, reqparse
from models.ShopHolidayMasterModel import ShopHolidayModel
from resources.FrameworkResource import Authorization, IsAuthenticate
from flask import request, jsonify, json
from sqlalchemy.exc import SQLAlchemyError

class ShopHoliday(Resource):

    def get(self):
        if IsAuthenticate(request):
            try:
                ShopID = request.headers['ShopID']
                Shop_Holiday = ShopHolidayModel.GetHolidayList(ShopID)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while fetching Shop Holiday details."}, 500  #error
            if Shop_Holiday:
                return jsonify({"result":[shop_holiday.json() for shop_holiday in Shop_Holiday]})
            return json.loads('{}'), 200 
        return {'message':'token not valid'}

    def post(self): 
        if IsAuthenticate(request):
            try: 
                data = request.get_json()
                ShopID = request.headers['ShopID']
                ShopHoliday = ShopHolidayModel(**data)
                ShopHoliday.ShopID = ShopID
                save_to_db(ShopHoliday)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while adding Shop Holiday."}, 500  #error
            return jsonify({"ShopHolidayID": ShopHoliday.id})
        return {'message':'token not valid'}
    
    def put(self):
        if IsAuthenticate(request):
            try:
                data = request.get_json()
                ShopHoliday = ShopHolidayModel.UpdateShopHoliday(**data)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while updating Shop Holidays."}, 500  #error 
            if ShopHoliday:
                return jsonify({"ShopHolidayID": ShopHoliday.id})
            else:
               return {"message": "An error occurred while updating Shop Holidays."}, 500  #error  
        return {'message':'token not valid'} 

    def delete(self):
        if IsAuthenticate(request):
            try:
                data = request.get_json()
                ShopHolidayID = data.get('ShopHolidayID')
                UpdatedBy = request.get_json().get('UpdatedBy')
                ShopHolidayModel.DeleteShopHoliday(ShopHolidayID,UpdatedBy)
            except SQLAlchemyError as e:
                error = str(e.__dict__['orig'])
                return {"message": "An error occurred while deleting Shop Holidays."}, 500  #error 
            return jsonify({"ShopHolidayID": ShopHolidayID}) 
        return {'message':'token not valid'} 