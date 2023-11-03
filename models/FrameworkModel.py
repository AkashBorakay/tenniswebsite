from sqlalchemy.sql.expression import null
from db import db
from datetime import datetime
import pytz

def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        #return self.id

def save_to_db_with_flush(self):
       db.session.add(self)
       db.session.flush()
       return self.id 
       
def commit():
        db.session.commit()

def rollback():
        db.session.rollback()



def update_to_db(self):
        db.session.add(self)
        #db.session.add(self)
        db.session.commit()
        #return self.id

def pagination(query,json_results):
        page_data = {
            'count': query.total,
             'next_page' : query.next_num,
             'total_pages' : query.pages,
             'current_page' : query.page,
             'prev_page' : query.prev_num ,
             'results' :   json_results   

        }
        return page_data

def PaginationForCustomerFilter(query,json_results,SearchParameter,SearchCondition):
        page_data = {
            'count': query.total,
             'next_page' : query.next_num,
             'total_pages' : query.pages,
             'current_page' : query.page,
             'prev_page' : query.prev_num,
             'results' :   json_results,
             'SearchParameter' : SearchParameter,
             'SearchCondition' : SearchCondition
        }
        return page_data


def PaginationForOrderDashboard(query,json_results):
        page_data = {
            'count': query.total,
             'next_page' : query.next_num,
             'total_pages' : query.pages,
             'current_page' : query.page,
             'prev_page' : query.prev_num ,
             'results' :   json_results
        #      'Counter1' : Counter1,
        #      'Counter2': Counter2,
        #      'Counter3': Counter3,
        #      'Counter4': Counter4,
        #      'Counter5' : Counter5
        }
        return page_data   

def PaginationForOrderDashboardWithOutResult(query,json_results,Counter1,Counter2,Counter3,Counter4,Counter5):
        page_data = {
            'count': 0,
             'next_page' : None,
             'total_pages' : 0,
             'current_page' : 1,
             'prev_page' : None,
             'results' :   json_results,
             'Counter1' : Counter1,
             'Counter2': Counter2,
             'Counter3': Counter3,
             'Counter4': Counter4,
             'Counter5' : Counter5
        }
        return page_data             

def getUTCTime():
        utc_dt = datetime.now(tz=pytz.utc)
        amsterdam_tz = pytz.timezone("Europe/Amsterdam")
        local_amsterdam_time = amsterdam_tz.normalize(utc_dt)
        return local_amsterdam_time