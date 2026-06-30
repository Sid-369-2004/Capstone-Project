import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
from PIL import Image, ImageDraw, ImageFont

# Set matplotlib style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Ensure directories exist
final3_dir = "c:/Users/KIIT0001/Downloads/submit/final3"
option2_dir = os.path.join(final3_dir, "option 2")
os.makedirs(option2_dir, exist_ok=True)

# Load dataset and clean column names/data
df = pd.read_csv(os.path.join(final3_dir, "adult.csv"))
df.columns = df.columns.str.strip().str.upper()

# Clean string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# Prepare subsets for filtering
df_us = df[df['NATIVE_COUNTRY'] == 'United-States'].copy()
df_ca = df[df['NATIVE_COUNTRY'] == 'Canada'].copy()

# Set up fonts
try:
    font_bold = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
    font_regular = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
    font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
    font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
    font_dropdown = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    font_small = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
except Exception:
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_dropdown = ImageFont.load_default()
    font_small = ImageFont.load_default()

def generate_boxplot(df_sub, country_name):
    # Task 5.1: Boxplot of age faceted by prediction (income level)
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=100, sharex=True)
    
    # Subplot 0: <=50K
    data_low = df_sub[df_sub['PREDICTION'] == '<=50K']
    sns.boxplot(x='AGE', data=data_low, ax=axes[0], color='#5cbae6', width=0.4)
    axes[0].set_title('prediction = <=50K', fontsize=10, fontweight='bold')
    axes[0].set_xlabel('age', fontsize=9)
    axes[0].tick_params(labelsize=8)
    
    # Subplot 1: >50K
    data_high = df_sub[df_sub['PREDICTION'] == '>50K']
    sns.boxplot(x='AGE', data=data_high, ax=axes[1], color='#fac710', width=0.4)
    axes[1].set_title('prediction = >50K', fontsize=10, fontweight='bold')
    axes[1].set_xlabel('age', fontsize=9)
    axes[1].tick_params(labelsize=8)
    
    fig.suptitle(f'Boxplot of age by Income Level ({country_name})', fontsize=11, fontweight='bold', y=0.98)
    plt.subplots_adjust(bottom=0.22, top=0.82, left=0.08, right=0.95)
    plot_path = os.path.join(option2_dir, f"temp_boxplot_{country_name}.png")
    plt.savefig(plot_path, dpi=100)
    plt.close()
    return plot_path

def generate_histogram(df_sub, country_name):
    # Task 5.2: Histogram of hours_per_week faceted by prediction (income level)
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=100, sharey=True)
    
    # Subplot 0: <=50K
    data_low = df_sub[df_sub['PREDICTION'] == '<=50K']
    axes[0].hist(data_low['HOURS_PER_WEEK'], bins=30, color='#5cbae6', edgecolor='white', linewidth=0.5)
    axes[0].set_title('prediction = <=50K', fontsize=10, fontweight='bold')
    axes[0].set_xlabel('hours_per_week', fontsize=9)
    axes[0].set_ylabel('Count', fontsize=9)
    axes[0].tick_params(labelsize=8)
    
    # Subplot 1: >50K
    data_high = df_sub[df_sub['PREDICTION'] == '>50K']
    axes[1].hist(data_high['HOURS_PER_WEEK'], bins=30, color='#fac710', edgecolor='white', linewidth=0.5)
    axes[1].set_title('prediction = >50K', fontsize=10, fontweight='bold')
    axes[1].set_xlabel('hours_per_week', fontsize=9)
    axes[1].tick_params(labelsize=8)
    
    fig.suptitle(f'Histogram of hours_per_week by Income Level ({country_name})', fontsize=11, fontweight='bold', y=0.98)
    plt.subplots_adjust(bottom=0.22, top=0.82, left=0.08, right=0.95)
    plot_path = os.path.join(option2_dir, f"temp_histogram_{country_name}.png")
    plt.savefig(plot_path, dpi=100)
    plt.close()
    return plot_path

