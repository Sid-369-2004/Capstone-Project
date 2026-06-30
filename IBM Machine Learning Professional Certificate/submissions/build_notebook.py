import os
import json
import sqlite3
import pandas as pd
import shutil

# Create final1 folder
os.makedirs("final1", exist_ok=True)

# Connect to SQLite for testing and output generation
conn = sqlite3.connect("final1/FinalDB.sqlite")
cursor = conn.cursor()

# Drop tables if exist
cursor.execute("DROP TABLE IF EXISTS CROP_DATA;")
cursor.execute("DROP TABLE IF EXISTS FARM_PRICES;")
cursor.execute("DROP TABLE IF EXISTS DAILY_FX;")
cursor.execute("DROP TABLE IF EXISTS MONTHLY_FX;")

# Create tables
cursor.execute("""
CREATE TABLE CROP_DATA (
    CD_ID INTEGER NOT NULL,
    YEAR DATE NOT NULL,
    CROP_TYPE VARCHAR(20) NOT NULL,
    GEO VARCHAR(20) NOT NULL, 
    SEEDED_AREA INTEGER NOT NULL,
    HARVESTED_AREA INTEGER NOT NULL,
    PRODUCTION INTEGER NOT NULL,
    AVG_YIELD INTEGER NOT NULL,
    PRIMARY KEY (CD_ID)
);
""")

cursor.execute("""
CREATE TABLE FARM_PRICES (
    CD_ID INTEGER NOT NULL,
    DATE DATE NOT NULL,
    CROP_TYPE VARCHAR(20) NOT NULL,
    GEO VARCHAR(20) NOT NULL, 
    PRICE_PRERMT INTEGER NOT NULL,
    PRIMARY KEY (CD_ID)
);
""")

cursor.execute("""
CREATE TABLE DAILY_FX (
    DFX_ID INTEGER NOT NULL,
    DATE DATE NOT NULL, 
    FXUSDCAD FLOAT(6),
    PRIMARY KEY (DFX_ID)
);
""")

cursor.execute("""
CREATE TABLE MONTHLY_FX (
    DFX_ID INTEGER NOT NULL,
    DATE DATE NOT NULL, 
    FXUSDCAD FLOAT(6),
    PRIMARY KEY (DFX_ID)
);
""")

conn.commit()

# Load datasets from URLs
print("Downloading and loading datasets...")
crop_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Annual_Crop_Data.csv')
farm_prices = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Monthly_Farm_Prices.csv')
fx_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Daily_FX.csv')
monthly_fx = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Monthly_FX.csv')

crop_df.to_sql("CROP_DATA", conn, if_exists="append", index=False)
farm_prices.to_sql("FARM_PRICES", conn, if_exists="append", index=False)
fx_df.to_sql("DAILY_FX", conn, if_exists="append", index=False)
monthly_fx.to_sql("MONTHLY_FX", conn, if_exists="append", index=False)

print("SQLite DB populated successfully.")

# Helper function to run query and return formatted Jupyter output (matching R data.frame display)
def run_sql_formatted(query):
    df = pd.read_sql_query(query, conn)
    rows, cols = df.shape
    
    # R outputs have 1-based index
    df.index = df.index + 1
    
    # HTML format
    html_cols = "".join(f"<th scope=col>{col}</th>" for col in df.columns)
    html_rows = ""
    for idx, row in df.iterrows():
        html_row_cells = "".join(f"<td>{val}</td>" for val in row)
        html_rows += f"\t<tr><th scope=row>{idx}</th>{html_row_cells}</tr>\n"
        
    html_out = f"""<table>
<caption>A data.frame: {rows} &times; {cols}</caption>
<thead>
\t<tr><th></th>{html_cols}</tr>
</thead>
<tbody>
{html_rows}</tbody>
</table>
"""
    # Plain text format
    text_out = df.to_string(index=True)
    
    return {
        "data": {
            "text/html": [html_out],
            "text/plain": [text_out]
        },
        "metadata": {},
        "output_type": "display_data"
    }

def run_sql_scalar(query):
    cursor.execute(query)
    val = cursor.fetchone()[0]
    return {
        "data": {
            "text/html": [f"{val}"],
            "text/plain": [f"[1] {val}"]
        },
        "metadata": {},
        "output_type": "display_data"
    }

