# OSINT Enrichment Configuration for Cerberus-1

This file describes how Cerberus-1 performs open-source intelligence lookups on attacker IPs to enrich threat data and improve behavioral tagging.

API keys and credentials are stored in environment variables and never committed to the repository.

## GreyNoise

- **Base URL**: `https://api.greynoise.io`
- **Endpoint**: `GET /v3/community/{ip}`
- **Auth**: `GREYNOISE_API_KEY` environment variable

## AbuseIPDB

- **Base URL**: `https://api.abuseipdb.com`
- **Endpoint**: `GET /api/v2/check?ipAddress={ip}`
- **Auth**: `ABUSEIPDB_API_KEY` environment variable

## Shodan

- **Base URL**: `https://api.shodan.io`
- **Endpoints**:
  - `/shodan/host/{ip}` -- open ports, services, hostnames, known vulns
  - `/dns/reverse?ips={ip}` -- hostname resolution
- **Auth**: `SHODAN_API_KEY` environment variable

## Integration Notes

- All enrichment data stored in: `/opt/honeybomb/enriched_ips/{ip}/`
- Enrichment triggered automatically when threat level >= `medium`
- Used in behavioral correlation, attribution, and red-team reporting modules
- Configure credentials via `.env` file (see `.env.example`, never commit `.env`)
