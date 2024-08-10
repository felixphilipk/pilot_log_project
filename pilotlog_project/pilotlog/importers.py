import logging
import subprocess
from django.utils.dateparse import parse_datetime
from django.db import transaction
from .models import PilotLog
from .utils import transform_data

logger = logging.getLogger(__name__)

def lint_json_file(file_path):
    try:
        subprocess.run(['python', '-m', 'json.tool', file_path, file_path + ".linted"], check=True)
        return True, file_path + ".linted"
    except subprocess.CalledProcessError:
        logger.error(f"JSON linting failed for file: {file_path}")
        return False, None

def import_pilotlog_data(file_path):
    # Lint the JSON file before processing
    is_valid_json, linted_file_path = lint_json_file(file_path)
    if not is_valid_json:
        logger.error(f"File {file_path} is not valid JSON. Aborting import.")
        return
    
    try:
        # Transform data using Spark
        transformed_data = transform_data(linted_file_path)

        # Import transformed data into Django models
        with transaction.atomic():
            for item in transformed_data:
                try:
                    guid = item.get('guid')
                    if not guid:
                        logger.error("Missing 'guid' in item, skipping this record.")
                        continue

                    # Map the flattened fields to the Django model fields
                    record_modified_str = item.get('record_modified')
                    record_modified = parse_datetime(record_modified_str) if record_modified_str else None

                    PilotLog.objects.update_or_create(
                        guid=guid,
                        defaults={
                            'fin': item.get('Fin', ''),
                            'sea': item.get('Sea', False),
                            'tmg': item.get('TMG', False),
                            'efis': item.get('Efis', False),
                            'fnpt': item.get('FNPT', 0),
                            'make': item.get('Make', ''),
                            'run2': item.get('Run2', False),
                            'class_category': item.get('Class', 0),
                            'model': item.get('Model', ''),
                            'power': item.get('Power', 0),
                            'seats': item.get('Seats', 0),
                            'active': item.get('Active', False),
                            'kg5700': item.get('Kg5700', False),
                            'rating': item.get('Rating', ''),
                            'company': item.get('Company', ''),
                            'complex': item.get('Complex', False),
                            'cond_log': item.get('CondLog', 0),
                            'fav_list': item.get('FavList', False),
                            'category': item.get('Category', 0),
                            'high_perf': item.get('HighPerf', False),
                            'sub_model': item.get('SubModel', ''),
                            'aerobatic': item.get('Aerobatic', False),
                            'ref_search': item.get('RefSearch', ''),
                            'reference': item.get('Reference', ''),
                            'tailwheel': item.get('Tailwheel', False),
                            'default_app': item.get('DefaultApp', 0),
                            'default_log': item.get('DefaultLog', 0),
                            'default_ops': item.get('DefaultOps', 0),
                            'device_code': item.get('DeviceCode', 0),
                            'aircraft_code': item.get('AircraftCode', ''),
                            'default_launch': item.get('DefaultLaunch', 0),
                            'record_modified': record_modified,
                            'platform': item.get('platform', 0),
                            'modified': item.get('modified', 0)
                        }
                    )
                except Exception as e:
                    logger.error(f"Error updating or creating PilotLog record: {e}")

    except Exception as e:
        logger.error(f"Unexpected error while importing pilot log data from {file_path}: {e}")
