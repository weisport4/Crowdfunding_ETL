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
            Welcome to the Climate Analysis API!                                                                                                                                            <br/>
            Available Routes:                                                                                                                                                               <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/full_data_sql">/api/v1.0/full_data_sql</a>                                                                                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/full_data_orm">/api/v1.0/full_data_orm</a>                                                                                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/reached_goal_sql">/api/v1.0/reached_goal_sql</a>                                                                                     <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/reached_goal_orm">/api/v1.0/reached_goal_orm</a>                                                                                     <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/count_of_categories_by_outcome_sql">/api/v1.0/count_of_categories_by_outcome_sql</a>                                                 <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/count_of_categories_by_outcome_orm">/api/v1.0/count_of_categories_by_outcome_orm</a>                                                 <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/count_of_subcategories_by_outcome_sql">/api/v1.0/count_of_subcategories_by_outcome_sql</a>                                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/count_of_subcategories_by_outcome_orm">/api/v1.0/count_of_subcategories_by_outcome_orm</a>                                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/percentage_goal_by_country_sql">/api/v1.0/percentage_goal_by_country_sql</a>                                                         <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;<a href="/api/v1.0/percentage_goal_by_country_orm">/api/v1.0/percentage_goal_by_country_orm</a>                                                         <br/>
                                                                                                                                                                                            <br/>
                                                                                                                                                                                            <br/>
            Explanation of the Routes:                                                                                                                                                      <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;full_data_sql: Returns all the data from the table using SQL.                                                                                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;full_data_orm: Returns all the data from the table using ORM.                                                                                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;reached_goal_sql: Returns the number of projects that have reached their funding goal and have been staff picked or are in the spotligh using SQL.      <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;reached_goal_orm: Returns the number of projects that have reached their funding goal and have been staff picked or are in the spotligh using ORM.      <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;count_of_categories_by_outcome_sql: Returns the count of projects by category and outcome using SQL.                                                    <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;count_of_categories_by_outcome_orm: Returns the count of projects by category and outcome using ORM.                                                    <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;count_of_subcategories_by_outcome_sql: Returns the count of projects by subcategory and outcome using SQL.                                              <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;count_of_subcategories_by_outcome_orm: Returns the count of projects by subcategory and outcome using ORM.                                              <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;percentage_goal_by_country_sql: Returns the percentage of projects that have reached their funding goal by country using SQL.                           <br/>
            &nbsp;&nbsp;&nbsp;&nbsp;percentage_goal_by_country_orm: Returns the percentage of projects that have reached their funding goal by country using ORM.                           <br/>
            ''')


@app.route("/api/v1.0/full_data_sql")
def full_data_sql():
    data = sql.full_data_sql()
    return (jsonify(data))


@app.route("/api/v1.0/full_data_orm")
def full_data_orm():
    data = sql.full_data_orm()
    return (jsonify(data))


@app.route("/api/v1.0/reached_goal_sql")
def reached_goal_sql():
    data = sql.reached_goal_sql()
    return (jsonify(data))


@app.route("/api/v1.0/reached_goal_orm")
def reached_goal_orm():
    data = sql.reached_goal_orm()
    return (jsonify(data))


@app.route("/api/v1.0/count_of_categories_by_outcome_sql")
def count_of_categories_by_outcome_sql():
    data = sql.count_of_categories_by_outcome_sql()
    return (jsonify(data))


@app.route("/api/v1.0/count_of_categories_by_outcome_orm")
def count_of_categories_by_outcome_orm():
    data = sql.count_of_categories_by_outcome_orm()
    return (jsonify(data))


@app.route("/api/v1.0/count_of_subcategories_by_outcome_sql")
def count_of_subcategories_by_outcome_sql():
    data = sql.count_of_subcategories_by_outcome_sql()
    return (jsonify(data))


@app.route("/api/v1.0/count_of_subcategories_by_outcome_orm")
def count_of_subcategories_by_outcome_orm():
    data = sql.count_of_subcategories_by_outcome_orm()
    return (jsonify(data))


@app.route("/api/v1.0/percentage_goal_by_country_sql")
def percentage_goal_by_country_sql():
    data = sql.percentage_goal_by_country_sql()
    return (jsonify(data))


@app.route("/api/v1.0/percentage_goal_by_country_orm")
def percentage_goal_by_country_orm():
    data = sql.percentage_goal_by_country_orm()
    return (jsonify(data))


# Run the App
if __name__ == '__main__':
    app.run(debug=True)
