import time
import cx_Oracle

class OracleConnection():

	def __init__(self, username, password_file):
	
		self.username=username
		self.password_file=password_file
		
		self.create_connection()
		self.qry_cnt=1
		self.start_time=time.time()
		self.end_time=time.time()
		
	def create_connection(self):
	
		password = open(self.password_file).read()
		dns = '******'
		self.connection = cx_Oracle.connect(self.username, password, dns)
		self.cur = self.connection.cursor()
		self.cur.execute('select 1 from dual')
		
	def connect():
		try:
			self.create_connection()
		except cx_Oracle.DatabaseError:
			time.sleep(300)
			self.create_connection()
			
	def disconnect(self):
		try:
			self.connection.close()
		except:
			pass
			
			
	def execute(self, qry, var=()):
	
		if qry_cnt>25 or self.end_time-self.start_time>400:
			self.disconnect()
			self.connect()
			self.start_time = time.time()
			self.end_time = time.time()
			qry_cnt=1
			
		try:
			self.cur.execute(qry,var)
			self.cur.execute('commit')
			self.end_time = time.time()
			gc.collect()
        #can define custom exceptions cx_Oracle.DatabaseError, etc
		except:
			time.sleep(60)
			self.create_connection()
			self.cur.execute(qry,var)
			self.cur.execute('commit')
			gc.collect()
			
		qry_cnt+=1
			