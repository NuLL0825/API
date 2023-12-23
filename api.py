from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "call_center"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/customers", methods=["GET"])
def get_customers():
    data = data_fetch("""select * from customers""")
    return make_response(jsonify(data), 200)

@app.route("/customers/<int:id>", methods=["GET"])
def get_customers_by_id(id):
    data = data_fetch("""select * from customers where customer_id = {}""".format(id))
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)


