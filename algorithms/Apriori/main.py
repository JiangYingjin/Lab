import os, itertools
import numpy as np
import pandas as pd


class Apriori(object):
    def __init__(self, itemSets, minSupport=0.5, minConf=0.7, sort=False):
        self.itemSets = itemSets
        self.minSupport = minSupport
        self.minConf = minConf
        self.sort = sort
        self.__Initialize()

    def __Initialize(self):
        self.__item()
        self.__creat_matrix()
        self.update(minSupport=self.minSupport, minConf=self.minConf)

    def __item(self):
        """获取项目元素列表"""
        self.item = []
        for itemSet in self.itemSets:
            for item in itemSet:
                if item not in self.item:
                    self.item.append(item)
        self.item.sort()

    def __creat_matrix(self):
        """将项集转为pandas.DataFrame数据类型"""
        self.data = pd.DataFrame(columns=self.item)
        print(self.data)
        for i in range(len(self.itemSets)):
            self.data.loc[i, self.itemSets[i]] = 1
        print(self.data)

    def __candidate_itemsets_l1(self):
        """创建单项频繁项集及L1"""
        self.L1 = self.data.loc[
            :, self.data.sum(axis=0) / len(self.itemSets) >= self.minSupport
        ]
        self.L1_support_selects = dict(
            self.L1.sum(axis=0) / len(self.itemSets)
        )  # 只作为分母，不进行拆分

    def __candidate_itemsets_lk(self):
        """根据L1创建多项频繁项集Lk，非频繁项集的任何超集都不是频繁项集"""
        last_support_selects = self.L1_support_selects.copy()  # 初始化
        while last_support_selects:
            new_support_selects = {}
            for last_support_select in last_support_selects.keys():
                for L1_support_name in set(self.L1.columns) - set(
                    last_support_select.split(",")
                ):
                    columns = sorted(
                        [L1_support_name] + last_support_select.split(",")
                    )  # 新的列名：合并后排序
                    count = (self.L1.loc[:, columns].sum(axis=1) == len(columns)).sum()
                    if count / len(self.itemSets) >= self.minSupport:
                        new_support_selects[",".join(columns)] = count / len(
                            self.itemSets
                        )
            self.support_selects.update(new_support_selects)
            last_support_selects = (
                new_support_selects.copy()
            )  # 作为新的 Lk，进行下一轮更新

    def __support_selects(self):
        """支持度选择"""
        self.__candidate_itemsets_l1()
        self.__candidate_itemsets_lk()
        self.item_Conf = self.L1_support_selects.copy()
        self.item_Conf.update(self.support_selects)

    def __confidence_selects(self):
        """生成关联规则，其中support_selects已经按照长度大小排列"""
        for groups, Supp_groups in self.support_selects.items():
            groups_list = groups.split(",")
            for recommend_len in range(1, len(groups_list)):
                for recommend in itertools.combinations(groups_list, recommend_len):
                    items = ",".join(sorted(set(groups_list) - set(recommend)))
                    Conf = Supp_groups / self.item_Conf[items]
                    if Conf >= self.minConf:
                        self.confidence_select.setdefault(items, {})
                        self.confidence_select[items].setdefault(
                            ",".join(recommend),
                            {"Support": Supp_groups, "Confidence": Conf},
                        )

    def show(self, **kwargs):
        """可视化输出"""
        if kwargs.get("data"):
            select = kwargs["data"]
        else:
            select = self.confidence_select
        items = []
        value = []
        for ks, vs in select.items():
            items.extend(list(zip([ks] * vs.__len__(), vs.keys())))
            for v in vs.values():
                value.append([v["Support"], v["Confidence"]])
        index = pd.MultiIndex.from_tuples(items, names=["Items", "Recommend"])
        self.rules = pd.DataFrame(value, index=index, columns=["Support", "Confidence"])
        if self.sort or kwargs.get("sort"):
            result = self.rules.sort_values(
                by=["Support", "Confidence"], ascending=False
            )
        else:
            result = self.rules.copy()
        return result

    def update(self, **kwargs):
        """用于更新数据"""
        if kwargs.get("minSupport"):
            self.minSupport = kwargs["minSupport"]
            self.support_selects = {}  # 用于储存满足支持度的频繁项集
            self.__support_selects()
        if kwargs.get("minConf"):
            self.minConf = kwargs["minConf"]
            self.confidence_select = {}  # 用于储存满足自信度的关联规则
            self.__confidence_selects()
        print(self.show())
        if kwargs.get("file_name"):
            file_name = kwargs["file_name"]
            if file_name.endswith(".xlsx"):
                self.show().to_excel(f"{file_name}")
            else:
                self.show().to_excel(f"{file_name}.xlsx")

        self.apriori_rules = self.rules.copy()

    def __get_Recommend_list(self, itemSet):
        """输入数据，获取关联规则列表"""
        self.recommend_selects = {}
        itemSet = set(itemSet) & set(self.apriori_rules.index.levels[0])
        if itemSet:
            for start_str in itemSet:
                for end_str in self.apriori_rules.loc[start_str].index:
                    start_list = start_str.split(",")
                    end_list = end_str.split(",")
                    self.__creat_Recommend_list(start_list, end_list, itemSet)

    def __creat_Recommend_list(self, start_list, end_list, itemSet):
        """迭代创建关联规则列表"""
        if set(end_list).issubset(itemSet):
            start_str = ",".join(sorted(start_list + end_list))
            if start_str in self.apriori_rules.index.levels[0]:
                for end_str in self.apriori_rules.loc[start_str].index:
                    start_list = start_str.split(",")
                    end_list = end_str.split(",")
                    self.__creat_Recommend_list(sorted(start_list), end_list, itemSet)
        elif not set(end_list) & itemSet:
            start_str = ",".join(start_list)
            end_str = ",".join(end_list)
            self.recommend_selects.setdefault(start_str, {})
            self.recommend_selects[start_str].setdefault(
                end_str,
                {
                    "Support": self.apriori_rules.loc[(start_str, end_str), "Support"],
                    "Confidence": self.apriori_rules.loc[
                        (start_str, end_str), "Confidence"
                    ],
                },
            )

    def get_Recommend(self, itemSet, **kwargs):
        """获取加权关联规则"""
        self.recommend = {}
        self.__get_Recommend_list(itemSet)
        self.show(data=self.recommend_selects)
        items = self.rules.index.levels[0]
        for item_str in items:
            for recommends_str in self.rules.loc[item_str].index:
                recommends_list = recommends_str.split(",")
                for recommend_str in recommends_list:
                    self.recommend.setdefault(recommend_str, 0)
                    self.recommend[recommend_str] += (
                        self.rules.loc[(item_str, recommends_str), "Support"]
                        * self.rules.loc[(item_str, recommends_str), "Confidence"]
                        * self.rules.loc[item_str, "Support"].mean()
                        / (
                            self.rules.loc[item_str, "Support"].sum()
                            * len(recommends_list)
                        )
                    )
        result = pd.Series(self.recommend, name="Weight").sort_values(ascending=False)
        result.index.name = "Recommend"
        result = result / result.sum()
        result = 1 / (1 + np.exp(-result))
        print(result)
        if kwargs.get("file_name"):
            file_name = kwargs["file_name"]
            if file_name.endswith(".xlsx"):
                excel_writer = pd.ExcelWriter(f"{file_name}")
            else:
                excel_writer = pd.ExcelWriter(f"{file_name}.xlsx")
            result.to_excel(excel_writer, "推荐项目及权重")
            self.rules.to_excel(excel_writer, "关联规则树状表")
            self.show().to_excel(excel_writer, "总关联规则树状表")
            self.show(sort=True).to_excel(excel_writer, "总关联规则排序表")
            excel_writer.save()
        return result


def str2itemsets(strings, split=","):
    """将字符串列表转化为对应的集合"""
    itemsets = []
    for string in strings:
        itemsets.append(sorted(string.split(split)))
    return itemsets


if __name__ == "__main__":
    # 1.导入数据（csv）
    data = pd.read_csv(
        f"{os.path.dirname(__file__)}/data.csv",
    )

    # 2.关联规则中不考虑多次购买同一件物品，删除重复数据
    data = data.drop_duplicates()

    # 3.初始化列表
    itemSets = []

    # 3.按销售单分组，只有1件商品的没有意义，需要进行过滤
    groups = data.groupby(by="销售单明细")

    # for group in groups:
    #     print(group[1])
    # exit()

    for group in groups:
        if len(group[1]) >= 2:
            itemSets.append(group[1]["商品编码"].tolist())
            print(group[1]["商品编码"].tolist())

    print(itemSets)

    # 4.训练 Apriori
    ap = Apriori(itemSets, minSupport=0.03, minConf=0.5)
    ap.get_Recommend("2BYP206,2BYW001-,2BYW013,2BYX029".split(","))
