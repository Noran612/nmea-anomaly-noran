def parse_lat_lon(lat, lat_dir, lon, lon_dir):
    try:
        lat = float(lat[:2]) + float(lat[2:]) / 60
        if lat_dir == 'S':
            lat = -lat
        lon = float(lon[:3]) + float(lon[3:]) / 60
        if lon_dir == 'W':
            lon = -lon
        return lat, lon
    except:
        return None, None

def parse_rmc(parts):
    lat, lon = parse_lat_lon(parts[3], parts[4], parts[5], parts[6])
    return {
        'timestamp': parts[1],
        'valid_fix': parts[2] == 'A',
        'lat': lat,
        'lon': lon,
        'speed': float(parts[7]) if parts[7] else 0.0,
        'heading': float(parts[8]) if parts[8] else None
    }

def parse_gga(parts):
    lat, lon = parse_lat_lon(parts[2], parts[3], parts[4], parts[5])
    try:
        fix_quality = int(parts[6]) if parts[6] else 0
    except:
        fix_quality = 0
    try:
        num_sats = int(parts[7]) if parts[7] else 0
    except:
        num_sats = 0

    return {
        'timestamp': parts[1],
        'lat': lat,
        'lon': lon,
        'fix_quality': fix_quality,
        'num_sats': num_sats
    }

def parse_vtg(parts):
    return {
        'heading': float(parts[1]) if parts[1] else None,
        'speed': float(parts[5]) if parts[5] else 0.0
    }

def parse_hdt(parts):
    return {
        'heading': float(parts[1]) if parts[1] else None
    }

def parse_line(line):
    if ',' not in line:
        return None

    parts = line.strip().split(',')
    if len(parts) < 3:
        return None

    timestamp = parts[0]
    sentence_type = parts[1]
    sentence = ','.join(parts[2:]).strip()

    if not sentence.startswith('$'):
        return None

    fields = sentence.split(',')

    if sentence.startswith('$GNRMC'):
        return {'type': 'GNRMC', 'timestamp': timestamp, **parse_rmc(fields)}
    elif sentence.startswith('$GPGGA'):
        return {'type': 'GPGGA', 'timestamp': timestamp, **parse_gga(fields)}
    elif sentence.startswith('$GNVTG') or sentence.startswith('$GPVTG'):
        return {'type': 'VTG', 'timestamp': timestamp, **parse_vtg(fields)}
    elif sentence.startswith('$HEHDT'):
        return {'type': 'HEHDT', 'timestamp': timestamp, **parse_hdt(fields)}

    return None
