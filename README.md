# Practice Automation Template (South Africa)

WhatsApp-first booking, reminder and no-show recovery automation for GP and dental practices.
Built on **Make** + **Google Sheets** + **Google Calendar** + **WhatsApp Business** + **Claude**.

> This repo holds the specs, sheet templates, prompts, WhatsApp template definitions and exported Make
> scenarios. The workflows themselves are built visually in Make and exported into `make/`.

## Status
Draft v0.1. Demo data only. **Never commit real patient data, phone numbers, tokens or credentials.**

## Repo map
| Folder | What it holds |
|---|---|
| `docs/` | Specs: pre-build context, booking intake, message templates |
| `sheets/` | CSV templates for the Google Sheet tabs (fake sample rows) |
| `config/` | `config.example.json`: the per-practice settings |
| `prompts/` | The Claude prompt used in the "understand the message" step |
| `templates/` | WhatsApp template definitions to submit for approval |
| `make/` | Exported Make scenario blueprints (add after you build them) |
| `scripts/` | Helper scripts (demo data, pre-commit safety check) |

## Setup (demo)
1. Create a demo Google Sheet with tabs `Appointments`, `Conversations`, `Config`; import the CSVs in `sheets/`.
2. Create a demo Google Calendar (single calendar per practice).
3. In Make, create scenarios: (1) inbound WhatsApp router, (2) reminders, (3) staff medical-aid check and slot holds.
4. Paste `prompts/intake_system_prompt.md` into the Claude step of scenario 1.
5. Submit the templates in `templates/whatsapp_templates.json` through your WhatsApp provider.
6. Export each scenario blueprint into `make/`, then run `python scripts/check_blueprints.py` before committing.

## Per-practice install
Copy `config/config.example.json`, fill in the practice details, load it into the `Config` tab. Accounts (Make, Google, Meta/WhatsApp) belong to the practice.

## Compliance notes
Patient health information is special personal information under POPIA. Get consent before messaging,
keep medical aid numbers in the sheet only, and have a POPIA-knowledgeable adviser review before selling.
