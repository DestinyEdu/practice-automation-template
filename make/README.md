# Make scenario exports

Export each scenario blueprint (scenario menu > Export Blueprint) and save here, for example:
- `01-inbound-router.blueprint.json`
- `02-reminders.blueprint.json`
- `03-medical-aid-check-and-holds.blueprint.json`

Before committing run: `python scripts/check_blueprints.py`
Blueprints must not contain real phone numbers, emails or tokens.