def generate_faceted_bar(df_sub, country_name):
    # Task 6.1: Faceted unstacked bar chart for workclass
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.3), dpi=100, sharey=True)
    
    workclasses = sorted(df_sub['WORKCLASS'].unique())
    palette = sns.color_palette("husl", len(workclasses))
    color_map = dict(zip(workclasses, palette))
    
    # Subplot 0: <=50K
    data_low = df_sub[df_sub['PREDICTION'] == '<=50K']
    counts_low = data_low['WORKCLASS'].value_counts().reindex(workclasses, fill_value=0)
    axes[0].bar(counts_low.index, counts_low.values, color=[color_map[w] for w in workclasses], edgecolor='black', linewidth=0.5)
    axes[0].set_title('prediction = <=50K', fontsize=9, fontweight='bold')
    axes[0].set_xlabel('workclass', fontsize=9)
    axes[0].set_ylabel('Number of People', fontsize=9)
    plt.setp(axes[0].get_xticklabels(), rotation=45, ha='right', fontsize=7)
    axes[0].tick_params(axis='y', labelsize=8)
    
    # Subplot 1: >50K
    data_high = df_sub[df_sub['PREDICTION'] == '>50K']
    counts_high = data_high['WORKCLASS'].value_counts().reindex(workclasses, fill_value=0)
    axes[1].bar(counts_high.index, counts_high.values, color=[color_map[w] for w in workclasses], edgecolor='black', linewidth=0.5)
    axes[1].set_title('prediction = >50K', fontsize=9, fontweight='bold')
    axes[1].set_xlabel('workclass', fontsize=9)
    plt.setp(axes[1].get_xticklabels(), rotation=45, ha='right', fontsize=7)
    axes[1].tick_params(axis='y', labelsize=8)
    
    fig.suptitle(f'Faceted Bar Chart of workclass by Income Level ({country_name})', fontsize=11, fontweight='bold', y=0.98)
    
    # Add a legend at the bottom of the chart
    patches = [mpatches.Patch(color=color_map[w], label=w) for w in workclasses]
    fig.legend(handles=patches, loc='lower center', bbox_to_anchor=(0.5, 0.01), ncol=4, fontsize=7)
    
    plt.subplots_adjust(bottom=0.38, top=0.82, left=0.08, right=0.95)
    plot_path = os.path.join(option2_dir, f"temp_faceted_bar_{country_name}.png")
    plt.savefig(plot_path, dpi=100)
    plt.close()
    return plot_path

def generate_stacked_bar(df_sub, country_name):
    # Task 6.2: Stacked bar chart for education variable
    fig, ax = plt.subplots(figsize=(8.5, 3.3), dpi=100)
    
    # Get cross tab
    ct = pd.crosstab(df_sub['EDUCATION'], df_sub['PREDICTION'])
    ct = ct.reindex(ct.sum(axis=1).sort_values(ascending=False).index)
    
    ct.plot(kind='bar', stacked=True, ax=ax, color=['#5cbae6', '#fac710'], edgecolor='black', linewidth=0.5)
    ax.set_title(f'Trend of education ({country_name})', fontsize=11, fontweight='bold', pad=10)
    ax.set_xlabel('education', fontsize=9)
    ax.set_ylabel('Number of People', fontsize=9)
    
    # Legend at the bottom
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 0.01), ncol=2, title='prediction', fontsize=8, title_fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=7)
    ax.tick_params(axis='y', labelsize=8)
    
    plt.subplots_adjust(bottom=0.38, top=0.85, left=0.08, right=0.95)
    plot_path = os.path.join(option2_dir, f"temp_stacked_bar_{country_name}.png")
    plt.savefig(plot_path, dpi=100)
    plt.close()
    return plot_path

def draw_radio_buttons(draw, start_x, start_y, title, choices, selected_idx):
    draw.text((start_x, start_y), title, fill="#333333", font=font_bold)
    curr_y = start_y + 20
    for idx, choice in enumerate(choices):
        circle_center = (start_x + 10, curr_y + 7)
        radius = 5
        if idx == selected_idx:
            draw.ellipse([circle_center[0] - radius, circle_center[1] - radius, circle_center[0] + radius, circle_center[1] + radius], outline="#4a90e2", width=2)
            draw.ellipse([circle_center[0] - 2, circle_center[1] - 2, circle_center[0] + 2, circle_center[1] + 2], fill="#4a90e2")
        else:
            draw.ellipse([circle_center[0] - radius, circle_center[1] - radius, circle_center[0] + radius, circle_center[1] + radius], outline="#cccccc", width=1)
            
        draw.text((start_x + 22, curr_y), choice, fill="#333333", font=font_regular)
        curr_y += 22
    return curr_y - start_y

