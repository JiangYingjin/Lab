# 全球GDP分布分级统计图分析报告

**生成时间**: 2025-10-02 20:03:24

## 1. 数据集基本信息

- **数据形状**: (5751, 7)
- **列名**: ['Country Name', 'Year', 'Employment Sector: Agriculture', 'Employment Sector: Industry', 'Employment Sector: Services', 'Unemployment Rate', 'GDP (in USD)']
- **年份范围**: 1991 - 2022
- **国家数量**: 183

## 2. 1991年GDP数据探索

### 2.1 数据完整性

- **总记录数**: 172
- **有GDP数据的国家数**: 172
- **GDP数据缺失数**: 0

### 2.2 GDP统计信息

```
最小值: 1.07e+08
最大值: 6.16e+12
中位数: 7.21e+09
平均值: 1.37e+11
标准差: 5.83e+11
```

### 2.3 GDP分位数分析

```
  10%: 5.99e+08
  25%: 2.63e+09
  50%: 7.21e+09
  75%: 4.66e+10
  90%: 2.63e+11
  95%: 4.45e+11
  99%: 2.39e+12
```

## 3. 数据处理过程

### 3.1 对数转换

由于GDP分布高度偏斜（从1.07e+08到6.16e+12），直接使用线性色图会导致大多数国家显示为同一种浅色。
因此采用对数转换来压缩极值范围，更好地分配颜色到数据。

**重要说明**：
- 对数转换仅用于**颜色映射**，确保颜色能够合理分布到所有国家
- 最终显示给用户的是**原始GDP数值**，便于理解
- 图例使用**分位数表示**（25%, 50%, 75%, 90%），直观易懂
- 颜色条显示**Billion/Trillion格式**的GDP值，简洁明了

```
log_gdp = np.log10(gdp_data)  # 用于颜色映射
# 但显示时使用原始GDP值
```

### 3.2 转换后的数据统计

```
         Year  Employment Sector: Agriculture  Employment Sector: Industry  Employment Sector: Services  Unemployment Rate  GDP (in USD)     log_GDP
count   172.0                      172.000000                   172.000000                   172.000000         172.000000  1.720000e+02  172.000000
mean   1991.0                       34.791883                    20.579806                    44.628292           7.464936  1.372943e+11   10.007749
std       0.0                       25.557142                    10.307817                    18.424735           5.942354  5.833545e+11    0.981694
min    1991.0                        0.399950                     2.074969                     5.581377           0.600000  1.074841e+08    8.031344
25%    1991.0                       11.598166                    12.099850                    31.822208           2.696000  2.625900e+09    9.419204
50%    1991.0                       28.413643                    21.482886                    45.126071           5.549500  7.206747e+09    9.857739
75%    1991.0                       54.356973                    27.534545                    58.430828          10.166000  4.657254e+10   10.667915
max    1991.0                       91.963821                    45.550193                    92.193517          25.669000  6.158129e+12   12.789449
```

## 4. 色彩映射选择

### 4.1 色图类型：顺序色彩映射 (Sequential Colormap)

**选择理由**：
- GDP是定量型数据，具有明确的'低-高'顺序关系
- 需要体现数值的连续性和递增性
- 主要依赖**亮度 (Luminance)** 变化来编码数值大小

**避免的色图类型**：
- **彩虹色图 (Rainbow Colormap)**：主要依赖色相变化，缺乏单调递增的亮度
- **分类色图**：不适用于连续数值数据

### 4.2 具体色图选择

- **色图名称**: GDP_Blue (Custom Sequential)
- **色图类型**: Sequential Colormap
- **颜色范围**: Light Blue to Dark Blue
- **设计原理**: 主要依赖亮度变化，从浅蓝（低GDP）到深蓝（高GDP），符合人类对'低-高'的直觉感知

## 5. 地理数据处理

### 5.1 世界地图数据

使用Natural Earth的世界地图数据，包含国家边界和基本地理信息。

- **地图数据形状**: (177, 3)
- **包含国家数**: 177
- **坐标系**: WGS84 (EPSG:4326)

### 5.2 国家名称匹配

处理数据集中的国家名称与地图数据中的国家名称不一致的问题。
主要匹配策略：
- 直接匹配
- 模糊匹配（处理拼写差异）
- 手动映射（处理特殊国家名称）

### 5.3 数据合并结果

- **1991年GDP数据总数**: 172
- **地图中国家总数**: 177
- **成功匹配的国家数**: 157
- **匹配成功率**: 91.3%
- **未匹配的GDP数据国家数**: 15
- **未匹配的地图国家数**: 20

