import json
from curl_cffi import requests
import os
from pydantic import BaseModel, Field
from rich import print
from typing import List, Optional
import sqlite3


class IriTemplateMapping(BaseModel):
    variable: str
    property: Optional[str]
    required: bool

class HydraSearch(BaseModel):
    template: str
    variable_representation: str
    mapping: List[IriTemplateMapping]

class HydraView(BaseModel):
    id: str
    type: str
    first: str
    last: str
    next: Optional[str]

class StudyDetail(BaseModel):
    id: int
    title: str
    type: str
    entity_type_id: str
    entity_id: str
    description: str
    url: str
    image_url: str
    image_title: str
    image_alt: str
    main_facet: str
    larested: str
    d7_nid: str
    site: str
    stedsnavn: str
    organisasjon: str
    utdanningsniva: str
    score: float
    forste_semester: str
    siste_semester: str
    program_status: str

class SearchResults(BaseModel):
    context: str = Field(alias="@context")
    id: str = Field(alias="@id")
    type: str = Field(alias="@type")
    total_items: int = Field(alias="hydra:totalItems")
    member: List[StudyDetail] = Field(alias="hydra:member")



def new_session():
    session = requests.Session(impersonate="chrome")
    return session


def search_studies(session: requests.Session, start_num: int = 1, items_per_page: int = 10000, omrade: str = None):
    urlomrade = ""
    if (omrade):
        urlomrade = f"&omrade=%22{omrade}%22"
    url = f"https://api.utdanning.no/search/result?page={start_num}&itemsPerPage={items_per_page}&hovedfasett=%22Utdanninger%22&utdanningsniva=%22Universitet%20og%20h%C3%B8gskole%22{urlomrade}"
    response = session.get(url)
    response.raise_for_status()
    #print(response.json())
    search = SearchResults(**response.json())
    return search


def insert_studies(conn: sqlite3.Connection, studies: list[StudyDetail]):
    # Prepare the data as a list of tuples
    studies_data = [
        (
            study.title,
            study.type,
            study.description,
            study.entity_type_id,
            study.entity_id,
            study.url,
            study.image_url,
            study.image_title,
            study.image_alt,
            study.main_facet,
            study.larested,
            study.d7_nid,
            study.site,
            study.stedsnavn,
            study.organisasjon,
            study.utdanningsniva,
            study.score,
            study.forste_semester,
            study.siste_semester,
            study.program_status,
        )
        for study in studies
    ]
    
    # Use executemany to insert all rows
    conn.executemany('''
        INSERT INTO studies (
            title, type, description, entity_type_id, entity_id, url, 
            image_url, image_title, image_alt, main_facet, larested, d7_nid, 
            site, stedsnavn, organisasjon, utdanningsniva, score, 
            forste_semester, siste_semester, program_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', studies_data)
    
    # Commit the transaction
    conn.commit()



def create_tables(conn: sqlite3.Connection):
    conn.execute('''CREATE TABLE IF NOT EXISTS studies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        type TEXT,
        description TEXT,
        entity_type_id TEXT,
        entity_id TEXT,
        url TEXT,
        image_url TEXT,
        image_title TEXT,
        image_alt TEXT,
        main_facet TEXT,
        larested TEXT,
        d7_nid TEXT,
        site TEXT,
        stedsnavn TEXT,
        organisasjon TEXT,
        utdanningsniva TEXT,
        score NUMERIC,
        forste_semester TEXT,
        siste_semester TEXT,
        program_status TEXT
    )''')


def get_omrade_list():
    return ["Oslo", "Vestland", "Trøndelag", "Møre og Romsdal", "Troms", "Innlandet", "Rogaland", "Nordland", "Agder", "Akershus", "Telemark", "Østfold", "Vestfold", "Buskerud", "Finnmark", "Svalbard"]



def main():
    conn = sqlite3.connect('studies.db')
    create_tables(conn)
    session = new_session()
    for omrade in get_omrade_list():
        search = search_studies(session, start_num=1, omrade=omrade)
        insert_studies(conn, search.member)
        with open(f'dumps/search_results_{omrade}.json', 'w', encoding='utf-8') as f:
            json.dump(search.model_dump()['member'], f, indent=4, ensure_ascii=False)
        print(f"Raw JSON search results written to search_results_{omrade}.json")
    # Write raw JSON search results to a text file
"""     with open('search_results.json', 'w', encoding='utf-8') as f:
        json.dump(search.model_dump()['member'], f, indent=4, ensure_ascii=False)
    print(f"Raw JSON search results written to search_results.json") """


if __name__ == "__main__":
    main()