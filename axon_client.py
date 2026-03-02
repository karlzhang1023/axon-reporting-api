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


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: axon_client.py <api_key> <command> [args...]")
        print("\nCommands:")
        print("  list <start> [end]              - List all campaigns (cohort)")
        print("  get <campaign> <start> [end]    - Get campaign data (cohort)")
        print("  summary <start> [end]           - Get summary of all campaigns (cohort)")
        print("  realtime <start> [end]          - Get realtime data (not cohort)")
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


if __name__ == "__main__":
    main()
