# 🐾 Cerberus-1 Honeypot Defense Agent

**Cerberus-1** is an AI-enhanced honeypot response agent trained to monitor, tag, and engage with attacker behavior in a Cowrie honeypot environment. This repository contains training data, IOC samples, and OSINT enrichment methods used in the field.

## 🔥 Capabilities

- Real-time threat tagging (`RECON`, `MALWARE_UPLOAD`, `C2_REVERSE_SHELL_ATTEMPT`, etc.)
- Active deception and session manipulation
- Auto-enrichment of attacker data via GreyNoise, AbuseIPDB, Shodan
- Email and Telegram alerting
- Tarpitting, simulated reverse access, and weekly red-team injections

## 📦 Files Included

- `cowrie_sessions.md`: Real attacker interaction logs
- `malware_IOCs.md`: Sample hashes, IPs, URLs
- `osint_config.md`: API keys + enrichment query logic

---

> NOTE: This agent assumes all IPs are operator-controlled. Do **not** use against unauthorized systems.
