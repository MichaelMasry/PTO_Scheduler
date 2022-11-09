import json
import pymysql as pymysql
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS


def sendToDB(ownerID, ownerName, ptolist):
    connection_l = pymysql.connect(host='localhost', user='root', password='', db='ptodb')
    myCursor_l = connection_l.cursor()
    print("Ready To pass value to DB")
    check_string = "INSERT INTO pto_record (ownerID, ownerName, ptolist) VALUES (%s, %s, %s)"
    val = (ownerID, ownerName, json.dumps(ptolist))
    print("Sending Request as follows: " + check_string)
    myCursor_l.execute(check_string, val)
    connection_l.commit()
    connection_l.close()
    # my_table_l = myCursor_l.fetchall()
    # print(my_table_l)
    # if len(my_table_l) == 0:
    #     print("No Record for this Email Please Register")
    #     return 0
    # else:
    #     real_pass = my_table_l[0][4]
    #     print("Real Pass is: " + real_pass)
    #     print("Entered Pass is: " + password)
    #     if real_pass == password:
    #         print("LOGIN IS SUCCESSFUL!")
    #         # global user
    #         # global user_name
    #         # global nt_name
    #         # global isMod
    #         # nt_name = my_table[0][3]
    #         # user_name = my_table[0][1]
    #         # isMod = my_table[0][5]
    #         # user = User(ident=my_table[0][0], n_t=my_table[0][3], first=my_table[0][1],
    #         #             last=my_table[0][2], is_mod=my_table[0][5])
    #         # print(user)
    #         # login_window.withdraw()
    #         # need to send ID and name
    #         user_id = my_table_l[0][0]
    #         connection_l.commit()
    #         connection_l.close()
    #         return user_id
    #     else:
    #         print("CREDENTIALS ARE WRONG!!!")
    #         return 500


def login_db(user, password):
    connection_l = pymysql.connect(host='localhost', user='root', password='', db='ptodb')
    myCursor_l = connection_l.cursor()
    print("Ready To login")
    check_string = "SELECT * FROM userlogin WHERE nt_name='" + user + "';"
    print("Sending Request as follows: " + check_string)
    myCursor_l.execute(check_string)
    my_table_l = myCursor_l.fetchall()
    print(my_table_l)
    isMod = 0
    if len(my_table_l) == 0:
        print("No Record for this Email Please Register")
        connection_l.close()
        return 0, isMod
    else:
        real_pass = my_table_l[0][2]
        print("Real Pass is: " + real_pass)
        print("Entered Pass is: " + password)
        if real_pass == password:
            print("LOGIN IS SUCCESSFUL!")
            # global user
            # global user_name
            # global nt_name
            # global isMod
            # nt_name = my_table[0][3]
            # user_name = my_table[0][1]
            # isMod = my_table[0][5]
            # user = User(ident=my_table[0][0], n_t=my_table[0][3], first=my_table[0][1],
            #             last=my_table[0][2], is_mod=my_table[0][5])
            # print(user)
            # login_window.withdraw()
            # need to send ID and name
            user_id = my_table_l[0][0]
            isMod = my_table_l[0][3]
            connection_l.commit()
            connection_l.close()
            return user_id, isMod
        else:
            print("CREDENTIALS ARE WRONG!!!")
            connection_l.close()
            return 500, isMod


def fetch_all_data():
    connection_l = pymysql.connect(host='localhost', user='root', password='', db='ptodb')
    myCursor_l = connection_l.cursor()
    print("Ready To pass value to DB")
    check_string = "SELECT * FROM pto_record"
    print("Sending Request as follows: " + check_string)
    myCursor_l.execute(check_string)
    myTable = myCursor_l.fetchall()
    print(myTable)
    connection_l.commit()
    connection_l.close()


connection = pymysql.connect(host='localhost', user='root', password='', db='ptodb')
myCursor = connection.cursor()
print("CONNECTED")
connection.close()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
CORS(app)
# cors = CORS(app, resources={r'/savelist': {'origins': '*'}})


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/savelist', methods=['POST'])
def post_list():
    payload = request.json
    print(payload)
    # wjdata = payload['value']
    # print(wjdata)
    # print(wjdata['ownerID'])
    # print(wjdata['name'])
    # print(wjdata['pto'])
    sendToDB(payload['ownerID'], payload['name'], payload['pto'])
    return jsonify({'status': "OK"})


@app.route('/getAll', methods=['GET'])
def get_list():
    fetch_all_data()
    return jsonify({'name': 'michael'})


@app.route('/login', methods=['POST'])
def login():
    print("Request reached Server")
    # print(request.form)
    # print(request.get_json())
    payload = request.json
    print(type(payload))
    user = payload['name']
    password = payload['password']
    print(user)
    print(password)
    # result shall be 0:table is empty, 500:wrong creds, any other integer: id of user
    result_integer, isMod = login_db(user, password)
    print(result_integer)
    if result_integer == 0:
        result_integer = "TABLE IS EMPTY"
    elif result_integer == 500:
        result_integer = "WRONG CREDS"
    return jsonify({'status_': result_integer, 'isMod': isMod})
    # return jsonify({'status': "OK"})


if __name__ == '__main__':
    print("Starting . . . ")
    app.run(host='localhost', port=8080, debug=True)
