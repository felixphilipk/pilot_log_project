import csv
from django.http import HttpResponse
from .models import PilotLog

def export_pilotlog_to_csv():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export-logbook.csv"'

    writer = csv.writer(response)

    # Write the header
    writer.writerow(['ForeFlight Logbook Import'])
    writer.writerow([])
    writer.writerow(["Aircraft Table"])
    writer.writerow([
        "AircraftID", "Fin", "Sea", "TMG", "Efis", "FNPT", "Make", "Run2", "Model", "Reference", "Active", 
        "Class", "Power", "Seats", "Kg5700", "Rating", "Company", "Complex", "CondLog", "FavList", 
        "Category", "HighPerf", "SubModel", "Aerobatic", "RefSearch", "Tailwheel", "DefaultApp", 
        "DefaultLog", "DefaultOps", "DeviceCode", "AircraftCode", "DefaultLaunch", "RecordModified"
    ])
    writer.writerow([])

    logs = PilotLog.objects.all()
    for aircraft in logs:
        writer.writerow([
            aircraft.guid, aircraft.fin, aircraft.sea, aircraft.tmg, aircraft.efis, aircraft.fnpt,
            aircraft.make, aircraft.run2, aircraft.model, aircraft.reference, aircraft.active, 
            aircraft.class_category, aircraft.power, aircraft.seats, aircraft.kg5700, 
            aircraft.rating, aircraft.company, aircraft.complex, aircraft.cond_log, 
            aircraft.fav_list, aircraft.category, aircraft.high_perf, aircraft.sub_model, 
            aircraft.aerobatic, aircraft.ref_search, aircraft.tailwheel, aircraft.default_app, 
            aircraft.default_log, aircraft.default_ops, aircraft.device_code, 
            aircraft.aircraft_code, aircraft.default_launch, 
            aircraft.record_modified.strftime('%Y-%m-%d %H:%M:%S') if aircraft.record_modified else ''
        ])

    return response
