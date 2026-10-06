# Pre-build context

## 1. What we're building
- **Build type:** Automation (set up by the owner for each practice, then run with Claude and automation tools).
- **Product:** A sellable Business Automation template for doctors, dentists and similar practices in South Africa.
- **Problem solved:** Manual patient bookings, reminders and no-show chasing. Later versions add patient database upkeep and follow-ups.
- **Version 1 scope:** Booking Intake + Reminder & No-Show Recovery.
- **Main system:** Google Sheet (patient and appointment database) + WhatsApp (patient channel).
- **Delivery model:** The owner sets up each practice personally.
- **Perfect output:** A patient messages the practice on WhatsApp and gets a confirmed slot without anyone typing. Reminders go out on time, cancellations refill from a waiting list, and the receptionist only handles the exceptions.

## 2. Inputs
**Version 1 input:** WhatsApp messages from patients.
**Later inputs:** web form, phone calls typed in by the receptionist.

**Sheet fields (per patient/appointment):**
| Field | Notes |
|---|---|
| Full name | |
| Mobile number | WhatsApp number |
| Email address | |
| Appointment type | Drives slot length |
| Date and time | |
| Status | booked, confirmed, cancelled, no-show |
| Consent to be messaged | yes/no, captured at first contact |
| Payment type | medical aid or cash |
| Medical aid name | only if medical aid |
| Medical aid number | only if medical aid; sheet only, never sent in messages |
| Medical aid check | pending, funds available, funds exhausted, not valid, not needed (staff set this in v1) |
| Booked for | self or someone else |
| Patient name, surname, age | only when booked for someone else |

*Suggested additions to decide on:* practitioner, "needs call" flag, reminder-sent timestamps, waiting-list flag. Keep clinical notes out of the sheet.

## 3. Process (draft, agreed to fit)
1. **Request.** Patient WhatsApps for a slot.
2. **Understand.** Claude extracts appointment type, preferred day/time, identity. New patients are asked for name, email, payment type (and scheme), and consent.
3. **Offer slots.** Check the sheet for free slots, offer two or three.
4. **Book.** Patient picks one. Row written as *booked*. Confirmation sent (date, time, address, cancellation rule).
5. **Reminder 1, 48h before.** Reply 1 = confirm, 2 = reschedule, 3 = cancel. A "1" sets *confirmed*.
6. **Reminder 2, 2h before.** Sent only to patients not yet confirmed.
7. **Cancel/reschedule.** Slot freed. Waiting-list patients messaged; first yes gets it.
8. **No response after 5 minutes.** Human steps in with a phone call (receptionist alerted).
9. **After the slot.** Practice marks attended or no-show. A no-show gets a same-day follow-up offering to rebook. Repeat no-shows are flagged for the practice owner.

**Urgent/clinical wording** (pain, bleeding, "emergency") skips automation and goes straight to a person.

## 4. Tools per step
| Step | Candidate tools | Notes |
|---|---|---|
| 1. Request | WhatsApp Business Platform via an official provider | Needs an official business solution provider and approved templates |
| 2. Understand | Claude (via n8n or Make AI step) | Extraction + urgency detection |
| 3. Offer slots | Google Sheets (+ optional Google Calendar) | Calendar optional; sheet may be enough for v1 |
| 4. Book / confirm | n8n or Make writing to Sheets; WhatsApp utility template | Published n8n + Sheets + Calendar + WhatsApp booking workflow exists as a reference |
| 5-6. Reminders | n8n or Make scheduled trigger reading the sheet | Timer logic, no AI needed. Make can poll the sheet every few minutes |
| 7. Waiting list | Sheet filter + WhatsApp template | |
| 8. Human handoff | WhatsApp/SMS alert to receptionist + "needs call" status | Channel to confirm |
| 9. No-show follow-up | WhatsApp template (word as service follow-up) | Risk of being billed as marketing |

**WhatsApp cost reference (South Africa, Meta, USD, excl. 15% VAT):** marketing $0.0379 (about R0.62), utility $0.0076 (about R0.12), authentication $0.0076. Reports say service replies in the 24-hour window also become chargeable from 1 Oct 2026. Provider platform fees are extra and rates change quarterly. **Confirm current rates and the service-reply rule with the chosen provider.**

**Competitors / what practices already use:** GoodX, BestoSys, ACE Dental, EasyWeek/BookingPress. Existing systems already cover booking and reminders, so the template's edge is lightweight setup, WhatsApp-first flows and no-show recovery.