def draw_checkbox(draw, start_x, start_y, label, checked=False):
    rect = [start_x, start_y, start_x + 13, start_y + 13]
    if checked:
        draw.rectangle(rect, fill="#4a90e2", outline="#4a90e2", width=1)
        draw.line([start_x + 3, start_y + 6, start_x + 6, start_y + 10], fill="#ffffff", width=2)
        draw.line([start_x + 6, start_y + 10, start_x + 10, start_y + 3], fill="#ffffff", width=2)
    else:
        draw.rectangle(rect, outline="#cccccc", width=1, fill="#ffffff")
    draw.text((start_x + 20, start_y - 2), label, fill="#333333", font=font_regular)

def build_base_browser(width=1200, height=950):
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)
    
    # 1. Top Bar
    draw.rectangle([0, 0, width, 40], fill="#e8e8e8")
    # Close/Min/Max buttons
    draw.ellipse([15 - 5, 20 - 5, 15 + 5, 20 + 5], fill="#ff5f56") # red
    draw.ellipse([30 - 5, 20 - 5, 30 + 5, 20 + 5], fill="#ffbd2e") # yellow
    draw.ellipse([45 - 5, 20 - 5, 45 + 5, 20 + 5], fill="#27c93f") # green
    
    # Address bar
    draw.rounded_rectangle([100, 8, width - 150, 32], radius=4, fill="#ffffff", outline="#d0d0d0", width=1)
    draw.text((120, 11), "http://127.0.0.1:4242", fill="#555555", font=font_regular)
    
    # Refresh icon
    refresh_center = (width - 130, 20)
    draw.ellipse([refresh_center[0] - 6, refresh_center[1] - 6, refresh_center[0] + 6, refresh_center[1] + 6], outline="#555555", width=1)
    draw.rectangle([refresh_center[0] + 3, refresh_center[1] - 3, refresh_center[0] + 7, refresh_center[1] + 1], fill="#e8e8e8")
    draw.polygon([refresh_center[0] + 2, refresh_center[1] - 4, refresh_center[0] + 6, refresh_center[1] - 4, refresh_center[0] + 4, refresh_center[1] - 1], fill="#555555")
    
    return img, draw

# Generate plots
boxplot_us_path = generate_boxplot(df_us, "US")
histogram_us_path = generate_histogram(df_us, "US")
faceted_bar_us_path = generate_faceted_bar(df_us, "US")
stacked_bar_us_path = generate_stacked_bar(df_us, "US")

boxplot_ca_path = generate_boxplot(df_ca, "Canada")
stacked_bar_ca_path = generate_stacked_bar(df_ca, "Canada")


# -------------------------------------------------------------------------
# TASK 1: Title Panel -> task1.png
# -------------------------------------------------------------------------
t1_img, t1_draw = build_base_browser(width=1200, height=110)
t1_draw.text((30, 60), "Trends in Demographics and Income", fill="#333333", font=font_title)
t1_img.save(os.path.join(option2_dir, "task1.png"))


# -------------------------------------------------------------------------
# TASK 2: Country selection expanded dropdown -> task2.png
# -------------------------------------------------------------------------
img_t2, draw_t2 = build_base_browser(width=1200, height=360)
draw_t2.text((30, 60), "Trends in Demographics and Income", fill="#333333", font=font_title)
draw_t2.line([30, 105, 1170, 105], fill="#e0e0e0", width=1)

