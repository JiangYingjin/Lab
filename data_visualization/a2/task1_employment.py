#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据可视化任务一：分组柱状图 (改进版)
创建三大部门（农业、工业、服务业）就业分布的分组柱状图
解决中文字体显示问题
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

# 全局变量存储所有数据用于生成报告
data_report = {
    "raw_data": None,
    "selected_data": None,
    "processed_data": None,
    "country_analysis": None,
    "sector_analysis": None,
    "dominant_sectors": None,
    "metadata": {},
}


def generate_markdown_report():
    """生成包含所有数据的 Markdown 报告"""
    print("\n=== Generating Markdown Report ===")

    with open("task1_employment.md", "w", encoding="utf-8") as f:
        f.write("# 就业分布数据可视化分析报告\n\n")
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

        # 2. 原始数据样本
        f.write("## 2. 原始数据样本\n\n")
        if data_report["raw_data"] is not None:
            f.write("```\n")
            f.write(data_report["raw_data"].head(10).to_string())
            f.write("\n```\n\n")

        # 3. 选定的年份和国家
        f.write("## 3. 选定的年份和国家\n\n")
        f.write(
            f"- **选定年份**: {data_report['metadata'].get('selected_year', 'N/A')}\n"
        )
        f.write(
            f"- **选定国家**: {data_report['metadata'].get('selected_countries', 'N/A')}\n\n"
        )

        # 4. 选定年份的可用数据
        f.write("## 4. 选定年份的可用数据\n\n")
        if data_report["selected_data"] is not None:
            f.write("```\n")
            f.write(data_report["selected_data"].to_string())
            f.write("\n```\n\n")

        # 5. 数据预处理结果
        f.write("## 5. 数据预处理结果\n\n")
        f.write("### 5.1 重命名后的数据\n\n")
        if data_report["selected_data"] is not None:
            df_renamed = data_report["selected_data"][
                [
                    "Country Name",
                    "Employment Sector: Agriculture",
                    "Employment Sector: Industry",
                    "Employment Sector: Services",
                ]
            ].copy()
            df_renamed.columns = ["Country", "Agriculture", "Industry", "Services"]
            f.write("```\n")
            f.write(df_renamed.to_string())
            f.write("\n```\n\n")

        f.write("### 5.2 转换后的长格式数据（用于可视化）\n\n")
        if data_report["processed_data"] is not None:
            f.write("```\n")
            f.write(data_report["processed_data"].to_string())
            f.write("\n```\n\n")

        # 6. 按国家统计分析
        f.write("## 6. 按国家统计分析\n\n")
        if data_report["country_analysis"] is not None:
            f.write("```\n")
            f.write(data_report["country_analysis"].to_string())
            f.write("\n```\n\n")

        # 7. 按部门统计分析
        f.write("## 7. 按部门统计分析\n\n")
        if data_report["sector_analysis"] is not None:
            f.write("```\n")
            f.write(data_report["sector_analysis"].to_string())
            f.write("\n```\n\n")

        # 8. 各国主导部门
        f.write("## 8. 各国主导部门\n\n")
        if data_report["dominant_sectors"] is not None:
            for country, info in data_report["dominant_sectors"].items():
                f.write(f"- **{country}**: {info['sector']} ({info['rate']:.1f}%)\n")
            f.write("\n")

        # 9. 数据质量检查
        f.write("## 9. 数据质量检查\n\n")
        if data_report["raw_data"] is not None:
            f.write("### 9.1 缺失值统计\n\n")
            f.write("```\n")
            f.write(data_report["raw_data"].isnull().sum().to_string())
            f.write("\n```\n\n")

            f.write("### 9.2 数据范围检查\n\n")
            numeric_cols = (
                data_report["raw_data"].select_dtypes(include=["number"]).columns
            )
            f.write("```\n")
            f.write(data_report["raw_data"][numeric_cols].describe().to_string())
            f.write("\n```\n\n")

        # 10. 可视化参数
        f.write("## 10. 可视化参数\n\n")
        f.write("- **图表类型**: 分组柱状图\n")
        f.write("- **图形大小**: 14x8 英寸\n")
        f.write("- **调色板**: Set2\n")
        f.write("- **图例位置**: 左上角\n")
        f.write("- **图例字体大小**: 标题10pt, 内容9pt\n")
        f.write("- **DPI**: 300\n\n")

        f.write("---\n")
        f.write("*此报告由 task1_employment.py 自动生成*\n")

    print("Markdown report saved as: task1_employment.md")


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


