import json
import psycopg2
from psycopg2 import sql


# Function to read JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Function to insert data into PostgreSQL
def insert_data_to_postgresql(data):
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            dbname="sampledb",
            user="postgres",
            password="yash",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        # Create table with auto-incrementing id if not exists
        tablename= "energy_data"
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {tablename} (
            id SERIAL PRIMARY KEY,
            end_year TEXT,
            intensity INT,
            sector TEXT,
            topic TEXT,
            insight TEXT,
            url TEXT,
            region TEXT,
            start_year TEXT,
            impact TEXT,
            added TIMESTAMP,
            published TIMESTAMP,
            country TEXT,
            relevance INT,
            pestle TEXT,
            source TEXT,
            title TEXT,
            likelihood INT
        )
        '''
        cursor.execute(create_table_query)
        connection.commit()
        print(f"tablecreted {tablename}")

        # Insert data into the table
        insert_query = '''
        INSERT INTO energy_data (
            end_year, intensity, sector, topic, insight, url, region, start_year, 
            impact, added, published, country, relevance, pestle, source, title, likelihood
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        for item in data:
            cursor.execute(insert_query, (
                item.get('end_year') or None,
                item.get('intensity') or None,
                item.get('sector') or None,
                item.get('topic') or None,
                item.get('insight') or None,
                item.get('url') or None,
                item.get('region') or None,
                item.get('start_year') or None,
                item.get('impact') or None,
                item.get('added') or None,
                item.get('published') or None,
                item.get('country') or None,
                item.get('relevance') or None,
                item.get('pestle') or None,
                item.get('source') or None,
                item.get('title') or None,
                item.get('likelihood') or None
            ))

        # Commit the transaction

        connection.commit()
        print("datainsered")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()


# Path to your JSON file
json_file_path = r"C:\Users\yashk\Downloads\jsondata.json"


# Read JSON data
data = read_json_file(json_file_path)

# Insert data into PostgreSQL
insert_data_to_postgresql(data)
