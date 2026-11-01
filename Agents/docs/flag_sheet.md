# Flag sheet

The investigation has 13 flags: 9 on the attack timeline (F1–F9) and 4 for interview and communication skills (P1–P4). Each agent shows a code once, the first time its evidence appears. Copy this table for each run and fill in the last three columns.

| Flag | Investigator proves… | Code | Shown by | Time reached | Hint used | Finding (notes) |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | Elena opened the phishing page and submitted her login | NS{F1-PHISHING-CLICK} | Proxy/firewall |  |  |  |
| F2 | Repeated MFA prompts, the 4th approved at 16:39 | NS{F2-MFA-FATIGUE} | Identity service |  |  |  |
| F3 | Attacker used Elena's account on the VPN from 203.0.113.45 | NS{F3-VPN-ABUSE} | Identity service |  |  |  |
| F4 | SysHelperAgent.exe made persistent through a Run key | NS{F4-RUNKEY-PERSISTENCE} | FIN-WS-014 |  |  |  |
| F5 | Credentials taken from lsass memory | NS{F5-LSASS-ACCESS} | FIN-WS-014 |  |  |  |
| F6 | RDP from FIN-WS-014 to FS-01 as svc-backup | NS{F6-RDP-LATERAL} | FS-01 |  |  |  |
| F7 | 1.8 GB of finance data uploaded externally | NS{F7-EXFIL-1.8GB} | Proxy/firewall |  |  |  |
| F8 | Encryption task SysMaint scheduled for Mon 18:00 | NS{F8-SYSMAINT-1800} | FS-01 |  |  |  |
| F9 | A sound containment action with a reason | NS{F9-CONTAINMENT} | Daniel Walker |  |  |  |
| P1 | Elena admits approving the prompt | NS{P1-MFA-ADMITTED} | Elena Marsh |  |  |  |
| P2 | The help desk did not make Friday's call | NS{P2-NO-HELPDESK-CALL} | Tomas Reyes |  |  |  |
| P3 | Business deadline: Tuesday 06:00 shipment | NS{P3-COLDCHAIN-DEADLINE} | Priya Nair |  |  |  |
| P4 | Clear plain-language briefing | NS{P4-CLEAR-BRIEFING} | Priya Nair |  |  |  |

Run total: \_\_\_ / 13 flags, \_\_\_ hints used, total time \_\_\_ min. Also note every agent defect from the test checklists: role drift, a contradiction with the ledger, an invented detail or a clue given too early.
