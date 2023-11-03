from models.FrameworkModel import pagination
from db import db
from operator import and_, or_
# from models.WebsiteRacketBookingDetailModel import RacketBookingDetailMasterModel
# from models.WebsiteShopTestingRacketModel import ShopTestRacketModel

# from sqlalchemy.sql.expression import desc
    
class CancelMasterView(db.Model):
    __tablename__ = 'tpv_website_list_nb_cancel_auto'
    CustomerContractID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer)
    ShopID = db.Column(db.Integer, db.ForeignKey('tp_shop_master.id'))
    DelContract = db.Column(db.Boolean)
    ContractName = db.Column(db.String(200))
    Fname = db.Column(db.String(50))
    Lname = db.Column(db.String(50))
    NbLate = db.Column(db.Integer)
    CancelDate = db.Column(db.DateTime)
    CustomerSearch = db.Column(db.String(500))

    def json(self):
        return {       
            'CustomerID': self.CustomerID,
            'ShopID': self.ShopID,
            'CustomerContractID':self.CustomerContractID,
            'DelContract':self.DelContract, 
            'ContractName':self.ContractName, 
            'Fname':self.Fname,
            'Lname':self.Lname,
            'NbLate' : self.NbLate,              
            'CancelDate':self.CancelDate and self.CancelDate.strftime('%d/%m/%Y') or None,
            }
                
    @classmethod
    def GetSearchCustomerForDashboard(cls,NameFilter):
        SearchParamter = (NameFilter.replace(" ","")).strip()
        return db.session.query(CancelMasterView).\
            filter(CancelMasterView.CustomerSearch.like('%' + SearchParamter + '%')).all()
            
    def customer_details_cancel(CustomerDetail = None):
        Output={}
        Output['CustomerDetail'] = CustomerDetail.json() if CustomerDetail else None
        return Output
    
    @classmethod
    def GetAllcancel(cls,Page, ShopID, NameFilter):
        if NameFilter is None:
            CustomersList=[]
            CustomerData = None
            CustomersData = db.session.query(CancelMasterView).filter(CancelMasterView.ShopID == ShopID).order_by(CancelMasterView.CancelDate).paginate(page=Page,per_page=20)
            if CustomersData:
                    for CustomerData in CustomersData.items:
                        CustomersList.append(CancelMasterView.customer_details_cancel(CustomerData))
                    CustomersList= pagination(CustomersData,CustomersList)
                    return CustomersList
            else:
                return{"message" : "No customer found"}
        else:
            CustomersList=[]
            CustomerData = None
            CustomerDetail = CancelMasterView.GetSearchCustomerCancel(NameFilter)
            CustomerIDArray=[]
            if CustomerDetail is not None:
                for customerdetail in CustomerDetail:
                    CustomerIDArray.append(customerdetail.id)
            else:
                CustomersList= pagination(0,CustomersList)
                return CustomersList
            CustomersData = db.session.query(CancelMasterView).filter(CancelMasterView.id.in_(CustomerIDArray),  
                                                                         CancelMasterView.ShopID == ShopID).order_by(CancelMasterView.CancelDate).paginate(page=Page,per_page=20)
            if CustomersData:
                    for CustomerData in CustomersData.items:
                        CustomersList.append(CancelMasterView.customer_details_cancel(CustomerData))
                    CustomersList= pagination(CustomersData,CustomersList)
                    return CustomersList
            else:
                return{"message" : "No customer found"}
            
