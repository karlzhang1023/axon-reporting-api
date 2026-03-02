---
description: Query Axon (AppLovin) Reporting API for advertising campaign data including ROAS, revenue, and performance metrics
---

# Axon Reporting API

Query Axon (AppLovin) Reporting API to fetch advertising campaign performance data, including ROAS metrics, revenue, impressions, clicks, and conversions.

## What This Skill Does

This skill helps you query Axon Reporting API for:
- Campaign performance data (impressions, clicks, conversions, cost)
- ROAS metrics (D7, D28, IAP ROAS, Total ROAS)
- Revenue data (IAP revenue, total revenue)
- Filter by campaign, date range, and more

## Required Configuration

Before using this skill, you need an **Axon Reporting Key**:

1. Log in to [Axon Dashboard](https://ads.axon.ai/)
2. Click your account (top right) → Select "Keys"
3. Copy your Reporting Key

## Usage

Tell me what you want to query, for example:

- "Get D7 ROAS data for campaign XYZ from Jan 15 to Jan 31"
- "Show all campaigns with their cost and ROAS for February"
- "What's the IAP revenue for InHisGrip_IOS campaign this month?"
- "Compare ROAS between Android and iOS campaigns"

## Available Metrics

| Metric | Description |
|--------|-------------|
| `impressions` | Ad impressions |
| `clicks` | Click count |
| `conversions` | Install conversions |
| `cost` | Ad spend |
| `roas_7d` | 7-day total ROAS |
| `iap_roas_7d` | 7-day IAP ROAS |
| `iap_rev_7d` | 7-day IAP revenue |
| `total_rev_7d` | 7-day total revenue |

## API Limitations

- **Data window**: Last 45 days only
- **Hourly data**: Last 30 days only
- **Timezone**: UTC

## Example Queries

```
Query campaign performance for InHisGrip_AL_IOS_D28IAP_ROAS_CPP_20260203 from 2026-02-01 to now
```

```
List all active campaigns with their D7 IAP ROAS for February 2026
```
