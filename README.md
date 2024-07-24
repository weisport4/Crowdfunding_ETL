# Crowdfunding_ETL
Project 2 Database Creation, ETL and Data Analysis
Project Overview
This project involves creating a comprehensive crowdfunding database. It is divided into four key steps:

Create the Category and Subcategory DataFrames: Develop DataFrames for storing information about different categories and subcategories of crowdfunding campaigns.

Create the Campaign DataFrame: Construct a DataFrame to capture all relevant details of the crowdfunding campaigns, such as campaign names, funding goals, start and end dates, and amounts raised.

Create the Contacts DataFrame: Build a DataFrame to manage contact information of individuals involved in the crowdfunding campaigns, including their names, email addresses, and roles.

Create the Crowdfunding Database: Integrate the Category, Subcategory, Campaign, and Contacts DataFrames into a unified database for easy access and management of the crowdfunding data.

Steps to run the application:
    A. Create the crowdfunding database using pgAdmin4
    B. To create the tables use crowdfunding_db_schema.sql, run that SQL in pfAdmin4 using the query tool while on the crowdfunding database
    C. After running the Schema and creating the database, verify the tables were created by running the SQL in select_sql.sql.  The counts will be zero as their is no data.
    D. Once the tables are created, run ETL_Mini_Project_JWeishan_CRuiz_GStalker.ipynb using jupyter notebook.  This will create your database input .CSV files stored  under DB_Input using the CSV input data under the resources directory.
    F. Prior to the next step create a config.py file in the same location as you python code. The config.py will include the following:
        SQL_USERNAME = 'postgres'
        SQL_PASSWORD = '<YOUR PASSWORD>'
        SQL_IP = 'localhost'
        SQL_PORT = '5432'
        DATABASE = 'crowdfunding_db'
    E. Now that your database and input files are ready, you can load the data into the database using ETL_pandas_to_Postgres.ipynb in jupyter notebook
    F. Run select_sql.sql again and you will get the row counts for each table.
    G. Once the tables are loaded, you can run Crowdfunding_Analysis.ipynb.  This will produce the SQL results and Visualization results that are discussed in the Written_analysis_for_crowdfunding.pdf

For extra analysis, you can run app.py which executes sqlHelper.py.  This application uses flask and was designed to seperate the application layer from the SQL layer.