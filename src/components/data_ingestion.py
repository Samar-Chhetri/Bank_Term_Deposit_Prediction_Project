import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException
import mysql.connector
from mysql.connector import Error

from src.utils import create_server_connection, create_db_connection, execute_query, read_query

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts', 'train.csv')
    test_data_path:str = os.path.join('artifacts', 'test.csv')
    raw_data_path:str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered into data ingestion method")
        try:

            pw = 'Mysql#11'
            db = 'bank'

            q1 = """
            Select * from bank_term_deposit;
            """
            connection = create_server_connection(host_name ='localhost', user_name='root', user_password=pw)
            connection = create_db_connection(host_name='localhost', user_name='root', db_name=db,user_password=pw)

            results = read_query(connection, q1)

            from_db = []
            
            for r in results:
                 res = list(r)
                 from_db.append(res)

            df = pd.DataFrame(from_db, columns=['age', 'job', 'marital', 'education', 'default', 'balance', 'housing','loan', 'contact', 'day', 
                                           'month', 'duration', 'campaign', 'pdays','previous', 'poutcome', 'deposit'])
            
            logging.info("Read the data from Mysql as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Train test split initiated")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=23)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )


        except Exception as e:
            raise CustomException(e, sys)
        

if __name__=="__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()