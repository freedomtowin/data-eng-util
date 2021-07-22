import numpy as np
import datetime 
import time
import gc

from custom_db_connection import CONNECTION_CLASS
from custom_table_handler import TABLE_CLASS

parser = argparse.ArgumentParser(description="",epilog="")
parser.add_argument('--inp_date',type=str,default='20201201',help='')
parser.add_argument('--out_date',type=str,default='20201202',help='')
parser.add_argument('--period',type=int,default=1,help='')
parser.add_argument('--stg_days',type=int,default=0',help='')
parser.add_argument('--db_username',type=str,default='',help='')
parser.add_argument('--db_password_location',type=str,default='C:/Users/Rohan/temp.txt',help='')
args=parser.parse_args()


inp_date = parser.inp_date
out_date = parser.out_date
period = parser.period
stg_days = parser.stg_days

date_diff =  datetime.datetime.strptime(out_date,'%Y%m%d')-datetime.datetime.strptime(inp_date,'%Y%m%d')
periods = [10 for _ in range(date_diff.days//period)

if date_diff.days%period>0:
    periods = periods+[date_diff.days%period]


db = CONNECTION_CLASS(db_username='',db_password='')    
table_class = TABLE_CLASS()


for num_days in periods:

    window_list = table_class.get_window_list(start_time = datetime.datetime(inp_date,'%Y%m%d'),
                                  end_time = datetime.datetime(inp_date,'%Y%m%d')+datetime.timedelta(days=num_days)
                                  )
       
    for dttm in window_list:
        
        end_dttm = dttm+datetime.timedelta(days=1)
        stg_dttm = dttm-datetime.timedelta(days=stg_days)
        
        table_name='stage_table'
        date_col='date'
        table_class.daily_insert(db, table_name, date_col, stg_dttm, end_dttm)
        
        table_name='agg_table'
        date_col='date'
        table_class.daily_insert(db, table_name, date_col, dttm, end_dttm)
    
