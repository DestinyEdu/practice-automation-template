# Message Templates (v0.3 DRAFT)

Save in `02 Reminders & Confirmations/`. Used by folders 01-04.
Placeholders: `[Practice]`, `[Practitioner]`, `[address]`, `[phone]` are set per practice. `{{1}}`, `{{2}}` are Meta template variables filled by Make.

## How to read this
- **A. Conversation messages** are free-form replies sent while the patient is chatting with us (inside the 24-hour window). No Meta approval needed, but they may still be billed per message (see Pre-build context).
- **B. Approved templates** are sent when WE start the message (reminders, offers, follow-ups). Each must be submitted to Meta through the provider and approved before use. Meta chooses the final category, so write them as plain service notices (utility), not promotions.
- Keep every message short, no diagnoses, no clinical detail, English only in v1.
- **Sign-off:** every message ends with "Your Friendly Doctor" (set per practice; shown below only on templates). **Replies use buttons** with typed replies as fallback. **Cancellation rule:** 24 hours' notice by WhatsApp, or the patient phones the practice.

## A. Conversation messages (inside the chat window)
| ID | When | Text |
|---|---|---|
| A1 | First contact | Hi, thanks for contacting [Practice]. Are you looking to book an appointment? |
| A2 | Consent ask (new patient) | To send you booking confirmations and reminders on WhatsApp, we need your OK. Reply YES to agree. |
| A3 | Consent declined | No problem. From here our staff will assist you directly, so please bear with us while a team member replies. |
| A4 | Details | Thanks. What is your full name, your email address, and is this visit medical aid or cash? |
| A4b | Medical aid details | Please send your medical aid name and membership number. If you're a dependant, please also send the main member's full name. |
| A4c | Check in progress | Thanks. We're confirming your medical aid cover for this visit and will come back to you shortly. |
| A5 | Returning patient email check | Is {{email}} still the best email for you? Reply YES, or send the new address and confirm you're happy for us to update it. |
| A5b | Who is it for? | Is this booking for yourself or someone else? *(buttons: Myself / Someone else)* |
| A5c | Someone else | Please send the patient's full name and surname, and their age. |
| A6 | Type + preference | What would you like to see us about (for example: check-up, follow-up, vaccination)? And which days suit you? |
| A7 | Offer slots | I have: 1) {{slot1}} 2) {{slot2}} 3) {{slot3}}. Reply with the number, or send other days that suit you. |
| A8 | Slot taken | Sorry, that slot was just taken. Here are the next options: 1) {{slot1}} 2) {{slot2}} 3) {{slot3}} |
| A9 | Booked | Booked: {{type}} for {{patient}} on {{date}} at {{time}} with [Practitioner], [address]. We need 24 hours' notice to cancel or change, or please call [phone]. Your Friendly Doctor |
| A10 | Didn't understand (1st) | Sorry, I didn't quite get that. Could you tell me what day and time you'd like? |
| A11 | Didn't understand (2nd) | I'll pass you to our team so they can help directly. |
| A12 | Urgent wording | This sounds urgent. If it's an emergency, please call 112 or 10177 now. We're alerting our team and will call you. *(Practice approves wording and numbers.)* |
| A13 | Unsupported media / language | Please send your message as text in English, or a team member will assist you shortly. |
| A14 | Asked for a person | Of course. A team member will reply to you shortly. |
| A15 | Cancel inside 24 hours | We need 24 hours' notice to cancel online. Please call [phone] and our team will help. We've let them know. |
| A17 | Cover confirmed | Good news, your medical aid cover is confirmed. Your booking is confirmed: {{type}} on {{date}} at {{time}}. Your Friendly Doctor |
| A18 | Cover not confirmed | We were unable to confirm available medical aid funds for this visit, so this booking will be a cash booking. Would you like to continue? *(buttons: Yes, continue / No, cancel)* |
| A19 | Member not valid | We couldn't verify your medical aid details. Please check the name and number and send them again, or choose a cash booking. |
| A20 | Check taking long | Thanks for waiting. Our team is still confirming your medical aid cover and will update you soon. |
| A16 | Cancel outside 24 hours | Your appointment on {{date}} at {{time}} is cancelled. To book a new time, reply here. Your Friendly Doctor |

## B. Approved templates (we start the message)
Suggested name in `snake_case`; buttons are WhatsApp quick replies.

**B1 `booking_confirmation`** (utility)
Hi {{1}}, your {{2}} appointment at [Practice] for {{3}} is booked for {{4}} at {{5}}. Address: [address]. We need 24 hours' notice to cancel or change, or please call [phone].
Your Friendly Doctor
Buttons: Confirm / Reschedule / Cancel

