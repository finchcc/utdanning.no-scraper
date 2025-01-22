import csv
import json
from curl_cffi import requests
import os
from pydantic import BaseModel, Field
from rich import print
from typing import List, Optional
import sqlite3


def create_tables(conn: sqlite3.Connection):
    conn.execute('''CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        navn TEXT,
        type TEXT,
        description TEXT,
        antall_innbyggere INTEGER,
        antall_studenter INTEGER,
        score NUMERIC,
        ammount_of_studies INTEGER
    )''')


def get_ammount_of_people_in_city(city_name: str):
    population_file = "city_population.csv"
    target_year = "2023"
    population_column = "Befolkning 1. januar"

    try:
        with open(population_file, mode="r", encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:
                if len(row) == 4:
                    city, year, description, population = row
                    city = city.strip('"')
                    year = year.strip('"')
                    description = description.strip('"')
                    population = population.strip()

                    if city_name in city and year == target_year and description == population_column:
                        return int(population)
        
        # Return None if the city or year is not found
        return None

    except FileNotFoundError:
        raise FileNotFoundError(f"The file {population_file} does not exist.")
    except ValueError:
        raise ValueError("Failed to parse the population data. Ensure the file is correctly formatted.")

def format_all_byer(conn: sqlite3.Connection):
    # Get all unique cities from studies table
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT stedsnavn FROM studies WHERE stedsnavn IS NOT NULL')
    cities = cursor.fetchall()
    # Insert each city into byer table if it doesn't already exist
    for city in cities:
        # Split the stedsnavn field on commas to handle multiple cities
        city_names = [name.strip() for name in city[0].split(',')]
        
        # Process each individual city
        for city_name in city_names:
            print(f"Processing {city_name}")
            # Count how many studies exist for this city
            cursor.execute('SELECT COUNT(*) FROM studies WHERE stedsnavn LIKE ?', (f'%{city_name}%',))
            study_count = cursor.fetchone()[0]
            
            # Check if city already exists
            cursor.execute('SELECT navn FROM cities WHERE navn = ?', (city_name,))
            if cursor.fetchone() is None:
                # City doesn't exist, insert it with study count
                population = get_ammount_of_people_in_city(city_name)
                print(f"Inserting {city_name} with population {population} and study count {study_count}")
                cursor.execute('''
                    INSERT INTO cities (navn, type, description, antall_innbyggere, antall_studenter, score, ammount_of_studies)
                    VALUES (?, NULL, NULL, ?, NULL, NULL, ?)
                ''', (city_name, population, study_count))
            else:
                # Update existing city with study count
                cursor.execute('''
                    UPDATE cities 
                    SET ammount_of_studies = ?
                    WHERE navn = ?
                ''', (study_count, city_name))
        
    conn.commit()


def main():
    conn = sqlite3.connect('studies.db')
    create_tables(conn)
    format_all_byer(conn)


    conn.close()


main()