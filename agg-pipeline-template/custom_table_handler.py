import datetime
import os
import time

class TABLE_CLASS():

    def __init__(self):
        pass
        
        
    def get_window_list(self, start_time, end_time):

        dates = []
        window=1
        cur_time = start_time
        buffer_time = cur_time+datetime.timedelta(days=1)
        
        while buffer_time<end_time:
            dates.append(cur_time)
            cur_time=buffer_time
            buffer_time = buffer_time+datetime.timedelta(days=1)

        return dates
        
    def current_date_list(self, db, table_name, date_col):
        result = db.cur.execute('select distinct trunc({0}) from {1}'.format(date_col, table_name)).fetchall()
        return list(map(lambda x: x[0], result))
        
    def drop(self, db, table_name):
        prefix=['drop_queries']
        table_name=table_name+'.sql'
        file_path=os.path.join(*prefix,table_name)
        qry = open(file_path).read()
        db.execute(qry)
        
    def insert_by_date(self, db, table_name,begin_dttm):
        prefix=['insert_queries']
        table_name=table_name+'.sql'
        file_path=os.path.join(*prefix,table_name)
        
        begin_date = datetime.datetime.strftime(begin_dttm,'%Y%m%d')
        end_date = datetime.datetime.strftime(begin_dttm+datetime.timedelta(days=1),'%Y%m%d')
        
        qry = open(file_path).read()
        db.execute(qry,(begin_date,end_date))
        
    def daily_insert(self, db, table_name, date_col, start_dttm, end_dttm,drop=False):
        
        if drop==True:
            self.drop(db,table_name)
            
        window_stack = self.get_window_date_list(start_dttm,end_dttm)
        current_stack = sorted(current_date_list(db,table_name,date_col))
        pull_stack = sorted(list(filter(lambda x: x not in current_stack, window_stack)))
        
        for date in pull_stack:
        
            self.insert_by_date(db,table_name,date)
            
    def truncate_between(self,db, file_name, date_col, begin_dttm, end_dttm):
        #create a temporary table with the date column between begin and end_date
        #drop current table and replace with truncated table
        continue
            