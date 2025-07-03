from math import radians, cos, sin, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    if None in (lat1, lon1, lat2, lon2):
        return 0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000  # in meters

def detect_anomalies(parsed_data):
    anomalies = []
    prev = None

    for entry in parsed_data:
        if not entry or 'lat' not in entry or 'lon' not in entry:
            continue

        if prev:
            # 1. Movement with zero speed
            dist = haversine(prev['lat'], prev['lon'], entry['lat'], entry['lon'])
            if entry.get('speed') == 0.0 and dist > 10:
                anomalies.append((entry['timestamp'], 'Moved with zero speed'))

            # 2. Heading spike
            if 'heading' in prev and 'heading' in entry:
                if prev['heading'] is not None and entry['heading'] is not None:
                    delta = abs(prev['heading'] - entry['heading'])
                    if delta > 45:
                        anomalies.append((entry['timestamp'], f'Heading spike: {delta:.1f}°'))

        # 3. Invalid fix or poor fix quality
        if entry.get('valid_fix') is False or entry.get('fix_quality') == 0:
            anomalies.append((entry['timestamp'], 'GPS fix lost'))

        prev = entry

    return anomalies
