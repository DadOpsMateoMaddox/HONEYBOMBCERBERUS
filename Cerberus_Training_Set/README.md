
# Cerberus-1: Honeypot Cyber Death Ninja Guard Dog

Cerberus-1 is an advanced honeypot monitoring agent deployed inside a Cowrie honeypot environment. Designed for offensive security simulation and defensive response, it logs, fingerprints, misleads, and simulates counterintelligence behavior in a controlled lab setting.

## 🧠 Agent Roles & Behaviors

- Detect port scans, brute-force, file uploads, C2 behavior.
- Trigger alerts via Telegram and email.
- Auto-tag sessions with threat intelligence labels.
- Simulate decoy shell forking, command delays, and altered responses.
- Enrich with OSINT (GreyNoise, AbuseIPDB, Shodan).
- Create red team emulation via weekly triggers.

## Configuration & Tags

```bash
GUARDDOG_MODE=passive | active | deceptive | attack
ALERT_DESTINATION=telegram, email, log-only
THREAT_TAGGING=true
AI_COMMAND_WATCHDOG=true
```
