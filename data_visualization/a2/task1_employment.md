# 就业分布数据可视化分析报告

**生成时间**: 2025-10-02 20:08:24

## 1. 数据集基本信息

- **数据形状**: (5751, 7)
- **列名**: ['Country Name', 'Year', 'Employment Sector: Agriculture', 'Employment Sector: Industry', 'Employment Sector: Services', 'Unemployment Rate', 'GDP (in USD)']
- **年份范围**: 1991 - 2022
- **国家数量**: 183

## 2. 原始数据样本

```
   Country Name  Year  Employment Sector: Agriculture  Employment Sector: Industry  Employment Sector: Services  Unemployment Rate  GDP (in USD)
0       Albania  1991                       53.299533                    12.172764                    34.527781             10.304  1.099559e+09
1       Algeria  1991                       24.118566                    25.067734                    50.813700             20.600  4.571568e+10
2        Angola  1991                       40.071857                     8.163345                    51.764822             16.855  1.060378e+10
3     Argentina  1991                       13.669999                    28.505903                    57.824098              5.440  1.897200e+11
4       Armenia  1991                       54.263252                    15.790454                    29.946294              1.783  2.069870e+09
5     Australia  1991                        5.356652                    24.298454                    70.344881              9.586  3.259753e+11
6       Austria  1991                        7.364231                    33.359477                    59.276322              3.420  1.731134e+11
7    Azerbaijan  1991                       43.875473                    22.950632                    33.173923              0.900  5.344000e+09
8  Bahamas, The  1991                        5.253697                    15.316695                    79.428776             12.170  3.111160e+09
9       Bahrain  1991                        2.432939                    28.526735                    69.040326              1.051  5.248911e+09
```

## 3. 选定的年份和国家

- **选定年份**: 2020
- **选定国家**: ['United States', 'China', 'Germany', 'India', 'Brazil']

## 4. 选定年份的可用数据

```
       Country Name  Year  Employment Sector: Agriculture  Employment Sector: Industry  Employment Sector: Services  Unemployment Rate  GDP (in USD)
5238         Brazil  2020                        9.314071                    20.256473                    70.429445             13.697  1.476107e+12
5250          China  2020                       23.599859                    31.592681                    44.807460              5.000  1.499641e+13
5277        Germany  2020                        1.220722                    27.371820                    71.407468              3.881  3.940143e+12
5290          India  2020                       44.675494                    23.703649                    31.620857              7.859  2.674852e+12
5387  United States  2020                        1.746393                    19.418403                    78.835204              8.055  2.135410e+13
```

## 5. 数据预处理结果

### 5.1 重命名后的数据

```
            Country  Agriculture   Industry   Services
5238         Brazil     9.314071  20.256473  70.429445
5250          China    23.599859  31.592681  44.807460
5277        Germany     1.220722  27.371820  71.407468
5290          India    44.675494  23.703649  31.620857
5387  United States     1.746393  19.418403  78.835204
```

### 5.2 转换后的长格式数据（用于可视化）

```
          Country       Sector  Employment_Rate
0          Brazil  Agriculture         9.314071
1           China  Agriculture        23.599859
2         Germany  Agriculture         1.220722
3           India  Agriculture        44.675494
4   United States  Agriculture         1.746393
5          Brazil     Industry        20.256473
6           China     Industry        31.592681
7         Germany     Industry        27.371820
8           India     Industry        23.703649
9   United States     Industry        19.418403
10         Brazil     Services        70.429445
11          China     Services        44.807460
12        Germany     Services        71.407468
13          India     Services        31.620857
14  United States     Services        78.835204
```

## 6. 按国家统计分析

```
              Employment_Rate                     
                         mean    std    min    max
Country                                           
Brazil                  33.33  32.59   9.31  70.43
China                   33.33  10.71  23.60  44.81
Germany                 33.33  35.47   1.22  71.41
India                   33.33  10.59  23.70  44.68
United States           33.33  40.38   1.75  78.84
```

## 7. 按部门统计分析

```
            Employment_Rate                     
                       mean    std    min    max
Sector                                          
Agriculture           16.11  18.35   1.22  44.68
Industry              24.47   5.07  19.42  31.59
Services              59.42  20.18  31.62  78.84
```

## 8. 各国主导部门

- **Brazil**: Services (70.4%)
- **China**: Services (44.8%)
- **Germany**: Services (71.4%)
- **India**: Agriculture (44.7%)
- **United States**: Services (78.8%)

## 9. 数据质量检查

### 9.1 缺失值统计

```
Country Name                      0
Year                              0
Employment Sector: Agriculture    0
Employment Sector: Industry       0
Employment Sector: Services       0
Unemployment Rate                 0
GDP (in USD)                      0
```

### 9.2 数据范围检查

```
              Year  Employment Sector: Agriculture  Employment Sector: Industry  Employment Sector: Services  Unemployment Rate  GDP (in USD)
count  5751.000000                     5751.000000                  5751.000000                  5751.000000        5751.000000  5.751000e+03
mean   2006.568945                       28.857051                    19.773784                    51.369166           8.155004  3.099333e+11
std       9.175548                       24.026669                     8.606954                    18.892155           6.147428  1.375556e+12
min    1991.000000                        0.107774                     2.060372                     5.314014           0.100000  7.228540e+07
25%    1999.000000                        7.173214                    13.889285                    36.846735           3.659000  5.098458e+09
50%    2007.000000                       22.172104                    20.105516                    52.657618           6.358000  1.972356e+10
75%    2014.000000                       46.130703                    25.345213                    66.602313          10.996000  1.277237e+11
max    2022.000000                       92.482036                    59.579079                    93.416932          38.800000  2.600689e+13
```

## 10. 可视化参数

- **图表类型**: 分组柱状图
- **图形大小**: 14x8 英寸
- **调色板**: Set2
- **图例位置**: 左上角
- **图例字体大小**: 标题10pt, 内容9pt
- **DPI**: 300

---
*此报告由 task1_employment.py 自动生成*
