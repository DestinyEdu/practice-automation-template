# Test cases (fake data only)
1. New patient books a check-up in one go.
2. Returning patient with a vague "need to see the doctor sometime next week".
3. Patient writes "my face is swollen" (must hand off, not book).
4. Patient picks a slot that has just been taken.
5. Patient declines consent (moves to staff, no automated messages).
6. Patient disappears mid-flow (5-minute rule alert).
7. Medical aid patient, funds available (booking confirmed).
8. Funds exhausted (patient told it becomes a cash booking and confirms).
9. Member not valid or number mistyped.
10. Staff don't update the sheet in time (second alert).
11. Cancel with more than 24 hours' notice (slot freed). Cancel inside 24 hours (staff alert, patient told to call).
12. Booking for someone else: name, surname, age captured; calendar uses patient's name.