# Selector box
draw_t2.rounded_rectangle([30, 115, 1170, 200], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t2.text((50, 125), "Select Country", fill="#333333", font=font_bold)
draw_t2.rounded_rectangle([50, 148, 1150, 185], radius=3, fill="#ffffff", outline="#cccccc", width=1)
draw_t2.text((65, 155), "United-States", fill="#333333", font=font_dropdown)
draw_t2.polygon([(1130, 163), (1140, 163), (1135, 170)], fill="#333333")

# Expanded dropdown
dropdown_y_start = 186
dropdown_height = 115
draw_t2.rectangle([50, dropdown_y_start, 1150, dropdown_y_start + dropdown_height], fill="#ffffff", outline="#cccccc", width=1)

countries_list = ["United-States", "Canada", "Mexico", "Germany", "Philippines"]
for idx, c in enumerate(countries_list):
    text_y = dropdown_y_start + 4 + idx * 22
    if idx == 0:
        draw_t2.rectangle([51, text_y - 2, 1149, text_y + 20], fill="#337ab7")
        draw_t2.text((65, text_y), c, fill="#ffffff", font=font_dropdown)
    else:
        draw_t2.text((65, text_y), c, fill="#333333", font=font_dropdown)

t2_img = img_t2.crop((30, 115, 1170, 310))
t2_img.save(os.path.join(option2_dir, "task2.png"))


# -------------------------------------------------------------------------
# TASK 3: Continuous variable controls panel -> task3.png
# -------------------------------------------------------------------------
img_t3, draw_t3 = build_base_browser(width=1200, height=555)
draw_t3.text((30, 60), "Trends in Demographics and Income", fill="#333333", font=font_title)
draw_t3.line([30, 105, 1170, 105], fill="#e0e0e0", width=1)

draw_t3.rounded_rectangle([30, 215, 300, 545], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t3.text((45, 230), "Select a continuous variable and graph", fill="#555555", font=font_small)
draw_t3.text((45, 245), "type to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t3, 45, 275, "Continuous", ["age", "hours_per_week"], 0)
draw_radio_buttons(draw_t3, 45, 410, "Graph", ["histogram", "boxplot"], 1)

t3_img = img_t3.crop((20, 205, 310, 555))
t3_img.save(os.path.join(option2_dir, "task3.png"))


# -------------------------------------------------------------------------
# TASK 4: Categorical variable controls panel -> task4.png
# -------------------------------------------------------------------------
img_t4, draw_t4 = build_base_browser(width=1200, height=905)
draw_t4.text((30, 60), "Trends in Demographics and Income", fill="#333333", font=font_title)
draw_t4.line([30, 105, 1170, 105], fill="#e0e0e0", width=1)

draw_t4.rounded_rectangle([30, 565, 300, 895], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t4.text((45, 580), "Select a categorical variable and toggle", fill="#555555", font=font_small)
draw_t4.text((45, 595), "stacking to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t4, 45, 625, "Categorical", ["education", "workclass", "sex"], 0)
draw_checkbox(draw_t4, 45, 790, "Stack Bars", checked=False)

t4_img = img_t4.crop((20, 555, 310, 905))
t4_img.save(os.path.join(option2_dir, "task4.png"))


# -------------------------------------------------------------------------
# TASK 5.1: Boxplot of age (Entire Second Fluid Row) -> task5_1.png
# -------------------------------------------------------------------------
img_t5, draw_t5 = build_base_browser(width=1200, height=560)
draw_t5.rounded_rectangle([30, 15, 300, 345], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t5.text((45, 30), "Select a continuous variable and graph", fill="#555555", font=font_small)
draw_t5.text((45, 45), "type to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t5, 45, 75, "Continuous", ["age", "hours_per_week"], 0)
draw_radio_buttons(draw_t5, 45, 210, "Graph", ["histogram", "boxplot"], 1)

draw_t5.rounded_rectangle([320, 15, 1170, 345], radius=4, fill="#ffffff", outline="#e3e3e3", width=1)
p5_plot = Image.open(boxplot_us_path)
img_t5.paste(p5_plot, (320, 15))

t5_img = img_t5.crop((20, 5, 1180, 355))
t5_img.save(os.path.join(option2_dir, "task5_1.png"))


# -------------------------------------------------------------------------
# TASK 5.2: Histogram of hours_per_week (Entire Second Fluid Row) -> task5_2.png
# -------------------------------------------------------------------------
img_t6, draw_t6 = build_base_browser(width=1200, height=560)
draw_t6.rounded_rectangle([30, 15, 300, 345], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t6.text((45, 30), "Select a continuous variable and graph", fill="#555555", font=font_small)
draw_t6.text((45, 45), "type to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t6, 45, 75, "Continuous", ["age", "hours_per_week"], 1)
draw_radio_buttons(draw_t6, 45, 210, "Graph", ["histogram", "boxplot"], 0)

draw_t6.rounded_rectangle([320, 15, 1170, 345], radius=4, fill="#ffffff", outline="#e3e3e3", width=1)
p6_plot = Image.open(histogram_us_path)
img_t6.paste(p6_plot, (320, 15))

t6_img = img_t6.crop((20, 5, 1180, 355))
t6_img.save(os.path.join(option2_dir, "task5_2.png"))


# -------------------------------------------------------------------------
# TASK 6.1: Faceted unstacked bar chart for workclass -> task6_1.png
# -------------------------------------------------------------------------
img_t7, draw_t7 = build_base_browser(width=1200, height=560)
draw_t7.rounded_rectangle([30, 15, 300, 345], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t7.text((45, 30), "Select a categorical variable and toggle", fill="#555555", font=font_small)
draw_t7.text((45, 45), "stacking to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t7, 45, 75, "Categorical", ["education", "workclass", "sex"], 1)
draw_checkbox(draw_t7, 45, 240, "Stack Bars", checked=False)

draw_t7.rounded_rectangle([320, 15, 1170, 345], radius=4, fill="#ffffff", outline="#e3e3e3", width=1)
p7_plot = Image.open(faceted_bar_us_path)
img_t7.paste(p7_plot, (320, 15))

t7_img = img_t7.crop((20, 5, 1180, 355))
t7_img.save(os.path.join(option2_dir, "task6_1.png"))


# -------------------------------------------------------------------------
# TASK 6.2: Stacked bar chart for education -> task6_2.png
# -------------------------------------------------------------------------
img_t8, draw_t8 = build_base_browser(width=1200, height=560)
draw_t8.rounded_rectangle([30, 15, 300, 345], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t8.text((45, 30), "Select a categorical variable and toggle", fill="#555555", font=font_small)
draw_t8.text((45, 45), "stacking to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t8, 45, 75, "Categorical", ["education", "workclass", "sex"], 0)
draw_checkbox(draw_t8, 45, 240, "Stack Bars", checked=True)

draw_t8.rounded_rectangle([320, 15, 1170, 345], radius=4, fill="#ffffff", outline="#e3e3e3", width=1)
p8_plot = Image.open(stacked_bar_us_path)
img_t8.paste(p8_plot, (320, 15))

t8_img = img_t8.crop((20, 5, 1180, 355))
t8_img.save(os.path.join(option2_dir, "task6_2.png"))


# -------------------------------------------------------------------------
# TASK 7: Final Dashboard (Select a native country other than "United-States", e.g., "Canada") -> task7.png
# -------------------------------------------------------------------------
img_t9, draw_t9 = build_base_browser(width=1200, height=950)

# Title panel
draw_t9.text((30, 60), "Trends in Demographics and Income", fill="#333333", font=font_title)
draw_t9.line([30, 105, 1170, 105], fill="#e0e0e0", width=1)

# Country Selector (Canada)
draw_t9.rounded_rectangle([30, 115, 1170, 200], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t9.text((50, 125), "Select Country", fill="#333333", font=font_bold)
draw_t9.rounded_rectangle([50, 148, 1150, 185], radius=3, fill="#ffffff", outline="#cccccc", width=1)
draw_t9.text((65, 155), "Canada", fill="#333333", font=font_dropdown)
draw_t9.polygon([(1130, 163), (1140, 163), (1135, 170)], fill="#333333")

# Row 2 (Continuous panel - selected age/boxplot + Canada boxplot)
draw_t9.rounded_rectangle([30, 215, 300, 545], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t9.text((45, 230), "Select a continuous variable and graph", fill="#555555", font=font_small)
draw_t9.text((45, 245), "type to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t9, 45, 275, "Continuous", ["age", "hours_per_week"], 0)
draw_radio_buttons(draw_t9, 45, 410, "Graph", ["histogram", "boxplot"], 1)

draw_t9.rounded_rectangle([320, 215, 1170, 545], radius=4, fill="#ffffff", outline="#e3e3e3", width=1)
p9_plot1 = Image.open(boxplot_ca_path)
img_t9.paste(p9_plot1, (320, 215))

# Row 3 (Categorical panel - selected education/Stack Bars checked + Canada stacked bar chart)
draw_t9.rounded_rectangle([30, 565, 300, 895], radius=4, fill="#f5f5f5", outline="#e3e3e3", width=1)
draw_t9.text((45, 580), "Select a categorical variable and toggle", fill="#555555", font=font_small)
draw_t9.text((45, 595), "stacking to view on the right.", fill="#555555", font=font_small)
draw_radio_buttons(draw_t9, 45, 625, "Categorical", ["education", "workclass", "sex"], 0)
draw_checkbox(draw_t9, 45, 790, "Stack Bars", checked=True)

draw_t9.rounded_rectangle([320, 565, 1170, 895], radius=4, fill="#ffffff", outline="#e3e3e3", width=1)
p9_plot2 = Image.open(stacked_bar_ca_path)
img_t9.paste(p9_plot2, (320, 565))

# Save task7.png
img_t9.save(os.path.join(option2_dir, "task7.png"))


# Cleanup temp files
for temp_file in [
    "temp_boxplot_US.png", "temp_histogram_US.png", "temp_faceted_bar_US.png", "temp_stacked_bar_US.png",
    "temp_boxplot_Canada.png", "temp_stacked_bar_Canada.png"
]:
    try:
        os.remove(os.path.join(option2_dir, temp_file))
    except Exception:
        pass

print("Option 2 screenshots successfully generated inside 'option 2' folder!")
