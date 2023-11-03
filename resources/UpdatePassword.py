from ast import Pass
from models.ShopMasterModel import ShopMasterModel
from models.StringerMasterModel_V2 import StringerMasterModel
from models.WebsiteCustomerModel import CustomerDetailModel
from flask_restful import Resource
from flask import request, render_template,make_response
from hashlib import sha256

class UpdatePasswordResource (Resource):

   def get(self):
      try:
        CustomerID = request.args.get("CustomerID")
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('Forgot_Password.html', CustomerID = CustomerID),200,headers)
      except Exception as e:
        error = str(e.__dict__['orig'])
        return {"message": "An error occurred while reseting password"}, 500  #error 

   def post(self):
      try:
        CustomerID = request.args.get("CustomerID")
        Password = "Password"
        Password = request.form.get("password1")
        EncodedPassword = sha256(Password.encode()).hexdigest()
        PasswordUpdate = CustomerDetailModel.UpdateShopPasswordThrougEmailFunctionality(CustomerID, EncodedPassword)
        if PasswordUpdate is not None:
          headers = {'Content-Type': 'text/html'}
          return make_response(render_template('Forgot_Password_Success.html'),200,headers)
        else:
          return {"message": "An error occurred while reseting password"}, 200  #error   
      except Exception as e:
        error = str(e.__dict__['orig'])
        return {"message": "An error occurred while reseting password"}, 200  #error 
    
class UpdatePasswordStringerResource (Resource):

    def get(self):
      try:
        StringerID = request.args.get("StringerID")
        ShopID = request.args.get("ShopID")
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('Forgot_Password.html', StringerID = StringerID, ShopID = ShopID),200,headers)
      except Exception as e:
        error = str(e.__dict__['orig'])
        return {"message": "An error occurred while reseting password"}, 500  #error 

    def post(self):
      try:
        StringerID = request.args.get("StringerID")
        ShopID = request.args.get("ShopID")
        Password = "Password"
        Password = request.form.get("password1")
        EncodedPassword = sha256(Password.encode()).hexdigest()
        PasswordUpdate = StringerMasterModel.UpdateStringerPasswordThrougEmailFunctionality(StringerID, ShopID, EncodedPassword)
        if PasswordUpdate is not None:
          headers = {'Content-Type': 'text/html'}
          return make_response(render_template('Forgot_Password_Success.html'),200,headers)
        else:
          return {"message": "An error occurred while reseting password"}, 200  #error   
      except Exception as e:
        error = str(e.__dict__['orig'])
        return {"message": "An error occurred while reseting password"}, 200  #error 