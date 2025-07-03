# NMEA Anomaly Detection – Noran Muhammed

This project was developed as a solution to the NMEA anomaly detection home assignment. It parses real-world NMEA 0183 marine GPS data, extracts structured information, and detects anomalies using custom-defined rules.

---

## ✅ How I Solved It

### 1. Parsing NMEA Sentences

I built a custom parser in `nmeaParser.py` to read NMEA sentences line by line from the log file (`nmea_output.txt`). Each line consists of a timestamp, a sentence type (e.g., `GNRMC`, `GPGGA`), and a raw NMEA message.

The parser supports the following sentence types:

- `$GNRMC` — Recommended Minimum Navigation Information
- `$GPGGA` — GPS Fix Data
- `$GNVTG` / `$GPVTG` — Track Made Good and Speed Over Ground
- `$HEHDT` — Heading – True

From these, I extract:

- Latitude and Longitude
- Speed (in knots)
- Heading (in degrees)
- Fix quality
- Timestamp
- Validity of GPS fix

The parser handles malformed or missing fields gracefully to avoid crashes on real-world noisy data.

---

### 2. Detecting Anomalies

The rule engine, implemented in `ruleEngine.py`, iterates over all parsed sentences and applies a set of anomaly detection rules. Each rule reflects a potential real-world issue a vessel might encounter.

#### Anomaly Rules Implemented

1. **Movement with Zero Speed**

   - If the vessel's reported speed is 0 but the location has changed significantly (> 10 meters), it’s flagged as an anomaly.
   - This could indicate a faulty speed sensor or inconsistent GPS data.

2. **Heading Spikes**

   - If the heading changes abruptly by more than 45° between consecutive reports, it is flagged as an anomaly.
   - This might indicate a malfunctioning compass or a rapid maneuver not aligned with the vessel's behavior.

3. **GPS Fix Lost**
   - If the sentence indicates that the GPS fix is invalid (`A`/`V` flag or fix quality = 0), it is flagged.
   - This is crucial for detecting outages in navigation systems.

---

## 🛠️ Project Structure

mea-anomaly-noran/
├── nmea_output.txt # Input file with NMEA data
├── nmeaParser.py # Parses and structures NMEA sentences
├── ruleEngine.py # Applies anomaly detection rules
├── main.py # Orchestrates parsing and detection
├── anomalies.log # Output file listing all detected anomalies
└── README.md # This file

## ▶️ How to Run

1. Ensure `nmea_output.txt` is in the same folder.
2. Run the script:

```bash
python main.py
```
