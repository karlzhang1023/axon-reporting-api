# Axon Reporting API 完整文档

> 本文档由 Claude 从 Axon 官方文档自动提取和学习
> 来源: https://support.axon.ai/en/growth/promoting-your-apps/api/reporting-api/
> 最后更新: 2026-03-04

## 📡 API 基础信息

### 请求端点
```
GET https://r.applovin.com/report
```

### 时区
所有数据使用 **UTC (协调世界时)**

### 数据窗口
- **限制**: 45天
- 日期参数必须在最近45天内

---

## 🔑 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `api_key` | Report Key (在 Axon Dashboard 的 Keys 页面获取) | `CmMT3xNyJa_CwqZcggeJMvIAQxLsq36L_-v8OcsIps0xBw7Ounh-h4IyTnwzhKBm6APccOMJX-yU9HAmhb0vRl` |
| `start` | 开始日期 (YYYY-MM-DD 或 Unix timestamp) | `2026-01-01` 或 `1735689600` |
| `end` | 结束日期 (YYYY-MM-DD 或 "now") | `2026-01-31` 或 `now` |
| `format` | 返回格式 | `json` 或 `csv` |
| `columns` | 列名列表 (逗号分隔) | `day,campaign,impressions,clicks,cost` |
| `report_type` | 报告类型 | `advertiser` 或 `publisher` (默认: publisher) |

---

## ⚙️ 可选参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `day_column` | 设置为 `day` 使用 cohort 数据 (默认为 realtime) | `day` |
| `limit` | 返回行数限制 | `500` |
| `offset` | 起始行偏移量 (分页用) | `100` |
| `having` | 基于数值过滤 (URL编码) | `impressions%20%3E%200%20AND%20revenue%20%3E%200` |
| `not_zero` | 过滤全数值为0的行 | `1` |

---

## 📊 Publisher 列 (22个)

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `ad_type` | 广告类型 | `APPOPEN`, `GRAPHIC`, `MRAID`, `PLAY`, `REWARD`, `VIDEO` |
| `application` | 应用名称 | `My Game` |
| `application_is_hidden` | 应用是否在 Dashboard 隐藏 | `true`/`false` |
| `bidding_integration` | 竞价集成提供商 | `MAX`, `Google`, `None` |
| `clicks` | 点击次数 | `1234` |
| `country` | 国家代码 (两位) | `US`, `CN`, `JP` |
| `ctr` | 点击率 (点击/展示) | `0.05` |
| `day` | 报告日期 | `2026-03-04` |
| `device_type` | 设备类型 | `phone`, `tablet`, `other` |
| `ecpm` | 千次展示收益 | `5.50` |
| `hour` | 报告小时 (仅最近30天) | `0-23` |
| `impressions` | 展示次数 | `100000` |
| `package_name` | 包名或 Bundle ID | `com.example.game` |
| `placement_type` | 展位类型 | `APP_OPEN`, `BANNER`, `INTER`, `LEADER`, `MREC`, `NATIVE`, `REWARDED_INTER` |
| `platform` | 平台 | `android`, `fireos`, `ios` |
| `revenue` | 收益 | `1234.56` |
| `size` | 广告尺寸 | `BANNER`, `INTER`, `LEADER`, `MREC`, `NATIVE` |
| `store_id` | iTunes ID 数字部分或 package_name | `123456789` |
| `zone` | Zone 名称 (需账户权限) | `Zone 1` |
| `zone_id` | Zone ID (需账户权限) | `12345` |

---

## 📊 Advertiser 列 (61个)

### 基础列

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `day` | 报告日期 | `2026-03-04` |
| `hour` | 报告小时 (仅最近30天) | `0-23` |
| `campaign` | Campaign 名称 | `My_Campaign_20260304` |
| `campaign_id_external` | Campaign 外部ID (重命名后不变) | `abc123` |
| `ad` | 广告名称 | `My Ad 1` |
| `application` | 源应用名称 | `My Game` |
| `app_id_external` | 应用ID哈希 (Site ID) | `1a2b3c4d` |

### 指标列 - 基础

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `impressions` | 展示次数 | `100000` |
| `clicks` | 点击次数 | `5000` |
| `conversions` | 转化数 (安装数) | `1000` |
| `ctr` | 点击率 (点击/展示) | `0.05` |
| `conversion_rate` | 转化率 (转化/展示) | `0.01` |
| `cost` | 广告支出 | `1234.56` |
| `average_cpc` | 平均点击成本 | `0.25` |
| `average_cpa` | 平均转化成本 | `1.23` |

### 指标列 - ROAS (支持时间后缀: `0d`, `1d`, `2d`, `3d`, `7d`, `14d`, `28d`, `30d`, `90d`, `1y`)

