from flask import Flask, jsonify
from sqlHelper import SQLHelper

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
sql = SQLHelper()

#################################################
# Flask Routes
#################################################


@app.route('/')
def welcome():
    return ('''
            Welcome to the Climate Analysis API!                                                        <br/>
            Available Routes:                                                                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/analysis1_orm">/api/v1.0/full_data_sql</a>       <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/analysis1_sql">/api/v1.0/full_data_orm</a>       <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/analysis1_orm">/api/v1.0/full_data_sql</a>       <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/analysis1_sql">/api/v1.0/full_data_orm</a>       <br/>
            ''')


@app.route("/api/v1.0/full_data_sql")
def full_data_sql():
    data = sql.full_data_sql()
    return (jsonify(data))


@app.route("/api/v1.0/full_data_orm")
def full_data_orm():
    data = sql.full_data_orm()
    return (jsonify(data))


# @app.route("/api/v1.0/analysis1_sql")
# def analysis1_sql():
#     data = sql.query_analysis1_sql()
#     return (jsonify(data))


# @app.route("/api/v1.0/analysis1_orm")
# def analysis1_orm():
#     data = sql.query_analysis1_orm()
#     return (jsonify(data))


# @app.route("/api/v1.0/analysis2_sql")
# def analysis1_sql():
#     data = sql.query_analysis2_sql()
#     return (jsonify(data))


# @app.route("/api/v1.0/analysis2_orm")
# def analysis1_orm():
#     data = sql.query_analysis2_orm()
#     return (jsonify(data))


# Run the App
if __name__ == '__main__':
    app.run(debug=True)
