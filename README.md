# GeneralAPI

### GeneralAPI is an all purpose REST API that returns JSON data for many categories from generating QR codes and crypto exchange rates to random dad jokes.

## ------OPEN TO CONTREBUTIONS------

# Endpoints:

# Generating QR code

GET "https://general-api.vercel.app/qr/generate?data="<br>

<details>
<summary>
Response example:
</summary>

```json
{
"QR_URL":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAcwAAAHMAQAAAABwoKUrAAABVklEQVR42u3dQW7DIBAFUNQLcP9b+gapFKUxMOBKkRhn8VhYwuFtWHyNxyQpj0/HUVAURTfSo4zjee+9YrXkp3w8UBRF/xltDsUwOqdxiR1GUXR7Nh0hql7TdV7ZYRRFs7PpfIirsglF0W/KptlFNqEomptNsd80n+o3oSial03LWsp7OhRF78qmxWhbTdPjB3YYRdGMbAph9KyW6vvT8pqqm1AUTXumq20YnZfhXtcQt8Moim6um86Uuj7p1K2zwyiKpmVTWzeVUEZ1x53sMIqim7OpbTCVy+NOD/0mFEWzs2k4wTS8tvsro9RNKIpmZNOxyqvl4fDqDAGKohnZNC+ZhtZ4V0HJJhRFM7Jp9nauzi+e6VAUvSubroondROKorfWTSV0o7rOkx1GUXR7NsV+U/t1ldr/1Jzv06EompJN4V48UhCbTnYYRdGd2eQvH1AU/Tr6C2lfsq92YuBDAAAAAElFTkSuQmCC"
}
```
### Optional parameters:
• back_color: str <br>
• front_color: str<br>
• scale: int<br>
• border_size: int<br>
• border_color: str<br>

</details>

# Finance

• GET "https://general-api.vercel.app/finance/general-info?ticker="<br>
Gets the general information about the stock

<details>
<summary>Expand response example:</summary>

