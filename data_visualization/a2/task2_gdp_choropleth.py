#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据可视化任务二：分级统计图 (Choropleth Map)
创建1991年全球GDP分布的分级统计图
使用顺序色彩映射展示GDP的地理分布
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from datetime import datetime
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches

warnings.filterwarnings("ignore")

# 全局变量存储所有数据用于生成报告
data_report = {
    "raw_data": None,
    "gdp_1991": None,
    "processed_gdp": None,
    "world_map": None,
    "merged_data": None,
    "colormap_info": None,
    "statistics": None,
    "metadata": {},
}


def generate_markdown_report():
    """生成包含所有数据的 Markdown 报告"""
    print("\n=== Generating Markdown Report ===")

    with open("task2_gdp_choropleth.md", "w", encoding="utf-8") as f:
        f.write("# 全球GDP分布分级统计图分析报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # 1. 数据集基本信息
        f.write("## 1. 数据集基本信息\n\n")
        if data_report["raw_data"] is not None:
            f.write(f"- **数据形状**: {data_report['raw_data'].shape}\n")
            f.write(f"- **列名**: {list(data_report['raw_data'].columns)}\n")
            f.write(
                f"- **年份范围**: {data_report['raw_data']['Year'].min()} - {data_report['raw_data']['Year'].max()}\n"
            )
            f.write(
                f"- **国家数量**: {data_report['raw_data']['Country Name'].nunique()}\n\n"
            )

        # 2. 1991年GDP数据探索
        f.write("## 2. 1991年GDP数据探索\n\n")
        if data_report["gdp_1991"] is not None:
            f.write("### 2.1 数据完整性\n\n")
            f.write(f"- **总记录数**: {len(data_report['gdp_1991'])}\n")
            f.write(
                f"- **有GDP数据的国家数**: {data_report['gdp_1991']['GDP (in USD)'].notna().sum()}\n"
            )
            f.write(
                f"- **GDP数据缺失数**: {data_report['gdp_1991']['GDP (in USD)'].isna().sum()}\n\n"
            )

            f.write("### 2.2 GDP统计信息\n\n")
            gdp_data = data_report["gdp_1991"]["GDP (in USD)"].dropna()
            f.write("```\n")
            f.write(f"最小值: {gdp_data.min():.2e}\n")
            f.write(f"最大值: {gdp_data.max():.2e}\n")
            f.write(f"中位数: {gdp_data.median():.2e}\n")
            f.write(f"平均值: {gdp_data.mean():.2e}\n")
            f.write(f"标准差: {gdp_data.std():.2e}\n")
            f.write("```\n\n")

            f.write("### 2.3 GDP分位数分析\n\n")
            f.write("```\n")
            quantiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
            for q in quantiles:
                f.write(f"{q*100:4.0f}%: {gdp_data.quantile(q):.2e}\n")
            f.write("```\n\n")

        # 3. 数据处理过程
        f.write("## 3. 数据处理过程\n\n")
        f.write("### 3.1 对数转换\n\n")
        f.write(
            "由于GDP分布高度偏斜（从1.07e+08到6.16e+12），直接使用线性色图会导致大多数国家显示为同一种浅色。\n"
        )
        f.write("因此采用对数转换来压缩极值范围，更好地分配颜色到数据。\n\n")
        f.write("**重要说明**：\n")
        f.write("- 对数转换仅用于**颜色映射**，确保颜色能够合理分布到所有国家\n")
        f.write("- 最终显示给用户的是**原始GDP数值**，便于理解\n")
        f.write("- 图例使用**分位数表示**（25%, 50%, 75%, 90%），直观易懂\n")
        f.write("- 颜色条显示**Billion/Trillion格式**的GDP值，简洁明了\n\n")
        f.write("```\n")
        f.write("log_gdp = np.log10(gdp_data)  # 用于颜色映射\n")
        f.write("# 但显示时使用原始GDP值\n")
        f.write("```\n\n")

        if data_report["processed_gdp"] is not None:
            f.write("### 3.2 转换后的数据统计\n\n")
            f.write("```\n")
            f.write(data_report["processed_gdp"].describe().to_string())
            f.write("\n```\n\n")

        # 4. 色彩映射选择
        f.write("## 4. 色彩映射选择\n\n")
        f.write("### 4.1 色图类型：顺序色彩映射 (Sequential Colormap)\n\n")
        f.write("**选择理由**：\n")
        f.write("- GDP是定量型数据，具有明确的'低-高'顺序关系\n")
        f.write("- 需要体现数值的连续性和递增性\n")
        f.write("- 主要依赖**亮度 (Luminance)** 变化来编码数值大小\n\n")

        f.write("**避免的色图类型**：\n")
        f.write(
            "- **彩虹色图 (Rainbow Colormap)**：主要依赖色相变化，缺乏单调递增的亮度\n"
        )
        f.write("- **分类色图**：不适用于连续数值数据\n\n")

        if data_report["colormap_info"] is not None:
            f.write("### 4.2 具体色图选择\n\n")
            f.write(f"- **色图名称**: {data_report['colormap_info']['name']}\n")
            f.write(f"- **色图类型**: {data_report['colormap_info']['type']}\n")
            f.write(f"- **颜色范围**: {data_report['colormap_info']['color_range']}\n")
            f.write(
                f"- **设计原理**: {data_report['colormap_info']['design_principle']}\n\n"
            )

        # 5. 地理数据处理
        f.write("## 5. 地理数据处理\n\n")
        f.write("### 5.1 世界地图数据\n\n")
        f.write("使用Natural Earth的世界地图数据，包含国家边界和基本地理信息。\n\n")

        if data_report["world_map"] is not None:
            f.write(f"- **地图数据形状**: {data_report['world_map'].shape}\n")
            f.write(f"- **包含国家数**: {len(data_report['world_map'])}\n")
            f.write(f"- **坐标系**: WGS84 (EPSG:4326)\n\n")

        f.write("### 5.2 国家名称匹配\n\n")
        f.write("处理数据集中的国家名称与地图数据中的国家名称不一致的问题。\n")
        f.write("主要匹配策略：\n")
        f.write("- 直接匹配\n")
        f.write("- 模糊匹配（处理拼写差异）\n")
        f.write("- 手动映射（处理特殊国家名称）\n\n")

        if data_report["merged_data"] is not None:
            f.write("### 5.3 数据合并结果\n\n")
            matched_countries = data_report["merged_data"][
                data_report["merged_data"]["GDP (in USD)"].notna()
            ]
            unmatched_gdp = data_report["gdp_1991"][
                ~data_report["gdp_1991"]["Country Name"].isin(
                    matched_countries["country_name"]
                )
            ]
            unmatched_map = data_report["merged_data"][
                data_report["merged_data"]["GDP (in USD)"].isna()
                & data_report["merged_data"]["name"].notna()
            ]

            f.write(f"- **1991年GDP数据总数**: {len(data_report['gdp_1991'])}\n")
            f.write(f"- **地图中国家总数**: {len(data_report['world_map'])}\n")
            f.write(f"- **成功匹配的国家数**: {len(matched_countries)}\n")
            f.write(
                f"- **匹配成功率**: {len(matched_countries) / len(data_report['gdp_1991']) * 100:.1f}%\n"
            )
            f.write(f"- **未匹配的GDP数据国家数**: {len(unmatched_gdp)}\n")
            f.write(f"- **未匹配的地图国家数**: {len(unmatched_map)}\n\n")

            f.write("### 5.4 成功匹配的国家列表（前20个，按GDP排序）\n\n")
            f.write("```\n")
            matched_list = matched_countries[
                ["country_name", "mapped_name", "GDP (in USD)"]
            ].sort_values("GDP (in USD)", ascending=False)
            for i, (_, row) in enumerate(matched_list.head(20).iterrows(), 1):
                f.write(
                    f"{i:3d}. {row['country_name']} -> {row['mapped_name']} (GDP: {row['GDP (in USD)']:.2e})\n"
                )
            f.write("```\n\n")

            f.write("### 5.5 未匹配的GDP数据国家详情\n\n")
            f.write("以下国家在GDP数据中存在但无法在地图中找到对应：\n\n")
            f.write("```\n")
            for i, country in enumerate(unmatched_gdp["Country Name"].tolist(), 1):
                f.write(f"{i:3d}. {country}\n")
            f.write("```\n\n")

            f.write("### 5.6 未匹配的地图国家详情（前20个）\n\n")
            f.write("以下国家在地图中存在但GDP数据中无对应：\n\n")
            f.write("```\n")
            for i, country in enumerate(unmatched_map["name"].head(20).tolist(), 1):
                f.write(f"{i:3d}. {country}\n")
            f.write("```\n\n")

            f.write("### 5.7 匹配失败原因分析\n\n")
            f.write("**主要原因**：\n")
            f.write("1. **国家名称不一致**：数据集和地图使用不同的国家名称标准\n")
            f.write("2. **特殊行政区**：如香港、澳门等特殊行政区在地图中可能不存在\n")
            f.write("3. **历史国家**：1991年存在但后来分裂或合并的国家\n")
            f.write("4. **小岛屿国家**：一些小的岛屿国家可能在地图数据中缺失\n")
            f.write("5. **拼写差异**：同一国家的不同拼写方式\n\n")

            f.write("**改进措施**：\n")
            f.write("1. **扩展映射表**：添加更多国家名称映射规则\n")
            f.write("2. **模糊匹配**：使用字符串相似度算法进行模糊匹配\n")
            f.write("3. **手动校正**：对重要国家进行手动映射\n")
            f.write("4. **数据源统一**：使用统一的国家名称标准\n\n")

        # 6. 可视化参数
        f.write("## 6. 可视化参数\n\n")
        f.write("- **图表类型**: 分级统计图 (Choropleth Map)\n")
        f.write("- **数据年份**: 1991年\n")
        f.write("- **数据指标**: GDP (in USD)\n")
        f.write("- **图形大小**: 16x10 英寸\n")
        f.write("- **色彩映射**: 顺序色图\n")
        f.write("- **数据转换**: 对数转换\n")
        f.write("- **DPI**: 300\n\n")

        # 7. 统计结果
        f.write("## 7. 统计结果\n\n")
        if data_report["statistics"] is not None:
            f.write("### 7.1 GDP分布统计\n\n")
            f.write("```\n")
            f.write(data_report["statistics"]["gdp_stats"].to_string())
            f.write("\n```\n\n")

            f.write("### 7.2 对数转换后统计\n\n")
            f.write("```\n")
            f.write(data_report["statistics"]["log_gdp_stats"].to_string())
            f.write("\n```\n\n")

            f.write("### 7.3 颜色分级统计\n\n")
            f.write("```\n")
            f.write(data_report["statistics"]["color_bins"].to_string())
            f.write("\n```\n\n")

        f.write("---\n")
        f.write("*此报告由 task2_gdp_choropleth.py 自动生成*\n")

    print("Markdown report saved as: task2_gdp_choropleth.md")


def load_and_explore_data():
    """加载并探索数据集"""
    print("Loading dataset...")

    # 加载数据
    df = pd.read_csv("Employment_Unemployment_GDP_data.csv")

    # 存储原始数据到全局变量
    data_report["raw_data"] = df.copy()

    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Number of countries: {df['Country Name'].nunique()}")

    return df


def load_1991_gdp_data(df):
    """加载1991年GDP数据"""
    print("\n=== Loading 1991 GDP Data ===")

    # 筛选1991年数据
    gdp_1991 = df[df["Year"] == 1991].copy()

    print(f"Total records for 1991: {len(gdp_1991)}")
    print(f"Countries with GDP data: {gdp_1991['GDP (in USD)'].notna().sum()}")
    print(f"Missing GDP data: {gdp_1991['GDP (in USD)'].isna().sum()}")

    # 基本统计信息
    gdp_data = gdp_1991["GDP (in USD)"].dropna()
    print(f"\nGDP Statistics:")
    print(f"Min: {gdp_data.min():.2e}")
    print(f"Max: {gdp_data.max():.2e}")
    print(f"Median: {gdp_data.median():.2e}")
    print(f"Mean: {gdp_data.mean():.2e}")
    print(f"Std: {gdp_data.std():.2e}")

    # 存储数据
    data_report["gdp_1991"] = gdp_1991
    data_report["metadata"]["selected_year"] = 1991

    return gdp_1991


def process_gdp_data(gdp_data):
    """处理GDP数据，进行对数转换"""
    print("\n=== Processing GDP Data ===")

    # 对数转换
    log_gdp = np.log10(gdp_data["GDP (in USD)"].dropna())

    # 创建处理后的数据框
    processed_data = gdp_data.copy()
    processed_data["log_GDP"] = np.log10(processed_data["GDP (in USD)"])

    print(f"Log-transformed GDP Statistics:")
    print(f"Min: {log_gdp.min():.2f}")
    print(f"Max: {log_gdp.max():.2f}")
    print(f"Median: {log_gdp.median():.2f}")
    print(f"Mean: {log_gdp.mean():.2f}")
    print(f"Std: {log_gdp.std():.2f}")

    # 存储处理后的数据
    data_report["processed_gdp"] = processed_data

    return processed_data


def load_world_map():
    """加载世界地图数据"""
    print("\n=== Loading World Map Data ===")

    try:
        # 尝试从在线源加载Natural Earth数据
        world_url = "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"
        world = gpd.read_file(world_url)
        print(f"World map loaded successfully: {world.shape}")
        print(f"Countries in map: {len(world)}")
        print(f"Columns: {list(world.columns)}")

        # 存储地图数据
        data_report["world_map"] = world

        return world
    except Exception as e:
        print(f"Error loading world map from URL: {e}")

        try:
            # 尝试使用本地文件
            world = gpd.read_file("world.geojson")
            print(f"World map loaded from local file: {world.shape}")
            data_report["world_map"] = world
            return world
        except Exception as e2:
            print(f"Error loading local world map: {e2}")
            print("Creating a simplified visualization without map data...")
            return None


def create_country_mapping():
    """创建国家名称映射表"""
    print("\n=== Creating Country Name Mapping ===")

    # 完善的国家名称映射表
    country_mapping = {
        # 美国相关
        "United States": "USA",
        "USA": "USA",
        # 中国相关
        "China": "China",
        "Hong Kong SAR, China": "Hong Kong",
        "Macao SAR, China": "Macao",
        # 俄罗斯相关
        "Russia": "Russia",
        "Russian Federation": "Russia",
        # 英国相关
        "United Kingdom": "England",  # 地图中使用England
        "UK": "England",
        # 韩国相关
        "South Korea": "South Korea",
        "Korea, Rep.": "South Korea",
        "Korea, South": "South Korea",
        # 朝鲜相关
        "North Korea": "North Korea",
        "Korea, Dem. Rep.": "North Korea",
        "Korea, North": "North Korea",
        # 刚果相关
        "Congo, Rep.": "Republic of the Congo",
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        # 其他常见映射
        "Iran, Islamic Rep.": "Iran",
        "Egypt, Arab Rep.": "Egypt",
        "Venezuela, RB": "Venezuela",
        "Yemen, Rep.": "Yemen",
        "Syrian Arab Republic": "Syria",
        "Lao PDR": "Laos",
        "Kyrgyz Republic": "Kyrgyzstan",
        "Slovak Republic": "Slovakia",
        "Czech Republic": "Czech Republic",
        "Czechia": "Czech Republic",
        "Macedonia, FYR": "Macedonia",
        "North Macedonia": "Macedonia",
        "Moldova": "Moldova",
        "Tanzania": "United Republic of Tanzania",
        "Gambia, The": "Gambia",
        "Bahamas, The": "The Bahamas",
        "Cape Verde": "Cabo Verde",
        "Cabo Verde": "Cabo Verde",
        "Cote d'Ivoire": "Ivory Coast",
        "Eswatini": "Swaziland",
        "Guinea-Bissau": "Guinea Bissau",
        "Timor-Leste": "East Timor",
        "Turkiye": "Turkey",
        "Viet Nam": "Vietnam",
        "Brunei Darussalam": "Brunei",
        "Samoa": "Samoa",
        "Sao Tome and Principe": "Sao Tome and Principe",
        "St. Lucia": "St. Lucia",
        "St. Vincent and the Grenadines": "St. Vincent and the Grenadines",
        "Tonga": "Tonga",
        "Maldives": "Maldives",
        "Malta": "Malta",
        "Mauritius": "Mauritius",
        "Comoros": "Comoros",
        "Barbados": "Barbados",
        "Bahrain": "Bahrain",
        "Singapore": "Singapore",
    }

    return country_mapping


def merge_data_with_map(gdp_data, world_map):
    """将GDP数据与地图数据合并"""
    print("\n=== Merging Data with Map ===")

    if world_map is None:
        print("No world map data available, skipping merge")
        return None

    # 创建国家名称映射
    country_mapping = create_country_mapping()

    # 准备GDP数据
    gdp_clean = gdp_data[["Country Name", "GDP (in USD)", "log_GDP"]].copy()
    gdp_clean = gdp_clean.rename(columns={"Country Name": "country_name"})

    # 应用国家名称映射
    gdp_clean["mapped_name"] = (
        gdp_clean["country_name"].map(country_mapping).fillna(gdp_clean["country_name"])
    )

    # 尝试合并数据
    merged = world_map.merge(
        gdp_clean, left_on="name", right_on="mapped_name", how="left"
    )

    # 统计合并结果
    matched_countries = merged["GDP (in USD)"].notna().sum()
    total_countries = len(gdp_clean)
    match_rate = matched_countries / total_countries * 100

    print(f"Successfully matched countries: {matched_countries}")
    print(f"Total countries in GDP data: {total_countries}")
    print(f"Match rate: {match_rate:.1f}%")

    # 显示未匹配的国家
    unmatched = merged[merged["GDP (in USD)"].isna() & merged["name"].notna()]
    if len(unmatched) > 0:
        print(f"\nUnmatched countries in map: {len(unmatched)}")
        print("Sample unmatched countries:")
        print(unmatched["name"].head(10).tolist())

    # 存储合并后的数据
    data_report["merged_data"] = merged

    return merged


def create_sequential_colormap():
    """创建顺序色彩映射"""
    print("\n=== Creating Sequential Colormap ===")

    # 选择蓝色系顺序色图（从浅蓝到深蓝）
    # 这种色图主要依赖亮度变化，适合编码有序数据
    colors = [
        "#E6F3FF",
        "#B3D9FF",
        "#80BFFF",
        "#4DA6FF",
        "#1A8CFF",
        "#0066CC",
        "#004D99",
        "#003366",
    ]

    colormap = LinearSegmentedColormap.from_list("GDP_Blue", colors, N=256)

    colormap_info = {
        "name": "GDP_Blue (Custom Sequential)",
        "type": "Sequential Colormap",
        "color_range": "Light Blue to Dark Blue",
        "design_principle": "主要依赖亮度变化，从浅蓝（低GDP）到深蓝（高GDP），符合人类对'低-高'的直觉感知",
    }

    # 存储色图信息
    data_report["colormap_info"] = colormap_info

    print(f"Colormap created: {colormap_info['name']}")
    print(f"Design principle: {colormap_info['design_principle']}")

    return colormap, colormap_info


def create_choropleth_map(merged_data, colormap, gdp_data):
    """创建分级统计图"""
    print("\n=== Creating Choropleth Map ===")

    if merged_data is None:
        print("No merged data available, creating a simplified visualization")
        create_simplified_visualization(gdp_data, colormap)
        return

    # 设置图形大小
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))

    # 创建分级统计图（使用log_GDP进行颜色映射，但显示原始GDP值）
    merged_data.plot(
        column="log_GDP",
        cmap=colormap,
        legend=False,  # 关闭自动图例，我们将手动添加
        ax=ax,
        edgecolor="white",
        linewidth=0.5,
        missing_kwds={"color": "lightgray", "alpha": 0.5},
    )

    # 设置标题和标签
    ax.set_title(
        "Global GDP Distribution in 1991",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    # 移除坐标轴
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # 计算原始GDP的分位数用于图例
    gdp_data = merged_data["GDP (in USD)"].dropna()
    log_gdp_data = merged_data["log_GDP"].dropna()

    # 计算原始GDP的分位数
    gdp_25 = gdp_data.quantile(0.25)
    gdp_50 = gdp_data.quantile(0.50)
    gdp_75 = gdp_data.quantile(0.75)
    gdp_90 = gdp_data.quantile(0.90)

    # 添加图例说明（使用分位数表示）
    legend_elements = [
        mpatches.Patch(color="#E6F3FF", label="Low GDP (< 25%)"),
        mpatches.Patch(color="#80BFFF", label="Medium-Low GDP (25% - 50%)"),
        mpatches.Patch(color="#4DA6FF", label="Medium GDP (50% - 75%)"),
        mpatches.Patch(color="#1A8CFF", label="High GDP (75% - 90%)"),
        mpatches.Patch(color="#003366", label="Very High GDP (> 90%)"),
        mpatches.Patch(color="lightgray", label="No Data"),
    ]

    ax.legend(handles=legend_elements, loc="lower left", bbox_to_anchor=(0, 0))

    # 添加颜色条显示原始GDP值映射
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    # 创建颜色条，显示原始GDP值
    sm = plt.cm.ScalarMappable(
        cmap=colormap,
        norm=plt.Normalize(vmin=log_gdp_data.min(), vmax=log_gdp_data.max()),
    )
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=cax, orientation="vertical")

    # 设置颜色条标签为原始GDP值（使用Billion/Trillion格式）
    gdp_ticks = np.array([gdp_25, gdp_50, gdp_75, gdp_90, gdp_data.max()])
    log_ticks = np.log10(gdp_ticks)
    cbar.set_ticks(log_ticks)

    # 转换GDP值为Billion/Trillion格式
    def format_gdp(gdp_value):
        if gdp_value >= 1e12:
            return f"${gdp_value/1e12:.1f}T"
        elif gdp_value >= 1e9:
            return f"${gdp_value/1e9:.1f}B"
        elif gdp_value >= 1e6:
            return f"${gdp_value/1e6:.1f}M"
        else:
            return f"${gdp_value/1e3:.1f}K"

    cbar.set_ticklabels([format_gdp(gdp) for gdp in gdp_ticks])
    cbar.set_label("GDP (USD)", fontsize=12, fontweight="bold")

    # 调整布局
    plt.tight_layout()

    # 保存图片
    plt.savefig(
        "task2_gdp_choropleth.png", dpi=300, bbox_inches="tight", facecolor="white"
    )
    print("Choropleth map saved as: task2_gdp_choropleth.png")

    # 显示图表
    plt.show()


