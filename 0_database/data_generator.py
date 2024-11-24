import time
from argparse import ArgumentParser
import pandas as pd
import psycopg2


def create_table(db_connect):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS loan_data (
        ID TEXT PRIMARY KEY,
        timestamp TIMESTAMP,
        대출금액 BIGINT,
        대출기간 TEXT,
        근로기간 TEXT,
        주택소유상태 TEXT,
        연간소득 BIGINT,
        부채_대비_소득_비율 FLOAT8,
        총계좌수 INT,
        대출목적 TEXT,
        최근_2년간_연체_횟수 INT,
        총상환원금 BIGINT,
        총상환이자 FLOAT8,
        총연체금액 FLOAT8,
        연체계좌수 FLOAT8,
        대출등급 TEXT
    );"""
    # print(create_table_query)
    with db_connect.cursor() as cur:
        cur.execute(create_table_query)
        db_connect.commit()


def insert_data(db_connect, data):
    insert_row_query = f"""
    INSERT INTO loan_data
        (ID, timestamp, 대출금액, 대출기간, 근로기간, 주택소유상태, 연간소득, 부채_대비_소득_비율, 총계좌수,
         대출목적, 최근_2년간_연체_횟수, 총상환원금, 총상환이자, 총연체금액, 연체계좌수, 대출등급)
        VALUES (
            '{data.ID}',
            NOW(),
            {data.대출금액},
            '{data.대출기간}',
            '{data.근로기간}',
            '{data.주택소유상태}',
            {data.연간소득},
            {data.부채_대비_소득_비율},
            {data.총계좌수},
            '{data.대출목적}',
            {data.최근_2년간_연체_횟수},
            {data.총상환원금},
            {data.총상환이자},
            {data.총연체금액},
            {data.연체계좌수},
            '{data.대출등급}'
        );
    """
    # print(insert_row_query)
    with db_connect.cursor() as cur:
        cur.execute(insert_row_query)
        db_connect.commit()


def generate_data(db_connect, df):
    for _, row in df.iterrows():
        insert_data(db_connect, row)
        time.sleep(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--db-host", dest="db_host", type=str, default="localhost")
    args = parser.parse_args()

    db_connect = psycopg2.connect(
        user="pguser",
        password="pgpassword",
        host=args.db_host,
        port=5432,
        database="pgdatabase",
    )
    create_table(db_connect)
    df = pd.read_csv('/user/app/data/train.csv')
    generate_data(db_connect, df)
