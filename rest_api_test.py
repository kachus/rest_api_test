from flask import Flask, jsonify,request
from flask_restful import Resource, Api, reqparse, abort
import sqlite3
import database as db
app = Flask(__name__)
api = Api(app)

orders = [{'user_name': 'Zhenya', 'user_secondname':'Kach', 'car_id':678}]

dealers =[ {'dealer_name': 'dealer1', 'dealer_info' : 'dealer1 info'},{'dealer_name': 'dealer2', 'dealer_info' : 'dealer2 info'}, {'dealer_name': 'dealer3', 'dealer_info' : 'dealer3 info'}]

cars = [{'car_id':678, 'car_name':'Kia_Rio', 'price' : 700000, 'amount' : 9, 'dealer' : 'dealer1'},

        {'car_id':978,'car_name':'Ford Focus', 'price' : 800000, 'amount' : 5, 'dealer' : 'dealer2'},
        {'car_id':768,'car_name':'Toyota Corolla', 'price' : 750000, 'amount' : 2, 'dealer' : 'dealer3'},
        {'car_id': 568,'car_name':'Honda Civik', 'price' : 890000, 'amount' : 0, 'dealer' : 'dealer1'},
        {'car_id': 858,'car_name':'Kia Rio', 'price' : 900000, 'amount': 3, 'dealer' : 'dealer1'},
        {'car_id': 677,'car_name':'Nissan Almera ', 'price' : 750000, 'amount': 1, 'dealer' : 'dealer2'}
        ]

db.create_db_cars()
db.create_table_orders()
db.insert_values_cars(cars)
db.create_db_dealers()
db.insert_values_dealers(dealers)



class CarsList(Resource):
  def get(self):
    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    sql = '''SELECT CAR_MODEL FROM CARS WHERE AMOUNT > 0'''
    cursor.execute(sql)
    list_available_cars = cursor.fetchall()
    app.logger.info("Available cars: %s", list_available_cars)
    if len(list_available_cars) == 0:
      return 'No cars available', 404
    return list_available_cars, 200

class Car(Resource):
  def get(self, id):
    car_id = int(id)
    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM CARS WHERE ID=?; ''', [car_id])
    car = cursor.fetchall()
    if len(car) > 0:
        app.logger.info("car info: %s", car)
        cursor.close()
        return car, 200
    else:
      return 'no such car', 404



class DealersList(Resource):
  def get(self):
    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    sql = '''SELECT DEALER FROM DEALERS'''
    cursor.execute(sql)
    dealers_list = cursor.fetchall()
    app.logger.info("dealers' list: %s", dealers_list)
    return dealers_list, 200

class Dealer(Resource):
  def get(self, dealer):
    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    sql = '''SELECT DEALER, DEALER_INFO FROM DEALERS WHERE DEALER = '{dealer}' '''
    query = sql.format(dealer = dealer)
    cursor.execute(query)
    dealers_list = cursor.fetchall()
    if len(dealers_list) > 0:
        return dealers_list, 200
    else:
        return 'no such dealer', 404

class CheckOut(Resource):
  def post(self, id):
    user_data = request.form
    user_name = user_data.get("user_name")
    surname = user_data.get("second_name")
    id = int(id)

    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    sql = '''SELECT * FROM CARS WHERE ID = {id} AND AMOUNT > 0'''.format(id = id)
    cursor.execute(sql)
    data = cursor.fetchall()

    if len(data) != 0:
      new_order = [{'name' : user_name,
                            'second_name' : surname,
                            'car_id' : id}]
      new_order_id  = db.insert_values_orders(new_order)

      #cursor.execute('''SELECT * FROM ORDERS ''')  check whether the order was added to db
      #orders = cursor.fetchall()

      app.logger.info("orders: %s", orders)
      app.logger.info("order %s was created: %s",  new_order_id, new_order)

      db.update_db_cars(id)
      # db cars amount -=1 + commit
      return 'order was created', 201

    else:
      return 'This car is not available for purchase', 404



class OrdersList(Resource):
  def get(self):
    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    query = '''SELECT * FROM ORDERS'''
    cursor.execute(query)
    orders_list = cursor.fetchall()
    if len(orders) > 0:
      return orders_list, 200
    else:
      return "you have no orders"

class Order(Resource):
  def get(self, order_id):
    conn = sqlite3.connect('Cars.db')  #connects to the database
    cursor = conn.cursor()
    sql = '''SELECT * FROM ORDERS WHERE ORDER_ID = '{order_id}' '''
    query = sql.format(order_id = order_id)
    cursor.execute(query)
    order = cursor.fetchall()
    conn.close()
    if len(order) > 0:
      return order
    else:
      return "no such order", 400

  def delete(self, order_id):
      conn = sqlite3.connect('Cars.db')  #connects to the database
      cursor = conn.cursor()
      sql = '''DELETE FROM ORDERS WHERE ORDER_ID = '{order_id}' '''
      query = sql.format(order_id = order_id)
      cursor.execute(query)
      app.logger.info('order %s was deleted', order_id)
      conn.commit()
      conn.close()
      return 204


api.add_resource(CarsList, '/cars')
api.add_resource(Car, '/cars/<id>')
api.add_resource(CheckOut, '/cars/<id>/checkout')
api.add_resource(DealersList, '/dealers')
api.add_resource(Dealer, '/dealers/<dealer>')
api.add_resource(OrdersList, '/orders')
api.add_resource(Order,'/orders/<order_id>')


if __name__ == "__main__":
        app.run(debug=True)




#cars/678/checkout
