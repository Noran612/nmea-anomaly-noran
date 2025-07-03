from nmeaParser import parse_line
from ruleEngine import detect_anomalies

def read_nmea_file(filepath):
    parsed_data = []
    with open(filepath, 'r') as f:
        for line in f:
            result = parse_line(line)
            if result:
                parsed_data.append(result)
    print(f"Parsed {len(parsed_data)} NMEA sentences")  # Moved outside loop
    return parsed_data

def main():
    parsed_data = read_nmea_file('nmea_output.txt')
    anomalies = detect_anomalies(parsed_data)

    for ts, msg in anomalies:
        print(f"[{ts}] Anomaly detected: {msg}")

    with open('anomalies.log', 'w') as log:
        for ts, msg in anomalies:
            log.write(f"[{ts}] {msg}\n")

if __name__ == '__main__':
    main()
