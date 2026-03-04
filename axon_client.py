#!/usr/bin/env python3
"""
Axon Reporting API Client
A Python client for querying Axon (AppLovin) Reporting API

ROAS Terminology:
- D0/D1/D3/D7/D28 ROAS = Total ROAS (IAA + IAP) by default
- IAP ROAS = IAP revenue only
- IAA ROAS = Ad revenue only

Data Source:
- Default: Cohort data (grouped by user acquisition date)
- Realtime: Use use_cohort=False for realtime estimates
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any


class AxonClient:
    """Client for Axon Reporting API"""

    BASE_URL = "https://r.applovin.com/report"

    # Column definitions from API documentation
    PUBLISHER_COLUMNS = {
        "ad_type": "广告类型 (APPOPEN, GRAPHIC, MRAID, PLAY, REWARD, VIDEO)",
        "application": "应用名称",
        "application_is_hidden": "应用是否在 Dashboard 隐藏 (true/false)",
        "bidding_integration": "竞价集成提供商 (MAX, Google, None)",
        "clicks": "点击次数",
        "country": "国家代码 (两位, 如 US, CN, JP)",
        "ctr": "点击率 (点击/展示)",
        "day": "报告日期 (YYYY-MM-DD)",
        "device_type": "设备类型 (phone, tablet, other)",
        "ecpm": "千次展示收益",
        "hour": "报告小时 (0-23, 仅最近30天)",
        "impressions": "展示次数",
        "package_name": "包名或 Bundle ID",
        "placement_type": "展位类型 (APP_OPEN, BANNER, INTER, LEADER, MREC, NATIVE, REWARDED_INTER)",
        "platform": "平台 (android, fireos, ios)",
        "revenue": "收益",
        "size": "广告尺寸 (BANNER, INTER, LEADER, MREC, NATIVE)",
        "store_id": "iTunes ID 数字部分或 package_name",
        "zone": "Zone 名称 (需账户权限)",
        "zone_id": "Zone ID (需账户权限)"
    }

    ADVERTISER_COLUMNS = {
        # 基础列
        "day": "报告日期 (YYYY-MM-DD)",
        "hour": "报告小时 (0-23, 仅最近30天)",
        "campaign": "Campaign 名称",
        "campaign_id_external": "Campaign 外部ID (重命名后不变)",
        "ad": "广告名称",
        "application": "源应用名称",
        "app_id_external": "应用ID哈希 (Site ID)",
        # 指标列 - 基础
        "impressions": "展示次数",
        "clicks": "点击次数",
        "conversions": "转化数 (安装数)",
        "ctr": "点击率 (点击/展示)",
        "conversion_rate": "转化率 (转化/展示)",
        "cost": "广告支出",
        "average_cpc": "平均点击成本",
        "average_cpa": "平均转化成本",
        # ROAS columns (支持时间后缀: 0d, 1d, 2d, 3d, 7d, 14d, 28d, 30d, 90d, 1y)
        "roas_x": "总ROAS (IAA + IAP) - 使用 roas_7d, roas_28d 等",
        "iap_roas_x": "IAP ROAS - 使用 iap_roas_7d, iap_roas_28d 等",
        "ad_roas_x": "Ad ROAS (IAA) - 使用 ad_roas_7d, ad_roas_28d 等",
        # 收入列 (支持时间后缀)
        "iap_rev_x": "IAP 收入 - 使用 iap_rev_7d, iap_rev_28d 等",
        "ad_rev_x": "Ad 收入 - 使用 ad_rev_7d, ad_rev_28d 等",
        "total_rev_x": "总收入 (IAA + IAP) - 使用 total_rev_7d, total_rev_28d 等",
        # 留存列 (支持后缀: 1d, 3d, 7d, 14d, 28d)
        "ret_x": "留存率 - 使用 ret_7d, ret_28d 等",
        # 销售/转化列
        "sales": "归因销售事件计数 (需要 revenue postbacks)",
        "sales_x": "特定时间段的销售 - 使用 sales_7d, sales_28d 等 (支持: 0d, 1d, 2d, 3d, 7d, 14d, 30d, 90d)",
        "first_purchase": "首次购买用户数",
        "unique_purchasers_x": "唯一购买者 - 使用 unique_purchasers_7d 等",
        # CPP (Cost Per Purchase)
        "cpp_x": "购买成本 - 使用 cpp_7d, cpp_28d 等 (支持: 0d, 1d, 2d, 3d, 7d, 14d, 30d, 90d)",
        # CPE (Cost Per Event)
        "target_event": "Campaign 定向的自定义事件 (仅CPE)",
        "target_event_count": "唯一目标事件",
        "target_event_count_x": "特定时间段的目标事件 - 使用 target_event_count_7d 等",
        "cost_per_target_event_x": "目标事件成本 - 使用 cost_per_target_event_7d 等",
        # Campaign 配置列
        "campaign_type": "Campaign 优化类型 (CPP, CPE, ad ROAS, IAP ROAS, ROAS)",
        "campaign_ad_type": "ua (用户获取) 或 rt (重定向)",
        "campaign_roas_goal": "ROAS 目标 (%) - 需同时请求 campaign 列",
        "campaign_bid_goal": "CPP/CPE Campaign 的出价目标 ($) - 需同时请求 campaign 列",
        "optimization_day_target": "Campaign 优化的天数 (0 或 7)",
        "bidding_and_billing_method": "竞价策略 (AUTO_BIDDING_WITH_CPM_BILLING 等)",
        # 创意列
        "ad_creative_type": "创意类型 (GRAPHIC, PLAYABLE, VIDEO, VIDEO_GRAPHIC, VIDEO_PLAYABLE)",
        "creative_set": "创意集名称",
        "creative_set_id": "创意集 ID (重命名后不变)",
        "custom_page_id": "关联的 iOS Custom Product Page 或 Android Store Listing",
        # 目标列
        "campaign_package_name": "推广应用的包名或 Bundle ID",
        "campaign_store_id": "iOS 的 iTunes ID 数字部分，或 campaign_package_name",
        # 流量源列
        "traffic_source": "AppLovin 或交易所名称 (AppLovin, IronSource)",
        # 设备/地域列
        "platform": "android, fireos, ios, tvos",
        "device_type": "phone, tablet, other",
        "country": "两位国家代码 (US, CN, JP)",
        "placement_type": "APP_OPEN, ARRAY, BANNER, CTV, INTER, LEADER, MREC, NATIVE, REWARDED_INTER",
        "size": "BANNER, INTER, LEADER, MREC, NATIVE, PRELOAD",
        "external_placement_id": "加密的应用ID (用于 API Source 竞价)"
    }

    def __init__(self, api_key: str):
        """
        Initialize the Axon client

        Args:
            api_key: Your Axon Reporting Key (get from Axon Dashboard)
        """
        self.api_key = api_key
        self.session = requests.Session()

    def query(
        self,
        start: str,
        end: str = "now",
        columns: Optional[List[str]] = None,
        report_type: str = "advertiser",
        filter_campaign: Optional[str] = None,
        limit: int = 1000,
        offset: int = 0,
        format: str = "json",
        use_cohort: bool = True
    ) -> Dict[str, Any]:
        """
        Query the Axon Reporting API

        Args:
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD or "now")
            columns: List of column names to retrieve
            report_type: "advertiser" or "publisher"
            filter_campaign: Filter by specific campaign name
            limit: Maximum number of results
            offset: Pagination offset
            format: "json" or "csv"
            use_cohort: Use cohort data (default True). False for realtime.

        Returns:
            API response as dictionary
        """
        if columns is None:
            columns = ["day", "campaign", "impressions", "clicks", "conversions", "cost"]

        params = {
            "api_key": self.api_key,
            "start": start,
            "end": end,
            "columns": ",".join(columns),
            "report_type": report_type,
            "limit": limit,
            "offset": offset,
            "format": format
        }

        if filter_campaign:
            params["filter_campaign"] = filter_campaign

        # Add day_column for cohort data (default behavior)
        if use_cohort:
            params["day_column"] = "day"

        response = self.session.get(self.BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_campaign_data(
        self,
        campaign_name: str,
        start: str,
        end: str = "now",
        metrics: Optional[List[str]] = None,
        use_cohort: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get data for a specific campaign

        Args:
            campaign_name: Name of the campaign
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD or "now")
            metrics: List of metric columns to retrieve
            use_cohort: Use cohort data (default True). False for realtime.

        Returns:
            List of daily data points
        """
        if metrics is None:
            # Default to D0 total ROAS (cohort data)
            metrics = ["day", "campaign", "impressions", "clicks", "conversions",
                      "cost", "roas_0d"]

        result = self.query(
            start=start,
            end=end,
            columns=metrics,
            filter_campaign=campaign_name,
            use_cohort=use_cohort
        )

        return result.get("results", [])

    def list_campaigns(
        self,
        start: str,
        end: str = "now",
        active_only: bool = True,
        use_cohort: bool = True
    ) -> List[str]:
        """
        List all campaigns in the date range

        Args:
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD or "now")
            active_only: Only return campaigns with data
            use_cohort: Use cohort data (default True). False for realtime.

        Returns:
            List of campaign names
        """
        result = self.query(
            start=start,
            end=end,
            columns=["campaign"],
            limit=2000,
            use_cohort=use_cohort
        )

        campaigns = set()
        for row in result.get("results", []):
            campaigns.add(row["campaign"])

        return sorted(list(campaigns))

    def get_campaign_summary(
        self,
        start: str,
        end: str = "now",
        metrics: Optional[List[str]] = None,
        use_cohort: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get summary data for all campaigns

        Args:
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD or "now")
            metrics: List of metric columns to retrieve
            use_cohort: Use cohort data (default True). False for realtime.

        Returns:
            Dictionary mapping campaign names to their summary stats
        """
        if metrics is None:
            # Default to D0 total ROAS
            metrics = ["day", "campaign", "impressions", "clicks", "conversions",
                      "cost", "roas_0d"]

        result = self.query(
            start=start,
            end=end,
            columns=metrics,
            limit=5000,
            use_cohort=use_cohort
        )

        summaries = {}
        for row in result.get("results", []):
            camp = row["campaign"]
            if camp not in summaries:
                summaries[camp] = {
                    "impressions": 0,
                    "clicks": 0,
                    "conversions": 0,
                    "cost": 0,
                    "roas_values": [],
                    "active_days": 0
                }

            stats = summaries[camp]
            stats["impressions"] += int(row.get("impressions", 0))
            stats["clicks"] += int(row.get("clicks", 0))
            stats["conversions"] += int(row.get("conversions", 0))
            stats["cost"] += float(row.get("cost", 0))

            # Track ROAS values only for active days
            if float(row.get("cost", 0)) > 0:
                stats["active_days"] += 1
                # Support both roas_0d and roas_7d
                if "roas_0d" in row:
                    stats["roas_values"].append(float(row.get("roas_0d", 0)))
                elif "roas_7d" in row:
                    stats["roas_values"].append(float(row.get("roas_7d", 0)))

        # Calculate averages
        for camp, stats in summaries.items():
            if stats["roas_values"]:
                stats["avg_roas"] = sum(stats["roas_values"]) / len(stats["roas_values"])
            else:
                stats["avg_roas"] = 0

        return summaries

    def print_summary_table(self, summaries: Dict[str, Dict[str, Any]]):
        """Print a formatted summary table"""
        print("| Campaign | Cost | Avg_ROAS | Impr | Conv | Days |")
        print("|----------|------|----------|------|------|------|")

        for camp, stats in sorted(summaries.items(), key=lambda x: x[1]["cost"], reverse=True):
            if stats["cost"] > 0:
                print(f"| {camp} | ${stats['cost']:.2f} | {stats['avg_roas']:.2f}% | "
                      f"{stats['impressions']:,} | {stats['conversions']} | {stats['active_days']} |")

    # ========== Learning Capability Methods ==========

    @staticmethod
    def search_columns(keyword: str, report_type: str = "advertiser") -> List[Dict[str, str]]:
        """
        搜索包含关键词的列名

        Args:
            keyword: 搜索关键词
            report_type: 报告类型 (advertiser/publisher)

        Returns:
            匹配的列名和描述列表
        """
        columns = AxonClient.ADVERTISER_COLUMNS if report_type == "advertiser" else AxonClient.PUBLISHER_COLUMNS
        keyword_lower = keyword.lower()

        results = []
        for col_name, description in columns.items():
            if keyword_lower in col_name.lower() or keyword_lower in description.lower():
                results.append({
                    "column": col_name,
                    "description": description
                })

        return results

    @staticmethod
    def get_column_info(column_name: str, report_type: str = "advertiser") -> Dict[str, Any]:
        """
        获取特定列的详细信息

        Args:
            column_name: 列名
            report_type: 报告类型 (advertiser/publisher)

        Returns:
            列的详细信息
        """
        columns = AxonClient.ADVERTISER_COLUMNS if report_type == "advertiser" else AxonClient.PUBLISHER_COLUMNS

        # 精确匹配
        if column_name in columns:
            return {
                "column": column_name,
                "description": columns[column_name],
                "exists": True,
                "type": "exact_match"
            }

        # 处理带时间后缀的列 (如 roas_7d, iap_rev_28d)
        for col_base in columns:
            if col_base.endswith("_x"):
                base_name = col_base[:-2]
                if column_name.startswith(base_name + "_"):
                    suffix = column_name[len(base_name) + 1:]
                    return {
                        "column": column_name,
                        "base_column": col_base,
                        "description": columns[col_base],
                        "suffix": suffix,
                        "exists": True,
                        "type": "time_suffix_variant"
                    }

        # 模糊匹配建议
        suggestions = []
        for col in columns:
            if column_name.lower() in col.lower():
                suggestions.append(col)

        return {
            "column": column_name,
            "exists": False,
            "type": "not_found",
            "suggestions": suggestions[:5]  # 最多返回5个建议
        }

    @staticmethod
    def list_all_columns(report_type: str = "advertiser", category: str = None) -> Dict[str, Any]:
        """
        列出所有可用的列

        Args:
            report_type: 报告类型 (advertiser/publisher)
            category: 分类筛选 (basic, roas, revenue, retention, sales, campaign, creative, device)

        Returns:
            按分类组织的列名列表
        """
        if report_type == "publisher":
            return {
                "all": list(AxonClient.PUBLISHER_COLUMNS.keys()),
                "total": len(AxonClient.PUBLISHER_COLUMNS)
            }

        # Advertiser 列分类
        categories = {
            "basic": ["day", "hour", "campaign", "campaign_id_external", "ad", "application", "app_id_external"],
            "metrics": ["impressions", "clicks", "conversions", "ctr", "conversion_rate", "cost", "average_cpc", "average_cpa"],
            "roas": ["roas_x", "iap_roas_x", "ad_roas_x"],
            "revenue": ["iap_rev_x", "ad_rev_x", "total_rev_x"],
            "retention": ["ret_x"],
            "sales": ["sales", "sales_x", "first_purchase", "unique_purchasers_x", "cpp_x"],
            "cpe": ["target_event", "target_event_count", "target_event_count_x", "cost_per_target_event_x"],
            "campaign": ["campaign_type", "campaign_ad_type", "campaign_roas_goal", "campaign_bid_goal",
                        "optimization_day_target", "bidding_and_billing_method"],
            "creative": ["ad_creative_type", "creative_set", "creative_set_id", "custom_page_id"],
            "target": ["campaign_package_name", "campaign_store_id"],
            "traffic": ["traffic_source"],
            "device": ["platform", "device_type", "country", "placement_type", "size", "external_placement_id"]
        }

        if category:
            return {
                "category": category,
                "columns": categories.get(category, []),
                "description": f"Columns in {category} category"
            }

        return {
            "all_columns": list(AxonClient.ADVERTISER_COLUMNS.keys()),
            "categories": categories,
            "total_columns": len(AxonClient.ADVERTISER_COLUMNS)
        }

    @staticmethod
    def get_time_suffix_info() -> Dict[str, Any]:
        """
        获取时间后缀支持的列和可用后缀

        Returns:
            时间后缀信息字典
        """
        return {
            "supported_suffixes": {
                "roas": ["0d", "1d", "2d", "3d", "7d", "14d", "28d", "30d", "90d", "1y"],
                "revenue": ["0d", "1d", "2d", "3d", "7d", "14d", "28d", "30d", "90d", "1y"],
                "sales": ["0d", "1d", "2d", "3d", "7d", "14d", "30d", "90d"],
                "cpp": ["0d", "1d", "2d", "3d", "7d", "14d", "30d", "90d"],
                "cpe": ["0d", "1d", "2d", "3d", "7d", "14d", "30d", "90d"],
                "retention": ["1d", "3d", "7d", "14d", "28d"]
            },
            "column_patterns": {
                "total_roas": "roas_{suffix}",
                "iap_roas": "iap_roas_{suffix}",
                "ad_roas": "ad_roas_{suffix}",
                "iap_revenue": "iap_rev_{suffix}",
                "ad_revenue": "ad_rev_{suffix}",
                "total_revenue": "total_rev_{suffix}",
                "sales": "sales_{suffix}",
                "cpp": "cpp_{suffix}",
                "retention": "ret_{suffix}",
                "target_event_count": "target_event_count_{suffix}",
                "cost_per_target_event": "cost_per_target_event_{suffix}"
            },
            "examples": [
                "roas_7d - 7日总ROAS (IAA + IAP)",
                "iap_roas_28d - 28日内购ROAS",
                "ad_roas_7d - 7日广告ROAS (IAA)",
                "ret_7d - 7日留存率",
                "iap_rev_7d - 7日内购收入",
                "sales_7d - 7日销售数"
            ]
        }


# Available column names reference
AVAILABLE_COLUMNS = {
    "basic": ["day", "campaign", "impressions", "clicks", "conversions", "cost"],
    # ROAS columns: D0/D1/D3/D7/D28 formats
    # Default: roas_Xd = Total ROAS (IAA + IAP)
    # IAP only: iap_roas_Xd
    "roas_d0": ["roas_0d", "iap_roas_0d", "iap_rev_0d", "total_rev_0d"],
    "roas_d1": ["roas_1d", "iap_roas_1d", "iap_rev_1d", "total_rev_1d"],
    "roas_d3": ["roas_3d", "iap_roas_3d", "iap_rev_3d", "total_rev_3d"],
    "roas_d7": ["roas_7d", "iap_roas_7d", "iap_rev_7d", "total_rev_7d"],
    "roas_d28": ["roas_28d", "iap_roas_28d", "iap_rev_28d", "total_rev_28d"],
    "revenue": ["iap_rev_0d", "iap_rev_7d", "total_rev_0d", "total_rev_7d"],
    "retention": ["ret_7d", "ret_28d"],
    "all_d0": ["day", "campaign", "impressions", "clicks", "conversions", "cost",
               "roas_0d", "iap_roas_0d", "iap_rev_0d", "total_rev_0d"],
}


# ========== Learning Capability Convenience Functions ==========

def search_columns(keyword: str, report_type: str = "advertiser") -> List[Dict[str, str]]:
    """搜索列名的便捷函数"""
    return AxonClient.search_columns(keyword, report_type)


def get_column_info(column_name: str, report_type: str = "advertiser") -> Dict[str, Any]:
    """获取列信息的便捷函数"""
    return AxonClient.get_column_info(column_name, report_type)


def list_all_columns(report_type: str = "advertiser", category: str = None) -> Dict[str, Any]:
    """列出所有列的便捷函数"""
    return AxonClient.list_all_columns(report_type, category)


def get_time_suffix_info() -> Dict[str, Any]:
    """获取时间后缀信息的便捷函数"""
    return AxonClient.get_time_suffix_info()


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: axon_client.py <api_key> <command> [args...]")
        print("\nCommands:")
        print("  list <start> [end]              - List all campaigns (cohort)")
        print("  get <campaign> <start> [end]    - Get campaign data (cohort)")
        print("  summary <start> [end]           - Get summary of all campaigns (cohort)")
        print("  realtime <start> [end]          - Get realtime data (not cohort)")
        print("\nLearning Commands:")
        print("  search <keyword>                - Search for columns by keyword")
        print("  info <column_name>              - Get info about a specific column")
        print("  columns [category]              - List all available columns")
        print("  suffixes                        - Show time suffix information")
        print("\nOptions:")
        print("  --realtime                     - Use realtime data instead of cohort")
        print("\nDates: YYYY-MM-DD format, or 'now' for end")
        sys.exit(1)

    api_key = sys.argv[1]
    client = AxonClient(api_key)

    # Check for realtime flag
    use_realtime = "--realtime" in sys.argv
    # Remove flag from args for cleaner processing
    clean_args = [arg for arg in sys.argv if arg != "--realtime"]

    if len(clean_args) < 3:
        sys.exit(1)

    command = clean_args[2]

    if command == "list":
        start = clean_args[3] if len(clean_args) > 3 else "2026-01-01"
        end = clean_args[4] if len(clean_args) > 4 else "now"
        campaigns = client.list_campaigns(start, end, use_cohort=not use_realtime)
        print("Campaigns:")
        for c in campaigns:
            print(f"  - {c}")

    elif command == "get":
        campaign = clean_args[3]
        start = clean_args[4] if len(clean_args) > 4 else "2026-01-01"
        end = clean_args[5] if len(clean_args) > 5 else "now"
        data = client.get_campaign_data(campaign, start, end, use_cohort=not use_realtime)
        print(json.dumps(data, indent=2))

    elif command == "summary":
        start = clean_args[3] if len(clean_args) > 3 else "2026-01-01"
        end = clean_args[4] if len(clean_args) > 4 else "now"
        summaries = client.get_campaign_summary(start, end, use_cohort=not use_realtime)
        client.print_summary_table(summaries)

    elif command == "realtime":
        start = clean_args[3] if len(clean_args) > 3 else "2026-03-02"
        end = clean_args[4] if len(clean_args) > 4 else "now"
        summaries = client.get_campaign_summary(start, end, use_cohort=False)
        client.print_summary_table(summaries)

    # Learning commands (no API key needed for these)
    elif command == "search":
        keyword = clean_args[3] if len(clean_args) > 3 else ""
        if not keyword:
            print("Error: Please provide a search keyword")
            sys.exit(1)
        results = AxonClient.search_columns(keyword)
        print(f"\n搜索结果 '{keyword}':")
        for r in results:
            print(f"  - {r['column']}: {r['description']}")

    elif command == "info":
        column_name = clean_args[3] if len(clean_args) > 3 else ""
        if not column_name:
            print("Error: Please provide a column name")
            sys.exit(1)
        info = AxonClient.get_column_info(column_name)
        print(f"\n列信息: {info['column']}")
        print(f"  存在: {'是' if info['exists'] else '否'}")
        print(f"  类型: {info['type']}")
        if info['exists']:
            print(f"  描述: {info.get('description', 'N/A')}")
            if 'suffix' in info:
                print(f"  后缀: {info['suffix']}")
        elif info.get('suggestions'):
            print(f"  建议: {', '.join(info['suggestions'])}")

    elif command == "columns":
        category = clean_args[3] if len(clean_args) > 3 else None
        result = AxonClient.list_all_columns(category=category)
        if category:
            print(f"\n{category.upper()} 分类列:")
            for col in result['columns']:
                print(f"  - {col}")
        else:
            print(f"\n所有可用列 (共 {result['total_columns']} 个):")
            for col in result['all_columns']:
                print(f"  - {col}")
            print("\n分类:")
            for cat, cols in result['categories'].items():
                print(f"  - {cat}: {len(cols)} 列")

    elif command == "suffixes":
        info = AxonClient.get_time_suffix_info()
        print("\n时间后缀信息:\n")
        print("支持的后缀:")
        for metric, suffixes in info['supported_suffixes'].items():
            print(f"  - {metric}: {', '.join(suffixes)}")
        print("\n列模式:")
        for name, pattern in info['column_patterns'].items():
            print(f"  - {name}: {pattern}")
        print("\n示例:")
        for ex in info['examples']:
            print(f"  - {ex}")


if __name__ == "__main__":
    main()
