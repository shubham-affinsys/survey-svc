import psycopg2

from robyn import Robyn
from models import *

DB_NAME = "robyn_db"
DB_HOST = "localhost"
DB_USER = "shubham"
DB_PASS = "9504"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT)

app = Robyn(__file__)


@app.post("/survey")
def create_survey(request):
    try:
        # Get the JSON data from the request (no 'await' needed)
        data = request.json()  # synchronous call
        # Insert the data into the database
        insert_data(data)
        return {"desc": "survey created successfully"}
    except Exception as e:
        print(f"Error while creating survey: {e}")
        return {"error": f"Error while creating survey: {e}"}


@app.get("/survey_responses")
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM survey_responses")
    all_users = cursor.fetchall()
    return {"survey_responses": all_users}

@app.get("/surveys")
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM surveys")
    all_users = cursor.fetchall()
    return {"surveys": all_users}


@app.get("/")
def index():
    return "Hello World!"




if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)



