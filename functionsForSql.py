from sqltest import tupleBreaker, tupleToDict
import MySQLdb as my
import os
from werkzeug.utils import secure_filename
from google.cloud import storage


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
            cursor.execute('insert into work.profile values (%s, \'%s\', 0, \'insert bio\', \'insert motto\', \'%s\', sha1(\'%s\'), \'No Session\')' % (
                str(id), form['name'], form['email_address'], form['password']))
            conn.commit()
            conn.close()
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
            else:
                if key == 'age':
                    cursor.execute(
                        "update work.profile set %s=%s where id=%s" % (key, form[key], id))
                elif key == 'password':
                    # try:
                    #     if 
                    pass
                elif key != 'password'and key != 'new_password' and key != 'new_password_confirm':
                    cursor.execute(
                        "update work.profile set %s=\"%s\" where id=%s" % (key, form[key], id))
    conn.commit()
    conn.close()
    try:
        photo = files['pro_pic']
        name = photo.filename.lower()
        print(name)
        if 'png' in name or 'jpg' in name or 'jpeg' in name:
            sc = storage.Client()
            bucket = sc.get_bucket('basic-flask-bucket')
            blob = bucket.blob('profiles/' + id + '/' +
                               id + '_profile_pic.png')
            blob.upload_from_file(photo)
    except Exception as e:
        print(e)


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


def queryInput(input):
    conn = my.connect(host='35.225.44.78', user='app', passwd='')
    cursor = conn.cursor()
    cursor.execute('use work')
    sql = 'select id, name, email_address from profile where name like \'%%%s%%\' or soundex(\'%s\') = soundex(name) limit 10' % (
        input, input)
    cursor.execute(sql)
    data = cursor.fetchall()
    resp = []
    for person in data:
        arr = {}
        count = 0
        for val in person:
            if count == 0:
                arr['id'] = val
            if count == 1:
                arr['name'] = val
            if count == 2:
                arr['email_address'] = val
            count += 1
        resp.append(arr)
    conn.close()
    return resp


def main():
    getFriendsOf(1)


if __name__ == '__main__':
    main()
