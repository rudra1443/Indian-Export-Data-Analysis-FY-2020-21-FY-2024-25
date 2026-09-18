SELECT * FROM india_trade_master itm ;

## Question_01:- Which Financial Years had Indian Export Trade Value above the overall average Export Trade Value?

SELECT
    Financial_Year,
    SUM(Trade_Value_Crore) AS Total_Export_Value
FROM India_Trade_Master
GROUP BY Financial_Year
HAVING SUM(Trade_Value_Crore) >
(
    SELECT AVG(Yearly_Total)
    FROM
    (
        SELECT
            Financial_Year,
            SUM(Trade_Value_Crore) AS Yearly_Total
        FROM India_Trade_Master
        GROUP BY Financial_Year
    ) AS Yearly_Data
)
ORDER BY Total_Export_Value DESC;

## Question_02:- Which Commodities consistently appeared amoung the top 10 export commodities across the 5 Financial Year?

WITH Commodity_Year_Value AS
(
    SELECT
        Financial_Year,
        HS_Code,
        Commodity,
        SUM(Trade_Value_Crore) AS Export_Value
    FROM India_Trade_Master
    GROUP BY
        Financial_Year,
        HS_Code,
        Commodity
),

Ranked_Commodities AS
(
    SELECT
        Financial_Year,
        HS_Code,
        Commodity,
        Export_Value,
        RANK() OVER
        (
            PARTITION BY Financial_Year
            ORDER BY Export_Value DESC
        ) AS Commodity_Rank
    FROM Commodity_Year_Value
)

SELECT
    HS_Code,
    Commodity,
    COUNT(*) AS Years_In_Top_10
FROM india_trade_master itm 
WHERE Commodity_Rank <= 10
GROUP BY
    HS_Code,
    Commodity
ORDER BY Years_In_Top_10 DESC;

## Question_03:- Which HS Chapters had the highest average Export Trade Value per Financial Year?

SELECT 
  HS_Code,
  Commodity,
  AVG(Trade_Value_Crore) AS 
  Average_Export_value,
  COUNT(DISTINCT Financial_Year) AS Year_Covered
  FROM india_trade_master itm 
  GROUP BY 
   hs_code,
   commodity
   ORDER BY average_export_value DESC LIMIT 10;


## Question_04:- Which Commodities experied negative YoY Export Growth most frequently?

SELECT
    HS_Code,
    Commodity,
    COUNT(*) AS Years_With_Data,
    SUM(
        CASE
            WHEN YoY_Growth_Pct < 0 THEN 1
            ELSE 0
        END
    ) AS Negative_Growth_Years
FROM India_Trade_Master
GROUP BY
    HS_Code,
    Commodity
ORDER BY Negative_Growth_Years DESC,
         Years_With_Data DESC
LIMIT 10;

## Question_05:- Which Commodities have high Export Trade Value but relatively Low Market Share?

SELECT
    HS_Code,
    Commodity,
    SUM(Trade_Value_Crore) AS Total_Export_Value,
    AVG(Market_share_Pct) AS Average_Market_Share
FROM India_Trade_Master
GROUP BY
    HS_Code,
    Commodity
HAVING
    SUM(Trade_Value_Crore) >
    (
        SELECT AVG(Total_Value)
        FROM
        (
            SELECT
                HS_Code,
                SUM(Trade_Value_Crore) AS Total_Value
            FROM India_Trade_Master
            GROUP BY HS_Code
        ) AS Commodity_Values
    )
    AND
    AVG(Market_share_Pct) <
    (
        SELECT AVG(Market_share_Pct)
        FROM India_Trade_Master
    )
ORDER BY Total_Export_Value DESC;

## Question_06:- Which Commodities Show high YoY Growth but relatively Low Export Trade Value?

SELECT
    HS_Code,
    Commodity,
    AVG(YoY_Growth_Pct) AS Average_YoY_Growth,
    SUM(Trade_Value_Crore) AS Total_Export_Value
FROM India_Trade_Master
GROUP BY
    HS_Code,
    Commodity
HAVING
    AVG(YoY_Growth_Pct) >
    (
        SELECT AVG(YoY_Growth_Pct)
        FROM India_Trade_Master
    )
    AND
    SUM(Trade_Value_Crore) <
    (
        SELECT AVG(Total_Value)
        FROM
        (
            SELECT
                HS_Code,
                SUM(Trade_Value_Crore) AS Total_Value
            FROM India_Trade_Master
            GROUP BY HS_Code
        ) AS Commodity_Values
    )
ORDER BY Average_YoY_Growth DESC
LIMIT 10;

## Question_07:- How did Indian total Export Trade Value Change Compareed with the Previous Financial Year?
USE ravvion_datalab;

SELECT
    '2021-2022' AS Financial_Year,
    3147021.51 AS Total_Export_Value,
    2219854.12 AS Previous_Year_Value,
    ROUND(((3147021.51 - 2219854.12) / 2219854.12) * 100, 2) AS YoY_Change_Pct

UNION ALL

SELECT
    '2022-2023',
    3621549.88,
    3147021.51,
    ROUND(((3621549.88 - 3147021.51) / 3147021.51) * 100, 2)

UNION ALL

SELECT
    '2023-2024',
    3618952.26,
    3621549.88,
    ROUND(((3618952.26 - 3621549.88) / 3621549.88) * 100, 2)

UNION ALL

SELECT
    '2024-2025',
    3703412.03,
    3618952.26,
    ROUND(((3703412.03 - 3618952.26) / 3618952.26) * 100, 2);

## Question_08:- What was the rank of each Commodity within its Financial Year based on Export Trade Value?

USE ravvion_datalab;

SELECT
    Financial_Year,
    HS_Code,
    Commodity,
    SUM(Trade_Value_Crore) AS Export_Value
FROM India_Trade_Master
GROUP BY
    Financial_Year,
    HS_Code,
    Commodity
ORDER BY
    Financial_Year,
    Export_Value DESC;


## Question_09:- Which commodities contribute the largest share of India total Export Trade Value across the 5-year period?
USE Ravvion_DataLab;

SELECT
    HS_Code,
    Commodity,
    ROUND(SUM(Trade_Value_Crore), 2) AS Total_Export_Value,
    ROUND(
        SUM(Trade_Value_Crore) /
        (SELECT SUM(Trade_Value_Crore)
         FROM India_Trade_Master) * 100,
        2
    ) AS Contribution_Pct
FROM India_Trade_Master
GROUP BY
    HS_Code,
    Commodity
ORDER BY
    Total_Export_Value DESC
LIMIT 10;

## Question_10:-Which Commodities have the strongest combination of Export Value, Growth and market Share?

USE Ravvion_DataLab;

SELECT
    HS_Code,
    Commodity,
    ROUND(SUM(Trade_Value_Crore), 2) AS Total_Export_Value,
    ROUND(AVG(YoY_Growth_Pct), 2) AS Avg_Growth,
    ROUND(AVG(Market_share_Pct), 4) AS Avg_Market_Share
FROM India_Trade_Master
GROUP BY HS_Code, Commodity;



















































   













