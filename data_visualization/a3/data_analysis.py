"""
COVID-19 数据清洗效果分析脚本
Data Cleaning Effect Analysis Script for COVID-19 Dataset

功能：
1. 对比原始数据和清洗后数据的质量
2. 分析数据清洗的效果
3. 生成数据质量对比报告
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def analyze_data_quality():
    """分析数据质量对比"""
    print("COVID-19 数据清洗效果分析")
    print("=" * 50)

    # 加载原始数据和清洗后数据
    print("1. 加载数据...")
    original_data = pd.read_csv("covid-19_full_data.csv")
    cleaned_data = pd.read_csv("covid-19_full_data_cleaned.csv")

    print(f"原始数据行数: {len(original_data):,}")
    print(f"清洗后数据行数: {len(cleaned_data):,}")
    print(f"数据减少: {len(original_data) - len(cleaned_data):,} 行")

    # 基本统计对比
    print("\n2. 基本统计对比...")
    print(f"原始数据地区数: {original_data['location'].nunique()}")
    print(f"清洗后地区数: {cleaned_data['location'].nunique()}")

    # 缺失值对比
    print("\n3. 缺失值对比...")
    key_fields = ["new_cases", "new_deaths", "total_cases", "total_deaths"]

    for field in key_fields:
        original_missing = original_data[field].isna().sum()
        cleaned_missing = cleaned_data[field].isna().sum()
        print(f"{field}:")
        print(f"  原始缺失值: {original_missing:,}")
        print(f"  清洗后缺失值: {cleaned_missing:,}")
        print(f"  修复数量: {original_missing - cleaned_missing:,}")

    # 最新日期数据对比
    print("\n4. 最新日期数据对比...")
    latest_date = cleaned_data["date"].max()
    print(f"最新日期: {latest_date}")

    original_latest = original_data[original_data["date"] == latest_date]
    cleaned_latest = cleaned_data[cleaned_data["date"] == latest_date]

    print(f"原始最新日期数据点数: {len(original_latest)}")
    print(f"清洗后最新日期数据点数: {len(cleaned_latest)}")

    # 有效数据对比
    print("\n5. 有效数据对比...")

    # 累计数据有效性
    original_valid_total = original_latest[
        (original_latest["total_cases"] > 0) & (original_latest["total_deaths"] > 0)
    ]
    cleaned_valid_total = cleaned_latest[
        (cleaned_latest["total_cases"] > 0) & (cleaned_latest["total_deaths"] > 0)
    ]

    print(f"原始有效累计数据点数: {len(original_valid_total)}")
    print(f"清洗后有效累计数据点数: {len(cleaned_valid_total)}")

    # 新增数据有效性
    original_valid_new = original_latest[
        (original_latest["new_cases"] > 0) | (original_latest["new_deaths"] > 0)
    ]
    cleaned_valid_new = cleaned_latest[
        (cleaned_latest["new_cases"] > 0) | (cleaned_latest["new_deaths"] > 0)
    ]

    print(f"原始有效新增数据点数: {len(original_valid_new)}")
    print(f"清洗后有效新增数据点数: {len(cleaned_valid_new)}")

    # 数据范围分析
    print("\n6. 数据范围分析...")

    if len(cleaned_valid_total) > 0:
        print("累计病例数范围:")
        print(f"  最小值: {cleaned_valid_total['total_cases'].min():,}")
        print(f"  最大值: {cleaned_valid_total['total_cases'].max():,}")
        print(f"  中位数: {cleaned_valid_total['total_cases'].median():,.0f}")

        print("累计死亡数范围:")
        print(f"  最小值: {cleaned_valid_total['total_deaths'].min():,}")
        print(f"  最大值: {cleaned_valid_total['total_deaths'].max():,}")
        print(f"  中位数: {cleaned_valid_total['total_deaths'].median():,.0f}")

    if len(cleaned_valid_new) > 0:
        print("新增病例数范围:")
        print(f"  最小值: {cleaned_valid_new['new_cases'].min():,}")
        print(f"  最大值: {cleaned_valid_new['new_cases'].max():,}")
        print(f"  中位数: {cleaned_valid_new['new_cases'].median():,.0f}")

        print("新增死亡数范围:")
        print(f"  最小值: {cleaned_valid_new['new_deaths'].min():,}")
        print(f"  最大值: {cleaned_valid_new['new_deaths'].max():,}")
        print(f"  中位数: {cleaned_valid_new['new_deaths'].median():,.0f}")

    # 病死率分析
    print("\n7. 病死率(CFR)分析...")
    if len(cleaned_valid_total) > 0:
        cleaned_valid_total = cleaned_valid_total.copy()
        cleaned_valid_total["cfr"] = (
            cleaned_valid_total["total_deaths"] / cleaned_valid_total["total_cases"]
        ) * 100

        print(f"CFR统计:")
        print(f"  最小值: {cleaned_valid_total['cfr'].min():.2f}%")
        print(f"  最大值: {cleaned_valid_total['cfr'].max():.2f}%")
        print(f"  中位数: {cleaned_valid_total['cfr'].median():.2f}%")
        print(f"  平均值: {cleaned_valid_total['cfr'].mean():.2f}%")

        # 高CFR国家
        high_cfr = cleaned_valid_total[cleaned_valid_total["cfr"] > 5].sort_values(
            "cfr", ascending=False
        )
        print(f"\n高CFR国家(>5%): {len(high_cfr)}个")
        if len(high_cfr) > 0:
            print("前10名:")
            for i, (_, row) in enumerate(high_cfr.head(10).iterrows()):
                print(f"  {i+1}. {row['location']}: {row['cfr']:.2f}%")

    # 生成可视化图表
    print("\n8. 生成数据质量对比图表...")
    create_quality_comparison_charts(original_data, cleaned_data, latest_date)

    print("\n✅ 数据质量分析完成！")
    print("📊 图表已保存: data_quality_analysis.png")


def create_quality_comparison_charts(original_data, cleaned_data, latest_date):
    """创建数据质量对比图表"""

    # 设置图表样式
    plt.style.use("seaborn-v0_8")
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("COVID-19 数据清洗效果分析", fontsize=16, fontweight="bold")

    # 1. 缺失值对比
    ax1 = axes[0, 0]
    fields = ["new_cases", "new_deaths", "total_cases", "total_deaths"]
    original_missing = [original_data[field].isna().sum() for field in fields]
    cleaned_missing = [cleaned_data[field].isna().sum() for field in fields]

    x = np.arange(len(fields))
    width = 0.35

    ax1.bar(
        x - width / 2, original_missing, width, label="原始数据", alpha=0.8, color="red"
    )
    ax1.bar(
        x + width / 2,
        cleaned_missing,
        width,
        label="清洗后数据",
        alpha=0.8,
        color="green",
    )

    ax1.set_xlabel("数据字段")
    ax1.set_ylabel("缺失值数量")
    ax1.set_title("缺失值对比")
    ax1.set_xticks(x)
    ax1.set_xticklabels(fields, rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 最新日期数据分布 - 累计病例
    ax2 = axes[0, 1]
    original_latest = original_data[original_data["date"] == latest_date]
    cleaned_latest = cleaned_data[cleaned_data["date"] == latest_date]

    valid_original = original_latest[original_latest["total_cases"] > 0]
    valid_cleaned = cleaned_latest[cleaned_latest["total_cases"] > 0]

    if len(valid_original) > 0 and len(valid_cleaned) > 0:
        ax2.hist(
            np.log10(valid_original["total_cases"]),
            bins=30,
            alpha=0.7,
            label="原始数据",
            color="red",
        )
        ax2.hist(
            np.log10(valid_cleaned["total_cases"]),
            bins=30,
            alpha=0.7,
            label="清洗后数据",
            color="green",
        )
        ax2.set_xlabel("累计病例数 (log10)")
        ax2.set_ylabel("频次")
        ax2.set_title("累计病例数分布对比")
        ax2.legend()
        ax2.grid(True, alpha=0.3)

    # 3. 最新日期数据分布 - 累计死亡
    ax3 = axes[1, 0]
    if len(valid_original) > 0 and len(valid_cleaned) > 0:
        valid_original_deaths = valid_original[valid_original["total_deaths"] > 0]
        valid_cleaned_deaths = valid_cleaned[valid_cleaned["total_deaths"] > 0]

        if len(valid_original_deaths) > 0 and len(valid_cleaned_deaths) > 0:
            ax3.hist(
                np.log10(valid_original_deaths["total_deaths"]),
                bins=30,
                alpha=0.7,
                label="原始数据",
                color="red",
            )
            ax3.hist(
                np.log10(valid_cleaned_deaths["total_deaths"]),
                bins=30,
                alpha=0.7,
                label="清洗后数据",
                color="green",
            )
            ax3.set_xlabel("累计死亡数 (log10)")
            ax3.set_ylabel("频次")
            ax3.set_title("累计死亡数分布对比")
            ax3.legend()
            ax3.grid(True, alpha=0.3)

    # 4. 数据质量指标对比
    ax4 = axes[1, 1]

    # 计算数据质量指标
    key_fields = ["new_cases", "new_deaths", "total_cases", "total_deaths"]

    original_quality = {
        "完整数据行数": len(original_latest),
        "有效累计数据": len(valid_original),
        "有效新增数据": len(
            original_latest[
                (original_latest["new_cases"] > 0) | (original_latest["new_deaths"] > 0)
            ]
        ),
        "数据完整性": (
            1
            - original_data[key_fields].isna().sum().sum()
            / (len(original_data) * len(key_fields))
        )
        * 100,
    }

    cleaned_quality = {
        "完整数据行数": len(cleaned_latest),
        "有效累计数据": len(valid_cleaned),
        "有效新增数据": len(
            cleaned_latest[
                (cleaned_latest["new_cases"] > 0) | (cleaned_latest["new_deaths"] > 0)
            ]
        ),
        "数据完整性": (
            1
            - cleaned_data[key_fields].isna().sum().sum()
            / (len(cleaned_data) * len(key_fields))
        )
        * 100,
    }

    metrics = list(original_quality.keys())
    original_values = list(original_quality.values())
    cleaned_values = list(cleaned_quality.values())

    x = np.arange(len(metrics))
    width = 0.35

    ax4.bar(
        x - width / 2, original_values, width, label="原始数据", alpha=0.8, color="red"
    )
    ax4.bar(
        x + width / 2,
        cleaned_values,
        width,
        label="清洗后数据",
        alpha=0.8,
        color="green",
    )

    ax4.set_xlabel("质量指标")
    ax4.set_ylabel("数值")
    ax4.set_title("数据质量指标对比")
    ax4.set_xticks(x)
    ax4.set_xticklabels(metrics, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("data_quality_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    analyze_data_quality()
