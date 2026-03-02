# Axon Reporting API Skill - Sharing Guide

## 🎯 What is This?

A reusable Claude Code skill for querying Axon (AppLovin) advertising data. Safe to share - each user provides their own API key.

---

## 📦 Installation for Others

### Step 1: Copy the Skill Files

Share these files with others:
```
axon-reporting-api/
├── skill.md           # Claude Code skill definition
├── axon_client.py     # Python client library
├── README.md          # Documentation
├── .env.example       # Configuration template
└── SHARING.md         # This file
```

### Step 2: Install to Claude Skills Directory

```bash
# Create skills directory if needed
mkdir -p ~/.claude/skills

# Copy the skill folder
cp -r axon-reporting-api ~/.claude/skills/
```

### Step 3: Configure API Key

```bash
# Copy the example file
cp ~/.claude/skills/axon-reporting-api/.env.example ~/.claude/skills/axon-reporting-api/.env

# Edit with your actual Reporting Key
nano ~/.claude/skills/axon-reporting-api/.env
```

Get the key from: https://ads.axon.ai/ → Account → Keys

---

## 🚀 Usage

### In Claude Code

Simply ask Claude to use the skill:

```
"Use axon-reporting-api skill to get campaign data for February"
```

### Python Library

```python
from axon_client import AxonClient

client = AxonClient(api_key="your_key")
summaries = client.get_campaign_summary("2026-02-01", "now")
client.print_summary_table(summaries)
```

### Command Line

```bash
python ~/.claude/skills/axon-reporting-api/axon_client.py YOUR_KEY summary 2026-02-01 now
```

---

## 🔐 Security Notes

- ✅ **Safe to share**: Your API key is NOT included
- ✅ **Each user** needs their own Axon account and Reporting Key
- ⚠️ **Never commit** `.env` file with real keys
- ⚠️ **Add `.env`** to `.gitignore`

---

## 📂 Files to Share

| File | Description | Share? |
|------|-------------|--------|
| `skill.md` | Claude skill definition | ✅ Yes |
| `axon_client.py` | Python client | ✅ Yes |
| `README.md` | Documentation | ✅ Yes |
| `.env.example` | Config template | ✅ Yes |
| `SHARING.md` | This guide | ✅ Yes |
| `.env` | Your actual keys | ❌ NO |

---

## 🎓 Common Queries

### Get All Campaigns Summary
```
"Show me all campaigns with their cost and D7 ROAS for this month"
```

### Specific Campaign Data
```
"Get detailed data for InHisGrip_AL_IOS_D28IAP_ROAS_CPP_20260203 from Feb 1 to now"
```

### Compare Performance
```
"Compare IAP ROAS between Joylit Android and iOS campaigns"
```

---

## 📞 Support

- **Axon Dashboard**: https://ads.axon.ai/
- **API Docs**: https://support.axon.ai/en/growth/promoting-your-apps/api/reporting-api/

---

## ✅ Verification

Test installation:

```bash
# Test the client
python ~/.claude/skills/axon-reporting-api/axon_client.py

# Should show usage instructions
```