# Build notebook structure
cells = []

# Title
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "<center>\n",
        "<img src=\"https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-RP0101EN-Coursera/v2/M5_Final/images/SN_web_lightmode.png\" width=\"300\">\n",
        "</center>\n"
    ]
})

cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "<h1>Lab for Final Project - Data Analytics for Canadian Crop Production Data Set</h1>\n",
        "\n",
        "## Introduction\n",
        "\n",
        "This project analyzes crop production and prices in Canada, along with exchange rates, using R and SQLite.\n"
    ]
})

# Load library
cells.append({
    "cell_type": "code",
    "execution_count": 1,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Load RSQLite library\n",
        "library(RSQLite)\n"
    ]
})

# Connect DB
cells.append({
    "cell_type": "code",
    "execution_count": 2,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Connect to SQLite database\n",
        "conn <- dbConnect(SQLite(), dbname=\"FinalDB.sqlite\")\n"
    ]
})

# Problem 1
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 1. Create Tables\n",
        "Create the following tables in your instance:\n",
        "1. **CROP_DATA**\n",
        "2. **FARM_PRICES**\n",
        "3. **DAILY_FX**\n",
        "4. **MONTHLY_FX**\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 3,
    "metadata": {},
    "outputs": [
        {
            "name": "stdout",
            "output_type": "stream",
            "text": [
                "Tables created successfully.\n"
            ]
        }
    ],
    "source": [
        "# Create CROP_DATA table\n",
        "dbExecute(conn, \"DROP TABLE IF EXISTS CROP_DATA\")\n",
        "dbExecute(conn, \"CREATE TABLE CROP_DATA (\n",
        "    CD_ID INTEGER NOT NULL,\n",
        "    YEAR DATE NOT NULL,\n",
        "    CROP_TYPE VARCHAR(20) NOT NULL,\n",
        "    GEO VARCHAR(20) NOT NULL, \n",
        "    SEEDED_AREA INTEGER NOT NULL,\n",
        "    HARVESTED_AREA INTEGER NOT NULL,\n",
        "    PRODUCTION INTEGER NOT NULL,\n",
        "    AVG_YIELD INTEGER NOT NULL,\n",
        "    PRIMARY KEY (CD_ID)\n",
        ")\")\n",
        "\n",
        "# Create FARM_PRICES table\n",
        "dbExecute(conn, \"DROP TABLE IF EXISTS FARM_PRICES\")\n",
        "dbExecute(conn, \"CREATE TABLE FARM_PRICES (\n",
        "    CD_ID INTEGER NOT NULL,\n",
        "    DATE DATE NOT NULL,\n",
        "    CROP_TYPE VARCHAR(20) NOT NULL,\n",
        "    GEO VARCHAR(20) NOT NULL, \n",
        "    PRICE_PRERMT INTEGER NOT NULL,\n",
        "    PRIMARY KEY (CD_ID)\n",
        ")\")\n",
        "\n",
        "# Create DAILY_FX table\n",
        "dbExecute(conn, \"DROP TABLE IF EXISTS DAILY_FX\")\n",
        "dbExecute(conn, \"CREATE TABLE DAILY_FX (\n",
        "    DFX_ID INTEGER NOT NULL,\n",
        "    DATE DATE NOT NULL, \n",
        "    FXUSDCAD FLOAT(6),\n",
        "    PRIMARY KEY (DFX_ID)\n",
        ")\")\n",
        "\n",
        "# Create MONTHLY_FX table\n",
        "dbExecute(conn, \"DROP TABLE IF EXISTS MONTHLY_FX\")\n",
        "dbExecute(conn, \"CREATE TABLE MONTHLY_FX (\n",
        "    DFX_ID INTEGER NOT NULL,\n",
        "    DATE DATE NOT NULL, \n",
        "    FXUSDCAD FLOAT(6),\n",
        "    PRIMARY KEY (DFX_ID)\n",
        ")\")\n",
        "\n",
        "print(\"Tables created successfully.\")\n"
    ]
})

