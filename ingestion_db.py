import pandas as pd
import os
from sqlalchemy import create_engine
import logging 
import time

logging.basicConfig(
    filename = "logs/ingestion_db.log",
    level = logging.DEBUG,
    format = ("%(asctime)s - %(levelname)s - %(message)s"),
    filemode = "a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    ''' This function will ingest dataframe into database table '''
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

def load_raw_data():
    ''' This function will load CSVs as dataframe and ingest inot db '''
    start = time.time()
    for file in os.listdir('Raw_data'):        
        if '.csv' in file:
            df = pd.read_csv('Raw_data/'+file)
            logging.info(f"Ingesting {file} in db")
            # file[:-4] -- here i m doing the index slicing removing the .csv from the file name
            ingest_db(df, file[:-4], engine)
    end = time.time()
    # when we subtract end - start it gives in seconds hence we divide it by 60 to convert it to mins
    total_time = (end - start)/60    
    logging.info('----Ingestion Complet----')
    
    logging.info(f'time taken to complet the ingestion: {total_time}')

if __name__ == '__main__':
    load_raw_data()