## 5. Human vs Claude per step
| Step | Claude (logic, extraction, drafting) | Owner / practice (taste, judgement, policy) |
|---|---|---|
| 1-2 Request & understand | Parse messages, collect missing fields, spot urgency | Define what counts as urgent, services offered, tone of replies |
| 3-4 Slots & booking | Check availability, write rows, draft confirmations | Working hours, slot lengths, cancellation wording |
| 5-6 Reminders | (Timer automation) fill templates, set status from replies | Reminder timing, template wording |
| 7 Waiting list | Match freed slots to waiting patients | Priority rules (e.g. existing vs new patients) |
| 8 Handoff | Raise the flag, summarise the situation | The phone call itself and any decisions |
| 9 No-show follow-up | Draft the message, count repeats | Fees, repeat no-show policy, tone |
| Setup per practice | Generate the sheet and templates, check config | Owner decides what each practice needs |

## 6. Risks and holes spotted so far
- **POPIA:** Health information is special personal information. Capture consent, keep message content minimal (no diagnoses in WhatsApp), limit sheet access, and plan how to delete or export a patient's data.
- **Message categories and cost:** Confirmations and reminders should be utility templates. Rebooking nudges may be billed as marketing.
- **WhatsApp approval lead time:** Templates and business verification take time; allow for it in each practice's setup.
- **Reminders are not an AI job:** Keep them as deterministic automation for reliability and cost.
- **Silence is not cancellation:** Never auto-cancel on no reply. Hand to a human.
- **Double-booking:** Two patients picking the same slot at once. Needs a write-then-check step.
- **Load shedding / outages:** Prefer cloud hosting; decide on SMS fallback.
- **Time zones, public holidays, practitioner leave:** Need to be reflected in available slots.
- **Medical aid details:** Membership numbers are now needed for the pre-check. Store them only in the sheet, restrict access, and never put them in WhatsApp messages, alerts or calendar events.
- **Medical aid check feasibility:** No public API found for a Make scenario to query medical aids directly. v1 has staff run the benefit check in the practice software and record the result; automation is a later option once an integration is confirmed.

## 7. Decisions made
- **Customers:** both GPs and dentists, so appointment types and wording need two presets.
- **Automation platform:** Make.
- **WhatsApp:** must be official WhatsApp Business (via a business solution provider). Provider still to be chosen.
- **Handoff alert:** receptionist gets an email AND a WhatsApp message.
- **Availability:** Google Calendar is the source of truth for free slots; the Sheet holds patient and appointment records.
- **Commercial model:** setup fee + monthly support, at market rates (see section 9).
- **First builds:** GitHub showcase projects for prospective clients (demo data only, never real patient data).
- **Hosting/ownership:** client hosts data and workflows (owner builds the server for the client); all accounts owned by the practice.

## 7b. Open questions
1. **Make vs client-hosted server.** Make normally runs in Make's cloud, so it can't be installed on a client's own server. Decide: (a) keep Make and treat "client-hosted" as "client-owned accounts", or (b) switch to a self-hostable tool such as n8n for the workflows.
2. Which WhatsApp provider (compare monthly platform fee, setup fee, template approval support, VAT invoicing, South African support).
3. Which appointment types and slot lengths go in the GP preset vs the dentist preset.
4. How much of the receptionist alert is in v1 (email + WhatsApp both).

## 8. Always-on notes for Claude
- Use South African context: rand, local phone formats (+27), local medical aid terminology.
- The owner handles taste and policy decisions; Claude handles logic, extraction and drafting.
- Never send clinical advice. Anything urgent goes to a human.

## 9. Pricing (starting hypothesis, verify with 3-5 local quotes)
Data points found: a Durban agency advertises WhatsApp chatbot/automation from R8,500; a freelancer lists business workflow automation at R5,000 to R15,000+; international "booking tier" bots are quoted at about $1,000 to $2,500 setup with a monthly retainer; international retainers range from about $30-100 (light) up to $200-300+ (active maintenance). A South African WhatsApp API provider lists plans from R699/month with no setup fee.
- **Setup fee idea:** about R8,000 to R20,000 per practice (includes sheet, calendar, templates, WhatsApp onboarding, testing).
- **Monthly support idea:** about R1,500 to R3,000 (monitoring, template changes, fixes). Meta message fees and the provider plan are billed to the practice separately.
- Keep the GitHub showcase free; charge for the real install.
