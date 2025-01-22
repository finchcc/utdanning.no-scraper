import json
from curl_cffi import requests
import os
from pydantic import BaseModel, Field
from rich import print
from typing import List, Optional
import sqlite3


class UtdanningEntry(BaseModel):
    id: str
    innholdstype: Optional[str] = None
    interesser: Optional[List[str]] = None
    sokeord: List[str] = Field(default_factory=list)
    sokeord_suggest: List[str] = Field(default_factory=list)
    sokeord_suggest_edge: List[str] = Field(default_factory=list)
    sokeord_suggest_ngram: List[str] = Field(default_factory=list)
    sokeord_s: List[str] = Field(default_factory=list)
    stat_vis_arb_markedskart: Optional[str] = None
    stat_vis_lonnstat: Optional[int] = None
    stat_vis_sammenligning: Optional[int] = None
    summary: Optional[str] = None
    tittel: Optional[str] = None
    title_suggest: List[str] = Field(default_factory=list)
    title_suggest_edge: List[str] = Field(default_factory=list)
    title_suggest_ngram: List[str] = Field(default_factory=list)
    title_s: List[str] = Field(default_factory=list)
    uno_id: Optional[str] = None
    update_hash: Optional[str] = None
    url: Optional[str] = None
    utdanningstype: List[str] = Field(default_factory=list)
    path: Optional[str] = None
    _version_: Optional[float] = None
    funksjon: Optional[str] = None
    score: Optional[float] = None
    sektor_antall_arbeidsledig: Optional[int] = None
    sektor_antall_ikkearbeid: Optional[int] = None
    sektor_antall_iutdanning: Optional[int] = None
    sektor_antall_offentlig: Optional[int] = None
    sektor_antall_personer: Optional[int] = None
    sektor_antall_privat: Optional[int] = None
    sektor_antall_selvstendig: Optional[int] = None

class UtdanningData(BaseModel):
    data: dict[str, UtdanningEntry]



def new_session():
    session = requests.Session(impersonate="chrome")
    return session


def search_studies(session: requests.Session):
    url = f"https://api.utdanning.no/sammenligning/main?innholdstype=utdanningsbeskrivelse&vis_alt=true&"
    response = session.get(url)
    response.raise_for_status()
    #print(response.json())
    search = response.json()
    return search
    


def create_tables(conn: sqlite3.Connection):
    conn.execute('''CREATE TABLE IF NOT EXISTS basic_studies (
                    id TEXT PRIMARY KEY,
                    innholdstype TEXT,
                    interesser TEXT,
                    sokeord TEXT,
                    sokeord_suggest TEXT,
                    sokeord_suggest_edge TEXT,
                    sokeord_suggest_ngram TEXT,
                    sokeord_s TEXT,
                    stat_vis_arb_markedskart TEXT,
                    stat_vis_lonnstat INTEGER,
                    stat_vis_sammenligning INTEGER,
                    summary TEXT,
                    tittel TEXT,
                    title_suggest TEXT,
                    title_suggest_edge TEXT,
                    title_suggest_ngram TEXT,
                    title_s TEXT,
                    uno_id TEXT,
                    update_hash TEXT,
                    url TEXT,
                    utdanningstype TEXT,
                    path TEXT,
                    _version_ FLOAT,
                    funksjon TEXT,
                    score FLOAT,
                    sektor_antall_arbeidsledig INTEGER,
                    sektor_antall_ikkearbeid INTEGER,
                    sektor_antall_iutdanning INTEGER,
                    sektor_antall_offentlig INTEGER,
                    sektor_antall_personer INTEGER,
                    sektor_antall_privat INTEGER,
                    sektor_antall_selvstendig INTEGER
                    )''')

