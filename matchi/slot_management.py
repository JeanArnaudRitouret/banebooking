from datetime import date, datetime, time, timedelta
from matchi.templates.matchi.models import Slot, SlotRule, Sport

def create_slots(
        slot_rules: list[SlotRule],
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[Slot]:
    print("start of the function create_slots")
    if not start_date:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=(7 - datetime.now().weekday()))
    if not end_date:
        end_date = start_date + timedelta(days=6)

    existing_slots = Slot.objects.filter(
        start_datetime__date__range=(start_date, end_date),
        end_datetime__date__range=(start_date, end_date)
    )

    new_slots = []
    for slot_rule in slot_rules:
        new_slots.extend(get_new_slots_for_slot_rule(slot_rule, start_date, end_date, existing_slots))

    # Bulk create all new slots in one database operation if there are any
    if new_slots:
        Slot.objects.bulk_create(new_slots)

    return list(existing_slots) + new_slots


def get_new_slots_for_slot_rule(
        slot_rule: SlotRule,
        start_datetime: datetime,
        end_datetime: datetime,
        existing_slots: set[datetime] | None = None
    ) -> list[Slot]:
    new_slots = []
    existing_dates_for_sport: list[date] = [
        existing_slot.start_datetime.date()
        for existing_slot in existing_slots
        if existing_slot.sport == slot_rule.sport
    ]
    slot_rule_dates: list[date] = get_slot_rule_dates(slot_rule, start_datetime, end_datetime)

    for slot_rule_date in slot_rule_dates:
        if slot_rule_date not in existing_dates_for_sport:
            new_slot = Slot(
                start_datetime=datetime.combine(slot_rule_date, slot_rule.start_time),
                end_datetime=datetime.combine(slot_rule_date, slot_rule.end_time),
                sport=slot_rule.sport,
                is_booked=False,
                location="",
                slot_rule=slot_rule,
            )
            new_slots.append(new_slot)
    return new_slots


def get_slot_rule_dates(
        slot_rule: SlotRule,
        start_datetime: datetime,
        end_datetime: datetime
    ) -> list[date]:
    # Convert comma-separated weekday string to list of integers
    weekdays = [int(day) for day in slot_rule.week_days.split(',')]

    # Start from beginning of date range
    current_date: date = start_datetime.date()

    # Get dates that match weekdays in slot rule
    slot_rule_dates: list[date] = []
    while current_date <= end_datetime.date():
        if current_date.weekday() in weekdays:
            slot_rule_dates.append(current_date)
        current_date: date = current_date + timedelta(days=1)
    return slot_rule_dates


def create_slot_rules() -> list[SlotRule]:
    print("start of the function create_slot_rules")
    existing_slot_rules = SlotRule.objects.all()
    new_slot_rules = []
    if not existing_slot_rules:
        new_slot_rules = [
            SlotRule(
                week_days="1",
                start_time=time(16,0),
                end_time=time(18,0),
                sport=Sport.PADEL,
            ),
            SlotRule(
                week_days="0,1,2,3,4,5,6",
                start_time=time(16,0),
                end_time=time(18,0),
                sport=Sport.HIIT,
            ),
            SlotRule(
                week_days="4",
                start_time=time(16,0),
                end_time=time(18,0),
                sport=Sport.TENNIS,
            ),
            SlotRule(
                week_days="6",
                start_time=time(10,0),
                end_time=time(16,0),
                sport=Sport.SQUASH,
            ),
        ]
        SlotRule.objects.bulk_create(new_slot_rules)
    print(f"{existing_slot_rules=}")
    print(f"{new_slot_rules=}")
    return list(existing_slot_rules) + new_slot_rules

