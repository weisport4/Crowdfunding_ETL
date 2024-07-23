from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func, case
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
        # Assign the classes to variables
        Contact = self.Base.classes.contact
        Campaign = self.Base.classes.campaign
        Category = self.Base.classes.category
        Subcategory = self.Base.classes.subcategory

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        results = session.query(
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

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        full_data_orm_df = pd.DataFrame(results, columns=['first_name', 'last_name', 'email', 'company_name', 'description', 'goal', 'pledged', 'outcome', 'backers_count', 'country', 'currency', 'launched_date', 'end_date', 'staff_pick', 'spotlight', 'category', 'subcategory'])

        # close session
        session.close()

        # Convert the query results to a Dictionary
        data = full_data_orm_df.to_dict(orient="records")
        return (data)


    def reached_goal_sql(self):
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
                WHERE
                    (staff_pick = TRUE OR spotlight = TRUE)
                    AND pledged >= goal
                ;
                """

        # Save the query results as a Pandas DataFrame
        reached_goal_sql_df = pd.read_sql(text(query), con=self.engine)
        data = reached_goal_sql_df.to_dict(orient="records")
        return (data)


    def reached_goal_orm(self):
        # Save reference to the table
        # Assign the classes to variables
        Contact = self.Base.classes.contact
        Campaign = self.Base.classes.campaign
        Category = self.Base.classes.category
        Subcategory = self.Base.classes.subcategory

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # ORM to get all campaigns that have been staff picked or are in the spotlight and have reached their goal
        results = session.query(
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
        ).filter(
            (Campaign.staff_pick == True) | (Campaign.spotlight == True),
            Campaign.pledged >= Campaign.goal
        ).all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        reached_goal_orm_df = pd.DataFrame(results, columns=['first_name', 'last_name', 'email', 'company_name', 'description', 'goal', 'pledged', 'outcome', 'backers_count', 'country', 'currency', 'launched_date', 'end_date', 'staff_pick', 'spotlight', 'category', 'subcategory'])

        # close session
        session.close()

        # Convert the query results to a Dictionary
        data = reached_goal_orm_df.to_dict(orient="records")
        return (data)


    def count_of_categories_by_outcome_sql(self):
        # Find the most recent date in the data set.
        query = """
                SELECT
                    category,
                    SUM(canceled) AS canceled,
                    SUM(failed) AS failed,
                    SUM(live) AS live,
                    SUM(successful) AS successful,
                    COUNT(category) AS grand_total
                FROM
                    (
                    SELECT
                        cat.category,
                        CASE WHEN camp.outcome = 'canceled' then 1 else 0 END AS canceled,
                        CASE WHEN camp.outcome = 'failed' then 1 else 0 END AS failed,
                        CASE WHEN camp.outcome = 'live' then 1 else 0 END AS live,
                        CASE WHEN camp.outcome = 'successful' then 1 else 0 END AS successful
                    FROM
                        public.campaign camp
                    INNER JOIN public.category cat
                        ON cat.category_id = camp.category_id
                    )
                GROUP BY
                    category
                ;
                """

        # Save the query results as a Pandas DataFrame
        count_of_categories_by_outcome_sql_df = pd.read_sql(text(query), con=self.engine)
        data = count_of_categories_by_outcome_sql_df.to_dict(orient="records")
        return (data)


    def count_of_categories_by_outcome_orm(self):
        # Save reference to the table
        # Assign the classes to variables
        Campaign = self.Base.classes.campaign
        Category = self.Base.classes.category

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        # ORM to get all campaigns that have been staff picked or are in the spotlight and have reached their goal
        results = session.query(
            Category.category,
            func.sum(case((Campaign.outcome == 'canceled', 1), else_=0)).label('canceled'),
            func.sum(case((Campaign.outcome == 'failed', 1), else_=0)).label('failed'),
            func.sum(case((Campaign.outcome == 'live', 1), else_=0)).label('live'),
            func.sum(case((Campaign.outcome == 'successful', 1), else_=0)).label('successful'),
            func.count(Category.category).label('grand_total')
        ).join(
            Campaign, Category.category_id == Campaign.category_id
        ).group_by(
            Category.category
        ).all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        count_of_categories_by_outcome_orm_df = pd.DataFrame(results, columns=['category', 'canceled', 'failed', 'live', 'successful', 'grand_total'])

        # close session
        session.close()

        # Convert the query results to a Dictionary
        data = count_of_categories_by_outcome_orm_df.to_dict(orient="records")
        return (data)


    def count_of_subcategories_by_outcome_sql(self):
        # Find the most recent date in the data set.
        query = """
                SELECT
                    subcategory,
                    SUM(canceled) AS canceled,
                    SUM(failed) AS failed,
                    SUM(live) AS live,
                    SUM(successful) AS successful,
                    COUNT(subcategory) AS grand_total
                FROM
                    (
                    SELECT
                        sub.subcategory,
                        CASE WHEN camp.outcome = 'canceled' then 1 else 0 END AS canceled,
                        CASE WHEN camp.outcome = 'failed' then 1 else 0 END AS failed,
                        CASE WHEN camp.outcome = 'live' then 1 else 0 END AS live,
                        CASE WHEN camp.outcome = 'successful' then 1 else 0 END AS successful
                    FROM
                        public.campaign camp
                    INNER JOIN public.subcategory sub
                        ON sub.subcategory_id = camp.subcategory_id
                    )
                GROUP BY
                    subcategory
                ;
                """

        # Save the query results as a Pandas DataFrame
        full_data_sql_df = pd.read_sql(text(query), con=self.engine)
        data = full_data_sql_df.to_dict(orient="records")
        return (data)


    def count_of_subcategories_by_outcome_orm(self):
        # Save reference to the table
        # Assign the classes to variables
        Campaign = self.Base.classes.campaign
        Subcategory = self.Base.classes.subcategory

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        results = session.query(
            Subcategory.subcategory,
            func.sum(case((Campaign.outcome == 'canceled', 1), else_=0)).label('canceled'),
            func.sum(case((Campaign.outcome == 'failed', 1), else_=0)).label('failed'),
            func.sum(case((Campaign.outcome == 'live', 1), else_=0)).label('live'),
            func.sum(case((Campaign.outcome == 'successful', 1), else_=0)).label('successful'),
            func.count(Subcategory.subcategory).label('grand_total')
        ).join(
            Campaign, Subcategory.subcategory_id == Campaign.subcategory_id
        ).group_by(
            Subcategory.subcategory
        ).all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        count_of_subcategories_by_outcome_orm_df = pd.DataFrame(results, columns=['subcategory', 'canceled', 'failed', 'live', 'successful', 'grand_total'])

        # close session
        session.close()

        # Convert the query results to a Dictionary
        data = count_of_subcategories_by_outcome_orm_df.to_dict(orient="records")
        return (data)


    def percentage_goal_by_country_sql(self):
        # Find the most recent date in the data set.
        query = """
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
                GROUP BY
                    country
                ;
                """

        # Save the query results as a Pandas DataFrame
        percentage_goal_by_country_sql_df = pd.read_sql(text(query), con=self.engine)
        data = percentage_goal_by_country_sql_df.to_dict(orient="records")
        return (data)


    def percentage_goal_by_country_orm(self):
        # Save reference to the table
        # Assign the classes to variables
        Campaign = self.Base.classes.campaign

        # Create our session (link) from Python to the DB
        session = Session(self.engine)

        results = session.query(
            Campaign.country,
            func.sum(case((Campaign.pledged >= Campaign.goal, 1), else_=0)).label('goalreached'),
            func.sum(case(((Campaign.pledged >= Campaign.goal * 0.9) & (Campaign.pledged < Campaign.goal), 1), else_=0)).label('ninetypercent_goalreached'),
            func.sum(case(((Campaign.pledged >= Campaign.goal * 0.8) & (Campaign.pledged < Campaign.goal * 0.9), 1), else_=0)).label('eightypercent_goalreached'),
            func.sum(case(((Campaign.pledged >= Campaign.goal * 0.7) & (Campaign.pledged < Campaign.goal * 0.8), 1), else_=0)).label('seventypercent_goalreached'),
            func.sum(case(((Campaign.pledged >= Campaign.goal * 0.6) & (Campaign.pledged < Campaign.goal * 0.7), 1), else_=0)).label('sixtypercent_goalreached'),
            func.sum(case(((Campaign.pledged >= Campaign.goal * 0.5) & (Campaign.pledged < Campaign.goal * 0.6), 1), else_=0)).label('fiftypercent_goalreached'),
            func.sum(case((Campaign.pledged < Campaign.goal * 0.5, 1), else_=0)).label('lessthanfiftypercent_goalreached'),
            func.count(Campaign.country).label('grand_total')
        ).group_by(
            Campaign.country
        ).all()

        # Save the query results as a Pandas DataFrame. Explicitly set the column names
        percentage_goal_by_country_orm_df = pd.DataFrame(results, columns=['country', 'goalreached', 'ninetypercent_goalreached', 'eightypercent_goalreached', 'seventypercent_goalreached', 'sixtypercent_goalreached', 'fiftypercent_goalreached', 'lessthanfiftypercent_goalreached', 'grand total'])

        # close session
        session.close()

        # Convert the query results to a Dictionary
        data = percentage_goal_by_country_orm_df.to_dict(orient="records")
        return (data)

