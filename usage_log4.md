buggy_4

df.info(), df.describe(), df.isna().sum()의 결과는 다음과 같으며, 이를 통해서 결측이 있는 행의 존재를 확인함
(500, 6)
<class 'pandas.DataFrame'>
RangeIndex: 500 entries, 0 to 499
Data columns (total 6 columns):
 #   Column    Non-Null Count  Dtype  
---  ------    --------------  -----  
 0   date      500 non-null    str    
 1   product   500 non-null    str    
 2   category  490 non-null    str    
 3   price     498 non-null    float64
 4   quantity  500 non-null    int64  
 5   stock     485 non-null    float64
dtypes: float64(2), int64(1), str(3)
memory usage: 23.6 KB
None
date         0
product      0
category    10
price        2
quantity     0
stock       15
dtype: int64


price(df["price"].describe()) 를 통해서 이상치 확인. 결과는 다음과 같다. 
count    4.980000e+02
mean     2.834237e+04
std      4.477810e+05
min     -4.500000e+03
25%      3.800000e+03
50%      5.000000e+03
75%      1.200000e+04
max      9.999999e+06
Name: price, dtype: float64


    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    outliers = df[(df["price"] < lower) | (df["price"]>upper) | (df["price"] <0)]
    print(f"이상치 {len(outliers)}건 / 전체 {len(df)}건")
    print(outliers)
위의 코드를 통해서 IQR 1.5배 이상 벗어난 심각한 outlier를 확인하였다.
date product category      price  quantity  stock
199  2026-02-04     마들렌     베이커리    -4500.0       119   93.0
250  2026-02-19    카페라떼       음료  9999999.0        76  116.0


이상치와 NaN 값으로 인하여 총 매출액을 믿을 수 없는 상황이다. 그러므로 NaN, 이상치를 건너뛰고 sum()하고 제외된 값을 추출하도록 코드를 구성하기로 프롬프트를 작성하기로 결정. 

프롬프트 : 월별 매출 집계 스크립트야. 이상치와 NaN값을 제외하고 sum할 수 있도록 코드 수정 제안해줘. 제외된 행은 제외되었다고 출력할 수 있도록 해줘. 


def main():
    df = pd.read_csv("dirty_sales.csv", encoding="utf-8")

    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    #결측치 및 이상치 행 확인
    print(df.isna().sum())
    print(df[df["price"].isna()].head())

    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    outliers = df[(df["price"] < lower) | (df["price"]>upper) | (df["price"] <0)]
    print(f"이상치 {len(outliers)}건 / 전체 {len(df)}건")
    print(outliers)

    df["revenue"] = df["price"] * df["quantity"]

    total = df["revenue"].sum()
    avg_price = df["price"].mean()

    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")



AI 답변 요지 :
수정 코드 제시

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

    ![alt text](image-3.png)



___

AI에게 코드에 설명을 요구. 

본인의 의견 : 
의도했던 바(잘못된 행의 출력 및 제거)를 정확하게 수정에 반영하였음을 확인하였다. 
1. replace를 통하여 ",", "원"이 포함된 값을 숫자만으로 고침
2. to_numeric을 통하여 str인 price의 값들을 숫자로 고침. 이 과정에서 errors="coerce"를 통하여 숫자로만 이루어진 값은 NaN으로 변환
3. isna()를 통하여 NaN 값이 포함되었는지 확인
4. IQR 방식으로 이상치 구함.
5. 4에서 구한 이상치 범위에 포함되는 행을 구함.
6. NaN이 포함된 행을 구함
7. 5,6에서 구한 행의 합집합을 구함
8. 제외된 행에 대한 출력
9. ~를 통하여 7로부터 정상 행만을 구함
10. 11. 정상 행으로만 계산




답변 전문:
물론. 수정한 코드의 핵심은 **“문제가 있는 행을 먼저 표시한 뒤, 그 행들을 제외한 데이터로만 매출을 계산한다”**는 흐름이야.

