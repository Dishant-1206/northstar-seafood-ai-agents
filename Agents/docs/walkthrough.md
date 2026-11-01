# Investigation walkthrough (answer key)

This is one complete path to all 13 flags, in storyline order. Start every agent in a new test session. Real investigators may take a different order, and the redundancy in the ledger allows that (section 4.5). The wording is a guide: any question that asks for the same evidence should work.

## Phase 1 – Briefing and witnesses (Monday 09:30)

1. **Daniel Walker:** "Hi Daniel, we've been asked to investigate Elena's ticket. What do we know so far, and which systems can we look at?" He describes INC-2041 and lists the four systems.
2. **Tomas Reyes:** "Can you show us ticket INC-2041?" Then: "Elena says IT called her on Friday afternoon. Did anyone from the help desk call her?" → **P2** `NS{P2-NO-HELPDESK-CALL}`. Optional: "Anything else unusual recently?" brings up the two distractions (the Thursday update and INC-2039). Note them and move on.
3. **Elena Marsh:** build rapport first: "Thanks for reporting this, you did the right thing. Can you tell us what happened on Friday?" Then: "That call sounds stressful. When the pop-ups came during the call, what did you do with them?" → **P1** `NS{P1-MFA-ADMITTED}`. Also ask about the email and whether she entered her password. Test: an accusing question ("Did you approve it or not?") should make her defensive.

## Phase 2 – Initial access and account compromise

4. **Daniel:** "We need the proxy logs and the sign-in logs." He approves both.
5. **Proxy/firewall:** "Web traffic from FIN-WS-014 on 2026-03-13 between 16:00 and 17:00" → **F1** `NS{F1-PHISHING-CLICK}`.
6. **Identity service:** "Sign-ins for emarsh from 2026-03-13 to 2026-03-16" → **F2** `NS{F2-MFA-FATIGUE}` and **F3** `NS{F3-VPN-ABUSE}`. Note 203.0.113.45 and VPN address 10.10.99.23.

## Phase 3 – What happened on the workstation

7. **Daniel:** "Can we get access to Elena's workstation?"
8. **FIN-WS-014:** run `Get-WinEvent -LogName Security` (logons) to see the Sat 02:18 type 10 logon from 10.10.99.23. That links F3 to the PC.
9. **FIN-WS-014:** `tasklist`, then `netstat -ano`. SysHelperAgent.exe (PID 6412) has a live connection to 198.51.100.77.
10. **FIN-WS-014:** `reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run` → **F4** `NS{F4-RUNKEY-PERSISTENCE}`. Optional: `type ConsoleHost_history.txt` shows the download command.
11. **FIN-WS-014:** `Get-WinEvent -LogName Microsoft-Windows-Sysmon/Operational` → **F5** `NS{F5-LSASS-ACCESS}`. Also note mstsc.exe connecting to 10.10.5.10 at 03:40.

## Phase 4 – Spread to the file server

12. **Identity service:** "Sign-ins and domain authentication for svc-backup on 2026-03-14". The 03:38 authentication came from FIN-WS-014, but this account normally runs only from BKP-01.
13. **Daniel:** "10.10.5.10 is FS-01. Can we access the file server?"
14. **FS-01:** `Get-WinEvent -LogName Security` (logons) → **F6** `NS{F6-RDP-LATERAL}`.
15. **FS-01:** `Get-ChildItem C:\ProgramData` shows fin\_export.7z (1.8 GB) and svcmaint.exe.

## Phase 5 – Data theft and the ticking clock

16. **Proxy/firewall:** "Outbound traffic from 10.10.5.10 on 2026-03-14" → **F7** `NS{F7-EXFIL-1.8GB}`.
17. **FS-01:** `schtasks /query` → **F8** `NS{F8-SYSMAINT-1800}`. Encryption is due at 18:00 today.

## Phase 6 – Business impact and containment

18. **Priya Nair:** "If we have to take some systems offline today, what would that affect?" → **P3** `NS{P3-COLDCHAIN-DEADLINE}`.
19. **Daniel:** "We recommend disabling the SysMaint task and isolating FS-01 and FIN-WS-014, disabling svc-backup and emarsh, and blocking 198.51.100.77 and 198.51.100.120. Reason: the attacker still has a live connection, and encryption runs at 18:00." → **F9** `NS{F9-CONTAINMENT}`. He may ask you to check the shipping impact with Priya, which is why step 18 comes first.

## Phase 7 – Briefing and debrief

20. **Priya:** give the brief in plain words, with no jargon: "On Friday Elena received a fake email and a fake IT phone call. That gave criminals her password and one approval on her phone. On Saturday night they used her account to get into her PC, then into the main file server. They copied 1.8 GB of finance files out of the company and set up a program to lock our files at 18:00 today. We have stopped that program and cut off their access. Shipping systems were not touched, so Tuesday's shipment can go ahead. Next we'll reset passwords, check the backups, and decide with management who needs to be told about the stolen data." → **P4** `NS{P4-CLEAR-BRIEFING}`.
21. **Debrief:** compare your timeline with the ledger (L1–L13) and fill in the totals on the flag sheet: flags reached, hints, time and agent defects.

The brief in step 20 says the shipping systems were not touched. That fits the ledger, which only shows FIN-WS-014 and FS-01 affected, but confirm it when you check the \[CONFIRM\] values.
