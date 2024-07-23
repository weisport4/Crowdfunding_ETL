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

    def full_data_sql(self):
        # Find the most recent date in the data set.
        query = """
                SELECT
                    cont.first_name,
                    cont.last_name,
                    cont.email,
                    camp.company_name,
                    camp.description,
                    camp.goal,
                    camp.pledged,
                    camp.outcome,
                    camp.backers_count,
                    camp.country,
                    camp.currency,
                    camp.launched_date,
                    camp.end_date,
                    camp.staff_pick,
                    camp.spotlight,
                    cat.category,
                    sub.subcategory
                FROM
                    public.contact cont
                INNER JOIN public.campaign camp
                    ON cont.contact_id = camp.contact_id
                INNER JOIN public.category cat
                    ON camp.category_id = cat.category_id
                INNER JOIN public.subcategory sub
                    ON camp.subcategory_id = sub.subcategory_id
                ;
                """

        # Save the query results as a Pandas DataFrame
        full_data_sql_df = pd.read_sql(text(query), con=self.engine)
        data = full_data_sql_df.to_dict(orient="records")
        return (data)
    
    def full_data_orm(self):
        # Save reference to the table
        full_data_orm = self.Base.classes.full_data_orm

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        full_data_orm = session.query(
            Contact.first_name,
            Contact.last_name,
            Contact.email,
            Campaign.company_name,
            Campaign.description,
            Campaign.goal,
            Campaign.pledged,
            Campaign.outcome,
            Campaign.backers_count,
            Campaign.country,
            Campaign.currency,
            Campaign.launched_date,
            Campaign.end_date,
            Campaign.staff_pick,
            Campaign.spotlight,
            Category.category,
            Subcategory.subcategory
        ).join(
            Campaign, Contact.contact_id == Campaign.contact_id
        ).join(
            Category, Campaign.category_id == Category.category_id
        ).join(
            Subcategory, Campaign.subcategory_id == Subcategory.subcategory_id
        ).all()

        # close session
        session.close()

        # Convert the query results to a Dictionary
        data = analysis1_df.to_dict(orient="records")
        return (data)

    # def reached_goal_sql(self):
    #     # Find the most recent date in the data set.
    #     query = """
    #             SELECT
    #                 cont.first_name,
    #                 cont.last_name,
    #                 cont.email,
    #                 camp.company_name,
    #                 camp.description,
    #                 camp.goal,
    #                 camp.pledged,
    #                 camp.outcome,
    #                 camp.backers_count,
    #                 camp.country,
    #                 camp.currency,
    #                 camp.launched_date,
    #                 camp.end_date,
    #                 camp.staff_pick,
    #                 camp.spotlight,
    #                 cat.category,
    #                 sub.subcategory
    #             FROM
    #                 public.contact cont
    #             INNER JOIN public.campaign camp
    #                 ON cont.contact_id = camp.contact_id
    #             INNER JOIN public.category cat
    #                 ON camp.category_id = cat.category_id
    #             INNER JOIN public.subcategory sub
    #                 ON camp.subcategory_id = sub.subcategory_id
    #             WHERE
    #                 (staff_pick = TRUE OR spotlight = TRUE)
    #                 AND pledged >= goal
    #             ;
    #             """

    #     # Save the query results as a Pandas DataFrame
    #     reached_goal_sql_df = pd.read_sql(text(query), con=self.engine)
    #     data = reached_goal_sql_df.to_dict(orient="records")
    #     return (data)
    
    # def reached_goal_orm(self):
    #     # Save reference to the table
    #     reached_goal_orm = self.Base.classes.analysis1

    #     # Create our session (link) from Python to the DB
    #     session = Session(self.engine)



    #     # close session
    #     session.close()

    #     # Convert the query results to a Dictionary
    #     data = reached_goal_orm_df.to_dict(orient="records")
    #     return (data)
    
    #     def query_analysis1_sql(self):
    #     # Find the most recent date in the data set.
    #     query = """
    #             SELECT 
    #             FROM 
    #             WHERE 
    #             ORDER BY ;
    #             """

    #     # Save the query results as a Pandas DataFrame
    #     analysis1_df = pd.read_sql(text(query), con=self.engine)
    #     data = analysis1_df.to_dict(orient="records")
    #     return (data)
    
    # def query_analysis1_orm(self):
    #     # Save reference to the table
    #     analysis1 = self.Base.classes.analysis1

    #     # Create our session (link) from Python to the DB
    #     session = Session(self.engine)



    #     # close session
    #     session.close()

    #     # Convert the query results to a Dictionary
    #     data = analysis1_df.to_dict(orient="records")
    #     return (data)

