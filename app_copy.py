from flask import Flask
from flask_restful import Api
import os
import urllib.parse
from flask_mail import Mail, Message

from resources.ShopMasterResource import AllShopList,GetShop
from resources.StringerMasterResource_V2 import StringerLogin,StringerRegister,StringerPasswordUpdate,StringerList, GetDataForForgotPasswordStringer
# from resources.WebsiteShopTestingRacketResource import AllTestRacketForShop,RacketDetail,GetRacketDetailAsPerUniqueValues,AssingNewQRCodeToExistingRacket,RacketDataBySuperAdmin,GetRacketDataBySuperAdmin, CheckQRCodeMessage
from resources.WebsiteShopTestingRacketResource import AllTestRacketForShop,RacketDetail,GetRacketDetailAsPerUniqueValues, AssingNewQRCode,RacketDataBySuperAdmin,GetRacketDataBySuperAdmin, CheckQRCodeMessage, RacketStatus
from resources.WebsiteQRCodeMasterResource import CheckQRCode, CheckQRCodeDecrypted
from resources.WebsiteCustomerResource import CustomerRegisterFromAdmin, CustomerLogin,CustomerDetail,CustomerPasswordUpdate,CustomerList,GetDataForForgotPassword, CustomerInfo, CustomerListV2, CheckCustomer
# from resources.WebsiteCustomerResource import CustomerLogin,CustomerDetail,CustomerPasswordUpdate,CustomerList,ForgotPassword,GetDataForForgotPassword, CustomerInfo
from resources.RacketFilterAndSearchViewResource import RacketFilterAccordingToSelection#,RacketFilterAccordingToSelection_V2
from resources.WebsiteRoleManagementResources import RoleDetail
from resources.WebsiteRacketBookingDetailResource import CancelOrder, BookedCalendarDates, CheckCountCustomerBookedRacket,CustomerBookedRacketCount,Dashboard,RacketOrderHistory,BookedCalendarDates_V2,CustomerHistoricOrder,CustomerOrder,ReturnRacketViaQrCode,AutoCancleCustomerOrder,OrderStatusInArray, QuestionBeenAsk, ReminderSendViaSendgrid, ReminderSendgridReturn
from resources.WebsiteRacketBookingResource import PlaceOrder,HandOverRacketByScanningQRCode,ReturnRacketToShop
from resources.CommanLoginResource_V2 import CommanLogin
from resources.RacketStatusMasterResource import RacketStatusMaster
from resources.SleeveSizeMasterResource import SleeveSizeList
from resources.ShopHolidayMasterResource import ShopHoliday
from resources.ShopTimingMasterResource import ShopTimingList
from resources.WebsiteContractMasterResource import ContractDetail
from resources.WebsiteCustomerContractResource import GetShopWiseCustomerContract,GetCustomerContracts, ContractCustomerDetail, AutoCancelCustomerContract, CheckContractNb, CheckContractActiveNb
from resources.CreatePassword import CreatePasswordResource
from resources.UpdatePassword import UpdatePasswordResource, UpdatePasswordStringerResource
from resources.CountryResource import CountryList
from resources.ClubResource import ClubList
from resources.FilterAndSearchRacketResource import RacketTestingFilter, RacketMasterFilter#, RacketTestingList
from resources.RacketMarkRessource import Racket_Marks, Racket_Marks_Info#, Racket_Marks_Client
from resources.CancelOrderRessource import CustomerCancelAuto

# params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=apptennispro.database.windows.net;DATABASE=tennispro_dev;UID=tennispro@apptennispro;PWD=Deploy@202103") # For Windows
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=apptennispro.database.windows.net;DATABASE=tennispro_dev;UID=tennispro@apptennispro;PWD=Deploy@202103") # For Linux
# params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=tennissport.database.windows.net;DATABASE=tennissport;UID=borakay;PWD=Seasonalsport@202110") # For Linux

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'

api = Api(app)

from db import db
db.init_app(app) 

