from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func
import pandas as pd
import datetime as dt
import config as cfg



# The Purpose of this Class is to separate out any Database logic
class SQLHelper():
    #################################################
    # Database Setup
    #################################################

    # define properties
    def __init__(self):
        # Setup the Postgres connection variables
        SQL_USERNAME = cfg.SQL_USERNAME
        SQL_PASSWORD = cfg.SQL_PASSWORD
        SQL_IP = cfg.SQL_IP
        SQL_PORT = cfg.SQL_PORT
        DATABASE = cfg.DATABASE

        connection_string = f'postgresql+psycopg2://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_IP}:{SQL_PORT}/{DATABASE}'
        # Connect to PostgreSQL server
        self.engine = create_engine(connection_string)
        self.Base = None

        # automap Base classes
        self.init_base()

    def init_base(self):
        # reflect an existing database into a new model
        self.Base = automap_base()
        # reflect the tables
        self.Base.prepare(autoload_with=self.engine)

    #################################################
    # Database Queries
    #################################################

    def query_analysis1_orm(self):
        # Save reference to the table
        analysis1 = self.Base.classes.analysis1

        # Create our session (link) from Python to the DB
        session = Session(self.engine)



        # close session
        session.close()

        # Convert the query results to a Dictionary
        data = analysis1_df.to_dict(orient="records")
        return (data)

    def query_pledges_per_goal_by_country_sql(self, country):
        # Number of Campaigns by Country which reached various pledges per goal
        query = f"""
                    SELECT
                        country,
                        SUM(perfect) AS goalreached,
                        SUM(ninety) AS ninetypercent_goalreached,
                        SUM(eighty) AS eightypercent_goalreached,
                        SUM(seventy) AS seventypercent_goalreached,
                        SUM(sixty) AS sixtypercent_goalreached,
                        SUM(fifty) AS fiftypercent_goalreached,
                        SUM(fail) AS lessthanfiftypercent_goalreached,
                        COUNT(Country) AS grand_total
                    FROM
                        (
                        SELECT
                            country,
                            CASE WHEN pledged >= goal then 1 else 0 END AS perfect,
                            CASE WHEN pledged >= goal * 0.9 AND pledged < goal then 1 else 0 END AS ninety,
                            CASE WHEN pledged >= goal * 0.8 AND pledged < goal * 0.9 then 1 else 0 END AS eighty,
                            CASE WHEN pledged >= goal * 0.7 AND pledged < goal * 0.8 then 1 else 0 END AS seventy,
                            CASE WHEN pledged >= goal * 0.6 AND pledged < goal * 0.7 then 1 else 0 END AS sixty,
                            CASE WHEN pledged >= goal * 0.5 AND pledged < goal * 0.6 then 1 else 0 END AS fifty,
                            CASE WHEN pledged < goal * 0.5 then 1 else 0 END AS fail
                        FROM
                            campaign
                        )
                    GROUsP BY
                        country
                    HAVING
                        country = '{start}';
                """

        # Save the query results as a Pandas DataFrame
        pledges_per_goal_by_country_df = pd.read_sql(text(query), con=self.engine)
        data = pledges_per_goal_by_country_df.to_dict(orient="records")
        return (data)