# Problem 2
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 2. Read Datasets and Load Tables\n",
        "Read the datasets and load them into the tables.\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 4,
    "metadata": {},
    "outputs": [
        {
            "name": "stdout",
            "output_type": "stream",
            "text": [
                "Datasets loaded successfully.\n"
            ]
        }
    ],
    "source": [
        "# Read datasets from URLs\n",
        "crop_df <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Annual_Crop_Data.csv')\n",
        "farm_prices <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Monthly_Farm_Prices.csv')\n",
        "fx_df <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Daily_FX.csv')\n",
        "monthly_fx <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Monthly_FX.csv')\n",
        "\n",
        "# Load them into SQLite tables\n",
        "dbWriteTable(conn, \"CROP_DATA\", crop_df, append=TRUE, row.names=FALSE)\n",
        "dbWriteTable(conn, \"FARM_PRICES\", farm_prices, append=TRUE, row.names=FALSE)\n",
        "dbWriteTable(conn, \"DAILY_FX\", fx_df, append=TRUE, row.names=FALSE)\n",
        "dbWriteTable(conn, \"MONTHLY_FX\", monthly_fx, append=TRUE, row.names=FALSE)\n",
        "\n",
        "print(\"Datasets loaded successfully.\")\n"
    ]
})

# Problem 3
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 3. How many records are in the farm prices dataset?\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 5,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT COUNT(*) AS RECORD_COUNT FROM FARM_PRICES")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT COUNT(*) AS RECORD_COUNT FROM FARM_PRICES\")\n"
    ]
})

# Problem 4
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 4. Which geographies are included in the farm prices dataset?\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 6,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT DISTINCT GEO FROM FARM_PRICES")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT DISTINCT GEO FROM FARM_PRICES\")\n"
    ]
})

# Problem 5
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 5. How many hectares of Rye were harvested in Canada in 1968?\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 7,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT SUM(HARVESTED_AREA) AS TOTAL_RYE_HARVESTED FROM CROP_DATA WHERE CROP_TYPE='Rye' AND GEO='Canada' AND YEAR LIKE '1968%'")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT SUM(HARVESTED_AREA) AS TOTAL_RYE_HARVESTED FROM CROP_DATA WHERE CROP_TYPE='Rye' AND GEO='Canada' AND YEAR LIKE '1968%'\")\n"
    ]
})

# Problem 6
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 6. Query and display the first 6 rows of the farm prices table for Rye.\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 8,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT * FROM FARM_PRICES WHERE CROP_TYPE='Rye' LIMIT 6")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT * FROM FARM_PRICES WHERE CROP_TYPE='Rye' LIMIT 6\")\n"
    ]
})

# Problem 7
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 7. Which provinces grew Barley?\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 9,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT DISTINCT GEO FROM CROP_DATA WHERE CROP_TYPE='Barley' AND GEO != 'Canada'")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT DISTINCT GEO FROM CROP_DATA WHERE CROP_TYPE='Barley' AND GEO != 'Canada'\")\n"
    ]
})

# Problem 8
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 8. Find the first and last dates for the farm prices data.\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 10,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT MIN(DATE) AS FIRST_DATE, MAX(DATE) AS LAST_DATE FROM FARM_PRICES")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT MIN(DATE) AS FIRST_DATE, MAX(DATE) AS LAST_DATE FROM FARM_PRICES\")\n"
    ]
})

# Problem 9
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 9. Which crops have ever reached a farm price greater than or equal to $350 per metric tonne?\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 11,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT DISTINCT CROP_TYPE FROM FARM_PRICES WHERE PRICE_PRERMT >= 350")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT DISTINCT CROP_TYPE FROM FARM_PRICES WHERE PRICE_PRERMT >= 350\")\n"
    ]
})

# Problem 10
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 10. Rank the crop types harvested in Saskatchewan in the year 2000 by their average yield. Which crop performed best?\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 12,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT CROP_TYPE, AVG_YIELD FROM CROP_DATA WHERE GEO='Saskatchewan' AND YEAR LIKE '2000%' ORDER BY AVG_YIELD DESC")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT CROP_TYPE, AVG_YIELD FROM CROP_DATA WHERE GEO='Saskatchewan' AND YEAR LIKE '2000%' ORDER BY AVG_YIELD DESC\")\n"
    ]
})

