# Axon Reporting API Skill

A Claude Code skill for querying Axon (AppLovin) Reporting API.

## 📋 What This Skill Does

This skill helps you fetch advertising campaign performance data from Axon, including:
- Campaign metrics (impressions, clicks, conversions, cost)
- ROAS data (D7, D28, IAP ROAS, Total ROAS)
- Revenue tracking (IAP revenue, total revenue)
- Campaign summaries and comparisons

## 🔑 Setup

### 1. Get Your Axon Reporting Key

1. Log in to [Axon Dashboard](https://ads.axon.ai/)
2. Click your account (top right) → Select "Keys"
3. Copy your **Reporting Key**

### 2. Configure the Skill

Create a `.env` file or set the environment variable:

```bash
export AXON_REPORTING_KEY="your_reporting_key_here"
```

**⚠️ Security Note**: Never commit your API key to version control!

## 📖 Usage Examples

### With Claude Code

```
# Get campaign data
Get Axon campaign data for InHisGrip_AL_IOS_D28IAP_ROAS_CPP_20260203 from Feb 1 to now

# List all campaigns
List all active campaigns for February 2026

# Get summary
Show me a summary of all campaigns with D7 ROAS from Jan 15 to Jan 31

# Compare campaigns
Compare ROAS between Android and iOS campaigns
```

### As a Python Library

```python
from axon_client import AxonClient

# Initialize with your API key
client = AxonClient(api_key="your_reporting_key_here")

# Get campaign data
data = client.get_campaign_data(
    campaign_name="InHisGrip_AL_IOS_D28IAP_ROAS_CPP_20260203",
    start="2026-02-01",
    end="now"
)

# Get summary of all campaigns
summaries = client.get_campaign_summary(start="2026-02-01", end="now")
client.print_summary_table(summaries)
```

### Command Line

```bash
# List all campaigns
python axon_client.py YOUR_KEY list 2026-02-01 now

# Get specific campaign
python axon_client.py YOUR_KEY get "InHisGrip_AL_IOS" 2026-02-01 now

# Get summary
python axon_client.py YOUR_KEY summary 2026-02-01 now
```

## 📊 Available Metrics

| Metric | Description |
|--------|-------------|
| `impressions` | Ad impressions |
| `clicks` | Click count |
| `conversions` | Install conversions |
| `cost` | Ad spend amount |
| `roas_7d` | 7-day total ROAS (IAA + IAP) |
| `iap_roas_7d` | 7-day IAP ROAS only |
| `iap_rev_7d` | 7-day IAP revenue |
| `total_rev_7d` | 7-day total revenue |
| `ret_7d` | 7-day retention |

## ⚠️ API Limitations

- **Data window**: Last 45 days only
- **Hourly data**: Last 30 days only
- **Timezone**: All times in UTC

## 🗂️ Column Naming Convention

Axon API uses `[metric]_[time]` format:

✅ **Correct**: `roas_7d`, `iap_rev_28d`, `ret_90d`
❌ **Wrong**: `roas_d7`, `d7_iap_revenue`, `roas7d`

**Time suffixes**: `0d`, `1d`, `3d`, `7d`, `14d`, `28d`, `30d`, `90d`, `1y`

## 📁 File Structure

```
~/.claude/skills/axon-reporting-api/
├── skill.md           # Claude Code skill definition
├── axon_client.py     # Python client library
├── README.md          # This file
└── .env.example       # Environment variable template
```

## 🔗 Useful Links

- **Axon Dashboard**: https://ads.axon.ai/
- **API Documentation**: https://support.axon.ai/en/growth/promoting-your-apps/api/reporting-api/
- **AppLovin Support**: https://support.applovin.com/

## 🤝 Sharing

This skill is safe to share with others! Each user needs their own Axon Reporting Key from their account.

## 📝 License

This skill is provided as-is for use with Axon Reporting API.
