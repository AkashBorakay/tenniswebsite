from sqlalchemy import true
from re import template
from models.ShopTimingMasterModel import ShopTimingMasterModel
from models.StringerMasterModel_V2 import StringerMasterModel
from models.ShopMasterModel import ShopMasterModel
from resources.FrameworkResource import send_mail_by_html_template, send_mail_by_html_template_client
from models.FrameworkModel import commit, pagination,getUTCTime
import locale
from models.WebsiteCustomerModel import CustomerDetailModel

import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

class OrderMasterService():
    @classmethod
    def EmailForPasswordCreationForCustomer(cls, CustomerID, Fname, Lname, ClientEmailAddress):
        kwargs = {}
        kwargs['name'] = Fname +' '+ Lname
        kwargs["Createpassword"] = os.environ.get('AzureAppServiceURL_Websiste') + "/api/V1/CreatePassword?CustomerID=" + str(CustomerID)
        (template) = OrderMasterService.GetEmailTemplateForPasswordCreateNotification()
        subject = 'Créez votre mot de passe'
        send_mail_by_html_template_client(ClientEmailAddress, subject, template, **kwargs)
       
    @classmethod
    def EmailForPasswordCreationForStringer(cls, StringerID,Fname,Lname,StringerEmailAddress,ShopID):
        kwargs = {}
        kwargs['ShopID'] = ShopID
        kwargs['name'] = Fname +' '+ Lname
        kwargs["Createpassword"] =  os.environ.get('AzureAppServiceURL_Websiste') + "/api/V1/CreatePassword?StringerID=" + str(StringerID) + "&" + "ShopID=" + str(ShopID)
        (template) = OrderMasterService.GetEmailTemplateForPasswordCreateNotification()
        subject = 'Créez votre mot de passe'
        send_mail_by_html_template(StringerEmailAddress, subject, template, **kwargs)
    def GetEmailTemplateForPasswordCreateNotification():
        return "Create_Password.html"
    
    
    @classmethod
    def EmailForForgotPassword(cls,CustomerName,CustomerEmail,CustomerID):
        kwargs = {}
        kwargs['CustomerName'] = CustomerName
        kwargs["Resetpassword"] = os.environ.get('AzureAppServiceURL_Websiste') + "/api/V1/UpdatePassword?CustomerID=" + str(CustomerID)
        template = 'Forgot_Password_Email.html'
        subject = 'Réinitialisez votre mot de passe'
        send_mail_by_html_template_client(CustomerEmail, subject, template, **kwargs)
        
    @classmethod
    def EmailForForgotPasswordStringer(cls, Name, Email, StringerID, ShopID):
        kwargs = {}
        kwargs['ShopID'] = ShopID
        kwargs['Name'] = Name
        kwargs["Resetpassword"] = os.environ.get('AzureAppServiceURL_Websiste') + "/api/V1/UpdatePassword?StringerID=" + str(StringerID)
        template = 'Forgot_Password_Email.html'
        subject = 'Réinitialisez votre mot de passe'
        send_mail_by_html_template(Email, subject, template, **kwargs)
        
    @classmethod
    def EmailForAutoCancelOrder(cls, CustomerName,CustomerEmailID,RacketName,BookedDate,ShopDetail):
        kwargs = {}
        kwargs['name'] = CustomerName
        kwargs["RacketName"] = RacketName
        kwargs["BookedDate"] = BookedDate
        kwargs["ShopName"] = ShopDetail.shopname
        kwargs["ShopAddress"] = ShopDetail.ShopAddress
        kwargs["ShopLogo"] = ShopDetail.ShopLogo
        kwargs["ShopID"] = str(ShopDetail.id)
        (template) = OrderMasterService.GetEmailTemplateForAutoCancelOrderNotification()
        subject = 'Votre commande est automatiquement annulée'
        send_mail_by_html_template(CustomerEmailID, subject, template, **kwargs)
        
    def GetEmailTemplateForAutoCancelOrderNotification():
        return "Auto_Cancel_Order.html"
    
    # sendgrid reminder
    @classmethod
    def SendReminder(cls, Subject, CustomerName, CustomerEmailID, OrderID, RacketName, PictureRacket, ShopAddress, ShopName, SleeveSize, BookedDate, ReturnDate):
        # from address we pass to our Mail object, edit with your name
        FROM_EMAIL = 'sybille.darbin@tennisapp.io'
        # update to your dynamic template id from the UI
        TEMPLATE_ID = 'd-0e2a9115f133417085b38ba9d115713b'
        # list of emails and preheader names, update with yours
        TO_EMAILS = [(CustomerEmailID, CustomerName)]
        
        # create Mail object and populate
        message = Mail(
            from_email = FROM_EMAIL,
            to_emails = TO_EMAILS)
        # pass custom values for our HTML placeholders
        message.dynamic_template_data = {
            'subject': Subject,
            'Racket': RacketName,
            'OrderID': OrderID,
            'PictureRacket': PictureRacket,
            'StartDate': BookedDate,
            'EndDate': ReturnDate,
            'ShopAdress': ShopAddress,
            'ShopName': ShopName,
            'SleeveSize': SleeveSize
            }
        message.template_id = TEMPLATE_ID
        # create our sendgrid client object, pass it our key, then send and return our response objects
        try:
            sg = SendGridAPIClient(os.environ.get('SendGridAPIKey_website'))
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            print(f"Response code: {code}")
            print(f"Response headers: {headers}")
            print(f"Response body: {body}")
            print("Dynamic Messages Sent!")
        except Exception as e:
            print("Error: {0}".format(e))
        return str(response.status_code)

