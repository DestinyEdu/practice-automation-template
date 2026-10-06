# 01 Booking Intake

**Goal:** a patient WhatsApps the practice and ends up with a confirmed slot (calendar event + sheet row), without the receptionist typing anything.
**Scope v1:** WhatsApp text messages only. Web form and phone calls come later.
**Status:** DRAFT v0.4, medical aid pre-check added. Anything in [brackets] is a placeholder the practice sets.

## 1. Trigger and stack
- **Trigger:** incoming WhatsApp message (webhook from the chosen provider into Make).
- **Make modules (outline, verify when building):** webhook trigger, Sheets "Conversations" lookup, AI step (Claude) for understanding, Calendar free/busy check, Sheets write, WhatsApp send.
- **State:** Make doesn't remember a conversation between messages, so keep a `Conversations` tab: phone, stage, collected fields so far, last message time. Every incoming message loads this row first.

## 2. Conversation flow
| Stage | System does | Example message |
|---|---|---|
| Greeting | Ask what they need; check if number already in the sheet | "Hi, thanks for contacting [Practice]. Are you looking to book an appointment?" |
| Consent (new patients) | Ask once, record yes/no | "To send reminders on WhatsApp we need your OK. Reply YES to agree." |
| Details (new patients) | Ask only for missing fields, one or two at a time | "What's your full name? And is this booking for medical aid or cash?" |
| Who is it for? | Ask: self or someone else. If someone else, ask the patient's full name and surname, and age | "Is this booking for yourself or someone else?" (buttons) then "Please send the patient's full name and surname, and their age." |
| Medical aid pre-check | If medical aid: collect scheme name and member number, hold the slot as pending, alert staff to run the benefit check, then continue or switch to cash (see section 5b) | "Thanks. We're confirming your medical aid cover for this visit and will come back to you shortly." |
| Type + preference | Map request to an appointment type, take day/time preference | "Is this a check-up or something specific? Which days suit you?" |
| Offer slots | Offer 2-3 free slots | "I have: 1) Thu 14:00 2) Fri 09:30 3) Fri 11:00. Reply with the number." |
| Book | Create calendar event, write row, send confirmation | "Booked: Thu 14:00 with [Practitioner] at [address]. Reply 3 anytime to cancel." |

Returning patients skip consent and details, but the system confirms the email on file ("Is [email] still the best address for you?"). If it's different, ask the patient's consent to update it before changing the record. Email is requested at first booking only. Keep messages short. v1 is English only.

## 3. What Claude extracts (per message)
```
intent: book | reschedule | cancel | question | other
appointment_type: [see presets]
preferred_day / preferred_time_window
full_name, email, payment_type (medical_aid | cash), medical_aid_name
medical_aid_number (only when payment_type = medical_aid)
booked_for: self | other
patient_full_name, patient_age (if booked_for = other)
consent: yes | no | unknown
urgent: true | false (+ reason)
confidence: high | low
```
Rules: ask for missing fields instead of guessing. If confidence is low twice in a row, hand off to a human.

## 4. Appointment presets (placeholders for the practice to confirm)
| GP | Slot | Dentist | Slot |
|---|---|---|---|
| Consultation | [15-20 min] | Check-up & clean | [45 min] |
| Follow-up | [15 min] | Filling | [45-60 min] |
| Repeat prescription review | [10-15 min] | Extraction | [45 min] |
| Vaccination | [10 min] | Dental emergency (toothache) | [30 min, same-day if possible] |

## 5. Urgent wording and handoff (human decides, not Claude)
- **Triggers (examples, practice to finalise):** GP: chest pain, can't breathe, severe bleeding, fainting, suspected stroke. Dentist: swelling of face or neck, uncontrolled bleeding, knocked-out tooth, severe pain.
- **Action:** do NOT offer a slot as normal. Send a short safe message, and alert the receptionist by email + WhatsApp straight away.
- **Safe message (practice to approve):** "This sounds urgent. If it's an emergency, please call 112 or 10177 now. We're alerting our team and will call you." Practice confirms the numbers it wants quoted.
- **Other handoff triggers:** patient asks for a person, complaint or billing dispute, low confidence twice, no reply after 5 minutes during a booking (per the agreed 5-minute rule).
- Claude gives no clinical advice, ever.

## 5b. Medical aid pre-check (new)
**Rule (owner):** for medical aid bookings, confirm funds with the medical aid BEFORE confirming the booking. Funds available: continue and confirm. Funds exhausted: tell the patient the booking will be a cash booking.

