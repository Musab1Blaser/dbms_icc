### How to Run
- Create a database called *ICC_Cricket_Management* using SSMS. Record your connection/login details and enter them in the *app.py* file in the *App* folder file around line 671 as follows
 ```python
server = {server_name}
database = "ICC_Cricket_Management"
username = "sa"
password = {password}
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};'
```

- Load the scripts in the *database_sql_scripts* folder into SSMS. Run in the following order:
  1. *Database_Initialisation.sql*
  2. *Database_Populate.sql*
  3. Run separately, each of the 2 stored procedures in *Database_Views.sql*
    
    In case of any error, run *Database_Clear.sql*

- Run app.py. Install any necessary packages

## [Demo](https://youtu.be/yz4mlXQm-No?si=SOKT1mlfzwcqZMxt)
