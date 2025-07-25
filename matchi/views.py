from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import calendar
from datetime import datetime
from matchi.slot_management import create_slot_rules, create_slots
import json
from matchi.templates.matchi.models import SlotRule, Slot
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def index(request):
    return HttpResponse("Hello, world. You're at the matchi index. Go to calendar.")

def view_calendar(request):
    print("start of the function view_calendar")

    # Slot.objects.all().delete()
    # SlotRule.objects.all().delete()

    # slot_rules = create_slot_rules()
    # slots = create_slots(slot_rules=slot_rules)

    slots = Slot.objects.all()
    slot_rules = SlotRule.objects.all()

    now = datetime.now()
    year = now.year
    month = now.month

    # Create a calendar
    cal = calendar.HTMLCalendar()
    html_calendar = cal.formatmonth(year, month)

    # Convert slots to FullCalendar event format
    events = []
    for slot in slots:
        event = {
            'title': (
                f'Booked: {slot.sport} - {slot.location} - {slot.start_datetime.strftime("%H:%M")} - {slot.end_datetime.strftime("%H:%M")}'
                if slot.is_booked
                else f'Not Booked: {slot.sport} - {slot.start_datetime.strftime("%H:%M")} - {slot.end_datetime.strftime("%H:%M")}'
            ),
            'start': slot.start_datetime.isoformat(),
            'end': slot.end_datetime.isoformat(),
            'allDay': False,
            'is_booked': slot.is_booked,
            'location': slot.location,
            'field_info': f'{slot.location} - {slot.sport}'
        }
        events.append(event)

    # Render the calendar template with events data
    return render(request, 'matchi/calendar.html', {'events': json.dumps(events), 'slot_rules': slot_rules})

@csrf_exempt  # Use this only for development; consider using CSRF tokens in production
def create_slot_rule(request):
    if request.method == 'POST':
        week_days = request.POST.get('week_days')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        sport = request.POST.get('sport')

        new_rule = SlotRule.objects.create(
            week_days=week_days,
            start_time=start_time,
            end_time=end_time,
            sport=sport
        )

        return JsonResponse({'id': new_rule.id, 'message': 'Slot rule created successfully!'}, status=201)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def delete_slot_rule(request, slot_rule_id):
    if request.method == 'DELETE':
        related_slots = Slot.objects.filter(slot_rule=slot_rule_id)
        booked_related_slots = related_slots.filter(is_booked=True)
        if booked_related_slots.exists():
            return JsonResponse({'error': 'Cannot delete a slot rule when there are booked slots related to it.'}, status=400)
        related_slots.delete()
        slot_rule = SlotRule.objects.get(id=slot_rule_id)
        slot_rule.delete()
        return JsonResponse({'message': 'Slot rule deleted successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