```json
{
  "address1": "1 Tesla Road",
  "city": "Austin",
  "state": "TX",
  "zip": "78725",
  "country": "United States",
  "phone": "512 516 8177",
  "website": "https://www.tesla.com",
  "industry": "Auto Manufacturers",
  "industryKey": "auto-manufacturers",
  "industryDisp": "Auto Manufacturers",
  "sector": "Consumer Cyclical",
  "sectorKey": "consumer-cyclical",
  "sectorDisp": "Consumer Cyclical",
  "longBusinessSummary": "Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems in the United States, China, and internationally. It operates in two segments, Automotive, and Energy Generation and Storage. The Automotive segment offers electric vehicles, as well as sells automotive regulatory credits; and non-warranty after-sales vehicle, used vehicles, retail merchandise, and vehicle insurance services. This segment also provides sedans and sport utility vehicles through direct and used vehicle sales, a network of Tesla Superchargers, and in-app upgrades; purchase financing and leasing services; services for electric vehicles through its company-owned service locations and Tesla mobile service technicians; and vehicle limited warranties and extended service plans. The Energy Generation and Storage segment engages in the design, manufacture, installation, sale, and leasing of solar energy generation and energy storage products, and related services to residential, commercial, and industrial customers and utilities through its website, stores, and galleries, as well as through a network of channel partners; and provision of service and repairs to its energy product customers, including under warranty, as well as various financing options to its solar customers. The company was formerly known as Tesla Motors, Inc. and changed its name to Tesla, Inc. in February 2017. Tesla, Inc. was incorporated in 2003 and is headquartered in Austin, Texas.",
  "fullTimeEmployees": 127855,
  "companyOfficers": [
    {
      "maxAge": 1,
      "name": "Mr. Elon R. Musk",
      "age": 50,
      "title": "Technoking of Tesla, CEO & Director",
      "yearBorn": 1972,
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 27819718656
    },
    {
      "maxAge": 1,
      "name": "Mr. Andrew D. Baglino",
      "age": 41,
      "title": "Senior Vice President of Powertrain & Energy Engineering",
      "yearBorn": 1981,
      "fiscalYear": 2022,
      "totalPay": 303000,
      "exercisedValue": 33866368,
      "unexercisedValue": 57355632
    },
    {
      "maxAge": 1,
      "name": "Mr. Vaibhav  Taneja",
      "age": 44,
      "title": "CFO, Corporate Controller & Chief Accounting Officer",
      "yearBorn": 1978,
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 0
    },
    {
      "maxAge": 1,
      "name": "Mr. Martin  Viecha",
      "title": "Senior Director for Investor Relations",
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 0
    },
    {
      "maxAge": 1,
      "name": "Mr. Alan  Prescott",
      "age": 43,
      "title": "Vice President of Legal",
      "yearBorn": 1979,
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 0
    },
    {
      "maxAge": 1,
      "name": "Mr. Dave  Arnold",
      "title": "Senior Director of Global Communications",
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 0
    },
    {
      "maxAge": 1,
      "name": "Brian  Scelfo",
      "title": "Senior Director of Corporate Development",
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 0
    },
    {
      "maxAge": 1,
      "name": "Mr. Jeffrey Brian Straubel",
      "age": 46,
      "title": "Independent Director",
      "yearBorn": 1976,
      "fiscalYear": 2022,
      "totalPay": 250560,
      "exercisedValue": 9413986,
      "unexercisedValue": 60867856
    },
    {
      "maxAge": 1,
      "name": "Mr. Franz  von Holzhausen",
      "title": "Chief Designer",
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 0
    },
    {
      "maxAge": 1,
      "name": "Mr. Xiaotong  Zhu",
      "age": 42,
      "title": "Senior Vice President of Automotive",
      "yearBorn": 1980,
      "fiscalYear": 2022,
      "exercisedValue": 0,
      "unexercisedValue": 0
    }
  ],
  "auditRisk": 8,
  "boardRisk": 9,
  "compensationRisk": 8,
  "shareHolderRightsRisk": 9,
  "overallRisk": 9,
  "governanceEpochDate": 1696118400,
  "compensationAsOfEpochDate": 1672444800,
  "maxAge": 86400,
  "priceHint": 2,
  "previousClose": 220.11,
  "open": 217.01,
  "dayLow": 210.42,
  "dayHigh": 218.8538,
  "regularMarketPreviousClose": 220.11,
  "regularMarketOpen": 217.01,
  "regularMarketDayLow": 210.42,
  "regularMarketDayHigh": 218.8538,
  "dividendYield": 0.0183,
  "payoutRatio": 0.0,
  "beta": 2.247,
  "trailingPE": 60.224434,
  "forwardPE": 55.93404,
  "volume": 136959880,
  "regularMarketVolume": 136959880,
  "averageVolume": 114622104,
  "averageVolume10days": 115745670,
  "averageDailyVolume10Day": 115745670,
  "bid": 212.75,
  "ask": 212.2,
  "bidSize": 3100,
  "askSize": 900,
  "marketCap": 672854114304,
  "fiftyTwoWeekLow": 10181,
  "fiftyTwoWeekHigh": 299.29,
  "priceToSalesTrailing12Months": 7.01445,
  "fiftyDayAverage": 249.1134,
  "twoHundredDayAverage": 214.6719,
  "trailingAnnualDividendRate": 0.0,
  "trailingAnnualDividendYield": 0.0,
  "currency": "USD",
  "enterpriseValue": 652625248256,
  "profitMargins": 0.11213,
  "floatShares": 2715321200,
  "sharesOutstanding": 3173989888,
  "sharesShort": 82428956,
  "sharesShortPriorMonth": 82093847,
  "sharesShortPreviousMonthDate": 1693440000,
  "dateShortInterest": 1695945600,
  "sharesPercentSharesOut": 0025999999,
  "heldPercentInsiders": 0.13043,
  "heldPercentInstitutions": 0.44206002,
  "shortRatio": 0.68,
  "shortPercentOfFloat": 0.0299,
  "impliedSharesOutstanding": 3173989888,
  "bookValue": 16.834,
  "priceToBook": 12.592967,
  "lastFiscalYearEnd": 1672444800,
  "nextFiscalYearEnd": 1703980800,
  "mostRecentQuarter": 1696032000,
  "earningsQuarterlyGrowth": -0.437,
  "netIncomeToCommon": 10796000256,
  "trailingEps": 3.52,
  "forwardEps": 3.79,
  "pegRatio": 21.32,
  "lastSplitFactor": "3:1",
  "lastSplitDate": 1661385600,
  "enterpriseToRevenue": 6.804,
  "enterpriseToEbitda": 43.072,
  "52WeekChange": 0003502965,
  "SandP52WeekChange": 0.1123997,
  "exchange": "NMS",
  "quoteType": "EQUITY",
  "symbol": "TSLA",
  "underlyingSymbol": "TSLA",
  "shortName": "Tesla, Inc.",
  "longName": "Tesla, Inc.",
  "firstTradeDateEpochUtc": 1277818200,
  "timeZoneFullName": "America/New_York",
  "timeZoneShortName": "EDT",
  "uuid": "ec367bc4-f92c-397c-ac81-bf7b43cffaf7",
  "messageBoardId": "finmb_27444752",
  "gmtOffSetMilliseconds": -14400000,
  "currentPrice": 211.99,
  "targetHighPrice": 358.95,
  "targetLowPrice": 2298,
  "targetMeanPrice": 218.83,
  "targetMedianPrice": 240.87,
  "recommendationMean": 2.7,
  "recommendationKey": "hold",
  "numberOfAnalystOpinions": 37,
  "totalCash": 26076999680,
  "totalCashPerShare": 8.211,
  "ebitda": 15152000000,
  "totalDebt": 4392999936,
  "quickRatio": 1.073,
  "currentRatio": 1.69,
  "totalRevenue": 95924002816,
  "debtToEquity": 8.061,
  "revenuePerShare": 30.279,
  "returnOnAssets": 0.07965,
  "returnOnEquity": 0.22459999,
  "grossProfits": 20853000000,
  "freeCashflow": 2224000000,
  "operatingCashflow": 12163999744,
  "earningsGrowth": -0.442,
  "revenueGrowth": 0088,
  "grossMargins": 0.19805999,
  "ebitdaMargins": 0.15796,
  "operatingMargins": 0.07555,
  "financialCurrency": "USD",
  "trailingPegRatio": 2.2905
}
```