# app.config['MAIL_SERVER']='hippo.o2switch.net'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'tennispro.boulogne@tennisapp.fr'
# app.config['MAIL_PASSWORD'] = 'Tunepeuxpasetreserieux'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

app.config['MAIL_SERVER']='ssl0.ovh.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tennispro@borakaydata.fr'
app.config['MAIL_PASSWORD'] = 'Tennismatch@202204'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


# app.config['SECRET_KEY'] = 'top-secret!'
# app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'apikey'
# app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
# app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
# mail = Mail(app)

# app.config['MAIL_SERVER']='ssl0.ovh.net'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'tennispro.boulogne@tennismatch.app'
# app.config['MAIL_PASSWORD'] = 'Tennismatch@202204'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True

from mail import mail
mail.init_app(app)

#Filter
api.add_resource(RacketTestingFilter,'/api/V1/RacketTestingFilter')
api.add_resource(RacketMasterFilter,'/api/V1/RacketMasterFilter')
# api.add_resource(RacketTestingList,'/api/V1/RacketTestingList')

#Customer Side Web Application API
api.add_resource(AllShopList, '/api/V1/AllShopList')
api.add_resource(GetShop, '/api/V1/GetShop')
# api.add_resource(AllTestRacketForShop,'/api/V1/AllTestingRacketList')
# api.add_resource(CustomerLogin,'/api/V1/CustomerLogin')
api.add_resource(GetShopWiseCustomerContract,'/api/V1/GetShopWiseCustomerContract')
api.add_resource(GetCustomerContracts,'/api/V1/GetCustomerContracts')
api.add_resource(CustomerOrder,'/api/V1/CustomerOrder')
api.add_resource(CustomerInfo,'/api/V1/CustomerInfo')
api.add_resource(CustomerRegisterFromAdmin,'/api/V1/CustomerRegisterFromAdmin')
api.add_resource(Racket_Marks,'/api/V1/Racket_Marks')
api.add_resource(Racket_Marks_Info,'/api/V1/Racket_Marks_Info')
api.add_resource(QuestionBeenAsk,'/api/V1/QuestionBeenAsk')
api.add_resource(CheckCountCustomerBookedRacket,'/api/V1/CheckCountCustomerBookedRacket')
# api.add_resource(Racket_Marks_Client,'/api/V1/Racket_Marks_Client')

#Admin Side Web Application API
api.add_resource(StringerRegister, '/api/V1/StringerRegister')
# api.add_resource(StringerLogin, '/api/V1/StringerLogin')
# api.add_resource(CheckQRCode, '/api/V1/CheckQRCode')
api.add_resource(CheckQRCodeDecrypted, '/api/V1/CheckQRCodeDecrypted')
api.add_resource(RacketDetail,'/api/V1/RacketDetail')
api.add_resource(GetRacketDetailAsPerUniqueValues,'/api/V1/GetRacketDetailAsPerUniqueValues')
# api.add_resource(RoleDetail,'/api/V1/RoleDetail')
api.add_resource(RacketStatusMaster,'/api/V1/racketstatuslist')
api.add_resource(SleeveSizeList,'/api/V1/SleeveSizeList')
api.add_resource(ReturnRacketToShop,'/api/V1/ReturnRacketToShop') # Return racket to shop at that time order status will be 9 if no need to repaire else order status is 10 racket need to repaired
api.add_resource(HandOverRacketByScanningQRCode,'/api/V1/HandOverRacketByScanningQRCode') # Give racket to customer at that time order status will be 8
api.add_resource(ShopHoliday,'/api/V1/shopholidaylist')
api.add_resource(ShopTimingList,'/api/V1/shoptiminglist')
api.add_resource(ContractDetail,'/api/V1/ContractDetail')
api.add_resource(StringerList,'/api/V1/StringerList')
api.add_resource(Dashboard,'/api/V1/Dashboard')
api.add_resource(RacketOrderHistory,'/api/V1/RacketOrderHistory')
api.add_resource(AssingNewQRCode,'/api/V1/AssingNewQRCode')
# api.add_resource(AssingNewQRCodeToExistingRacket,'/api/V1/AssingNewQRCodeToExistingRacket')
# api.add_resource(CustomerList,'/api/V1/CustomerList')
api.add_resource(CustomerListV2,'/api/V2/CustomerList')
api.add_resource(CustomerHistoricOrder,'/api/V1/CustomerHistoricOrder')
api.add_resource(RacketDataBySuperAdmin,'/api/V1/RacketManipulationBySuperAdmin')
api.add_resource(GetRacketDataBySuperAdmin,'/api/V1/GetRacketDataBySuperAdmin')
api.add_resource(ReturnRacketViaQrCode,'/api/V1/ReturnRacketViaQrCode')
api.add_resource(CheckQRCodeMessage,'/api/V1/CheckQRCodeMessage')
api.add_resource(OrderStatusInArray,'/api/V1/OrderStatusInArray')
api.add_resource(ContractCustomerDetail,'/api/V1/ContractCustomerDetail')
api.add_resource(RacketStatus,'/api/V1/RacketStatus')
api.add_resource(CheckCustomer,'/api/V1/CheckCustomer')
api.add_resource(CheckContractNb,'/api/V1/CheckContractNb')
api.add_resource(CheckContractActiveNb,'/api/V1/CheckContractActiveNb')
api.add_resource(CustomerCancelAuto,'/api/V1/CancelAutoInfo')