**B2 `appointment_reminder_48h`** (utility)
Hi {{1}}, a reminder of the {{2}} appointment for {{3}} at [Practice] on {{4}} at {{5}}. Please confirm or let us know if you can't make it. We need 24 hours' notice to cancel, or please call [phone].
Your Friendly Doctor
Buttons: Confirm / Reschedule / Cancel

**B3 `appointment_reminder_2h`** (utility), sent to ALL booked patients, confirmed or not
Hi {{1}}, a reminder that the appointment for {{2}} at [Practice] is today at {{3}}. See you soon, or call [phone] if you can't make it.
Your Friendly Doctor
Buttons: I'll be there / Can't make it
*("Can't make it" inside 24 hours triggers message A15 and a receptionist alert, not an automatic cancellation.)*

**B4 `appointment_cancelled`** (utility)
Hi {{1}}, the appointment on {{2}} at {{3}} has been cancelled. To book a new time, reply to this message.
Your Friendly Doctor

**B5 `slot_available_waitlist`** (utility)
Hi {{1}}, a slot has opened at [Practice] on {{2}} at {{3}}. Would you like it?
Your Friendly Doctor
Buttons: Yes, book it / No thanks

**B6 `missed_appointment_followup`** (utility, risk of being treated as marketing)
Hi {{1}}, we missed you at [Practice] today at {{2}}. If you'd still like to be seen, reply here and we'll find you a new time.
Your Friendly Doctor
Keep this plain: no discounts, no promotions, no "we miss you" marketing tone.

**B7 `staff_will_call`** (utility), only if used for outbound patient messages
Hi {{1}}, our team at [Practice] will call you shortly about your appointment. If it's a bad time, reply here with a better time.
Your Friendly Doctor

## C. Internal alerts (to the receptionist, not patients)
Sent by email AND WhatsApp. Keep identifying details minimal.

**C1 Handoff / no response**
Subject: Action needed: call patient
Body: No reply from {{name}} ({{mobile}}) about {{type}} on {{date}} {{time}} after 5 minutes. Please phone them. Sheet row: {{row_link}}.

**C2 Urgent wording**
Subject: URGENT: patient message
Body: {{name}} ({{mobile}}) sent a message flagged urgent. Please call now. Message received at {{time}}.

**C3 Consent declined**
Subject: Patient declined messaging consent
Body: {{name}} ({{mobile}}) declined WhatsApp consent. Conversation moved to staff. No automated messages will be sent.

**B8 `medical_aid_update`** (utility), used only if the 24-hour chat window has closed
Hi {{1}}, an update on your booking at [Practice] for {{2}}: {{3}}. Please reply here if you have questions.
Your Friendly Doctor
*(Make fills {{3}} with a short fixed sentence, either "your medical aid cover is confirmed" or "we could not confirm medical aid funds, so this will be a cash booking". No amounts or balances.)*

**C4 Medical aid check needed (to receptionist)**
Subject: Medical aid check needed
Body: Please check cover for {{name}} ({{mobile}}), scheme {{scheme}}, booking {{date}} {{time}}, then set the result in row {{row_link}}. Do not reply to the patient about balances.

## Rules for submitting templates
1. Submit B1-B6 through the chosen provider; allow time for approval and for a resubmission if Meta recategorises or rejects one.
2. Don't put medical details, diagnoses or medical aid numbers in any template.
3. Test every template with fake patients before going live.
4. Only message patients whose Consent column is YES.
5. Log each template version used, so changes are traceable per practice.

## Decisions (owner)
1. Patients reply with **buttons**; typed replies are the fallback.
2. The 2-hour reminder goes to **all** booked patients, confirmed or not.
3. Sign-off: **"Your Friendly Doctor"**.
4. **24 hours' notice** to cancel by WhatsApp, or the patient calls the practice.
5. Booking conversation asks **self or someone else**; if someone else: name, surname and age.

6. Medical aid bookings: ask for scheme name and membership number (and main member for dependants); confirm funds before booking; if funds are exhausted, tell the patient it will be a cash booking and let them confirm.

## Still open
- Cancel inside 24 hours: the draft only alerts staff and tells the patient to call, without freeing the slot. Confirm that's the intent, and whether a late-cancel or no-show fee applies.
- Should reminders go to the person who booked, the patient, or both (relevant for children)?

## Iterations log
- v0.1: first draft.
- v0.2: buttons, 2h reminder for all, sign-off, 24h cancellation rule, self/someone-else flow.
- v0.3: medical aid pre-check messages (A4b, A4c, A17-A20, B8, C4).