def insert_studies(conn: sqlite3.Connection, studies: dict):
    studies_data = []
    for study in studies:
        # Convert lists to strings for storage
        interesser = ','.join(study.interesser) if study.interesser else None
        sokeord = ','.join(study.sokeord) if study.sokeord else None
        sokeord_suggest = ','.join(study.sokeord_suggest) if study.sokeord_suggest else None
        sokeord_suggest_edge = ','.join(study.sokeord_suggest_edge) if study.sokeord_suggest_edge else None
        sokeord_suggest_ngram = ','.join(study.sokeord_suggest_ngram) if study.sokeord_suggest_ngram else None
        sokeord_s = ','.join(study.sokeord_s) if study.sokeord_s else None
        title_suggest = ','.join(study.title_suggest) if study.title_suggest else None
        title_suggest_edge = ','.join(study.title_suggest_edge) if study.title_suggest_edge else None
        title_suggest_ngram = ','.join(study.title_suggest_ngram) if study.title_suggest_ngram else None
        title_s = ','.join(study.title_s) if study.title_s else None
        utdanningstype = ','.join(study.utdanningstype) if study.utdanningstype else None

        studies_data.append((
            study.id,
            study.innholdstype,
            interesser,
            sokeord,
            sokeord_suggest,
            sokeord_suggest_edge, 
            sokeord_suggest_ngram,
            sokeord_s,
            study.stat_vis_arb_markedskart,
            study.stat_vis_lonnstat,
            study.stat_vis_sammenligning,
            study.summary,
            study.tittel,
            title_suggest,
            title_suggest_edge,
            title_suggest_ngram,
            title_s,
            study.uno_id,
            study.update_hash,
            study.url,
            utdanningstype,
            study.path,
            study._version_,
            study.funksjon,
            study.score,
            study.sektor_antall_arbeidsledig,
            study.sektor_antall_ikkearbeid,
            study.sektor_antall_iutdanning,
            study.sektor_antall_offentlig,
            study.sektor_antall_personer,
            study.sektor_antall_privat,
            study.sektor_antall_selvstendig
        ))

    conn.executemany('''
        INSERT OR REPLACE INTO basic_studies (
            id, innholdstype, interesser, sokeord, sokeord_suggest,
            sokeord_suggest_edge, sokeord_suggest_ngram, sokeord_s,
            stat_vis_arb_markedskart, stat_vis_lonnstat, stat_vis_sammenligning,
            summary, tittel, title_suggest, title_suggest_edge,
            title_suggest_ngram, title_s, uno_id, update_hash, url,
            utdanningstype, path, _version_, funksjon, score,
            sektor_antall_arbeidsledig, sektor_antall_ikkearbeid,
            sektor_antall_iutdanning, sektor_antall_offentlig,
            sektor_antall_personer, sektor_antall_privat,
            sektor_antall_selvstendig
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', studies_data)

def main():
    session = new_session()
    search = search_studies(session)
    conn = sqlite3.connect('studies.db')
    create_tables(conn)
    #print first 100 characthes 
    parsed_data = UtdanningData(data={key: UtdanningEntry(**value) for key, value in search.items()})
    print("Total number of studies: ", len(parsed_data.data))
    # Count entries with utdanningstype "Universitet og høgskole"
    uh_count = sum(1 for entry in parsed_data.data.values() 
                   if "Universitet og høgskole" in entry.utdanningstype)
    print(f"Total number of university/college studies: {uh_count}")
    fagskole_count = sum(1 for entry in parsed_data.data.values() 
                   if "Fagskole" in entry.utdanningstype)
    print(f"Total number of fagskole studies: {fagskole_count}")
    videregaaende_count = sum(1 for entry in parsed_data.data.values() 
                   if "Videregående" in entry.utdanningstype)
    print(f"Total number of videregående studies: {videregaaende_count}")

    fagskole_and_uh_entries = [entry for entry in parsed_data.data.values() 
                  if "Universitet og høgskole" in entry.utdanningstype or "Fagskole" in entry.utdanningstype]
    print(f"Total number of university/college studies with personer: {len(fagskole_and_uh_entries)}")
    #write the 10 first to a json file
    with open(f'uh_studies.json', 'w', encoding='utf-8') as f:
        json.dump([entry.model_dump() for entry in fagskole_and_uh_entries][:1], f, indent=4, ensure_ascii=False)
    print("Wrote 1 uh studies to uh_studies.json")
    print("trying to insert")
    insert_studies(conn, fagskole_and_uh_entries)
    print("inserted")
    conn.commit()
    conn.close()

main()
