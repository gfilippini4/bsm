import MySQLdb as my
import sys

def main(conn):
	bool = True
	cursor = conn.cursor()
	while(bool):
		try:
			sql = input('give me something to execute: ')
			if 'quit' == sql:
				conn.close()
				sys.exit()
			print(cursor.execute(sql))
			conn.commit()
			if 'show' in sql:
				var = cursor.fetchall()
				for i in var:
					print(i[0])
			if 'select' in sql:
				var = cursor.fetchall()
				for i in var:
					print(i)
			print('\n')
		except Exception as e:
			print(e)
			main(conn)
		
def prepared_statement(arr):
	conn = my.connect(host='35.225.44.78', user='app', passwd='')
	cursor = conn.cursor()
	sql = """insert into work.adv (name, nickname, salary, position, age, location) 
		values (%s, %s, %s, %s, %s, %s)"""

	insert_tuple = (arr[0], arr[1], int(arr[2]), arr[3], int(arr[4]), arr[5]) 
	cursor.execute(sql,insert_tuple)
	conn.commit()
	conn.close()
	
def prepared_query(sql):
	if ('insert' in sql or 'delete' in sql or 'update' in sql[0:6]):
		return 'No updating the database in this module.'
	conn = my.connect(host='localhost', user='app', passwd='')
	cursor = conn.cursor()
	try:
		cursor.execute(sql)
		return cursor.fetchall()
	except Exception as e:
		return e
		
def tupleBreaker(tuple):
	info = ''
	for tuples in tuple:
		for items in tuples:
			info += str(items) + ' '
		info += '\n'
	return info
		
def tupleToDict(tuple):
	count = 0
	dict = {
		'id' : '',
		'name' : '',
		'age' : '',
		'bio' : '',
		'motto' : '',
		'password' : '',
		'email_address' : '',
		'session' : ''
		
	}
	for tuples in tuple:
		for items in tuples:
			info = ''
			info += str(items)
			if count == 0:
				dict['id'] = info
			elif count == 1:
				dict['name'] = info
			elif count == 2:
				dict['age'] = info
			elif count == 3:
				dict['bio'] = info
			elif count == 4:
				dict['motto'] = info
			elif count == 5:
				dict['email_address'] = info
			elif count == 6:
				dict['password'] = info
			else: 
				dict['session'] = info
			count += 1
	return dict

def filter(keyword):
	sql = 'select %s from work.adv' % keyword
	conn = my.connect(host='35.225.44.78', user='app', passwd='')
	cursor = conn.cursor()
	cursor.execute(sql)
	return cursor.fetchall()
	conn.commit()
	conn.close()
	
if __name__ == '__main__':
	conn = my.connect(host='35.225.44.78', user='app', passwd='')
	print(conn)
	main(conn)