</details>
<br>

• GET "https://general-api.vercel.app/finance/current-value?ticker="<br>
Gets the current value of the stock in USD<br>

Response example:

```json
{
  "current_value": 326.6700134277344
}
```

• GET "https://general-api.vercel.app/finance/currency-convert?from_curr=&to_curr=&amount=" <br>
Converts the currency<br>
Example:<br> https://general-api.vercel.app/finance/currency-convert?from_curr=usd&to_curr=eur&amount=50 <br>
Result:

```json
{
  "result": 47.17999994754791
}
```

# Entertainment
### Random dad joke
• GET "https://general-api.vercel.app/entertainment/dad-joke" <br>
```json
{
    "joke":"A man walked in to a bar with some asphalt on his arm. He said “Two beers please, one for me and one for the road.”"
}
```
### Random yo momma joke
• GET "https://general-api.vercel.app/entertainment/yo-momma-joke" <br>
```json
{
    "joke":"Yo mamma so fat Bill Gates couldn't pay for her liposuction"
}
```
### Random chuck norris joke
• GET "https://general-api.vercel.app/entertainment/yo-momma-joke" <br>
```json
{
    "joke":"Chuck Norris always has to have sex with large groups of women, to distribute the 'workload' - if he ever fucks a single woman, the intensity of the orgasm will induce spontaneous combustion."
}
```
### Random facts
• GET "https://general-api.vercel.app/entertainment/random-fact"
```json
{
    "fact":"One quarter of the bones in your body are in your feet."
}
```
### Random riddle
• GET "https://general-api.vercel.app/entertainment/random-riddle"
```json
{
    "riddle":"How do you make “one”disappear?",
    "answer":"Add a “g”to make it “gone”or an “n”to make it “none“!"
}
```