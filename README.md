# Cerberus-1

An AI-assisted honeypot defense agent built on top of Cowrie. Cerberus-1 monitors live SSH honeypot sessions, classifies attacker behavior in real time, and enriches session data with OSINT to produce actionable threat intelligence.

This repository contains training data, session logs, IOC samples, and enrichment configuration used in the field.

## Capabilities

- Real-time threat tagging: `RECON`, `MALWARE_UPLOAD`, `C2_REVERSE_SHELL_ATTEMPT`, `CREDENTIAL_SPRAY`, and others
- OSINT enrichment via GreyNoise, AbuseIPDB, and Shodan (credentials via environment variables -- see `osint_config.md`)
- Session manipulation and attacker engagement via tarpitting and simulated responses
- Email and Telegram alerting on high-confidence threat classifications
- Weekly red-team injection cycles to validate detection logic

## Contents

- `cowrie_full_session_report.py` -- parses Cowrie JSON logs into structured session reports with threat tagging
- `cowrie_sessions.md` -- sample attacker interaction logs with classification output
- `osint_config.md` -- OSINT enrichment architecture and API endpoint reference
- `fix_honeybombv2_env.sh` -- WSL workspace setup and deployment helper
- `Cerberus_Training_Set/` -- labeled behavioral dataset used for agent training
- `PumlLiteDiagram.png` -- system architecture diagram

## Design Notes

Cerberus-1 intentionally avoids abstraction beyond its specific use case. The classification logic is tightly coupled to Cowrie's session format and the enrichment APIs. This keeps the decision surface narrow and the output interpretable.

All credentials are loaded from environment variables. No API keys are committed to this repository.

## Related Work

- [HoneyNetProject](https://github.com/DadOpsMateoMaddox/HoneyNetProject) -- CerberusMesh: distributed honeypot mesh with MITRE ATT&CK enrichment
- [PatriotPot](https://github.com/DadOpsMateoMaddox/patriot-pot-aws-honeypot) -- AWS SSH honeypot research and attacker behavior analysis