원래 코드는 이상치를 찾아서 `outliers`에 저장하고 출력은 했지만, 실제 계산은 여전히 원본 `df`를 사용했어.

```python
df["revenue"] = df["price"] * df["quantity"]
total = df["revenue"].sum()
```

그래서 이상치가 발견돼도 `total` 계산에는 그대로 포함되는 문제가 있었어. 수정 코드에서는 이 부분을 해결한 거야.

### 1. `price` 문자열 정리

```python
df["price"] = (df["price"].astype(str)
                          .str.replace(",", "", regex=False)
                          .str.replace("원", "", regex=False)
                          .str.strip())
```

예를 들어 데이터가

```text
"5,200원"
```

이면 그대로는 숫자로 바꿀 수 없으니까,

```text
"5,200원"
→ "5200원"
→ "5200"
```

처럼 정리해.

`str.strip()`은 앞뒤 공백도 제거해.

`regex=False`는 여기서 `","`, `"원"`을 정규표현식이 아니라 그냥 일반 문자열로 처리하라는 뜻이야.

---

### 2. 숫자로 변환

```python
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
```

`pd.to_numeric()`은 데이터를 숫자로 변환해.

여기서 중요한 건

```python
errors="coerce"
```

야.

숫자로 바꿀 수 없는 값이 있으면 에러를 내는 대신 `NaN`으로 바꿔줘.

예를 들어

```text
"5200" → 5200
"4000" → 4000
"abc" → NaN
"" → NaN
```

이렇게 돼.

`quantity`도 마찬가지로 숫자가 아닌 값이 있을 수 있으니까 같이 처리한 거야.

---

### 3. 결측치 확인

```python
print(df.isna().sum())
```

각 열에 `NaN`이 몇 개 있는지 보여줘.

예를 들어

```text
price       2
quantity    1
```

처럼 나오면 `price`에 결측치 2개, `quantity`에 1개가 있다는 뜻이야.

---

### 4. IQR을 이용해서 이상치 기준 계산

```python
q1 = df["price"].quantile(0.25)
q3 = df["price"].quantile(0.75)
iqr = q3 - q1
```

여기서는 IQR 방식으로 이상치를 찾고 있어.

* `q1`: 하위 25% 지점
* `q3`: 하위 75% 지점
* `iqr`: `q3 - q1`

그리고

```python
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
```

를 이용해서 정상 범위를 정해.

즉,

```text
lower 이상 ~ upper 이하
```

정도를 정상 범위로 보는 거야.

---

### 5. 이상치인 행 표시

```python
outlier_mask = (
    (df["price"] < lower) |
    (df["price"] > upper) |
    (df["price"] < 0)
)
```

여기서 `mask`는 각 행에 대해 `True / False`를 저장하는 조건표라고 생각하면 돼.

예를 들어 가격이

```text
4500
5000
-3000
9999999
```

라면 상황에 따라

```text
False
False
True
True
```

처럼 나올 수 있어.

`|`는 OR 조건이야.

즉 아래 조건 중 하나라도 만족하면 이상치로 판단해.

```python
price < lower
price > upper
price < 0
```

특히

```python
(df["price"] < 0)
```

를 따로 넣은 이유는 **가격이 음수인 경우는 매출 데이터상 비정상값이라고 판단하기 위해서**야.

---

### 6. NaN이 포함된 행 표시

```python
nan_mask = (
    df["price"].isna() |
    df["quantity"].isna()
)
```

여기도 마찬가지로 `True / False` 조건표를 만드는 거야.

예를 들어

```text
price     quantity
5000      2
NaN       1
4000      NaN
```

이라면 결과는 대략

```text
False
True
True
```

가 돼.

즉 `price` 또는 `quantity` 둘 중 하나라도 `NaN`이면 그 행을 계산에서 제외해.

왜냐하면 매출액은

```python
price * quantity
```

