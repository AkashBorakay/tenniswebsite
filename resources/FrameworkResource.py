import re
from unicodedata import name
from flask import render_template
from flask.globals import request
from flask_mail import Message
from mail import mail
from models.ShopMasterModel import ShopMasterModel
from mimetypes import MimeTypes
import requests


def Authorization(ShopID,TokenId):
        verified = ShopMasterModel.Auth(ShopID,TokenId)
        return verified

def IsAuthenticate(request):
    ShopID = request.headers['ShopID']
    TokenId = request.headers['Authorization']
    return Authorization(ShopID,TokenId)

    
def send_mail_by_html_template_client(to,subject,template,**kwargs):
    msg = Message(subject=subject,sender='noshop@borakaydata.fr', recipients=[to],bcc=['sybille.darbin@borakay.fr'],reply_to='Akash Patel <app.tennispro@gmail.com>') 
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
    
    
def send_mail_by_html_template(to,subject,template,**kwargs):
    if kwargs["ShopID"] == "1":
        msg = Message(subject=subject,sender='tennispro_boulogne@borakaydata.fr', recipients=[to],bcc=['kapil.kori@borakay.fr'],reply_to='Akash Patel <app.tennispro@gmail.com>') # add this when live app storeemail@tennisapp.fr
    elif kwargs["ShopID"] == "2":
        msg = Message(subject=subject,sender='tennispro_bois-colombes@borakaydata.fr', recipients=[to],bcc=['kapil.kori@borakay.fr'],reply_to='Akash Patel <app.tennispro@gmail.com>') 
    elif kwargs["ShopID"] == None:
        msg = Message(subject=subject,sender='noshop@borakaydata.fr', recipients=[to],bcc=['kapil.kori@borakay.fr'],reply_to='Akash Patel <app.tennispro@gmail.com>') 
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
    
def send_mail_by_text_template(to,subject,template,**kwargs):
    msg = Message(subject=subject,sender='tennispro@borakaydata.fr', recipients=[to])
    msg.body = render_template(template, **kwargs)
    mail.send(msg)
