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

    # 결측치 확인
    print("결측치 개수")
    print(df.isna().sum())

    # 이상치 기준 계산
    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    # 이상치 조건
    outlier_mask = (
        (df["price"] < lower) |
        (df["price"] > upper) |
        (df["price"] < 0)
    )

    # NaN 조건
    nan_mask = (
        df["price"].isna() |
        df["quantity"].isna()
    )

    # 제외할 행
    exclude_mask = outlier_mask | nan_mask
    excluded = df[exclude_mask]

    print(f"\n제외된 행: {len(excluded)}건 / 전체 {len(df)}건")
    print(excluded)

    # 정상 데이터만 남김
    clean_df = df[~exclude_mask].copy()

    # 정상 데이터로 매출 계산
    clean_df["revenue"] = clean_df["price"] * clean_df["quantity"]

    total = clean_df["revenue"].sum()
    avg_price = clean_df["price"].mean()

    print(f"\n집계에 사용된 행: {len(clean_df)}건")
    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")
    
if __name__ == "__main__":
    main()
