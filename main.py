from flask import Flask, jsonify, request
import mysql.connector
import sqlparse
import sys
import configparser
from datetime import datetime


def setup_database():
    # setting up database based on rates.sql
    queriesPath = "rate.sql"
    myCursor.execute("create database xeneta_rates")
    myCursor.execute("use xeneta_rates")
    print("setting up the database, this may take few minutes")
    with open(queriesPath, 'r') as rateFile:
        sqlScript = rateFile.read()
        for individualQuery in sqlScript.split(';'):
            # logic for removing comments and whitespaces
            individualQuery = sqlparse.format(individualQuery, strip_comments=True).strip()
            myCursor.execute(individualQuery)


# this is used for declaring connection of browser with flask
app = Flask(__name__)


# API endpoint to get average prices per day between routes.
@app.route("/rates", methods=["GET"])
def get_average_rates():
    # reading inputs from API
    dateFrom = request.args.get("date_from")
    dateTo = request.args.get("date_to")
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    # trying to convert string to date format to eventually handle incorrect date format
    try:
        if dateFrom is not None:
            datetime.strptime(dateFrom, "%Y-%m-%d")
        if dateTo is not None:
            datetime.strptime(dateTo, "%Y-%m-%d")
    except:
        return "Invalid date format observed, please enter date in the format YYYY-MM-DD"
    queryDateFrom = None
    queryDateTo = None
    queryOrigin = None
    queryDestination = None
    queryPart1 = "select day,CASE WHEN cnt < 3 THEN NULL ELSE AVG_PRICE END AS AVG_PRICE from ( \
        select count(*)as cnt, round(avg(price),0) as AVG_PRICE, day from prices as a inner join ports \
         as b on a.orig_code = b.code inner join ports as c on a.dest_code = c.code "
    queryEnd = "group by day ) as tmp"
    # logic for partial input, so that query can run with any, all or no filters
    if dateFrom is not None:
        queryDateFrom = "day >= \"" + dateFrom + "\" "
    if dateTo is not None:
        queryDateTo = "day <= \"" + dateTo + "\" "
    if origin is not None:
        queryOrigin = "(a.orig_code = \"" + origin + "\" OR  b.parent_slug = \"" + origin + "\") "
    if destination is not None:
        queryDestination = "(a.dest_code = \"" + destination + "\" OR  c.parent_slug = \"" + destination + "\") "
    # removing duplicate None objects by creating a set
    mySet = {queryDateFrom, queryDateTo, queryOrigin, queryDestination}
    # converting the set into a list as set can not be modified
    myList = list(mySet)
    if None in myList:
        myList.remove(None)

    # logic for collating the final query
    if len(myList) == 0:
        query = queryPart1 + queryEnd
    elif len(myList) == 1:
        query = queryPart1 + "where " + myList[0] + queryEnd
    elif len(myList) == 2:
        query = queryPart1 + "where " + myList[0] + " AND " + myList[1] + queryEnd
    elif len(myList) == 3:
        query = queryPart1 + "where " + myList[0] + " AND " + myList[1] + " AND " + myList[2] + queryEnd
    else:
        query = queryPart1 + "where " + myList[0] + " AND " + myList[1] + " AND " + myList[2] + \
                " AND " + myList[3] + queryEnd
    #print(query)
    try:
        myCursor.execute(query)
        result = myCursor.fetchall()
        # drafting the result in JSON format
        response = [
            {"day": day.strftime("%Y-%m-%d"), "average_price": avg_price}
            for day, avg_price in result
        ]
        # handling blank response
        if not response:
            return "The data you entered is either wrong, or there is no entry for the combination of inputs entered."
        return jsonify(response)
    except:
        return "Something went wrong while fetching the data requested"


# setting config parser to avoid hard-coding of connection details
config = configparser.ConfigParser()
config.read("config.ini")

# establishing connection with SQL database
try:
    mydb = mysql.connector.connect(
        host=config["databaseConnection"]["host"],
        user=config["databaseConnection"]["user"],
        password=config["databaseConnection"]["password"]
    )
    myCursor = mydb.cursor()
except:
    print("Unable to establish connection with database")
    # exiting code if connection failure as API won't be able to fetch data
    sys.exit(1)

try:
    # using database if exists
    myCursor.execute("use xeneta_rates")
except:
    # setting up database if not exists
    setup_database()

# hosting the API
if __name__ == "__main__":
    app.run(host=config["apiServer"]["host"], port=int(config["apiServer"]["port"]), debug=True)