def create_simplified_visualization(gdp_data, colormap):
    """创建简化的可视化（当无法获取地图数据时）"""
    print("Creating simplified GDP visualization...")

    # 设置图形大小
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

    # 子图1：GDP分布直方图
    log_gdp = gdp_data["log_GDP"].dropna()

    # 创建颜色映射
    colors = colormap(np.linspace(0, 1, len(log_gdp)))

    # 绘制直方图
    n, bins, patches = ax1.hist(
        log_gdp, bins=20, alpha=0.7, edgecolor="black", linewidth=0.5
    )

    # 为每个柱子设置颜色
    for i, (patch, color) in enumerate(
        zip(patches, colors[:: len(colors) // len(patches)])
    ):
        patch.set_facecolor(color)

    ax1.set_title(
        "GDP Distribution in 1991\n(Log-transformed values)",
        fontsize=14,
        fontweight="bold",
    )
    ax1.set_xlabel("Log10(GDP in USD)", fontsize=12)
    ax1.set_ylabel("Number of Countries", fontsize=12)
    ax1.grid(True, alpha=0.3)

    # 子图2：GDP排名前20的国家
    top_20 = gdp_data.nlargest(20, "GDP (in USD)")

    # 创建颜色映射
    colors_top20 = colormap(np.linspace(0, 1, len(top_20)))

    bars = ax2.barh(
        range(len(top_20)),
        top_20["log_GDP"],
        color=colors_top20,
        alpha=0.8,
        edgecolor="black",
        linewidth=0.5,
    )

    ax2.set_yticks(range(len(top_20)))
    ax2.set_yticklabels(top_20["Country Name"], fontsize=10)
    ax2.set_xlabel("Log10(GDP in USD)", fontsize=12)
    ax2.set_title("Top 20 Countries by GDP in 1991", fontsize=14, fontweight="bold")
    ax2.grid(True, alpha=0.3, axis="x")

    # 反转y轴，使最高的国家在顶部
    ax2.invert_yaxis()

    # 添加颜色条
    sm = plt.cm.ScalarMappable(
        cmap=colormap, norm=plt.Normalize(vmin=log_gdp.min(), vmax=log_gdp.max())
    )
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax2, orientation="vertical", pad=0.1)
    cbar.set_label("Log10(GDP in USD)", fontsize=12)

    # 调整布局
    plt.tight_layout()

    # 保存图片
    plt.savefig(
        "task2_gdp_choropleth.png", dpi=300, bbox_inches="tight", facecolor="white"
    )
    print("Simplified GDP visualization saved as: task2_gdp_choropleth.png")

    # 显示图表
    plt.show()


def create_detailed_analysis(merged_data):
    """创建详细的数据分析"""
    print("\n=== Detailed Data Analysis ===")

    if merged_data is None:
        print("No data available for analysis")
        return

    # 基本统计
    gdp_stats = merged_data["GDP (in USD)"].describe()
    log_gdp_stats = merged_data["log_GDP"].describe()

    # 颜色分级统计
    log_gdp_clean = merged_data["log_GDP"].dropna()
    bins = np.linspace(log_gdp_clean.min(), log_gdp_clean.max(), 8)
    color_bins = (
        pd.cut(log_gdp_clean, bins=bins, include_lowest=True)
        .value_counts()
        .sort_index()
    )

    print("GDP Statistics:")
    print(gdp_stats)
    print("\nLog-transformed GDP Statistics:")
    print(log_gdp_stats)
    print("\nColor Bins Distribution:")
    print(color_bins)

    # 存储统计结果
    statistics = {
        "gdp_stats": gdp_stats,
        "log_gdp_stats": log_gdp_stats,
        "color_bins": color_bins,
    }
    data_report["statistics"] = statistics


def main():
    # 1. 加载和探索数据
    df = load_and_explore_data()

    # 2. 加载1991年GDP数据
    gdp_1991 = load_1991_gdp_data(df)

    # 3. 处理GDP数据（对数转换）
    processed_gdp = process_gdp_data(gdp_1991)

    # 4. 加载世界地图数据
    world_map = load_world_map()

    # 5. 合并数据与地图
    merged_data = merge_data_with_map(processed_gdp, world_map)

    # 6. 创建顺序色彩映射
    colormap, colormap_info = create_sequential_colormap()

    # 7. 创建分级统计图
    create_choropleth_map(merged_data, colormap, processed_gdp)

    # 8. 详细数据分析
    create_detailed_analysis(merged_data)

    # 9. 生成 Markdown 报告
    generate_markdown_report()


if __name__ == "__main__":
    main()
