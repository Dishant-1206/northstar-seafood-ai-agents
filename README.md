# Northstar Seafood – AI-assisted cyber incident response agents

Eight prompt-configured Microsoft Copilot Studio agents for a tabletop cyber incident response exercise. Investigators interview four human personas and query four simulated systems to reconstruct a fictional ransomware intrusion at Northstar Seafood, a fictional fish processing and export company.

Developed for a bachelor's thesis at Turku University of Applied Sciences (TUAS) by Dishant Patel, 2026.

> **Everything here is fictional.** Company, people and evidence are invented. External addresses and domains use ranges reserved for documentation (192.0.2.x, 198.51.100.x, 203.0.113.x, `*.example`). No real systems, malware, credentials or hashes are included, and the agents run no commands.

## Contents

```
agents/
├── Northstar_Seafood_Agents_1_0_0_0.zip   Copilot Studio solution (all 8 agents, unmanaged)
├── README.md
├── prompts/                               Agent instructions as plain text
│   ├── 01_elena_marsh.md                  Finance officer – phishing and MFA witness
│   ├── 02_tomas_reyes.md                  Help desk technician – ticket history
│   ├── 03_priya_nair.md                   Operations manager – business impact
│   ├── 04_daniel_walker.md                IT manager – access, hints, containment approval
│   ├── 05_fin-ws-014.md                   Finance workstation – simulated PowerShell
│   ├── 06_identity_service.md             Sign-in, MFA and domain authentication logs
│   ├── 07_proxy_firewall.md               Web proxy and firewall logs
│   └── 08_fs-01.md                        File server – simulated PowerShell
└── docs/
    ├── evidence_ledger.md                 Ground truth shared by all agents
    ├── flag_sheet.md                      13 flags to record progress per run
    ├── walkthrough.md                     Full solution path (answer key)
    └── test_log.md                        Prompt test log and test checklists
```

## Option 1 – Import the solution file

Needs a Copilot Studio environment and at least the System Customizer security role.

1. In Copilot Studio, open **Solutions** and select **Import solution**.
2. Select `Northstar_Seafood_Agents_1_0_0_0.zip` and finish the import wizard.
3. If the import fails, select **Download log file**. Missing components are the most common cause.
4. Open each agent from the imported solution and check its settings (see Option 2, steps 5–6).
5. Publish an agent before sharing it. Microsoft notes that the icon and channel settings may not carry over.

Reference: [Export and import agents using solutions](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-solutions-import-export)

## Option 2 – Rebuild from the prompts

Repeat for each of the eight files in `prompts/`. Copilot Studio labels change often and may differ slightly.

1. Go to copilotstudio.microsoft.com and sign in.
2. On **Home**, describe the agent briefly (e.g. "Role-play persona Elena Marsh for a cybersecurity tabletop exercise"). The **Overview** page opens.
3. Dismiss the suggested name, description and instructions.
4. Set the **Name** (e.g. "NS – Elena Marsh (Finance)") and a one-line **Description**.
5. Paste everything inside the text block of the prompt file into **Instructions**.
6. Under **Knowledge**, turn **Web Search** off and add no knowledge files. In **Settings → Generative AI**, turn **Let other agents connect to and use this one** off. If **Allow ungrounded responses** is shown, leave it on.
7. Optional: replace the greeting in **Topics → Conversation Start** with an in-character line, or delete it.
   - Elena: "Oh, hi… is this about my ticket?"
   - Tomas: "Help desk, Tomas speaking."
   - Priya: "Yes? I've got five minutes."
   - Daniel: "Good, you're here. Let's get started."
8. In **Test your agent**, run the checklists in `docs/test_log.md`.

## Running an exercise

1. Start a new session for every agent before each run, so each flag can appear again.
2. The facilitator briefs investigators: find how the attacker got in, which accounts and systems are affected, what data left the company, and what to contain now. In the scenario it is Monday 09:30, and the encryption is set for 18:00.
3. Investigators ask Daniel Walker for access to systems, then interview the personas and query the systems in any order.
4. Each agent shows a flag code (`NS{...}`) once, when its key evidence is found. Record flags, times and hints on `docs/flag_sheet.md`.
5. The run ends with a plain-language briefing to Priya Nair and a debrief against `docs/evidence_ledger.md`.

`docs/walkthrough.md` and the flag codes give away the full solution. Do not share them with participants.

## Notes and limitations

- Agent replies come from a language model and are not deterministic. Check outputs against the evidence ledger during each run.
- Values marked `[CONFIRM]` are draft scenario values. If you change one, update every prompt that uses it.
- Tested in the Copilot Studio test pane on 1 November 2026; see `docs/test_log.md` for defects found, fixes and open realism observations.
- Not a forensic tool: it is not connected to any live telemetry, and it needs a facilitator to run.