| 列名 | 说明 | 示例 |
|------|------|------|
| `roas_x` | 总ROAS (IAA + IAP) | `roas_7d`, `roas_28d` |
| `iap_roas_x` | IAP ROAS | `iap_roas_7d`, `iap_roas_28d` |
| `ad_roas_x` | Ad ROAS (IAA) | `ad_roas_7d`, `ad_roas_28d` |

**示例值**: `1.50` (150%)

### 指标列 - 收入 (支持时间后缀)

| 列名 | 说明 | 示例 |
|------|------|------|
| `iap_rev_x` | IAP 收入 | `iap_rev_7d`, `iap_rev_28d` |
| `ad_rev_x` | Ad 收入 | `ad_rev_7d`, `ad_rev_28d` |
| `total_rev_x` | 总收入 (IAA + IAP) | `total_rev_7d`, `total_rev_28d` |

**示例值**: `1234.56`

### 指标列 - 留存 (支持后缀: `1d`, `3d`, `7d`, `14d`, `28d`)

| 列名 | 说明 | 示例 |
|------|------|------|
| `ret_x` | 留存率 | `ret_7d`, `ret_28d` |

**示例值**: `0.35` (35%)

### 指标列 - 销售/转化

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `sales` | 归因销售事件计数 (需要 revenue postbacks) | `500` |
| `sales_x` | 特定时间段的销售 (支持后缀: `0d`, `1d`, `2d`, `3d`, `7d`, `14d`, `30d`, `90d`, `1y`) | `sales_7d` |
| `first_purchase` | 首次购买用户数 (需要 revenue postbacks) | `200` |
| `unique_purchasers_x` | 特定时间段的唯一购买者 (支持后缀) | `unique_purchasers_7d` |

### 指标列 - CPP (Cost Per Purchase)

| 列名 | 说明 | 示例 |
|------|------|------|
| `cpp_x` | 特定时间段的购买成本 (支持后缀: `0d`, `1d`, `2d`, `3d`, `7d`, `14d`, `30d`, `90d`, `1y`) | `cpp_7d` |

### 指标列 - CPE (Cost Per Event)

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `target_event` | Campaign 定向的自定义事件 (仅CPE) | `level_complete` |
| `target_event_count` | 唯一目标事件 | `5000` |
| `target_event_count_x` | 特定时间段的目标事件 (支持后缀) | `target_event_count_7d` |
| `cost_per_target_event_x` | 特定时间段的目标事件成本 (支持后缀) | `cost_per_target_event_7d` |

### Campaign 配置列

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `campaign_type` | Campaign 优化类型 | `CPP`, `CPE`, `ad ROAS`, `IAP ROAS`, `ROAS` |
| `campaign_ad_type` | `ua` (用户获取) 或 `rt` (重定向) | `ua` |
| `campaign_roas_goal` | ROAS 目标 (%) - 需同时请求 `campaign` 列 | `150` |
| `campaign_bid_goal` | CPP/CPE Campaign 的出价目标 ($) - 需同时请求 `campaign` 列 | `2.50` |
| `optimization_day_target` | Campaign 优化的天数 | `0` 或 `7` |
| `bidding_and_billing_method` | 竞价策略 | `AUTO_BIDDING_WITH_CPM_BILLING`, `CAPPED_GOAL_BIDDING_WITH_CPM_BILLING`, `FIXED_GOAL_BIDDING_WITH_CPI_BILLING`, `FIXED_GOAL_BIDDING_WITH_CPM_BILLING` |

### 创意列

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `ad_creative_type` | `GRAPHIC`, `PLAYABLE`, `VIDEO`, `VIDEO_GRAPHIC`, `VIDEO_PLAYABLE` | `VIDEO` |
| `creative_set` | 创意集名称 | `Creative Set 1` |
| `creative_set_id` | 创意集 ID (重命名后不变) | `cs_123` |
| `custom_page_id` | 关联的 iOS Custom Product Page 或 Android Store Listing | `custom_page_1` |

### 目标列

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `campaign_package_name` | 推广应用的包名或 Bundle ID | `com.example.game` |
| `campaign_store_id` | iOS 的 iTunes ID 数字部分，或 campaign_package_name | `123456789` |

### 流量源列

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `traffic_source` | `AppLovin` 或交易所名称 | `AppLovin`, `IronSource` |

### 设备/地域列

| 列名 | 说明 | 示例值 |
|------|------|--------|
| `platform` | `android`, `fireos`, `ios`, `tvos` | `ios` |
| `device_type` | `phone`, `tablet`, `other` | `phone` |
| `country` | 两位国家代码 | `US`, `CN`, `JP` |
| `placement_type` | `APP_OPEN`, `ARRAY`, `BANNER`, `CTV`, `INTER`, `LEADER`, `MREC`, `NATIVE`, `REWARDED_INTER` | `INTER` |
| `size` | `BANNER`, `INTER`, `LEADER`, `MREC`, `NATIVE`, `PRELOAD` | `INTER` |
| `external_placement_id` | 加密的应用ID (用于 API Source 竞价) | `encrypted_id_123` |