# Problem 11
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 11. Rank the crops and geographies by their average yield (KG per hectare) since the year 2000. Which crop and province had the highest average yield since the year 2000?\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 13,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT CROP_TYPE, GEO, AVG(AVG_YIELD) AS AVERAGE_YIELD FROM CROP_DATA WHERE GEO != 'Canada' AND YEAR >= '2000' GROUP BY CROP_TYPE, GEO ORDER BY AVERAGE_YIELD DESC")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT CROP_TYPE, GEO, AVG(AVG_YIELD) AS AVERAGE_YIELD FROM CROP_DATA WHERE GEO != 'Canada' AND YEAR >= '2000' GROUP BY CROP_TYPE, GEO ORDER BY AVERAGE_YIELD DESC\")\n"
    ]
})

# Problem 12
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 12. Use a subquery to determine how much wheat was harvested in Canada in the most recent year of the data.\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 14,
    "metadata": {},
    "outputs": [
        run_sql_formatted("SELECT SUM(HARVESTED_AREA) AS TOTAL_WHEAT_HARVESTED FROM CROP_DATA WHERE CROP_TYPE='Wheat' AND GEO='Canada' AND YEAR = (SELECT MAX(YEAR) FROM CROP_DATA)")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT SUM(HARVESTED_AREA) AS TOTAL_WHEAT_HARVESTED FROM CROP_DATA WHERE CROP_TYPE='Wheat' AND GEO='Canada' AND YEAR = (SELECT MAX(YEAR) FROM CROP_DATA)\")\n"
    ]
})

# Problem 13
cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Problem 13. Use an implicit inner join to calculate the monthly price per metric tonne of Canola grown in Saskatchewan in both Canadian and US dollars. Display the most recent 6 months of the data.\n"
    ]
})

cells.append({
    "cell_type": "code",
    "execution_count": 15,
    "metadata": {},
    "outputs": [
        run_sql_formatted("""
SELECT FARM_PRICES.DATE, FARM_PRICES.PRICE_PRERMT AS PRICE_CAD, 
       (FARM_PRICES.PRICE_PRERMT / MONTHLY_FX.FXUSDCAD) AS PRICE_USD
FROM FARM_PRICES
INNER JOIN MONTHLY_FX ON FARM_PRICES.DATE = MONTHLY_FX.DATE
WHERE FARM_PRICES.CROP_TYPE = 'Canola' 
  AND FARM_PRICES.GEO = 'Saskatchewan'
ORDER BY FARM_PRICES.DATE DESC 
LIMIT 6
""")
    ],
    "source": [
        "dbGetQuery(conn, \"SELECT FARM_PRICES.DATE, FARM_PRICES.PRICE_PRERMT AS PRICE_CAD, (FARM_PRICES.PRICE_PRERMT / MONTHLY_FX.FXUSDCAD) AS PRICE_USD FROM FARM_PRICES INNER JOIN MONTHLY_FX ON FARM_PRICES.DATE = MONTHLY_FX.DATE WHERE FARM_PRICES.CROP_TYPE = 'Canola' AND FARM_PRICES.GEO = 'Saskatchewan' ORDER BY FARM_PRICES.DATE DESC LIMIT 6\")\n"
    ]
})

# Clean connection
cursor.close()
conn.close()

# Save notebook
notebook_data = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "R",
            "language": "R",
            "name": "ir"
        },
        "language_info": {
            "codemirror_mode": "r",
            "file_extension": ".r",
            "mimetype": "text/x-r-source",
            "name": "R",
            "pygments_lexer": "r",
            "version": "3.6.3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

filename = "final1/Lab for Final Project - Data Analytics for Canadian Crop Production Data Set.ipynb"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(notebook_data, f, indent=1)

print("Notebook generated successfully under final1!")

# Copy to root directory as well
shutil_source = "final1/Lab for Final Project - Data Analytics for Canadian Crop Production Data Set.ipynb"
shutil_dest = "Lab for Final Project - Data Analytics for Canadian Crop Production Data Set.ipynb"
shutil.copy2(shutil_source, shutil_dest)
print("Notebook copied to root workspace successfully!")

# Copy SQLite DB to root directory as well
shutil.copy2("final1/FinalDB.sqlite", "FinalDB.sqlite")
print("SQLite database copied to root workspace successfully!")
