# -*- coding: utf-8 -*-
"""
buggy_1.py  ―  판매 데이터 매출 집계 (csv 모듈 버전)

dirty_sales.csv를 한 줄씩 읽어 '매출액 = 단가 x 수량'을 누적한다.
잘 돌아가는 것처럼 보이지만, 어떤 행에서 갑자기 멈춘다.

[과제] 이 스크립트를 실행해 Traceback을 얻고,
       진단 3단계 루틴(무엇이 / 어디서 / 왜)으로 원인을 특정한 뒤
       전처리로 해결하라. (힌트: 예외 타입은 무엇인가?)
"""
import csv



def calc_total(path): 
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # 사전타입으로 데이터를 읽음.
        """FIXED : 문자에 ,가 삽입되어 ValueError 발생. 이후 확인해보니 다른 행에서 '원', 빈값으로 인하여 Error가 발생할 가능성을 수정하고자 
            빈 값이 존재하는 행에 대해서는 이후 행으로 넘긴 뒤, .replace를 이용하여 ,와 원을 제거하면서 price와 quantity의 값을 int로 변환"""
        for i, row in enumerate(reader):
            price_text = row["price"].strip()
            qty_text = row["quantity"].strip()

            if price_text == "" or qty_text == "":
                print(f"{i}행: 빈 값이 있어 건너뜀")
                continue

            price = int(
                price_text
                .replace(",", "")
                .replace("원", "")
            )
            qty = int(qty_text)
            total += price * qty
    return total

if __name__ == "__main__":
    total = calc_total("./dirty_sales.csv")
    print(f"총 매출액: {total:,}원")
