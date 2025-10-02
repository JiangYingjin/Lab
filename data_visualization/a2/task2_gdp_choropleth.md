# 全球GDP分布分级统计图分析报告

**生成时间**: 2025-10-02 20:04:20

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

## 7. 每个国家的详细数据

### 7.1 成功匹配的国家数据（按GDP排序）

| 排名 | 国家名称 | 映射名称 | 原始GDP (USD) | 对数GDP | GDP分位数 | 颜色分类 |
|------|----------|----------|---------------|---------|-----------|----------|
|   1 | United States | USA | $6.2T | 12.79 | > 90% | Very High GDP |
|   2 | Japan | Japan | $3.6T | 12.56 | > 90% | Very High GDP |
|   3 | Germany | Germany | $1.9T | 12.27 | > 90% | Very High GDP |
|   4 | France | France | $1.3T | 12.10 | > 90% | Very High GDP |
|   5 | Italy | Italy | $1.2T | 12.10 | > 90% | Very High GDP |
|   6 | United Kingdom | England | $1.1T | 12.06 | > 90% | Very High GDP |
|   7 | Canada | Canada | $612.5B | 11.79 | > 90% | Very High GDP |
|   8 | Spain | Spain | $576.8B | 11.76 | > 90% | Very High GDP |
|   9 | Russian Federation | Russia | $518.0B | 11.71 | > 90% | Very High GDP |
|  10 | China | China | $384.5B | 11.58 | > 90% | Very High GDP |
|  11 | Brazil | Brazil | $342.5B | 11.53 | > 90% | Very High GDP |
|  12 | Korea, Rep. | South Korea | $330.6B | 11.52 | > 90% | Very High GDP |
|  13 | Netherlands | Netherlands | $328.0B | 11.52 | > 90% | Very High GDP |
|  14 | Australia | Australia | $326.0B | 11.51 | > 90% | Very High GDP |
|  15 | Mexico | Mexico | $313.1B | 11.50 | > 90% | Very High GDP |
|  16 | Sweden | Sweden | $273.8B | 11.44 | > 90% | Very High GDP |
|  17 | India | India | $270.1B | 11.43 | 75% - 90% | High GDP |
|  18 | Switzerland | Switzerland | $268.9B | 11.43 | 75% - 90% | High GDP |
|  19 | Belgium | Belgium | $210.5B | 11.32 | 75% - 90% | High GDP |
|  20 | Argentina | Argentina | $189.7B | 11.28 | 75% - 90% | High GDP |
|  21 | Austria | Austria | $173.1B | 11.24 | 75% - 90% | High GDP |
|  22 | Turkiye | Turkey | $151.0B | 11.18 | 75% - 90% | High GDP |
|  23 | Denmark | Denmark | $139.2B | 11.14 | 75% - 90% | High GDP |
|  24 | South Africa | South Africa | $135.2B | 11.13 | 75% - 90% | High GDP |
|  25 | Saudi Arabia | Saudi Arabia | $132.2B | 11.12 | 75% - 90% | High GDP |
|  26 | Iran, Islamic Rep. | Iran | $131.6B | 11.12 | 75% - 90% | High GDP |
|  27 | Finland | Finland | $127.8B | 11.11 | 75% - 90% | High GDP |
|  28 | Norway | Norway | $121.9B | 11.09 | 75% - 90% | High GDP |
|  29 | Indonesia | Indonesia | $116.6B | 11.07 | 75% - 90% | High GDP |
|  30 | Greece | Greece | $103.7B | 11.02 | 75% - 90% | High GDP |
|  31 | Thailand | Thailand | $98.2B | 10.99 | 75% - 90% | High GDP |
|  32 | Portugal | Portugal | $89.2B | 10.95 | 75% - 90% | High GDP |
|  33 | Poland | Poland | $85.5B | 10.93 | 75% - 90% | High GDP |
|  34 | Ukraine | Ukraine | $77.4B | 10.89 | 75% - 90% | High GDP |
|  35 | Israel | Israel | $71.0B | 10.85 | 75% - 90% | High GDP |
|  36 | Nigeria | Nigeria | $59.5B | 10.77 | 75% - 90% | High GDP |
|  37 | Venezuela, RB | Venezuela | $53.5B | 10.73 | 75% - 90% | High GDP |
|  38 | Philippines | Philippines | $51.8B | 10.71 | 75% - 90% | High GDP |
|  39 | United Arab Emirates | United Arab Emirates | $51.6B | 10.71 | 75% - 90% | High GDP |
|  40 | Ireland | Ireland | $49.8B | 10.70 | 75% - 90% | High GDP |
|  41 | Colombia | Colombia | $49.6B | 10.70 | 50% - 75% | Medium GDP |
|  42 | Malaysia | Malaysia | $49.1B | 10.69 | 50% - 75% | Medium GDP |
|  43 | Algeria | Algeria | $45.7B | 10.66 | 50% - 75% | Medium GDP |
|  44 | Pakistan | Pakistan | $45.6B | 10.66 | 50% - 75% | Medium GDP |
|  45 | Sudan | Sudan | $44.2B | 10.65 | 50% - 75% | Medium GDP |
|  46 | New Zealand | New Zealand | $42.7B | 10.63 | 50% - 75% | Medium GDP |
|  47 | Chile | Chile | $38.2B | 10.58 | 50% - 75% | Medium GDP |
|  48 | Egypt, Arab Rep. | Egypt | $37.4B | 10.57 | 50% - 75% | Medium GDP |
|  49 | Hungary | Hungary | $34.9B | 10.54 | 50% - 75% | Medium GDP |
|  50 | Peru | Peru | $34.3B | 10.54 | 50% - 75% | Medium GDP |
|  51 | Morocco | Morocco | $32.3B | 10.51 | 50% - 75% | Medium GDP |
|  52 | Libya | Libya | $32.0B | 10.51 | 50% - 75% | Medium GDP |
|  53 | Bangladesh | Bangladesh | $31.0B | 10.49 | 50% - 75% | Medium GDP |
|  54 | Czechia | Czech Republic | $30.1B | 10.48 | 50% - 75% | Medium GDP |
|  55 | Romania | Romania | $28.9B | 10.46 | 50% - 75% | Medium GDP |
|  56 | Kazakhstan | Kazakhstan | $24.9B | 10.40 | 50% - 75% | Medium GDP |
|  57 | Cuba | Cuba | $24.3B | 10.39 | 50% - 75% | Medium GDP |
|  58 | Croatia | Croatia | $18.8B | 10.27 | 50% - 75% | Medium GDP |
|  59 | Belarus | Belarus | $18.4B | 10.26 | 50% - 75% | Medium GDP |
|  60 | Ecuador | Ecuador | $17.0B | 10.23 | 50% - 75% | Medium GDP |
|  61 | Yemen, Rep. | Yemen | $14.7B | 10.17 | 50% - 75% | Medium GDP |
|  62 | Slovak Republic | Slovakia | $14.5B | 10.16 | 50% - 75% | Medium GDP |
|  63 | Slovenia | Slovenia | $14.5B | 10.16 | 50% - 75% | Medium GDP |
|  64 | Luxembourg | Luxembourg | $13.8B | 10.14 | 50% - 75% | Medium GDP |
|  65 | Uzbekistan | Uzbekistan | $13.8B | 10.14 | 50% - 75% | Medium GDP |
|  66 | Ethiopia | Ethiopia | $13.8B | 10.14 | 50% - 75% | Medium GDP |
|  67 | Tunisia | Tunisia | $13.1B | 10.12 | 50% - 75% | Medium GDP |
|  68 | Syrian Arab Republic | Syria | $13.0B | 10.11 | 50% - 75% | Medium GDP |
|  69 | Oman | Oman | $12.9B | 10.11 | 50% - 75% | Medium GDP |
|  70 | Cameroon | Cameroon | $11.8B | 10.07 | 50% - 75% | Medium GDP |
|  71 | Uruguay | Uruguay | $11.2B | 10.05 | 50% - 75% | Medium GDP |
|  72 | Kuwait | Kuwait | $11.0B | 10.04 | 50% - 75% | Medium GDP |
|  73 | Angola | Angola | $10.6B | 10.03 | 50% - 75% | Medium GDP |
|  74 | Cote d'Ivoire | Ivory Coast | $10.5B | 10.02 | 50% - 75% | Medium GDP |
|  75 | Dominican Republic | Dominican Republic | $9.8B | 9.99 | 50% - 75% | Medium GDP |
|  76 | Congo, Dem. Rep. | Democratic Republic of the Congo | $9.6B | 9.98 | 50% - 75% | Medium GDP |
|  77 | Viet Nam | Vietnam | $9.6B | 9.98 | 50% - 75% | Medium GDP |
|  78 | Guatemala | Guatemala | $9.4B | 9.97 | 50% - 75% | Medium GDP |
|  79 | Sri Lanka | Sri Lanka | $9.0B | 9.95 | 50% - 75% | Medium GDP |
|  80 | Zimbabwe | Zimbabwe | $8.6B | 9.94 | 25% - 50% | Medium-Low GDP |
|  81 | Kenya | Kenya | $8.2B | 9.91 | 25% - 50% | Medium-Low GDP |
|  82 | Bulgaria | Bulgaria | $7.6B | 9.88 | 25% - 50% | Medium-Low GDP |
|  83 | Senegal | Senegal | $7.3B | 9.86 | 25% - 50% | Medium-Low GDP |
|  84 | Costa Rica | Costa Rica | $7.2B | 9.86 | 25% - 50% | Medium-Low GDP |
|  85 | Tanzania | United Republic of Tanzania | $7.2B | 9.86 | 25% - 50% | Medium-Low GDP |
|  86 | Panama | Panama | $7.1B | 9.85 | 25% - 50% | Medium-Low GDP |
|  87 | Paraguay | Paraguay | $7.0B | 9.84 | 25% - 50% | Medium-Low GDP |
|  88 | Iceland | Iceland | $6.9B | 9.84 | 25% - 50% | Medium-Low GDP |
|  89 | Qatar | Qatar | $6.9B | 9.84 | 25% - 50% | Medium-Low GDP |
|  90 | Ghana | Ghana | $6.6B | 9.82 | 25% - 50% | Medium-Low GDP |
|  91 | Georgia | Georgia | $6.3B | 9.80 | 25% - 50% | Medium-Low GDP |
|  92 | Brunei Darussalam | Brunei | $6.3B | 9.80 | 25% - 50% | Medium-Low GDP |
|  93 | Bosnia and Herzegovina | Bosnia and Herzegovina | $6.1B | 9.79 | 25% - 50% | Medium-Low GDP |
|  94 | Cyprus | Cyprus | $5.8B | 9.76 | 25% - 50% | Medium-Low GDP |
|  95 | Gabon | Gabon | $5.4B | 9.73 | 25% - 50% | Medium-Low GDP |
|  96 | Azerbaijan | Azerbaijan | $5.3B | 9.73 | 25% - 50% | Medium-Low GDP |
|  97 | Bolivia | Bolivia | $5.3B | 9.73 | 25% - 50% | Medium-Low GDP |
|  98 | Trinidad and Tobago | Trinidad and Tobago | $5.3B | 9.72 | 25% - 50% | Medium-Low GDP |
|  99 | El Salvador | El Salvador | $5.3B | 9.72 | 25% - 50% | Medium-Low GDP |
| 100 | North Macedonia | Macedonia | $4.9B | 9.69 | 25% - 50% | Medium-Low GDP |
| 101 | Lebanon | Lebanon | $4.7B | 9.67 | 25% - 50% | Medium-Low GDP |
| 102 | Honduras | Honduras | $4.6B | 9.67 | 25% - 50% | Medium-Low GDP |
| 103 | Guinea | Guinea | $4.4B | 9.64 | 25% - 50% | Medium-Low GDP |
| 104 | Jordan | Jordan | $4.3B | 9.64 | 25% - 50% | Medium-Low GDP |
| 105 | Jamaica | Jamaica | $4.1B | 9.61 | 25% - 50% | Medium-Low GDP |
| 106 | Botswana | Botswana | $3.9B | 9.60 | 25% - 50% | Medium-Low GDP |
| 107 | Nepal | Nepal | $3.9B | 9.59 | 25% - 50% | Medium-Low GDP |
| 108 | Mozambique | Mozambique | $3.9B | 9.59 | 25% - 50% | Medium-Low GDP |
| 109 | Papua New Guinea | Papua New Guinea | $3.8B | 9.58 | 25% - 50% | Medium-Low GDP |
| 110 | Haiti | Haiti | $3.5B | 9.54 | 25% - 50% | Medium-Low GDP |
| 111 | Zambia | Zambia | $3.4B | 9.53 | 25% - 50% | Medium-Low GDP |
| 112 | Uganda | Uganda | $3.3B | 9.52 | 25% - 50% | Medium-Low GDP |
| 113 | Niger | Niger | $3.3B | 9.52 | 25% - 50% | Medium-Low GDP |
| 114 | Madagascar | Madagascar | $3.3B | 9.51 | 25% - 50% | Medium-Low GDP |
| 115 | Turkmenistan | Turkmenistan | $3.2B | 9.51 | 25% - 50% | Medium-Low GDP |
| 116 | Malawi | Malawi | $3.2B | 9.51 | 25% - 50% | Medium-Low GDP |
| 117 | Burkina Faso | Burkina Faso | $3.1B | 9.50 | 25% - 50% | Medium-Low GDP |
| 118 | Bahamas, The | The Bahamas | $3.1B | 9.49 | 25% - 50% | Medium-Low GDP |
| 119 | Moldova | Moldova | $3.1B | 9.49 | < 25% | Low GDP |
| 120 | Namibia | Namibia | $3.0B | 9.48 | < 25% | Low GDP |
| 121 | Congo, Rep. | Republic of the Congo | $2.7B | 9.44 | < 25% | Low GDP |
| 122 | Mali | Mali | $2.7B | 9.44 | < 25% | Low GDP |
| 123 | New Caledonia | New Caledonia | $2.7B | 9.42 | < 25% | Low GDP |
| 124 | Kyrgyz Republic | Kyrgyzstan | $2.5B | 9.41 | < 25% | Low GDP |
| 125 | Tajikistan | Tajikistan | $2.5B | 9.40 | < 25% | Low GDP |
| 126 | Mongolia | Mongolia | $2.4B | 9.38 | < 25% | Low GDP |
| 127 | Togo | Togo | $2.3B | 9.35 | < 25% | Low GDP |
| 128 | Mauritania | Mauritania | $2.1B | 9.33 | < 25% | Low GDP |
| 129 | Armenia | Armenia | $2.1B | 9.32 | < 25% | Low GDP |
| 130 | Myanmar | Myanmar | $2.1B | 9.32 | < 25% | Low GDP |
| 131 | Cambodia | Cambodia | $2.1B | 9.31 | < 25% | Low GDP |
| 132 | Benin | Benin | $2.0B | 9.30 | < 25% | Low GDP |
| 133 | Rwanda | Rwanda | $1.9B | 9.28 | < 25% | Low GDP |
| 134 | Chad | Chad | $1.9B | 9.27 | < 25% | Low GDP |
| 135 | Nicaragua | Nicaragua | $1.5B | 9.17 | < 25% | Low GDP |
| 136 | Fiji | Fiji | $1.4B | 9.14 | < 25% | Low GDP |
| 137 | Central African Republic | Central African Republic | $1.4B | 9.14 | < 25% | Low GDP |
| 138 | Burundi | Burundi | $1.2B | 9.07 | < 25% | Low GDP |
| 139 | Eswatini | Swaziland | $1.2B | 9.06 | < 25% | Low GDP |
| 140 | Albania | Albania | $1.1B | 9.04 | < 25% | Low GDP |
| 141 | Lao PDR | Laos | $1.0B | 9.01 | < 25% | Low GDP |
| 142 | Sierra Leone | Sierra Leone | $780.0M | 8.89 | < 25% | Low GDP |
| 143 | Somalia | Somalia | $718.0M | 8.86 | < 25% | Low GDP |
| 144 | Lesotho | Lesotho | $704.3M | 8.85 | < 25% | Low GDP |
| 145 | Gambia, The | Gambia | $690.3M | 8.84 | < 25% | Low GDP |
| 146 | Guinea-Bissau | Guinea Bissau | $668.5M | 8.83 | < 25% | Low GDP |
| 147 | Belize | Belize | $597.1M | 8.78 | < 25% | Low GDP |
| 148 | Djibouti | Djibouti | $462.4M | 8.67 | < 25% | Low GDP |
| 149 | Suriname | Suriname | $448.1M | 8.65 | < 25% | Low GDP |
| 150 | Iraq | Iraq | $407.8M | 8.61 | < 25% | Low GDP |
| 151 | Guyana | Guyana | $348.5M | 8.54 | < 25% | Low GDP |
| 152 | Liberia | Liberia | $348.0M | 8.54 | < 25% | Low GDP |
| 153 | Bhutan | Bhutan | $240.3M | 8.38 | < 25% | Low GDP |
| 154 | Solomon Islands | Solomon Islands | $227.5M | 8.36 | < 25% | Low GDP |
| 155 | Vanuatu | Vanuatu | $201.3M | 8.30 | < 25% | Low GDP |
| 156 | Timor-Leste | East Timor | $147.7M | 8.17 | < 25% | Low GDP |
| 157 | Equatorial Guinea | Equatorial Guinea | $110.9M | 8.04 | < 25% | Low GDP |

