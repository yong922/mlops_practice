import numpy as np
import pandas as pd

# 근로기간 문자열을 숫자로 변환
def to_num(value):
    try:
        return int(value.split()[0])
    except ValueError:
        if value in ("10+ years", "10+yea|rs"):
            return 10
        elif value in ("< 1 year", "<1 year"):
            return 0
        else:
            return np.nan

# 근로기간 처리
def working_period_to_num(df):
    df["근로기간"] = df["근로기간"].apply(to_num)
    return df

# 상위 95% 값 제한
def upper_limit_95(df, columns):
    for col in columns:
        per95 = df[col].quantile(0.95)
        df[col] = df[col].apply(lambda x: per95 if x > per95 else x)

# 주요 전처리 과정
def feature_preprocessing(df):
    # 상한값 설정
    limit_col = ["연간소득", "총계좌수", "부채_대비_소득_비율", "총상환원금", "총상환이자", "상환원금이자비율"]
    upper_limit_95(df, limit_col)

    # 범주형 데이터 라벨 인코딩
    to_label_col = ["대출기간", "주택소유상태", "대출목적"]
    for col in to_label_col:
        df[col] = pd.factorize(df[col])[0]

    # 불필요한 실수를 정수로 변환
    to_int_col = ["연간소득", "총계좌수", "총상환이자", "총연체금액", "연체계좌수", "최근_2년간_연체_횟수", "총상환원금"]
    df[to_int_col] = df[to_int_col].astype(int)

    return df

# 파생 변수 생성
def feature_create(df):
    # 연체 관련 변수
    df["연체여부"] = df["총연체금액"].apply(lambda x: 1 if x != 0 else 0)
    df["연체계좌여부"] = df["연체계좌수"].apply(lambda x: 1 if x != 0 else 0)

    # 상환 비율 계산
    df["상환비율"] = df["총상환원금"] / df["대출금액"]
    df["상환이자비율"] = df["총상환이자"] / df["대출금액"]
    df["상환원금이자비율"] = df["총상환원금"] / (df["총상환이자"] + 1)

    # 근로 기간 및 월 상환 금액 계산
    df["장기근로자"] = df["근로기간"].apply(lambda x: 0 if x < 10 else 1)
    df["월상환금액"] = df["대출금액"] / df["대출기간"].apply(lambda x: 36 if x == " 36 months" else 60)

    return df

# 통합 전처리 함수
def preprocess_input(df):
    # 순차적으로 전처리 수행
    df = working_period_to_num(df)
    df = feature_create(df)
    df = feature_preprocessing(df)

    # 모델 입력에 필요 없는 컬럼 제거
    df = df.drop(columns=["id", "timestamp", "대출등급"], errors="ignore")

    return df
