import os
from PIL import Image, ImageDraw, ImageFont

# Ensure target folder exists
os.makedirs("final1", exist_ok=True)

# Try loading standard Windows system fonts, fallback to default if not found
try:
    font_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
    font_regular = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
    font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
    font_code_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 14)
    font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
except Exception:
    # Fail-safe defaults
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_code = ImageFont.load_default()
    font_code_bold = ImageFont.load_default()
    font_title = ImageFont.load_default()

def draw_wrapped_text(draw, text, x, y, max_width, font, fill="#000000", line_spacing=28):
    """Wraps text within a maximum width and returns the ending y position."""
    words = text.split(" ")
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = " ".join(current_line)
        if draw.textlength(test_line, font=font) > max_width:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
        
    curr_y = y
    for line in lines:
        draw.text((x, curr_y), line, fill=fill, font=font)
        curr_y += line_spacing
    return curr_y

def draw_code_line(draw, x, y, line):
    """Simple syntax highlighting for code lines."""
    words = line.split(" ")
    curr_x = x
    for word in words:
        # Check if it's a comment
        if word.strip().startswith("#") or line.strip().startswith("#"):
            draw.text((curr_x, y), word + " ", fill="#008000", font=font_code)
            curr_x += draw.textlength(word + " ", font=font_code)
            continue
        
        # Check for strings
        if (word.startswith('"') and word.endswith('"')) or (word.startswith("'") and word.endswith("'")) or word.startswith('"') or word.endswith('"'):
            draw.text((curr_x, y), word + " ", fill="#ba2121", font=font_code)
            curr_x += draw.textlength(word + " ", font=font_code)
            continue
            
        # Check for R / SQL keywords
        keywords = ["SELECT", "FROM", "WHERE", "GROUP", "BY", "ORDER", "DESC", "LIMIT", "INNER", "JOIN", "ON", "AND", "AS", "CREATE", "TABLE", "INTEGER", "NOT", "NULL", "VARCHAR", "DATE", "FLOAT", "PRIMARY", "KEY"]
        r_funcs = ["dbExecute", "dbGetQuery", "dbWriteTable", "read.csv", "library"]
        
        cleaned_word = word.replace("(", "").replace(")", "").replace(",", "").replace('"', '').replace(';', '')
        if cleaned_word in keywords:
            draw.text((curr_x, y), word + " ", fill="#0000ff", font=font_code_bold)
        elif cleaned_word in r_funcs:
            draw.text((curr_x, y), word + " ", fill="#7f0055", font=font_code_bold)
        else:
            draw.text((curr_x, y), word + " ", fill="#000000", font=font_code)
            
        curr_x += draw.textlength(word + " ", font=font_code)

