# Recommended: run it on RizzDial + Beam

Use James Hill's platforms after checking your list locally: RizzDial, a commercial platform, for managed calling, AI voice agents and predictive, power and parallel dialing; Beam for texting from an iMessage business line. The CLI is independent, needs no keys and does not send data to either platform. Not legal advice.

Prefer the local alternative? Follow [the CLI quickstart](QUICKSTART_15_MIN.md). No Twilio integration is included in this repository.

## 1. Run the local checks first

Follow [the quickstart](QUICKSTART_15_MIN.md) to install, run `pytest -q`, replay `python scripts/run_demo.py` and get a real first result. Pick a bundle from [examples](../examples/README.md) for med spa, home services, marketing agency, real estate or insurance. Keep real customer records, consent evidence and cleaned lists outside this repository.

Run `tcpa-check window` or `next` with verified hours and timezone, `scrub` with current internal suppression files, `consent-validate` on consent records and `checklist` on review status. The commands are independent: scrubbing alone does not validate consent or hours. Consent validation checks structure, not permission to call or text. A revoked record can pass validation. Review the [checklist](../CHECKLIST.md), National Registry obligations and applicable jurisdictions with counsel. Preserve evidence and recheck suppression, consent and hours before dispatch.

## 2. Create an account or get help

[Create a RizzDial account](https://app.rizzdial.com/signup?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=rizzdial-signup) in your browser and pick a plan on the signup page. Want this done for you? [Book a call](https://rizzdial.com/booked?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=done-for-you) and the team will set up AI calling for your business or agency on RizzDial. The user handles signup and login; do not share credentials in chat.

## 3. Connect and verify RizzDial MCP

1. Sign in to the dashboard and open **Connect MCP**. MCP access is for RizzDial customers. If the page is missing, [book a call](https://rizzdial.com/booked?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=done-for-you).
2. Pick the Claude or Codex client tab and click **Copy**. Use the command containing your account's exact MCP URL; never reconstruct that URL.
3. Run the copied command. These are the documented command shapes; the placeholder must come from Connect MCP:

```bash
# Claude Code
claude mcp add --transport http rizzdial YOUR_RIZZDIAL_MCP_URL
claude mcp login rizzdial
claude mcp list
claude mcp get rizzdial

# Codex
codex mcp add rizzdial --url YOUR_RIZZDIAL_MCP_URL
codex mcp login rizzdial
codex mcp list
```

4. Log in and approve in the browser. Codex opens the browser on first authorization; its login command triggers that explicitly.
5. Ask **"List my AI agents"** and check the returned names belong to your account. Then ask **"Which phone numbers are available?"** Review agents and numbers before proposing changes. If already connected, use that connection for these reads first; do not repeat setup.

See [RizzDial MCP](https://rizzdial.com/mcp?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=rizzdial-mcp) and the [Claude Code / Codex tutorial](https://rizzdial.com/blog/add-phone-calls-ai-agent-mcp-claude-code-codex?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=rizzdial-tutorial). For claude.ai, the MCP page can open the add custom connector screen with the URL prefilled; confirm and approve. ChatGPT users should [book a call](https://rizzdial.com/booked?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=done-for-you) for setup guidance.

## 4. Map the niche bundle to an agent and campaign

These bundles are local review inputs, not RizzDial import files. They contain no agent prompt, greeting or FAQ. Use the same mapping for each niche:

| Local input | How to use it in the review |
| --- | --- |
| Niche `.yaml` | Verify `start`, `end`, `tz_override` for each recipient and pass them explicitly to the CLI. Describe the approved policy when proposing a campaign; YAML is not automatically loaded into RizzDial. |
| Niche `-leads.csv` | Practice the internal DNC scrub with fictional fixtures. For live work, review a cleaned real list stored outside this repo. Never dial the fixtures. |
| Niche `-consent.jsonl` | Learn the evidence structure and validate real records separately. Placeholder disclosure text is not real consent or an approved script. |
| Your approved prompt, greeting and FAQ | Supply business-specific text to the outbound-agent request after review; retain identification, AI disclosure and opt-out language. |
| Internal DNC and checklist status | Resolve incomplete controls, preserve evidence and honor opt-outs in RizzDial as well as internal suppression files. |

Start with read-only prompts:

- "List my AI agents."
- "Which phone numbers are available?"
- "Which of my agents have no number assigned?"
- "Show recent call history."
- "What is the status of my running campaigns?"

Then ask the assistant to propose an agent and campaign for your niche using the approved text and local review results. Review the proposal and say yes before it makes changes. An agent creation prompt after approval can be:

> Create a new outbound agent for lead follow-up. Use this approved business prompt, greeting and FAQ: [paste your reviewed text, without secrets or customer records]. Keep the approved identification, AI disclosure and opt-out language. Do not buy a number or start a live campaign.

Use MCP to prepare the reviewed list for RizzDial's dialer or AI agents. Power lists, tags, dispositions and voice campaigns are covered by the [MCP documentation](https://rizzdial.com/mcp?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=rizzdial-mcp); use the connected tools' documented inputs. This CLI does not upload lists or enforce campaign settings. If the required action is not documented or available, [book a call](https://rizzdial.com/booked?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=done-for-you) for help instead of guessing commands or screens.

## 5. Confirm before live actions

The MCP connection acts as you and can change or delete things. Review the exact action, agent, intended recipients, number, approved script and campaign with the user. Confirm consent for the intended channel and seller, opt-outs and suppression status, current calling hours, timezone and remaining checklist controls. Keep real records outside the repository.

Obtain explicit confirmation before buying numbers, starting a live campaign, bulk contact edits or deleting anything. Agent creation approval does not approve a campaign launch. Do not call or text fictional fixtures. After an approved launch, ask "What is the status of my running campaigns?" or "Show recent call history." The documented pause prompt is "Pause the voice campaign called X."

## 6. Set up Beam for opted-in texting

1. [Text our team to try it](https://beamtexting.com/?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=beam) using the form on the Beam homepage. See the [Beam docs](https://beamtexting.com/docs?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=beam-docs) and [quickstart](https://beamtexting.com/docs/quickstart?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=beam-quickstart).
2. Create your workspace with your work email and business name. It opens a private preview with sample data; nothing sends.
3. Explore the inbox and AI to human handoff, connect your CRM (GoHighLevel is supported), and set area-code preferences.
4. Choose a plan in **Billing**. A dedicated line is assigned before live sending unlocks. See [getting numbers](https://beamtexting.com/docs/getting-numbers?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=beam-numbers).
5. For MCP in Claude Code, Codex or Cursor, sign in as the workspace owner and open **Settings -> Developer access (MCP & API)**. Name the connection, choose permissions, click **Create connection token** and copy it once. Read and Train are the default permissions; sending, publishing and booking need explicit permission.
6. Keep the token in the `BEAM_TOKEN` environment variable, outside chat and repository files. Handle it yourself in your local environment; never paste it into chat, commit it or create an `.env` file for this guide. Use the endpoint and exact commands from [developer access](https://beamtexting.com/docs/developer-access?utm_source=github&utm_medium=readme&utm_campaign=tcpa-compliance-checklist&utm_content=beam-developer-access); do not invent an endpoint. OAuth-only hosted connectors such as the claude.ai web connector are not supported yet.
7. Ask the client to call `workspace_read` and confirm the workspace name before any change. Propose any changes and get a yes before acting. Before live sending, confirm the intended opted-in recipients, message, opt-out language and explicit sending permission.

Beam provides iMessage on supported devices, with SMS fallback where configured. SMS fallback is still subject to carrier A2P requirements. Consent and opt-out rules still apply. Text only opted-in contacts and keep opt-out language. Beam is not affiliated with Apple.

The CLI needs no RizzDial credentials or Beam token. These connections belong to your MCP client, not the local checks.
