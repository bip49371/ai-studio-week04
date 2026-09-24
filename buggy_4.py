# -*- coding: utf-8 -*-
"""
buggy_4.py  ―  총 매출액 집계 (에러 없이 '조용히' 틀리는 스크립트)

이 스크립트는 에러 없이 잘 돌아가고, 그럴듯한 숫자를 출력한다.
하지만 그 숫자는 '틀렸다'.

[과제] 이 스크립트는 예외를 던지지 않는다. 대신
       (1) info()/describe()로 데이터 상태를 먼저 세어 보고
       (2) '무엇이 틀렸는지 어떻게 알아챘는지'를 서술한 뒤
       (3) 결측 규모를 보고하고 처리 방법을 선택·적용하여
           올바른 총매출을 산출하라.
       (힌트: 가격 결측은 몇 건인가? 음수 가격과 9999999 같은 값은 정상인가?)
"""
import pandas as pd

def main():
    df = pd.read_csv("dirty_sales.csv", encoding="utf-8")

    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    #FIXED: NaN, 이상치를 건너뛰고 sum()하고 제외된 값을 추출하도록 코드를 구성
    print("결측치 개수")
    print(df.isna().sum())

    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outlier_mask = (
        (df["price"] < lower) |
        (df["price"] > upper) |
        (df["price"] < 0)
    )

    nan_mask = (
        df["price"].isna() |
        df["quantity"].isna()
    )

    exclude_mask = outlier_mask | nan_mask
    excluded = df[exclude_mask]

    print(f"\n제외된 행: {len(excluded)}건 / 전체 {len(df)}건")
    print(excluded)

    clean_df = df[~exclude_mask].copy()

    clean_df["revenue"] = clean_df["price"] * clean_df["quantity"]

    total = clean_df["revenue"].sum()
    avg_price = clean_df["price"].mean()

    print(f"\n집계에 사용된 행: {len(clean_df)}건")
    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")
    
if __name__ == "__main__":
    main()