#Password Customer
api.add_resource(CustomerPasswordUpdate,'/api/V1/CustomerPasswordUpdate')
# api.add_resource(UpdatePasswordResource,'/api/V1/UpdatePassword')
# api.add_resource(ForgotPassword,'/api/V1/ForgotPassword')#use sendgrid
api.add_resource(GetDataForForgotPassword,'/api/V1/GetDataForForgotPassword')
#Password Stringer
# api.add_resource(CreatePasswordResource,'/api/V1/CreatePassword')
# api.add_resource(UpdatePasswordStringerResource,'/api/V1/UpdatePasswordStringer')
api.add_resource(StringerPasswordUpdate,'/api/V1/StringerPasswordUpdate')
api.add_resource(GetDataForForgotPasswordStringer,'/api/V1/GetDataForForgotPasswordStringer')

# api.add_resource(ForgotPasswordStringer,'/api/V1/ForgotPasswordStringer')#use sendgrid

#Common
api.add_resource(CustomerDetail,'/api/V1/CustomerDetail')
# api.add_resource(BookedCalendarDates,'/api/V1/BookedCalendarDates')
# api.add_resource(CustomerBookedRacketCount,'/api/V1/CustomerBookedRacketCount')
api.add_resource(PlaceOrder,'/api/V1/PlaceOrder') #Booking From Website using customer website so status is 7
api.add_resource(CommanLogin,'/api/V1/CommanLogin')
api.add_resource(RacketFilterAccordingToSelection,'/api/V1/RacketFilterAccordingToSelection')#currently used by admin side
api.add_resource(CountryList,'/api/V1/CountryList')
# api.add_resource(ClubList,'/api/V1/ClubList')
api.add_resource(CancelOrder,'/api/V1/CancelOrder')

#API for Schedular
api.add_resource(AutoCancleCustomerOrder,'/api/V1/AutoCancleCustomerOrder')
api.add_resource(AutoCancelCustomerContract,'/api/V1/AutoCancelCustomerContract')
api.add_resource(ReminderSendViaSendgrid,'/api/V1/ReminderSendViaSendgrid')
api.add_resource(ReminderSendgridReturn,'/api/V1/ReminderSendgridReturn')

#Common V2
# api.add_resource(RacketFilterAccordingToSelection_V2,'/api/V2/RacketFilterAccordingToSelection') #currently used by customer side
api.add_resource(BookedCalendarDates_V2,'/api/V2/BookedCalendarDates')


if __name__ == '__main__':

     app.run(port=5000, debug=True)