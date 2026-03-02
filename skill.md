---
description: Query Axon (AppLovin) Reporting API for advertising campaign data including ROAS, revenue, and performance metrics
---

# Axon Reporting API

Query Axon (AppLovin) Reporting API to fetch advertising campaign performance data, including ROAS metrics, revenue, impressions, clicks, and conversions.

## What This Skill Does

This skill helps you query Axon Reporting API for:
- Campaign performance data (impressions, clicks, conversions, cost)
- ROAS metrics (D0, D1, D3, D7, D28 ROAS)
- Revenue breakdown (IAP revenue, IAA revenue, total revenue)
- Filter by campaign, date range, and more

## Required Configuration

Before using this skill, you need an **Axon Reporting Key**:

1. Log in to [Axon Dashboard](https://ads.axon.ai/)
2. Click your account (top right) → Select "Keys"
3. Copy your Reporting Key

## Usage

Tell me what you want to query, for example:

- "Get D7 ROAS for campaign XYZ from Jan 15 to Jan 31"
- "Show all campaigns with their cost and D0 ROAS for today"
- "What's the D7 IAP ROAS for InHisGrip_IOS campaign?"
- "Compare D0 IAP vs D0 IAA ROAS between campaigns"
- "Get realtime data for today's campaigns"

## ROAS Terminology

**Default Behavior:**
- **D0/D1/D3/D7/D28 ROAS** = Total ROAS (IAA + IAP combined)
- **D0/D1/D3/D7/D28 IAP ROAS** = IAP ROAS only
- **D0/D1/D3/D7/D28 IAA ROAS** = IAA (Ad) ROAS only

**Examples:**
- "Show D7 ROAS" → Returns total ROAS (IAA + IAP)
- "Show D7 IAP ROAS" → Returns IAP ROAS only
- "Show D7 IAA ROAS" → Returns Ad ROAS only

## Data Source

**Default: Cohort Data**
- All queries use **cohort data** by default (grouped by user acquisition date)
- Cohort data is accurate and updates over time
- Uses `day_column=day` parameter

**Realtime Data (when specified)**
- Only use when explicitly requested: "show realtime data"
- Realtime data is an estimate and may differ from cohort
- Omit `day_column` parameter for realtime queries

## Available Metrics

| Metric | Description |
|--------|-------------|
| `impressions` | Ad impressions |
| `clicks` | Click count |
| `conversions` | Install conversions |
| `cost` | Ad spend |
| `roas_0d` | D0 Total ROAS (default) |
| `iap_roas_0d` | D0 IAP ROAS only |
| `iap_rev_0d` | D0 IAP revenue |
| `total_rev_0d` | D0 Total revenue |
| `roas_7d` | D7 Total ROAS (default) |
| `iap_roas_7d` | D7 IAP ROAS only |
| `iap_rev_7d` | D7 IAP revenue |
| `total_rev_7d` | D7 Total revenue |

## API Limitations

- **Data window**: Last 45 days only
- **Hourly data**: Last 30 days only
- **Timezone**: UTC

## Example Queries

```
# Cohort data (default)
Query D7 ROAS for campaign XYZ from 2026-03-01 to now

# Specific ROAS type
Query D7 IAP ROAS for campaign XYZ

# Realtime data (explicit)
Show realtime D0 ROAS for today's campaigns

# Comparison
Compare D0 IAP vs D0 IAA ROAS for all campaigns
```
