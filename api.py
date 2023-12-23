from flask import Flask, make_response, jsonify, request, render_template, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "call_center"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def base():
    if not session.get('logged_in'):
        return render_template('login-page.html')
    else:
        return 'Logged in'

@app.route('/login', methods=['POST'])  
def login():
    if request.form['username'] == 'maui' and request.form['password'] == 'password':
        
        return jsonify({'Status' : "Logged In"}), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

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

@app.route("/customers", methods=["POST"])
def add_customer():
    cur = mysql.connection.cursor()
    info = request.get_json()
    customer_other_details = info["customer_other_details"]
    business_sector_id = info["ref_business_sector_business_sector_id"]
    cur.execute(
        """INSERT INTO customers(customer_other_details, ref_business_sector_business_sector_id)
        VALUES (%s, %s)""", (customer_other_details,business_sector_id)
    )
    mysql.connection.commit()
    print("rows(s) affected: {}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "customer added successfully", "rows_affected" : rows_affected}), 201)

@app.route("/customers/<int:id>", methods=["PUT"])
def update_customers(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    customer_other_details = info["customer_other_details"]
    business_sector_id = info["ref_business_sector_business_sector_id"]
    cur.execute(
        """ UPDATE customers SET customer_other_details = %s, ref_business_sector_business_sector_id = %s WHERE customer_id = %s """,
        (customer_other_details, business_sector_id, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "customer updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customers(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM customers where customer_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "customer deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/customers/search", methods=["GET"])
def search_customers():
    search = request.args.get("search")
    query = f"""SELECT * FROM customers WHERE customer_other_details LIKE '%{search}%';"""
    data = data_fetch(query)

    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)