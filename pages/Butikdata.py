import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
 
con = sqlite3.connect(r"C:\Users\Nevai\OneDrive\Desktop\Skolarbete\Data Science\Kunskapskontrol_3\Köksglädje.db")

# df med data från kunder
Kunddata_df = pd.read_sql('''
    SELECT c.CustomerID,
        JoinDate,
        COUNT(DISTINCT t.TransactionID) AS TotalTransactions,
        MIN(DATE(t.TransactionDate)) AS FirstTransactionDate,
        MAX(DATE(t.TransactionDate)) AS LastTransactionDate
    FROM Customers c
    JOIN Transactions t ON c.CustomerID = t.CustomerID
    JOIN TransactionDetails td ON t.TransactionID = td.TransactionID
    GROUP BY c.CustomerID, c.JoinDate
    ORDER BY TotalTransactions
    ''', con)

Kunddata_df_sorted = Kunddata_df["TotalTransactions"].value_counts().sort_index()

Kunddata_df_purchase_dates = pd.read_sql('''
    SELECT
        substr(t.TransactionDate, 1, 7) as PurchaseDate,
        COUNT(DISTINCT c.CustomerID) AS NumCustomers
    FROM Customers c
    JOIN Transactions t ON c.CustomerID = t.CustomerID
    JOIN TransactionDetails td ON t.TransactionID = td.TransactionID
    GROUP BY substr(t.TransactionDate, 1, 7)
    ORDER BY PurchaseDate
''', con)

# df med data sorterat med kategori
Category_df = pd.read_sql('''
    SELECT p.CategoryName,
        SUM(t.Quantity) AS TotalSold,
        SUM(t.PriceAtPurchase * t.Quantity) AS ActualPrice,
        SUM(p.CostPrice * t.Quantity) AS TotalCost,
        SUM(t.PriceAtPurchase * t.Quantity) - SUM(p.CostPrice * t.Quantity) AS Margin,
        (SUM(t.PriceAtPurchase * t.Quantity) - SUM(p.CostPrice * t.Quantity)) / SUM(t.PriceAtPurchase * t.Quantity) * 100 AS MarginPercentage
    FROM TransactionDetails t
    JOIN Products p ON t.ProductID = p.ProductID
    GROUP BY p.CategoryName
               
    UNION ALL
               
    SELECT "Total" AS CategoryName,
        SUM(t.Quantity),
        SUM(t.PriceAtPurchase * t.Quantity),
        SUM(p.CostPrice * t.Quantity) AS TotalCost,
        SUM(t.PriceAtPurchase * t.Quantity) - SUM(p.CostPrice * t.Quantity) AS Margin,
        (SUM(t.PriceAtPurchase * t.Quantity) - SUM(p.CostPrice * t.Quantity)) / SUM(t.PriceAtPurchase * t.Quantity) * 100 AS MarginPercentage
    FROM TransactionDetails t
    JOIN Products p ON t.ProductID = p.ProductID
    ''', con)

Category_df_NoTotal = Category_df[Category_df["CategoryName"] != "Total"]
Category_df_OnlyTotal = Category_df[Category_df["CategoryName"] == "Total"]