이기 때문에 둘 중 하나라도 없으면 정상적인 매출 계산을 할 수 없기 때문이야.

---

### 7. 이상치와 NaN을 한 번에 묶기

```python
exclude_mask = outlier_mask | nan_mask
```

이 부분이 수정 코드의 핵심 중 하나야.

뜻은:

> 이상치이거나 NaN인 행을 모두 제외 대상으로 지정

이야.

즉,

```text
이상치 → 제외
NaN → 제외
둘 다 해당 → 제외
정상 → 유지
```

가 돼.

---

### 8. 실제로 제외될 행 확인

```python
excluded = df[exclude_mask]
```

`exclude_mask`가 `True`인 행만 가져와.

그래서 `excluded`에는 계산에서 빠질 행들이 들어가.

```python
print(f"\n제외된 행: {len(excluded)}건 / 전체 {len(df)}건")
print(excluded)
```

예를 들어 출력이

```text
제외된 행: 3건 / 전체 500건
```

이라고 나오면 전체 500개 데이터 중 3개를 매출 계산에서 제외했다는 뜻이야.

---

### 9. 정상 행만 가져오기

```python
clean_df = df[~exclude_mask].copy()
```

여기가 제일 중요해.

`~`는 Boolean 값을 반대로 바꾸는 연산자야.

원래

```text
exclude_mask

True
False
True
False
```

였다면

```python
~exclude_mask
```

는

```text
False
True
False
True
```

가 돼.

즉,

```python
df[~exclude_mask]
```

는 **제외 대상이 아닌 정상 행만 가져오는 것**이야.

`.copy()`는 이렇게 선택한 데이터를 별도의 DataFrame으로 복사해두는 거야.

그래서 이후 `clean_df`를 수정해도 원본 `df`에 예상치 못한 영향을 주는 일을 줄일 수 있어.

---

### 10. 정상 데이터로만 매출 계산

```python
clean_df["revenue"] = clean_df["price"] * clean_df["quantity"]
```

이제 이상치와 NaN이 제거된 데이터만 가지고

```text
매출액 = 가격 × 수량
```

을 계산해.

예를 들어

```text
price   quantity   revenue
5000    2          10000
4000    3          12000
```

가 되는 거야.

---

### 11. 합계와 평균 계산

```python
total = clean_df["revenue"].sum()
avg_price = clean_df["price"].mean()
```

여기서 중요한 차이는 원래 코드가

```python
df
```

를 사용했다면 수정 코드에서는

```python
clean_df
```

를 사용한다는 점이야.

즉,

```python
total = clean_df["revenue"].sum()
```

은 **NaN과 이상치를 제외한 매출액만 합산**하게 돼.

---

전체 흐름을 아주 간단히 정리하면 이렇게 보면 돼.

```text
CSV 읽기
   ↓
price 문자열 정리
   ↓
숫자 변환
   ↓
NaN 찾기
   ↓
IQR로 이상치 찾기
   ↓
NaN 또는 이상치인 행 표시
   ↓
제외된 행 출력
   ↓
정상 행만 clean_df에 저장
   ↓
clean_df로 매출액 계산
   ↓
총매출 / 평균단가 계산
```

과제 보고서에 설명한다면 핵심은 이렇게 적으면 깔끔해:

> `price`와 `quantity` 열을 숫자형으로 변환한 후, 숫자로 변환할 수 없는 값은 `NaN`으로 처리하였다. 이후 IQR 방식으로 가격 이상치를 탐지하고, 결측치 또는 이상치에 해당하는 행을 `exclude_mask`로 구분하였다. 제외 대상 행은 별도로 출력하고, `~exclude_mask`를 이용하여 정상 데이터만 `clean_df`에 저장하였다. 최종 매출액 합계와 평균 단가는 `clean_df`를 기준으로 계산하여 결측치와 이상치가 집계 결과에 포함되지 않도록 하였다.
