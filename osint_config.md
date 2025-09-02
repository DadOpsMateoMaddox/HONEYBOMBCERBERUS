# 🌍 OSINT Enrichment Configuration for Cerberus-1

This file defines how Cerberus-1 performs open-source intelligence lookups on attacker IPs to enrich threat data and improve behavioral tagging.

## 🔎 GreyNoise

- **API Key**: `Fqyk27ii8P3iiyiimeET1ooEl9iXxBEXRoxnLRNBLPmSBMLndUrbZDfoaURJ3REx`
- **Base URL**: `https://api.greynoise.io`
- **Endpoint**: `GET /v3/community/{ip}`

**Sample Usage**:
```bash
curl -H "key: Fqyk27ii8P3iiyiimeET1ooEl9iXxBEXRoxnLRNBLPmSBMLndUrbZDfoaURJ3REx" \
"https://api.greynoise.io/v3/community/172.16.0.54"
```

## 🛑 AbuseIPDB

- **API Key**: `0bb2c17a985dcc891773d25307ff950cf5fb9899b9eef1cb7e7993d7b977371cc391b7a7bf491a03`
- **Base URL**: `https://api.abuseipdb.com`
- **Endpoint**: `GET /api/v2/check?ipAddress={ip}`

**Sample Usage**:
```bash
curl -G https://api.abuseipdb.com/api/v2/check \
--data-urlencode "ipAddress=172.16.0.54" \
-H "Key: 0bb2c17a985dcc891773d25307ff950cf5fb9899b9eef1cb7e7993d7b977371cc391b7a7bf491a03" \
-H "Accept: application/json"
```

## 🧠 Shodan

- **API Key**: `z9W9eDodEBro84JX6CqYCbe0JgMjP8qo`
- **Base URL**: `https://api.shodan.io`

**Endpoints Used**:
- `/shodan/host/{ip}` → Fetches open ports, services, hostnames, known vulns
- `/dns/reverse?ips={ip}` → Resolves hostname

**Sample Usage**:
```bash
curl -s "https://api.shodan.io/shodan/host/172.16.0.54?key=z9W9eDodEBro84JX6CqYCbe0JgMjP8qo" \
-o /opt/honeybomb/enriched_ips/172.16.0.54/shodan.json
```

## 📌 Integration Notes

- All data is stored in: `/opt/honeybomb/enriched_ips/{ip}/`
- Enrichment is triggered automatically when threat level ≥ `medium`
- Used in behavioral correlation, attribution, and red-team reporting modules