# df med butik data
Butik_df = pd.read_sql('''
SELECT s.StoreName AS Butik,
        SUM(td.Quantity) AS TotalSold,
        SUM(td.PriceAtPurchase * td.Quantity) AS ActualPrice,
        SUM(p.CostPrice * td.Quantity) AS TotalCost,
        SUM(td.PriceAtPurchase * td.Quantity) - SUM(p.CostPrice * td.Quantity) AS Margin,
        (SUM(td.PriceAtPurchase * td.Quantity) - SUM(p.CostPrice * td.Quantity)) / SUM(td.PriceAtPurchase * td.Quantity) * 100 AS MarginPercentage
        FROM Stores s
        JOIN Transactions t ON s.StoreID = t.StoreID
        JOIN TransactionDetails td ON t.TransactionID = td.TransactionID
        JOIN Products p ON td.ProductID = p.ProductID
        GROUP BY s.StoreName
                       
        UNION ALL

        SELECT 
        'Total' AS Butik,
        SUM(td.Quantity) AS TotalSold,
        SUM(td.PriceAtPurchase * td.Quantity) AS ActualPrice,
        SUM(p.CostPrice * td.Quantity) AS TotalCost,
        SUM(td.PriceAtPurchase * td.Quantity) - SUM(p.CostPrice * td.Quantity) AS Margin,
        (SUM(td.PriceAtPurchase * td.Quantity) - SUM(p.CostPrice * td.Quantity)) / SUM(td.PriceAtPurchase * td.Quantity) * 100 AS MarginPercentage
        FROM Stores s
        JOIN Transactions t ON s.StoreID = t.StoreID
        JOIN TransactionDetails td ON t.TransactionID = td.TransactionID
        JOIN Products p ON td.ProductID = p.ProductID;
''', con)


Butik_df_NoTotal = Butik_df[Butik_df["Butik"] != "Total"]

st.sidebar.title("Alternativ")
Data = st.sidebar.selectbox("Välj dataset", [ "Butik", "Kategori", "Kund"])



# Ändrar vilken data som är synlig i streamlit appen beroende på vad användaren väljer
if Data == "Butik":
    Filter = st.sidebar.selectbox("Hur vill du filtrera det?", ["Försäljning", "Kostnad", "Marginal", "Total"])

    if Filter == "Försäljning":
        st.title("Försäljning Butik")
        st.bar_chart(Butik_df_NoTotal, x="Butik", y="ActualPrice", horizontal=True)

    elif Filter == "Kostnad":
        st.title("Kostnad Butik")
        st.bar_chart(Butik_df_NoTotal, x="Butik", y="TotalCost", horizontal=True)

    elif Filter == "Marginal":
        st.title("Marginal Butik")
        st.bar_chart(Butik_df_NoTotal, x="Butik", y="Margin", horizontal=True)
        st.bar_chart(Butik_df_NoTotal, x="Butik", y="MarginPercentage", horizontal=True)

    elif Filter == "Total":
        st.title("Total Data")
        st.write(Butik_df)
    

elif Data == "Kategori":
    Filter = st.sidebar.selectbox("Hur vill du filtrera det?", ["Försäljning", "Kostnad", "Marginal", "Total"])

    if Filter == "Försäljning":
        st.title("Försäljning Kategori")

        st.bar_chart(Category_df_NoTotal, x="CategoryName", y="ActualPrice", x_label="Försäljning", y_label="Kategori", horizontal=True)

    elif Filter == "Kostnad":
        st.title("Kostnad Kategori")
        st.bar_chart(Category_df_NoTotal, x="CategoryName", y="TotalCost", x_label="Kostnad", y_label="Kategori", horizontal=True)
        
    elif Filter == "Marginal":
        st.subheader("Marginal Kategori")
        st.bar_chart(Category_df_NoTotal, x="CategoryName", y="Margin", x_label="Margin", y_label="Kategori", horizontal=True)

        st.subheader("Marginal Kategori Procent")
        st.bar_chart(Category_df_NoTotal, x="CategoryName", y="MarginPercentage", x_label="Margin Procent", y_label="Kategori", horizontal=True)

    elif Filter == "Total":
        st.subheader("Total Data")
        st.write(Category_df)


elif Data == "Kund":
    Filter = st.sidebar.selectbox("Hur vill du filtrera det?", ["Köp Statistik", "Kund Registrering"])
    if Filter == "Köp Statistik":
        st.subheader("Kund Köp Historik")
        st.bar_chart(Kunddata_df_sorted, y_label="Antal Kunder", x_label="Antal Köp")

    elif Filter == "Kund Registrering":
        st.subheader("Kund Data kring Registrering")

        st.bar_chart(Kunddata_df_purchase_dates.set_index('PurchaseDate')['NumCustomers'], horizontal=True)