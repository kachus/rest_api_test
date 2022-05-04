import sqlite3
import  uuid
import json

def create_db_cars():
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    sql ='''CREATE TABLE IF NOT EXISTS CARS(
        ID STRING NOT NULL,
        CAR_MODEL STRING,
        PRICE FLOAT,
        AMOUNT INT,
        DEALER STRING)'''
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def insert_values_cars(json_cars):
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    for item in json_cars:
        query = '''INSERT INTO CARS(ID, CAR_MODEL, PRICE, AMOUNT, DEALER) VALUES ('{car_id}', '{car_name}', '{price}', {amount}, '{dealer}')'''
        string = query.format(car_id = item['car_id'], car_name = item['car_name'], price = item['price'], amount =  item['amount'], dealer = item['dealer'])
        cursor.execute(string)

    #conn.commit() # to commit changes
    #cursor.execute('''SELECT * FROM CARS''')
    #print(cursor.fetchall())  to check whether the values were inserted
    cursor.close()




def create_table_orders():
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS ORDERS (
            ORDER_ID STRING NOT NULL,
            NAME STRING,
            SECOND_NAME STRING, 
            CAR_ID STRING
                )'''
    cursor.execute(sql)
    conn.commit()
    cursor.close()
def insert_values_orders(json_orders):
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    for item in json_orders:
        new_order_id = str(uuid.uuid1())
        query = '''INSERT INTO ORDERS( ORDER_ID, NAME, SECOND_NAME , CAR_ID) VALUES ('{order_id}', '{name}', '{second_name}', {car_id})'''
        string = query.format( order_id = new_order_id, name = item['name'], second_name = item['second_name'], car_id =  int(item['car_id']))
        cursor.execute(string)
    conn.commit()

    cursor.close()
    return new_order_id





def create_db_dealers():
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    sql ='''CREATE TABLE IF NOT EXISTS DEALERS(
        DEALER STRING,
        DEALER_INFO STRING)
        '''
    cursor.execute(sql)
    conn.commit()
    cursor.close()
def insert_values_dealers(json_dealer):
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    sql = '''INSERT INTO DEALERS(DEALER, DEALER_INFO) VALUES ('{dealer}', '{dealer_info}')'''
    for item in json_dealer:
        string = sql.format(dealer = item['dealer_name'], dealer_info = item['dealer_info'])
        cursor.execute(string)

    #conn.commit()
    cursor.close()


def update_db_cars(car_id):
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    sql = '''UPDATE CARS SET AMOUNT = AMOUNT - 1 WHERE ID = '{car_id}' '''
    cursor.execute(sql.format(car_id = car_id))

    conn.commit()

    cursor.close()


def get_car_id(order_id):
    conn = sqlite3.connect('Cars.db')
    cursor = conn.cursor()
    sql = '''SELECT CAR_ID FROM ORDERS WHERE ORDER_ID = '{order_id}' '''
    query = sql.format(order_id = order_id)
    cursor.execute(query)
    data = cursor.fetchall()
    car_id = data[0][0]
    return car_id

def delete_order(order_id):
    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    sql = '''DELETE FROM ORDERS WHERE ORDER_ID = '{order_id}' '''
    query = sql.format(order_id = order_id)
    cursor.execute(query)
    car_id = get_car_id(order_id)
    sql = '''UPDATE CARS SET AMOUNT = AMOUNT + 1 WHERE ID = '{car_id}' '''
    cursor.execute(sql.format(car_id = car_id))
    conn.commit()
    cursor.close()
'''''
orders = [{'user_name': 'Zhenya', 'user_secondname':'Kach', 'car_id':678}]

dealers =[ {'dealer_name': 'dealer1', 'dealer_info' : 'dealer1 info'},{'dealer_name': 'dealer2', 'dealer_info' : 'dealer2 info'}, {'dealer_name': 'dealer3', 'dealer_info' : 'dealer3 info'}]

cars = [{'car_id':678, 'car_name':'Kia_Rio', 'price' : 700000, 'amount' : 9, 'dealer' : 'dealer1'},

        {'car_id':978,'car_name':'Ford Focus', 'price' : 800000, 'amount' : 5, 'dealer' : 'dealer2'},
        {'car_id':768,'car_name':'Toyota Corolla', 'price' : 750000, 'amount' : 2, 'dealer' : 'dealer3'},
        {'car_id': 568,'car_name':'Honda Civik', 'price' : 890000, 'amount' : 0, 'dealer' : 'dealer1'},
        {'car_id': 858,'car_name':'Kia Rio', 'price' : 900000, 'amount': 3, 'dealer' : 'dealer1'},
        {'car_id': 677,'car_name':'Nissan Almera ', 'price' : 750000, 'amount': 1, 'dealer' : 'dealer2'}
        ]
        
'''''