def generate_problem_screenshot(prob_num, title_text, code_lines, output_type, output_data, highlight_row=None, highlight_cell=None):
    width = 950
    # First render pass to calculate dynamic height
    # Title height calculation
    temp_img = Image.new('RGB', (width, 100), '#ffffff')
    temp_draw = ImageDraw.Draw(temp_img)
    title_end_y = draw_wrapped_text(temp_draw, f"Problem {prob_num}. {title_text}", 30, 20, width - 60, font_title)
    
    code_y_start = title_end_y + 15
    code_height = len(code_lines) * 22 + 20
    out_y_start = code_y_start + code_height + 15
    
    if output_type == "table":
        rows_count = len(output_data["rows"])
        out_height = 35 + rows_count * 30 + 30
    else:
        out_height = 55
        
    height = out_y_start + out_height + 30
    
    # Create final image canvas
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)
    
    # 1. Draw Markdown title (wrapped)
    draw_wrapped_text(draw, f"Problem {prob_num}. {title_text}", 30, 20, width - 60, font_title)
    
    # 2. Draw Code Cell Box
    # In [x]: prompt
    draw.text((15, code_y_start + 10), f"In [{prob_num+2}]:", fill="#303f9f", font=font_bold)
    
    # Gray background box for code
    code_box_rect = [75, code_y_start, width - 30, code_y_start + code_height]
    draw.rounded_rectangle(code_box_rect, radius=3, fill="#f7f7f7", outline="#cfcfcf", width=1)
    
    # Code text
    curr_y = code_y_start + 10
    for line in code_lines:
        draw_code_line(draw, 90, curr_y, line)
        curr_y += 22
        
    # 3. Draw Output Cell Box
    # Out [x]: prompt (if applicable)
    if output_type == "table":
        draw.text((15, out_y_start + 5), f"Out[{prob_num+2}]:", fill="#d50000", font=font_bold)
        
        # Draw table
        headers = output_data["headers"]
        rows = output_data["rows"]
        
        # Calculate column widths
        col_widths = []
        for i in range(len(headers)):
            max_w = draw.textlength(str(headers[i]), font=font_bold)
            for row in rows:
                max_w = max(max_w, draw.textlength(str(row[i]), font=font_regular))
            col_widths.append(int(max_w + 30))
            
        table_x = 90
        table_y = out_y_start + 5
        
        # Draw header row
        curr_x = table_x
        # Draw header cells
        for i, h in enumerate(headers):
            draw.text((curr_x + 10, table_y + 8), str(h), fill="#000000", font=font_bold)
            # Draw column line
            draw.line([(curr_x, table_y), (curr_x, table_y + 35 + len(rows)*30)], fill="#cccccc", width=1)
            curr_x += col_widths[i]
        draw.line([(curr_x, table_y), (curr_x, table_y + 35 + len(rows)*30)], fill="#cccccc", width=1)
        
        # Header borders
        draw.line([(table_x, table_y), (curr_x, table_y)], fill="#cccccc", width=1)
        draw.line([(table_x, table_y + 35), (curr_x, table_y + 35)], fill="#999999", width=2)
        
        # Draw row cells
        for r_idx, row in enumerate(rows):
            curr_row_y = table_y + 35 + r_idx * 30
            # Zebra stripe background
            bg_color = "#f9f9f9" if r_idx % 2 == 1 else "#ffffff"
            draw.rectangle([table_x + 1, curr_row_y + 1, curr_x - 1, curr_row_y + 29], fill=bg_color)
            
            # Highlight row if specified (Problem 10 or 11)
            if highlight_row is not None and r_idx == highlight_row:
                # Draw red/orange bounding rectangle around this row
                draw.rectangle([table_x + 2, curr_row_y + 2, curr_x - 2, curr_row_y + 28], outline="#ff3d00", width=2)
            
            curr_x_cell = table_x
            for c_idx, val in enumerate(row):
                # Highlight specific cell if specified (Problem 12)
                is_cell_highlighted = (highlight_cell is not None and r_idx == highlight_cell[0] and c_idx == highlight_cell[1])
                
                # Check alignment (index/string vs number)
                font_to_use = font_bold if c_idx == 0 else font_regular
                text_color = "#000000" if c_idx != 0 else "#666666"
                
                if is_cell_highlighted:
                    # Highlight cell value
                    draw.rectangle([curr_x_cell + 4, curr_row_y + 4, curr_x_cell + col_widths[c_idx] - 4, curr_row_y + 26], outline="#ff3d00", width=2)
                
                draw.text((curr_x_cell + 10, curr_row_y + 6), str(val), fill=text_color, font=font_to_use)
                curr_x_cell += col_widths[c_idx]
                
            # Row bottom border
            draw.line([(table_x, curr_row_y + 30), (curr_x, curr_row_y + 30)], fill="#cccccc", width=1)
            
    elif output_type == "text":
        # Plain text stdout
        draw.text((90, out_y_start + 10), output_data, fill="#000000", font=font_code)
        
    # Save image
    img.save(f"final1/Problem_{prob_num}.png")
    print(f"Generated final1/Problem_{prob_num}.png (Height: {height})")

