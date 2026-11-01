# Evidence ledger (ground truth)

Single source of truth for all eight agents. Values marked [CONFIRM] are drafts; any change must be made in every prompt that uses the value.

## Persona-level values

| Placeholder | Draft value | Used by |
| --- | --- | --- |
| Company email domain | northstarseafood.example | All |
| Elena's username | emarsh | Elena, Tomas, Daniel |
| Phishing email sender | accounts-portal@northstar-payments.example | Elena |
| Phishing email subject | Supplier payment portal – verify your account before Monday | Elena |
| Caller's name and claim | "Mark from the IT help desk" about a mailbox security update | Elena, Tomas |
| Number of MFA prompts Friday | About 4; Elena approved 1 during the call | Elena |
| Help desk hours Friday | Until 16:00, so no staff at 16:35 | Tomas |
| Elena's Monday ticket | INC-2041, logged Monday 08:20 | Tomas, Daniel |
| Distractor ticket | INC-2039, warehouse user lockout (unrelated) | Tomas |
| Distractor patch | Routine Windows update pushed Thursday evening | Tomas, Daniel |
| Key shipment | Frozen salmon export to a Japanese customer, dispatch Tuesday 06:00 | Priya |
| File server name | FS-01 | Daniel |
| Workshop "now" | Monday 09:30 | All |

## System-level ledger

All four system agents use the same ledger, so the same address, account and time appear wherever two systems overlap (sections 4.7 and 5.10). Build them in Copilot Studio exactly like the personas, with web search off and other agents unable to connect. Every value below is a draft marked \[CONFIRM\], because the thesis gives none. External addresses and domains use ranges reserved for documentation (203.0.113.x, 198.51.100.x, \*.example), so no real infrastructure appears (section 4.7).

Draft dates: Friday 2026-03-13, Saturday 2026-03-14, Monday 2026-03-16. Times are local (EET, UTC+2). Simulated "now" is Monday 09:30.

| # | Time | Event | Seen by |
| --- | --- | --- | --- |
| L1 | Fri 16:12 | FIN-WS-014 (10.10.20.14) opens https://northstar-payments.example/login and POSTs the form at 16:13 | Proxy |
| L2 | Fri 16:36–16:39 | 4 MFA push prompts for emarsh from 203.0.113.45; 3 denied or timed out, the 4th approved at 16:39 | Identity |
| L3 | Sat 02:15 | emarsh signs in to Northstar Remote Access (VPN) from 203.0.113.45, success, VPN address 10.10.99.23 | Identity, Proxy |
| L4 | Sat 02:18 | Remote interactive logon (type 10) to FIN-WS-014 as emarsh from 10.10.99.23 | Workstation |
| L5 | Sat 02:30 | powershell.exe downloads SysHelperAgent.exe from cdn.syncupdate.example (198.51.100.77) to C:\\Users\\emarsh\\AppData\\Roaming\\SysHelper; Run key "SysHelper" created | Workstation, Proxy |
| L6 | Sat 03:05 | SysHelperAgent.exe accesses lsass.exe memory | Workstation |
| L7 | Sat 03:38 | Account svc-backup authenticates from FIN-WS-014 | Identity |
| L8 | Sat 03:40 | RDP session FIN-WS-014 → FS-01 (10.10.5.10) as svc-backup | File server, Workstation |
| L9 | Sat 04:05 | Archive C:\\ProgramData\\fin\_export.7z (1.8 GB) created from D:\\Shares\\Finance | File server |
| L10 | Sat 04:30–04:52 | FS-01 uploads 1.8 GB to files.quickshare.example (198.51.100.120) | Proxy, File server |
| L11 | Sat 04:50 | Scheduled task "SysMaint" created on FS-01, runs C:\\ProgramData\\svcmaint.exe at Mon 18:00 (not yet run) | File server |
| L12 | Mon 08:02, 08:10 | 2 more MFA prompts for emarsh from 203.0.113.45, both denied | Identity |
| L13 | Mon 09:30 (now) | SysHelperAgent.exe still running on FIN-WS-014 with an open connection to 198.51.100.77:443 | Workstation, Proxy |
| D1 | Thu evening | Routine Windows cumulative update installed on staff PCs (distractor) | Workstation |
| D2 | Mon 07:45 | User jlindqvist (warehouse), 5 failed sign-ins from 10.10.40.22, account locked (INC-2039, distractor) | Identity |

Elena's phishing sender and the company domain now use reserved domains too (northstar-payments.example, northstarseafood.example), because the earlier `.com` and `.fi` drafts could be real domains.
