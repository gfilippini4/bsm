from sqltest import tupleBreaker, tupleToDict
import MySQLdb as my
import os
from werkzeug.utils import secure_filename


def authLogin(form):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute('select count(*) from work.profile where email_address=\'%s\' and password=sha1(\'%s\')' %
                   (form['email_address'], form['password']))
    var = tupleBreaker(cursor.fetchall())
    if int(var) == 1:
        return True
    else:
        return False


def newUser(form):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute("select count(*) from work.profile where email_address=\'%s\'" %
                   (form['email_address']))
    num = tupleBreaker(cursor.fetchall())
    if int(num) == 0:
        if form['password'] == form['cpassword']:
            cursor.execute(
                'insert into work.adv (name, nickname, salary, position, age, location) values (\'%s\', \'no nick\', 0, \'no position\', 0, \'no location\')' % (form['name']))
            cursor.execute(
                'select id from work.adv where name = \'%s\'' % form['name'])
            var = cursor.fetchall()
            id = tupleBreaker(var)
            cursor.execute('insert into work.profile values (%s, \'%s\', 0, \'insert bio\', \'insert motto\', \'%s\', sha1(\'%s\'))' % (
                str(id), form['name'], form['email_address'], form['password']))
            conn.commit()
            conn.close()
            id = getData(form['email_address'])['id']
            path = os.getcwd() + '\\static\\profiles\\' + str(id)
            os.mkdir(path)
            return True
    conn.close()
    return False


def setCookie(session, email_address):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    sql = """ update work.profile set session=\'%s\' where email_address=\'%s\'""" % (
        session, email_address)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def checkSession(session, email_address):
	conn = my.connect(host='35.225.44.78', user='app', passwd='')
	cursor = conn.cursor()
	cursor.execute(
	'select * from work.profile where email_address = \'%s\'' % email_address)
	data = tupleToDict(cursor.fetchall())
	print(data['session'] == session)
	return data['session'] == session
    # data['friends'] = getFriendsOf(data['id'])
    # data['posts'] = getPosts(data['id'])
    # conn.close()

def getData(email_address):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute(
        'select * from work.profile where email_address = \'%s\'' % email_address)
    data = tupleToDict(cursor.fetchall())
    print(data['id'])
    data['friends'] = getFriendsOf(data['id'])
    data['posts'] = getPosts(data['id'])
    conn.close()
    return data


def getPosts(id):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute('use work')
    cursor.execute("""select poster_id, name as poster_name, 
	date_posted, content from profile as pro join posts as p 
	where poster_id=id and profile_id=%s 
	order by date_posted desc;""" % id)
    data = cursor.fetchall()
    conn.close()
    return data


def updateInfo(form, files, id):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    for key in form:
        if form[key] != '':
            if key == 'name':
                if "'" not in form[key]:
                    cursor.execute("SET FOREIGN_KEY_CHECKS=0")
                    cursor.execute(
                        "update work.adv set name=\'%s\' where id=%s" % (form[key], id))
                    cursor.execute(
                        "update work.profile set name=\'%s\' where id=%s" % (form[key], id))
                    cursor.execute("SET FOREIGN_KEY_CHECKS=1")
                # Edge case, return the edit page with an alert
            else:
                if key == 'age':
                    cursor.execute(
                        "update work.profile set %s=%s where id=%s" % (key, form[key], id))
                else:
                    cursor.execute(
                        "update work.profile set %s=\"%s\" where id=%s" % (key, form[key], id))
    try:
        file = files['pro_pic']
        if 'png' in file.filename or 'jpg' in file.filename:
            filename = str(id) + '_profile_pic.png'
            dir_path = os.getcwd()
            path = dir_path + '\\static\\profiles\\' + str(id) + '\\'
            file.save(os.path.join(path, filename))
    except Exception as e:
        print(e)
    conn.commit()
    conn.close()


def getFriendsOf(id):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute('use work')
    sql = """select profile.id, profile.name, profile.email_address from profile 
		where id in (select receiver_id from friends where initiator_id= %s) 
		or id in (select initiator_id from friends where receiver_id= %s);
		""" % (str(id), str(id))
    cursor.execute(sql)
    data = cursor.fetchall()
    friends = []
    for item in data:
        friends.append(
            {'id': item[0], 'name': item[1], 'email_address': item[2]})
    return friends


def posting(form):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute('use work')
    sql = """insert into posts values(%s, %s, sysdate(), \"%s\")
	""" % (str(form['poster_id']), str(form['poster_id']), form['content'])
    cursor.execute(sql)
    conn.commit()
    conn.close()


def postingFriend(profile, poster, content):
    profile_id = getData(profile)['id']
    poster_id = getData(poster)['id']
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute('use work')
    sql = """insert into posts values(%s, %s, sysdate(), \"%s\")
	""" % (str(profile_id), str(poster_id), content)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def main():
    getFriendsOf(1)


if __name__ == '__main__':
    main()