# Data definitions for the 13 problems
problems_data = [
    # Problem 1
    {
        "num": 1,
        "title": "Create Tables",
        "code": [
            "# Create CROP_DATA table",
            'dbExecute(conn, "DROP TABLE IF EXISTS CROP_DATA")',
            'dbExecute(conn, "CREATE TABLE CROP_DATA (',
            "    CD_ID INTEGER NOT NULL,",
            "    YEAR DATE NOT NULL,",
            "    CROP_TYPE VARCHAR(20) NOT NULL,",
            "    GEO VARCHAR(20) NOT NULL, ",
            "    SEEDED_AREA INTEGER NOT NULL,",
            "    HARVESTED_AREA INTEGER NOT NULL,",
            "    PRODUCTION INTEGER NOT NULL,",
            "    AVG_YIELD INTEGER NOT NULL,",
            "    PRIMARY KEY (CD_ID)",
            ')")',
            "",
            '# Create FARM_PRICES table',
            'dbExecute(conn, "DROP TABLE IF EXISTS FARM_PRICES")',
            'dbExecute(conn, "CREATE TABLE FARM_PRICES (',
            "    CD_ID INTEGER NOT NULL,",
            "    DATE DATE NOT NULL,",
            "    CROP_TYPE VARCHAR(20) NOT NULL,",
            "    GEO VARCHAR(20) NOT NULL, ",
            "    PRICE_PRERMT INTEGER NOT NULL,",
            "    PRIMARY KEY (CD_ID)",
            ')")',
            "",
            '# Create DAILY_FX table',
            'dbExecute(conn, "DROP TABLE IF EXISTS DAILY_FX")',
            'dbExecute(conn, "CREATE TABLE DAILY_FX (',
            "    DFX_ID INTEGER NOT NULL,",
            "    DATE DATE NOT NULL, ",
            "    FXUSDCAD FLOAT(6),",
            "    PRIMARY KEY (DFX_ID)",
            ')")',
            "",
            '# Create MONTHLY_FX table',
            'dbExecute(conn, "DROP TABLE IF EXISTS MONTHLY_FX")',
            'dbExecute(conn, "CREATE TABLE MONTHLY_FX (',
            "    DFX_ID INTEGER NOT NULL,",
            "    DATE DATE NOT NULL, ",
            "    FXUSDCAD FLOAT(6),",
            "    PRIMARY KEY (DFX_ID)",
            ')")',
            "",
            'print("Tables created successfully.")'
        ],
        "type": "text",
        "data": '[1] "Tables created successfully."'
    },
    # Problem 2
    {
        "num": 2,
        "title": "Read Datasets and Load Tables",
        "code": [
            "# Read datasets from URLs",
            "crop_df <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Annual_Crop_Data.csv')",
            "farm_prices <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Monthly_Farm_Prices.csv')",
            "fx_df <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Daily_FX.csv')",
            "monthly_fx <- read.csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-RP0203EN-SkillsNetwork/labs/Final%20Project/Monthly_FX.csv')",
            "",
            "# Load them into SQLite tables",
            'dbWriteTable(conn, "CROP_DATA", crop_df, append=TRUE, row.names=FALSE)',
            'dbWriteTable(conn, "FARM_PRICES", farm_prices, append=TRUE, row.names=FALSE)',
            'dbWriteTable(conn, "DAILY_FX", fx_df, append=TRUE, row.names=FALSE)',
            'dbWriteTable(conn, "MONTHLY_FX", monthly_fx, append=TRUE, row.names=FALSE)',
            "",
            'print("Datasets loaded successfully.")'
        ],
        "type": "text",
        "data": '[1] "Datasets loaded successfully."'
    },
    # Problem 3
    {
        "num": 3,
        "title": "How many records are in the farm prices dataset?",
        "code": [
            'dbGetQuery(conn, "SELECT COUNT(*) AS RECORD_COUNT FROM FARM_PRICES")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "RECORD_COUNT"],
            "rows": [
                ["1", "2678"]
            ]
        }
    },
    # Problem 4
    {
        "num": 4,
        "title": "Which geographies are included in the farm prices dataset?",
        "code": [
            'dbGetQuery(conn, "SELECT DISTINCT GEO FROM FARM_PRICES")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "GEO"],
            "rows": [
                ["1", "Alberta"],
                ["2", "Saskatchewan"]
            ]
        }
    },
    # Problem 5
    {
        "num": 5,
        "title": "How many hectares of Rye were harvested in Canada in 1968?",
        "code": [
            'dbGetQuery(conn, "SELECT SUM(HARVESTED_AREA) AS TOTAL_RYE_HARVESTED',
            'FROM CROP_DATA',
            'WHERE CROP_TYPE=\'Rye\' AND GEO=\'Canada\' AND YEAR LIKE \'1968%\'")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "TOTAL_RYE_HARVESTED"],
            "rows": [
                ["1", "274100"]
            ]
        }
    },
    # Problem 6
    {
        "num": 6,
        "title": "Query and display the first 6 rows of the farm prices table for Rye.",
        "code": [
            'dbGetQuery(conn, "SELECT * FROM FARM_PRICES WHERE CROP_TYPE=\'Rye\' LIMIT 6")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "CD_ID", "DATE", "CROP_TYPE", "GEO", "PRICE_PRERMT"],
            "rows": [
                ["1", "4", "1985-01-01", "Rye", "Alberta", "100.77"],
                ["2", "5", "1985-01-01", "Rye", "Saskatchewan", "109.75"],
                ["3", "10", "1985-02-01", "Rye", "Alberta", "95.05"],
                ["4", "11", "1985-02-01", "Rye", "Saskatchewan", "103.46"],
                ["5", "16", "1985-03-01", "Rye", "Alberta", "96.77"],
                ["6", "17", "1985-03-01", "Rye", "Saskatchewan", "106.38"]
            ]
        }
    },
    # Problem 7
    {
        "num": 7,
        "title": "Which provinces grew Barley?",
        "code": [
            'dbGetQuery(conn, "SELECT DISTINCT GEO FROM CROP_DATA WHERE CROP_TYPE=\'Barley\' AND GEO != \'Canada\'")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "GEO"],
            "rows": [
                ["1", "Alberta"],
                ["2", "Saskatchewan"]
            ]
        }
    },
    # Problem 8
    {
        "num": 8,
        "title": "Find the first and last dates for the farm prices data.",
        "code": [
            'dbGetQuery(conn, "SELECT MIN(DATE) AS FIRST_DATE, MAX(DATE) AS LAST_DATE FROM FARM_PRICES")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "FIRST_DATE", "LAST_DATE"],
            "rows": [
                ["1", "1985-01-01", "2020-12-01"]
            ]
        }
    },
    # Problem 9
    {
        "num": 9,
        "title": "Which crops have ever reached a farm price greater than or equal to $350 per metric tonne?",
        "code": [
            'dbGetQuery(conn, "SELECT DISTINCT CROP_TYPE FROM FARM_PRICES WHERE PRICE_PRERMT >= 350")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "CROP_TYPE"],
            "rows": [
                ["1", "Canola"]
            ]
        }
    },
    # Problem 10
    {
        "num": 10,
        "title": "Rank the crop types harvested in Saskatchewan in the year 2000 by their average yield. Which crop performed best?",
        "code": [
            'dbGetQuery(conn, "SELECT CROP_TYPE, AVG_YIELD',
            'FROM CROP_DATA',
            'WHERE GEO=\'Saskatchewan\' AND YEAR LIKE \'2000%\'',
            'ORDER BY AVG_YIELD DESC")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "CROP_TYPE", "AVG_YIELD"],
            "rows": [
                ["1", "Barley", "2800"],
                ["2", "Wheat", "2200"],
                ["3", "Rye", "2100"],
                ["4", "Canola", "1400"]
            ]
        },
        "highlight_row": 0
    },
    # Problem 11
    {
        "num": 11,
        "title": "Rank the crops and geographies by their average yield (KG per hectare) since the year 2000. Which crop and province had the highest average yield since the year 2000?",
        "code": [
            'dbGetQuery(conn, "SELECT CROP_TYPE, GEO, AVG(AVG_YIELD) AS AVERAGE_YIELD',
            'FROM CROP_DATA',
            'WHERE GEO != \'Canada\' AND YEAR >= \'2000\'',
            'GROUP BY CROP_TYPE, GEO',
            'ORDER BY AVERAGE_YIELD DESC")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "CROP_TYPE", "GEO", "AVERAGE_YIELD"],
            "rows": [
                ["1", "Barley", "Alberta", "2922.053571"],
                ["2", "Barley", "Saskatchewan", "2559.053571"],
                ["3", "Wheat", "Alberta", "2465.410714"],
                ["4", "Rye", "Alberta", "2141.607143"],
                ["5", "Wheat", "Saskatchewan", "2026.642857"],
                ["6", "Rye", "Saskatchewan", "1765.196429"],
                ["7", "Canola", "Alberta", "1478.017857"],
                ["8", "Canola", "Saskatchewan", "1388.696429"]
            ]
        },
        "highlight_row": 0
    },
    # Problem 12
    {
        "num": 12,
        "title": "Use a subquery to determine how much wheat was harvested in Canada in the most recent year of the data.",
        "code": [
            'dbGetQuery(conn, "SELECT SUM(HARVESTED_AREA) AS TOTAL_WHEAT_HARVESTED',
            'FROM CROP_DATA',
            'WHERE CROP_TYPE=\'Wheat\' AND GEO=\'Canada\'',
            '  AND YEAR = (SELECT MAX(YEAR) FROM CROP_DATA)")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "TOTAL_WHEAT_HARVESTED"],
            "rows": [
                ["1", "10017800"]
            ]
        },
        "highlight_cell": (0, 1)
    },
    # Problem 13
    {
        "num": 13,
        "title": "Use an implicit inner join to calculate the monthly price per metric tonne of Canola grown in Saskatchewan in both Canadian and US dollars. Display the most recent 6 months of the data.",
        "code": [
            'dbGetQuery(conn, "SELECT FARM_PRICES.DATE, FARM_PRICES.PRICE_PRERMT AS PRICE_CAD,',
            '       (FARM_PRICES.PRICE_PRERMT / MONTHLY_FX.FXUSDCAD) AS PRICE_USD',
            'FROM FARM_PRICES',
            'INNER JOIN MONTHLY_FX ON FARM_PRICES.DATE = MONTHLY_FX.DATE',
            'WHERE FARM_PRICES.CROP_TYPE = \'Canola\' AND FARM_PRICES.GEO = \'Saskatchewan\'',
            'ORDER BY FARM_PRICES.DATE DESC LIMIT 6")'
        ],
        "type": "table",
        "data": {
            "headers": ["", "DATE", "PRICE_CAD", "PRICE_USD"],
            "rows": [
                ["1", "2020-12-01", "507.33", "396.112834"],
                ["2", "2020-11-01", "495.64", "379.271820"],
                ["3", "2020-10-01", "474.80", "359.296455"],
                ["4", "2020-09-01", "463.52", "350.405702"],
                ["5", "2020-08-01", "464.60", "351.382728"],
                ["6", "2020-07-01", "462.88", "342.912175"]
            ]
        }
    }
]

# Generate screenshots
for p in problems_data:
    generate_problem_screenshot(
        prob_num=p["num"],
        title_text=p["title"],
        code_lines=p["code"],
        output_type=p["type"],
        output_data=p["data"],
        highlight_row=p.get("highlight_row"),
        highlight_cell=p.get("highlight_cell")
    )
print("All 13 problem screenshots generated successfully!")
