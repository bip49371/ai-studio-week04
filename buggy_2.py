# -*- coding: utf-8 -*-
"""
buggy_2.py  ―  카테고리별 매출 집계 (pandas 버전)

dirty_sales.csv를 pandas로 읽어 카테고리별 매출 합계를 구하려 한다.
그런데 실행하자마자 죽는다.

[과제] Traceback을 얻어 예외 타입을 확인하고,
       '원인을 데이터에서 직접 확인'한 뒤(힌트: 실제 컬럼명이 무엇인가?)
       코드를 수정하라.
"""
import pandas as pd

def load(path):
    df = pd.read_csv(path, encoding="utf-8")
    return df

def summarize(df):
    # 단가 x 수량으로 매출액 컬럼을 만든 뒤 카테고리별 합계를 낸다
    
    df["매출액"] = df["price"] * df["quantity"]        # 단가, 수량 대신 본래 열인 price, quantity 사용
    return df.groupby("category")["매출액"].sum()

def summarize(df):
    # 단가 x 수량으로 매출액 컬럼을 만든 뒤 카테고리별 합계를 낸다
    df["price"] = pd.to_numeric(df["price"], errors="coerce") #price, quantity행을 숫자로 변환. errors="coerce"를 통해 변환 불가능한 행 NaN으로 표시
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    print("숫자로 변환하지 못한 행:")
    print(df[df["price"].isna() | df["quantity"].isna()]) #결측값인지 검사하여 True, False 반환하고 결측값이면 출력.

    df["매출액"] = df["price"] * df["quantity"]

    return df.groupby("category")["매출액"].sum()

if __name__ == "__main__":
    df = load("dirty_sales.csv")
    result = summarize(df)
    print(result)