---

## 🔍 过滤 (Filtering)

### 基本过滤
```
filter_columnname=value1,value2,value3
```

**示例**:
```
filter_platform=ios
filter_campaign=Campaign_A,Campaign_B
```

### 负向过滤
```
filter_not_columnname=value1,value2
```

**示例**:
```
filter_not_platform=android
```

### 空值/Null 过滤 (仅 `custom_page_id`)
```
filter_null_custom_page_id=
filter_blank_custom_page_id=
filter_not_null_custom_page_id=
filter_not_blank_custom_page_id=
```

---

## 📶 排序 (Sorting)

```
sort_columnname=ASC   # 升序
sort_columnname=DESC  # 降序
```

**示例**:
```
sort_campaign=ASC
sort_cost=DESC
```

> **注意**: 所有排序均为字典序 (lexicographical sort)

---

## 📋 请求示例

### Advertiser 请求
```
https://r.applovin.com/report?api_key=«your-report-key»&start=2015-04-20&end=now&columns=day,campaign,impressions,clicks,ctr,conversions,conversion_rate,app_id_external,cost,sales&format=json&report_type=advertiser
```

### Publisher 请求 (带过滤)
```
https://r.applovin.com/report?api_key=«your-report-key»&start=2016-07-01&end=2016-07-07&columns=day,platform,country,application,package_name,size,ad_type,impressions,clicks,revenue,device_type&having=impressions%20%3E%200%20AND%20revenue%20%3E%200&format=csv
```

### Cohort 数据查询
```
https://r.applovin.com/report?api_key=«your-report-key»&start=2026-02-01&end=now&columns=day,campaign,roas_7d,iap_roas_7d&format=json&report_type=advertiser&day_column=day
```

---

## 🎯 常用查询场景

### 1. 查询 Campaign 的 7日 ROAS
```
columns: day,campaign,cost,roas_7d,iap_roas_7d,ad_rev_7d,iap_rev_7d,total_rev_7d
report_type: advertiser
day_column: day (cohort 数据)
```

### 2. 查询留存数据
```
columns: day,campaign,ret_7d,ret_28d
report_type: advertiser
day_column: day
```

### 3. 查询实时数据
```
columns: day,campaign,impressions,clicks,cost
report_type: advertiser
# 不设置 day_column 即为 realtime
```

### 4. 按平台过滤
```
filter_platform=ios
```

### 5. 按多个 Campaign 过滤
```
filter_campaign=Campaign_A,Campaign_B,Campaign_C
```

---

## 📚 时间后缀说明

以下指标支持时间后缀:

| 后缀 | 说明 | 适用列 |
|------|------|--------|
| `0d` | 当天 | `roas_0d`, `iap_roas_0d`, `ad_roas_0d`, `iap_rev_0d`, `ad_rev_0d`, `total_rev_0d`, `sales_0d`, `cpp_0d`, `target_event_count_0d`, `cost_per_target_event_0d`, `unique_purchasers_0d` |
| `1d` | 1天 | 同上 + `sales_1d` |
| `2d` | 2天 | 同上 |
| `3d` | 3天 | 同上 |
| `7d` | 7天 | 同上 |
| `14d` | 14天 | 同上 |
| `28d` | 28天 | 同上 |
| `30d` | 30天 | 同上 (不包括 `cpp_30d`, `cost_per_target_event_30d`) |
| `90d` | 90天 | 同上 |
| `1y` | 1年 (365天) | 同上 (不包括 `sales_1y`, `cpp_1y`, `cost_per_target_event_1y`) |

**留存专用后缀**:
| 后缀 | 适用列 |
|------|--------|
| `1d`, `3d`, `7d`, `14d`, `28d` | `ret_1d`, `ret_3d`, `ret_7d`, `ret_14d`, `ret_28d` |

---

## ⚠️ 重要注意事项

1. **数据限制**: API 请求时间窗口限制为 45 天
2. **时区**: 所有数据为 UTC 时间
3. **Cohort vs Realtime**:
   - 默认为 realtime 数据 (估算值)
   - 设置 `day_column=day` 获取 cohort 数据 (按用户获取日期分组)
4. **分页**: 使用 `limit` 和 `offset` 参数处理大量数据
5. **性能**: `having` 参数会降低响应速度并增加超时可能性
6. **权限**: 某些列 (如 `zone`, `zone_id`) 需要联系账户经理获取权限

---

## 📖 相关资源

- **Axon Dashboard**: https://dashboard.axon.ai/
- **API Support**: https://support.axon.ai/
- **AppLovin Max Integration**: https://dash.applovin.com/documentation/mediation/axios/android

---

*最后更新: 2026-03-04*
*文档版本: 1.0*