### 5.4 成功匹配的国家列表（前20个，按GDP排序）

```
  1. United States -> USA (GDP: 6.16e+12)
  2. Japan -> Japan (GDP: 3.65e+12)
  3. Germany -> Germany (GDP: 1.88e+12)
  4. France -> France (GDP: 1.26e+12)
  5. Italy -> Italy (GDP: 1.25e+12)
  6. United Kingdom -> England (GDP: 1.14e+12)
  7. Canada -> Canada (GDP: 6.13e+11)
  8. Spain -> Spain (GDP: 5.77e+11)
  9. Russian Federation -> Russia (GDP: 5.18e+11)
 10. China -> China (GDP: 3.85e+11)
 11. Brazil -> Brazil (GDP: 3.43e+11)
 12. Korea, Rep. -> South Korea (GDP: 3.31e+11)
 13. Netherlands -> Netherlands (GDP: 3.28e+11)
 14. Australia -> Australia (GDP: 3.26e+11)
 15. Mexico -> Mexico (GDP: 3.13e+11)
 16. Sweden -> Sweden (GDP: 2.74e+11)
 17. India -> India (GDP: 2.70e+11)
 18. Switzerland -> Switzerland (GDP: 2.69e+11)
 19. Belgium -> Belgium (GDP: 2.11e+11)
 20. Argentina -> Argentina (GDP: 1.90e+11)
```

### 5.5 未匹配的GDP数据国家详情

以下国家在GDP数据中存在但无法在地图中找到对应：

```
  1. Bahrain
  2. Barbados
  3. Cabo Verde
  4. Comoros
  5. Hong Kong SAR, China
  6. Macao SAR, China
  7. Maldives
  8. Malta
  9. Mauritius
 10. Samoa
 11. Sao Tome and Principe
 12. Singapore
 13. St. Lucia
 14. St. Vincent and the Grenadines
 15. Tonga
```

### 5.6 未匹配的地图国家详情（前20个）

以下国家在地图中存在但GDP数据中无对应：

```
  1. Afghanistan
  2. Antarctica
  3. French Southern and Antarctic Lands
  4. Northern Cyprus
  5. Eritrea
  6. Estonia
  7. Falkland Islands
  8. Greenland
  9. Kosovo
 10. Lithuania
 11. Latvia
 12. Montenegro
 13. Puerto Rico
 14. North Korea
 15. Western Sahara
 16. South Sudan
 17. Somaliland
 18. Republic of Serbia
 19. Taiwan
 20. West Bank
```

### 5.7 匹配失败原因分析

**主要原因**：
1. **国家名称不一致**：数据集和地图使用不同的国家名称标准
2. **特殊行政区**：如香港、澳门等特殊行政区在地图中可能不存在
3. **历史国家**：1991年存在但后来分裂或合并的国家
4. **小岛屿国家**：一些小的岛屿国家可能在地图数据中缺失
5. **拼写差异**：同一国家的不同拼写方式

**改进措施**：
1. **扩展映射表**：添加更多国家名称映射规则
2. **模糊匹配**：使用字符串相似度算法进行模糊匹配
3. **手动校正**：对重要国家进行手动映射
4. **数据源统一**：使用统一的国家名称标准

## 6. 可视化参数

- **图表类型**: 分级统计图 (Choropleth Map)
- **数据年份**: 1991年
- **数据指标**: GDP (in USD)
- **图形大小**: 16x10 英寸
- **色彩映射**: 顺序色图
- **数据转换**: 对数转换
- **DPI**: 300

## 7. 统计结果

### 7.1 GDP分布统计

```
count    1.570000e+02
mean     1.494349e+11
std      6.093181e+11
min      1.109060e+08
25%      3.111160e+09
50%      9.000363e+09
75%      4.978750e+10
max      6.158129e+12
```

### 7.2 对数转换后统计

```
count    157.000000
mean      10.097180
std        0.943603
min        8.044955
25%        9.492922
50%        9.954260
75%       10.697120
max       12.789449
```

### 7.3 颜色分级统计

```
log_GDP
(8.044, 8.723]      10
(8.723, 9.401]      22
(9.401, 10.078]     56
(10.078, 10.756]    33
(10.756, 11.434]    20
(11.434, 12.112]    13
(12.112, 12.789]     3
```

---
*此报告由 task2_gdp_choropleth.py 自动生成*
