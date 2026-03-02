#!/usr/bin/env python3
"""
Axon Reporting API Client
A Python client for querying Axon (AppLovin) Reporting API
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any


class AxonClient:
    """Client for Axon Reporting API"""

    BASE_URL = "https://r.applovin.com/report"

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
        format: str = "json"
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

        response = self.session.get(self.BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def get_campaign_data(
        self,
        campaign_name: str,
        start: str,
        end: str = "now",
        metrics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get data for a specific campaign

        Args:
            campaign_name: Name of the campaign
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD or "now")
            metrics: List of metric columns to retrieve

        Returns:
            List of daily data points
        """
        if metrics is None:
            metrics = ["day", "campaign", "impressions", "clicks", "conversions",
                      "cost", "roas_7d", "iap_roas_7d", "iap_rev_7d", "total_rev_7d"]

        result = self.query(
            start=start,
            end=end,
            columns=metrics,
            filter_campaign=campaign_name
        )

        return result.get("results", [])

    def list_campaigns(
        self,
        start: str,
        end: str = "now",
        active_only: bool = True
    ) -> List[str]:
        """
        List all campaigns in the date range

        Args:
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD or "now")
            active_only: Only return campaigns with data

        Returns:
            List of campaign names
        """
        result = self.query(
            start=start,
            end=end,
            columns=["campaign"],
            limit=2000
        )

        campaigns = set()
        for row in result.get("results", []):
            campaigns.add(row["campaign"])

        return sorted(list(campaigns))

    def get_campaign_summary(
        self,
        start: str,
        end: str = "now",
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get summary data for all campaigns

        Args:
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD or "now")
            metrics: List of metric columns to retrieve

        Returns:
            Dictionary mapping campaign names to their summary stats
        """
        if metrics is None:
            metrics = ["day", "campaign", "impressions", "clicks", "conversions",
                      "cost", "roas_7d", "iap_roas_7d", "iap_rev_7d", "total_rev_7d"]

        result = self.query(
            start=start,
            end=end,
            columns=metrics,
            limit=5000
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
                    "roas_7d_values": [],
                    "iap_roas_7d_values": [],
                    "iap_rev_7d_total": 0,
                    "active_days": 0
                }

            stats = summaries[camp]
            stats["impressions"] += int(row.get("impressions", 0))
            stats["clicks"] += int(row.get("clicks", 0))
            stats["conversions"] += int(row.get("conversions", 0))
            stats["cost"] += float(row.get("cost", 0))
            stats["iap_rev_7d_total"] += float(row.get("iap_rev_7d", 0))

            # Track ROAS values only for active days
            if float(row.get("cost", 0)) > 0:
                stats["active_days"] += 1
                stats["roas_7d_values"].append(float(row.get("roas_7d", 0)))
                stats["iap_roas_7d_values"].append(float(row.get("iap_roas_7d", 0)))

        # Calculate averages
        for camp, stats in summaries.items():
            if stats["roas_7d_values"]:
                stats["avg_roas_7d"] = sum(stats["roas_7d_values"]) / len(stats["roas_7d_values"])
                stats["avg_iap_roas_7d"] = sum(stats["iap_roas_7d_values"]) / len(stats["iap_roas_7d_values"])
            else:
                stats["avg_roas_7d"] = 0
                stats["avg_iap_roas_7d"] = 0

        return summaries

    def print_summary_table(self, summaries: Dict[str, Dict[str, Any]]):
        """Print a formatted summary table"""
        print("| Campaign | Cost | Avg_ROAS_7d | Avg_IAP_ROAS_7d | IAP_Rev | Impr | Conv | Days |")
        print("|----------|------|-------------|-----------------|---------|------|------|------|")

        for camp, stats in sorted(summaries.items(), key=lambda x: x[1]["cost"], reverse=True):
            if stats["cost"] > 0:
                print(f"| {camp} | ${stats['cost']:.2f} | {stats['avg_roas_7d']:.2f}% | "
                      f"{stats['avg_iap_roas_7d']:.2f}% | ${stats['iap_rev_7d_total']:.2f} | "
                      f"{stats['impressions']:,} | {stats['conversions']} | {stats['active_days']} |")


# Available column names reference
AVAILABLE_COLUMNS = {
    "basic": ["day", "campaign", "impressions", "clicks", "conversions", "cost"],
    "roas": ["roas_7d", "roas_28d", "iap_roas_7d", "iap_roas_28d"],
    "revenue": ["iap_rev_7d", "iap_rev_28d", "total_rev_7d", "total_rev_28d"],
    "retention": ["ret_7d", "ret_28d"],
    "all": ["day", "campaign", "impressions", "clicks", "conversions", "cost",
            "roas_7d", "iap_roas_7d", "iap_rev_7d", "total_rev_7d", "ret_7d"]
}


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: axon_client.py <api_key> <command> [args...]")
        print("\nCommands:")
        print("  list <start> [end]              - List all campaigns")
        print("  get <campaign> <start> [end]    - Get campaign data")
        print("  summary <start> [end]           - Get summary of all campaigns")
        print("\nDates: YYYY-MM-DD format, or 'now' for end")
        sys.exit(1)

    api_key = sys.argv[1]
    client = AxonClient(api_key)

    if sys.argv[2] == "list":
        start = sys.argv[3] if len(sys.argv) > 3 else "2026-01-01"
        end = sys.argv[4] if len(sys.argv) > 4 else "now"
        campaigns = client.list_campaigns(start, end)
        print("Campaigns:")
        for c in campaigns:
            print(f"  - {c}")

    elif sys.argv[2] == "get":
        campaign = sys.argv[3]
        start = sys.argv[4] if len(sys.argv) > 4 else "2026-01-01"
        end = sys.argv[5] if len(sys.argv) > 5 else "now"
        data = client.get_campaign_data(campaign, start, end)
        print(json.dumps(data, indent=2))

    elif sys.argv[2] == "summary":
        start = sys.argv[3] if len(sys.argv) > 3 else "2026-01-01"
        end = sys.argv[4] if len(sys.argv) > 4 else "now"
        summaries = client.get_campaign_summary(start, end)
        client.print_summary_table(summaries)


if __name__ == "__main__":
    main()
