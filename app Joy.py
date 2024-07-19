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
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/analysis1_orm">/api/v1.0/analysis1_orm</a>       <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/analysis1_sql">/api/v1.0/pledges_per_goal_by_country_sql</a>       <br/>
            ''')


@app.route("/api/v1.0/analysis1_orm")
def analysis1_orm():
    data = sql.query_analysis1_orm()
    return (jsonify(data))


@app.route("/api/v1.0/pledges_per_goal_by_country_sql")
def pledges_per_goal_by_country_sql():
    data = sql.query_pledges_per_goal_by_country_sql()
    return (jsonify(data))


# Run the App
if __name__ == '__main__':
    app.run(debug=True)