**v1 approach (semi-automated):** I found no public, general-purpose way for a Make scenario to query medical aids directly. Practices normally run benefit checks from their own practice software (for example GoodX offers a validation yes/no, a dependant check and a benefit check for a stated amount, and limits benefit checks to three per main member per day). So in v1 the system does the chat and the staff do the check:
1. Patient gives scheme name and member number (and main member name and dependant details if the patient is a dependant).
2. Sheet row set to `pending_medical_aid_check`; the calendar slot is held provisionally.
3. Receptionist gets an alert (email + WhatsApp, no member number in the message) and runs the benefit check in the practice software.
4. Receptionist sets `medical_aid_check` in the sheet: **funds available / funds exhausted / not valid**.
5. Make notices the change and continues:
   - **Funds available:** confirm the booking (A9 or template B1).
   - **Funds exhausted or not valid:** send A18, set payment type to cash, and ask the patient to confirm (buttons).
6. If staff haven't updated the sheet within [30 minutes in office hours], alert again.

**v2 (later):** automate the check if the practice's software or claims switch offers an integration. Don't promise this to clients until it's tested.

**Privacy rules:** the medical aid number lives only in the sheet, with restricted access. Never repeat it in WhatsApp messages or alerts, never put it in calendar events, and tell the patient only that we couldn't confirm cover for this visit, not their balances.

## 6. Writes
- **Sheet row (Appointments tab):** full name, mobile, email, appointment type, date/time, status = booked, consent, payment type, medical aid name, medical aid number, medical_aid_check (pending / funds available / funds exhausted / not valid / not needed), booked_for (self/other), patient full name and age (when booking for someone else). The mobile is the booker's number, and reminders go to it.
- **Calendar event:** title "[Type] - [Name]", practitioner calendar, no clinical notes in the event.
- **Double-booking guard:** create the event, then re-check the slot is still the only booking; if not, apologise and offer new slots.

## 7. Edge cases to handle
- Medical aid check pending when the patient stops replying: slot is released after [1 hour], patient told.
- Patient is a dependant: ask for the main member's name and dependant details; practice decides what its software needs.
- Patient changes to cash while pending: skip the check and confirm.
- Patient messages from a different number than the one on file.
- Booking for someone else (child, parent): ask for the patient's name, surname and age, keep the booker's number. Calendar event uses the patient's name.
- Slot taken while the patient was replying.
- Patient replies with something unrelated mid-flow (answer or hand off, then resume).
- Messages outside practice hours (still book, but no promises about phone calls).
- Voice notes or images: reply asking for text, and flag for the receptionist.
- Public holidays and practitioner leave (block these in the calendar).
- Patient replies in a language other than English: reply once in English, then hand off to staff.

## 8. Test cases (use fake data only)
1. New patient books a check-up in one go.
2. Returning patient with a vague "need to see the doctor sometime next week".
3. Patient writes "my face is swollen" (must hand off, not book).
4. Patient picks a slot that has just been taken.
5. Patient declines consent: system tells them the conversation will move to practice staff from here on, flags the receptionist, and sends no further automated messages.
6. Patient disappears mid-flow (5-minute rule triggers alert).

7. Medical aid pre-check: patient on medical aid, funds available (booking confirmed).
8. Funds exhausted (patient told it becomes a cash booking, confirms).
9. Member not valid or number mistyped.
10. Staff don't update the sheet in time (second alert fires).

## 9. Human vs Claude in this step
- **Claude:** parse messages, fill missing fields, check availability, write rows, draft replies.
- **Staff (v1):** run the medical aid benefit check and record the result.
- **Owner/practice:** appointment types and lengths, urgent-word list and safe message, tone and language, consent wording, what happens without consent.

## 10. Decisions (owner)
1. **Email:** requested at first booking only. For returning patients, confirm the email on file; if it differs, get consent before updating.
2. **Consent declined:** tell the patient the interaction moves to staff from there on; alert the receptionist; no further automated messages (no booking, no reminders).
3. **Language:** English only in v1.
4. **Calendar:** a single calendar per practice.

5. **Booking for self or someone else:** always asked. If someone else, collect the patient's name, surname and age.
6. **Cancellation notice:** 24 hours by WhatsApp, otherwise the patient calls the practice (see Message Templates A15).

7. **Medical aid:** collect scheme name and number; pre-confirm funds before booking; if exhausted, advise it becomes a cash booking.

## 10b. Still open
- Funds exhausted: the draft asks the patient to confirm the cash booking (buttons) rather than assuming it. Confirm that's acceptable.
- How long to hold a pending slot, and what the practice charges for cash visits (maybe quoted in the message).
- Consent for a child or other person: the booker consents on their behalf. Practice should confirm wording with a POPIA-knowledgeable adviser, since health information about children has extra protection.
- Medical aid details when the patient is a dependant (main member name?). Decide what the practice needs.
- Appointment types and slot lengths need confirming by a real GP and dentist.
- Urgent-word list and safe message need approval by each practice.
- Should consent be re-asked periodically, or is once enough?

## Iterations log
- v0.1: first draft from interview and research.
- v0.2: owner decisions on email, declined consent, language and calendar added.
- v0.3: added 'self or someone else' step, extra sheet fields and the 24-hour cancellation rule.
- v0.4: medical aid number, pre-check flow, new sheet fields.
