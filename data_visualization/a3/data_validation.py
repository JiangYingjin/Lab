"""
COVID-19 数据质量分析和修复脚本
Data Quality Analysis and Repair Script for COVID-19 Dataset

功能：
1. 数据质量分析 - 识别缺失值、异常值、不一致性
2. 数据修复 - 基于逻辑规则补充缺失数据
3. 数据验证 - 确保数据一致性
4. 生成清洗后的完整数据集
"""

import pandas as pd
import numpy as np
import warnings
from datetime import datetime, timedelta
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class COVID19DataValidator:
    """COVID-19数据验证和修复类"""

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.df = None
        self.cleaned_df = None
        self.validation_report = {}

        # 非国家实体列表（需要过滤的聚合数据）
        self.non_country_entities = {
            "World",
            "Africa",
            "Asia",
            "Europe",
            "North America",
            "South America",
            "Oceania",
            "European Union",
            "High-income countries",
            "Low-income countries",
            "Lower-middle-income countries",
            "Upper-middle-income countries",
            "International",
        }

    def load_data(self):
        """加载CSV数据"""
        try:
            logger.info(f"正在加载数据文件: {self.csv_file_path}")
            self.df = pd.read_csv(self.csv_file_path)
            logger.info(f"成功加载 {len(self.df)} 行数据")
            return True
        except Exception as e:
            logger.error(f"数据加载失败: {e}")
            return False

    def analyze_data_quality(self):
        """分析数据质量"""
        logger.info("开始数据质量分析...")

        # 基本信息
        self.validation_report["basic_info"] = {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "date_range": (self.df["date"].min(), self.df["date"].max()),
            "unique_locations": self.df["location"].nunique(),
        }

        # 关键字段的缺失值分析
        key_fields = ["new_cases", "new_deaths", "total_cases", "total_deaths"]
        missing_analysis = {}

        for field in key_fields:
            missing_count = self.df[field].isna().sum()
            empty_count = (self.df[field] == "").sum()
            zero_count = (self.df[field] == 0).sum()

            missing_analysis[field] = {
                "missing_values": missing_count,
                "empty_strings": empty_count,
                "zero_values": zero_count,
                "total_invalid": missing_count + empty_count,
                "valid_values": len(self.df) - missing_count - empty_count,
            }

        self.validation_report["missing_analysis"] = missing_analysis

        # 数据类型分析
        self.validation_report["data_types"] = self.df.dtypes.to_dict()

        # 数据一致性检查
        self._check_data_consistency()

        logger.info("数据质量分析完成")
        return self.validation_report

    def _check_data_consistency(self):
        """检查数据一致性"""
        logger.info("检查数据一致性...")

        consistency_issues = []

        # 1. 检查累计数据是否单调递增
        for location in self.df["location"].unique():
            location_data = self.df[self.df["location"] == location].sort_values("date")

            # 检查total_cases单调性
            if not location_data["total_cases"].is_monotonic_increasing:
                non_monotonic = location_data[
                    location_data["total_cases"] < location_data["total_cases"].shift(1)
                ]
                if len(non_monotonic) > 0:
                    consistency_issues.append(
                        {
                            "type": "total_cases_decreasing",
                            "location": location,
                            "count": len(non_monotonic),
                            "dates": non_monotonic["date"].tolist(),
                        }
                    )

            # 检查total_deaths单调性
            if not location_data["total_deaths"].is_monotonic_increasing:
                non_monotonic = location_data[
                    location_data["total_deaths"]
                    < location_data["total_deaths"].shift(1)
                ]
                if len(non_monotonic) > 0:
                    consistency_issues.append(
                        {
                            "type": "total_deaths_decreasing",
                            "location": location,
                            "count": len(non_monotonic),
                            "dates": non_monotonic["date"].tolist(),
                        }
                    )

        self.validation_report["consistency_issues"] = consistency_issues

        # 2. 检查新增数据与累计数据的关系
        self._check_new_vs_total_consistency()

    def _check_new_vs_total_consistency(self):
        """检查新增数据与累计数据的一致性"""
        logger.info("检查新增数据与累计数据的一致性...")

        new_total_issues = []

        for location in self.df["location"].unique():
            location_data = self.df[self.df["location"] == location].sort_values("date")

            # 计算理论上的新增数据
            location_data = location_data.copy()
            location_data["calculated_new_cases"] = location_data["total_cases"].diff()
            location_data["calculated_new_deaths"] = location_data[
                "total_deaths"
            ].diff()

            # 检查new_cases与total_cases的差异
            new_cases_diff = location_data[
                (location_data["new_cases"].notna())
                & (location_data["calculated_new_cases"].notna())
                & (
                    abs(
                        location_data["new_cases"]
                        - location_data["calculated_new_cases"]
                    )
                    > 1
                )
            ]

            if len(new_cases_diff) > 0:
                new_total_issues.append(
                    {
                        "type": "new_cases_inconsistency",
                        "location": location,
                        "count": len(new_cases_diff),
                    }
                )

        self.validation_report["new_total_consistency_issues"] = new_total_issues

    def clean_and_repair_data(self):
        """清洗和修复数据"""
        logger.info("开始数据清洗和修复...")

        # 复制原始数据
        self.cleaned_df = self.df.copy()

        # 1. 数据类型转换
        self._convert_data_types()

        # 2. 处理缺失值
        self._handle_missing_values()

        # 3. 修复数据一致性
        self._repair_consistency_issues()

        # 4. 过滤非国家实体
        self._filter_non_country_entities()

        # 5. 最终验证
        self._final_validation()

        logger.info("数据清洗和修复完成")
        return self.cleaned_df

    def _convert_data_types(self):
        """转换数据类型"""
        logger.info("转换数据类型...")

        numeric_fields = [
            "new_cases",
            "new_deaths",
            "total_cases",
            "total_deaths",
            "weekly_cases",
            "weekly_deaths",
            "biweekly_cases",
            "biweekly_deaths",
        ]

        for field in numeric_fields:
            # 将空字符串和无效值转换为NaN
            self.cleaned_df[field] = pd.to_numeric(
                self.cleaned_df[field], errors="coerce"
            )

        # 转换日期格式
        self.cleaned_df["date"] = pd.to_datetime(self.cleaned_df["date"])

        logger.info("数据类型转换完成")

    def _handle_missing_values(self):
        """处理缺失值"""
        logger.info("处理缺失值...")

        # 按国家分组处理
        for location in self.cleaned_df["location"].unique():
            location_mask = self.cleaned_df["location"] == location
            location_data = self.cleaned_df[location_mask].sort_values("date")

            # 前向填充累计数据
            self.cleaned_df.loc[location_mask, "total_cases"] = location_data[
                "total_cases"
            ].fillna(method="ffill")
            self.cleaned_df.loc[location_mask, "total_deaths"] = location_data[
                "total_deaths"
            ].fillna(method="ffill")

            # 对于新增数据，如果缺失则用0填充
            self.cleaned_df.loc[location_mask, "new_cases"] = location_data[
                "new_cases"
            ].fillna(0)
            self.cleaned_df.loc[location_mask, "new_deaths"] = location_data[
                "new_deaths"
            ].fillna(0)

        logger.info("缺失值处理完成")

    def _repair_consistency_issues(self):
        """修复数据一致性问题"""
        logger.info("修复数据一致性问题...")

        for location in self.cleaned_df["location"].unique():
            location_mask = self.cleaned_df["location"] == location
            location_data = self.cleaned_df[location_mask].sort_values("date")

            # 确保累计数据单调递增
            self.cleaned_df.loc[location_mask, "total_cases"] = location_data[
                "total_cases"
            ].cummax()
            self.cleaned_df.loc[location_mask, "total_deaths"] = location_data[
                "total_deaths"
            ].cummax()

            # 重新计算新增数据以确保一致性
            location_data = self.cleaned_df[location_mask].sort_values("date")
            calculated_new_cases = (
                location_data["total_cases"].diff().fillna(location_data["total_cases"])
            )
            calculated_new_deaths = (
                location_data["total_deaths"]
                .diff()
                .fillna(location_data["total_deaths"])
            )

            # 如果原始新增数据与计算值差异很大，使用计算值
            mask_cases = abs(location_data["new_cases"] - calculated_new_cases) > 1
            mask_deaths = abs(location_data["new_deaths"] - calculated_new_deaths) > 1

            self.cleaned_df.loc[location_mask & mask_cases, "new_cases"] = (
                calculated_new_cases[mask_cases]
            )
            self.cleaned_df.loc[location_mask & mask_deaths, "new_deaths"] = (
                calculated_new_deaths[mask_deaths]
            )

        logger.info("数据一致性修复完成")

    def _filter_non_country_entities(self):
        """过滤非国家实体"""
        logger.info("过滤非国家实体...")

        original_count = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df[
            ~self.cleaned_df["location"].isin(self.non_country_entities)
        ]
        filtered_count = len(self.cleaned_df)

        logger.info(f"过滤了 {original_count - filtered_count} 行非国家实体数据")

    def _final_validation(self):
        """最终数据验证"""
        logger.info("进行最终数据验证...")

        # 确保没有负值
        numeric_fields = ["new_cases", "new_deaths", "total_cases", "total_deaths"]
        for field in numeric_fields:
            negative_count = (self.cleaned_df[field] < 0).sum()
            if negative_count > 0:
                logger.warning(f"发现 {negative_count} 个负值在字段 {field}，将设置为0")
                self.cleaned_df[field] = self.cleaned_df[field].clip(lower=0)

        # 确保累计数据 >= 新增数据
        for location in self.cleaned_df["location"].unique():
            location_mask = self.cleaned_df["location"] == location
            location_data = self.cleaned_df[location_mask].sort_values("date")

            # 检查并修复累计数据小于新增数据的情况
            mask = location_data["total_cases"] < location_data["new_cases"]
            if mask.any():
                logger.warning(f"修复 {location} 的累计病例数据不一致问题")
                self.cleaned_df.loc[location_mask, "total_cases"] = location_data[
                    "total_cases"
                ].cumsum()

            mask = location_data["total_deaths"] < location_data["new_deaths"]
            if mask.any():
                logger.warning(f"修复 {location} 的累计死亡数据不一致问题")
                self.cleaned_df.loc[location_mask, "total_deaths"] = location_data[
                    "total_deaths"
                ].cumsum()

        logger.info("最终数据验证完成")

    def generate_cleaned_dataset(self, output_file=None):
        """生成清洗后的数据集"""
        if output_file is None:
            output_file = self.csv_file_path.replace(".csv", "_cleaned.csv")

        logger.info(f"生成清洗后的数据集: {output_file}")

        # 确保日期格式正确
        self.cleaned_df["date"] = self.cleaned_df["date"].dt.strftime("%Y-%m-%d")

        # 保存到CSV
        self.cleaned_df.to_csv(output_file, index=False)

        logger.info(f"清洗后的数据集已保存: {output_file}")
        return output_file

    def generate_validation_report(self, output_file=None):
        """生成数据验证报告"""
        if output_file is None:
            output_file = "data_validation_report.txt"

        logger.info(f"生成数据验证报告: {output_file}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("COVID-19 数据质量验证报告\n")
            f.write("=" * 50 + "\n\n")

            # 基本信息
            f.write("1. 基本信息\n")
            f.write("-" * 20 + "\n")
            basic_info = self.validation_report["basic_info"]
            f.write(f"总行数: {basic_info['total_rows']:,}\n")
            f.write(f"总列数: {basic_info['total_columns']}\n")
            f.write(
                f"日期范围: {basic_info['date_range'][0]} 到 {basic_info['date_range'][1]}\n"
            )
            f.write(f"不同地区数: {basic_info['unique_locations']:,}\n\n")

            # 缺失值分析
            f.write("2. 缺失值分析\n")
            f.write("-" * 20 + "\n")
            for field, info in self.validation_report["missing_analysis"].items():
                f.write(f"{field}:\n")
                f.write(f"  缺失值: {info['missing_values']:,}\n")
                f.write(f"  空字符串: {info['empty_strings']:,}\n")
                f.write(f"  零值: {info['zero_values']:,}\n")
                f.write(f"  有效值: {info['valid_values']:,}\n\n")

            # 一致性检查结果
            f.write("3. 数据一致性检查\n")
            f.write("-" * 20 + "\n")
            consistency_issues = self.validation_report.get("consistency_issues", [])
            f.write(f"发现 {len(consistency_issues)} 个一致性问题\n")

            for issue in consistency_issues[:10]:  # 只显示前10个
                f.write(
                    f"- {issue['type']} in {issue['location']}: {issue['count']} 个问题\n"
                )

            if len(consistency_issues) > 10:
                f.write(f"... 还有 {len(consistency_issues) - 10} 个问题\n")

            f.write("\n")

            # 清洗后数据统计
            if self.cleaned_df is not None:
                f.write("4. 清洗后数据统计\n")
                f.write("-" * 20 + "\n")
                f.write(f"清洗后行数: {len(self.cleaned_df):,}\n")
                f.write(f"清洗后地区数: {self.cleaned_df['location'].nunique():,}\n")
                f.write(f"最新日期: {self.cleaned_df['date'].max()}\n")

                # 最新日期的数据统计
                latest_date = self.cleaned_df["date"].max()
                latest_data = self.cleaned_df[self.cleaned_df["date"] == latest_date]
                f.write(f"最新日期数据点数: {len(latest_data):,}\n")

                # 有效数据统计
                valid_total = latest_data[
                    (latest_data["total_cases"] > 0) & (latest_data["total_deaths"] > 0)
                ]
                valid_new = latest_data[
                    (latest_data["new_cases"] > 0) | (latest_data["new_deaths"] > 0)
                ]
                f.write(f"有效累计数据点数: {len(valid_total):,}\n")
                f.write(f"有效新增数据点数: {len(valid_new):,}\n")

        logger.info(f"数据验证报告已保存: {output_file}")
        return output_file


def main():
    """主函数"""
    print("COVID-19 数据质量分析和修复工具")
    print("=" * 50)

    # 初始化验证器
    validator = COVID19DataValidator("covid-19_full_data.csv")

    # 加载数据
    if not validator.load_data():
        return

    # 分析数据质量
    print("\n1. 分析数据质量...")
    validation_report = validator.analyze_data_quality()

    # 清洗和修复数据
    print("\n2. 清洗和修复数据...")
    cleaned_df = validator.clean_and_repair_data()

    # 生成清洗后的数据集
    print("\n3. 生成清洗后的数据集...")
    cleaned_file = validator.generate_cleaned_dataset()

    # 生成验证报告
    print("\n4. 生成验证报告...")
    report_file = validator.generate_validation_report()

    print(f"\n✅ 数据清洗完成！")
    print(f"📁 清洗后的数据文件: {cleaned_file}")
    print(f"📊 验证报告: {report_file}")
    print(f"📈 原始数据行数: {len(validator.df):,}")
    print(f"📈 清洗后数据行数: {len(cleaned_df):,}")


if __name__ == "__main__":
    main()