def select_year_and_countries(df):
    """选择合适的年份和五个国家"""
    print("\n=== Year and Country Selection ===")

    # 选择年份：2020年（数据相对完整，且处于世纪之交有代表性）
    selected_year = 2020
    print(f"Selected year: {selected_year}")

    # 选择五个具有代表性的国家
    selected_countries = ["United States", "China", "Germany", "India", "Brazil"]

    print(f"Selected countries: {selected_countries}")

    # 检查这些国家在选定年份是否有数据
    available_data = df[
        (df["Year"] == selected_year) & (df["Country Name"].isin(selected_countries))
    ]

    print(f"\nAvailable data for {selected_year}:")
    print(
        available_data[
            [
                "Country Name",
                "Employment Sector: Agriculture",
                "Employment Sector: Industry",
                "Employment Sector: Services",
            ]
        ]
    )

    # 存储选定数据和元数据到全局变量
    data_report["selected_data"] = available_data.copy()
    data_report["metadata"]["selected_year"] = selected_year
    data_report["metadata"]["selected_countries"] = selected_countries

    return selected_year, selected_countries, available_data


def prepare_data_for_visualization(data):
    """准备可视化数据"""
    print("\n=== Data Preprocessing ===")

    # 选择需要的列
    columns_needed = [
        "Country Name",
        "Employment Sector: Agriculture",
        "Employment Sector: Industry",
        "Employment Sector: Services",
    ]

    df_selected = data[columns_needed].copy()

    # 重命名列以便更好地显示
    df_selected.columns = ["Country", "Agriculture", "Industry", "Services"]

    # 将数据从宽格式转换为长格式（用于分组柱状图）
    df_melted = df_selected.melt(
        id_vars="Country", var_name="Sector", value_name="Employment_Rate"
    )

    print("Transformed data format:")
    print(df_melted.head(10))

    # 存储处理后的数据到全局变量
    data_report["processed_data"] = df_melted.copy()

    return df_melted


def create_grouped_bar_chart(data, year):
    """创建分组柱状图"""
    print("\n=== Creating Grouped Bar Chart ===")

    # 设置图形大小和样式
    plt.figure(figsize=(14, 8))

    # 创建分组柱状图
    ax = sns.barplot(
        data=data,
        x="Country",
        y="Employment_Rate",
        hue="Sector",
        palette="Set2",  # 分类色彩映射
        edgecolor="black",
        linewidth=0.8,
        alpha=0.8,
    )

    # 设置标题和标签
    plt.title(
        f"Employment Distribution in {year} for Selected Countries",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Country", fontsize=12, fontweight="bold")
    plt.ylabel(
        "Employment Rate in Economic Sectors (%)", fontsize=12, fontweight="bold"
    )

    # 设置图例
    plt.legend(
        title="Economic Sector",
        title_fontsize=10,
        fontsize=9,
        loc="upper left",
        frameon=True,
        fancybox=True,
        shadow=True,
    )

    # 设置y轴范围，从0开始
    plt.ylim(0, max(data["Employment_Rate"]) * 1.1)

    # 在柱子上添加数值标签
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f", fontsize=9, rotation=0, padding=2)

    # 旋转x轴标签以避免重叠
    plt.xticks(rotation=45, ha="right")

    # 添加网格线（仅y轴）
    plt.grid(axis="y", alpha=0.3, linestyle="--")

    # 调整布局
    plt.tight_layout()

    # 保存图片
    plt.savefig(
        "task1_employment.png",
        dpi=300,
        bbox_inches="tight",
    )
    print("Chart saved as: task1_employment.png")

    # 显示图表
    plt.show()


def create_detailed_analysis(data, year):
    """创建详细的数据分析"""
    print("\n=== Detailed Data Analysis ===")

    # 按国家分组分析
    country_analysis = (
        data.groupby("Country")
        .agg({"Employment_Rate": ["mean", "std", "min", "max"]})
        .round(2)
    )

    print("Employment Rate Statistics by Country:")
    print(country_analysis)

    # 按部门分组分析
    sector_analysis = (
        data.groupby("Sector")
        .agg({"Employment_Rate": ["mean", "std", "min", "max"]})
        .round(2)
    )

    print("\nEmployment Rate Statistics by Sector:")
    print(sector_analysis)

    # 找出每个国家的主导部门
    print("\nDominant Sector by Country:")
    dominant_sectors = {}
    for country in data["Country"].unique():
        country_data = data[data["Country"] == country]
        dominant_sector = country_data.loc[
            country_data["Employment_Rate"].idxmax(), "Sector"
        ]
        max_rate = country_data["Employment_Rate"].max()
        print(f"{country}: {dominant_sector} ({max_rate:.1f}%)")
        dominant_sectors[country] = {"sector": dominant_sector, "rate": max_rate}

    # 存储分析结果到全局变量
    data_report["country_analysis"] = country_analysis
    data_report["sector_analysis"] = sector_analysis
    data_report["dominant_sectors"] = dominant_sectors


def main():
    # 1. 加载和探索数据
    df = load_and_explore_data()

    # 2. 选择年份和国家
    year, countries, selected_data = select_year_and_countries(df)

    # 3. 准备可视化数据
    viz_data = prepare_data_for_visualization(selected_data)

    # 4. 创建分组柱状图
    create_grouped_bar_chart(viz_data, year)

    # 5. 详细数据分析
    create_detailed_analysis(viz_data, year)

    # 6. 生成 Markdown 报告
    generate_markdown_report()


if __name__ == "__main__":
    main()