### 7.2 未匹配的GDP数据国家

以下国家在GDP数据中存在但无法在地图中找到对应：

| 序号 | 国家名称 | 原始GDP (USD) | 对数GDP | GDP分位数 |
|------|----------|---------------|---------|-----------|
|   1 | Bahrain | $5.2B | 9.72 | 25% - 50% |
|   2 | Barbados | $2.0B | 9.31 | < 25% |
|   3 | Cabo Verde | $319.8M | 8.50 | < 25% |
|   4 | Comoros | $424.1M | 8.63 | < 25% |
|   5 | Hong Kong SAR, China | $89.0B | 10.95 | 75% - 90% |
|   6 | Macao SAR, China | $3.8B | 9.58 | 25% - 50% |
|   7 | Maldives | $244.4M | 8.39 | < 25% |
|   8 | Malta | $2.8B | 9.44 | 25% - 50% |
|   9 | Mauritius | $2.9B | 9.46 | 25% - 50% |
|  10 | Samoa | $125.6M | 8.10 | < 25% |
|  11 | Sao Tome and Principe | $107.5M | 8.03 | < 25% |
|  12 | Singapore | $45.5B | 10.66 | 50% - 75% |
|  13 | St. Lucia | $613.7M | 8.79 | < 25% |
|  14 | St. Vincent and the Grenadines | $254.8M | 8.41 | < 25% |
|  15 | Tonga | $132.2M | 8.12 | < 25% |

## 8. 统计结果

### 8.1 GDP分布统计

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

### 8.2 对数转换后统计

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

### 8.3 颜色分级统计

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
