# digantara-pdn-load-transient-test
Python automation script for PDN load transient testing using SCPI/PyVISA - Digantara assessment
# Digantara PDN Load Transient Test

## What This Script Does

I developed this script to automate load transient testing 
of a satellite Power Distribution Network (PDN).

The PDN takes +5V input and generates four output rails:
- +3V6 at 2.5A max
- +1V8 at 3.0A max  
- +3V3 at 3.0A max
- +2V5 at 1.5A max

The script applies a load step from 50% to 100% of rated 
current on each rail, takes 10 captures, and checks if the 
rail recovers within specification.

---

## Instruments Used

| Instrument | Model | Purpose |
|---|---|---|
| DC Power Supply | Keithley 2230-30-1 | Provides 5V input to PDN |
| Electronic Load | Keithley 2380 Series | Applies load steps |
| Oscilloscope | Keysight DSOX6004A | Captures waveforms |
| Digital Multimeter | Keithley DMM6500 | Measures DC voltage |

---

## Acceptance Criteria

| Parameter | Limit |
|---|---|
| DC Voltage | Within ±5% of nominal |
| Output Ripple | Less than 50 mV p-p |
| Recovery Time | Less than 1.0 ms |

---

## How to Run

No instrument connection needed to run in simulation mode.

Step 1 - Save the file
Save pdn_clean.py to your local folder

Step 2 - Run
python pdn_clean.py

Step 3 - Output
Script will print results rail by rail in terminal.
Two files get auto-saved in same folder:
- PDN_Test_Log_TIMESTAMP.csv
- PDN_Test_Report_TIMESTAMP.txt

---

## Test Output I Got

When I ran this locally I got:

Rail +3V6 — 10/10 PASS
- All captures within spec
- Max Ripple: 43.61 mV
- All recovery times under 1ms

Rail +1V8 — 10/10 PASS  
- All captures within spec
- Max Ripple: 43.61 mV

Rail +3V3 — 6/10 PASS, 4/10 FAIL
- Intermittent failures observed
- Max Ripple: 69.91 mV (above 50mV spec)
- This matches the SN-017 failure scenario in the assessment
- Fails are intermittent not consistent — points to marginal ESR issue

Rail +2V5 — 10/10 PASS
- All captures within spec
- Max Ripple: 44.72 mV

Overall Board Result: FAIL (due to +3V3 rail)

---

## What the Script Checks Per Capture

For each capture the script checks 3 things:

1. Is DC voltage within ±5% of nominal?
2. Is ripple below 50mV p-p?
3. Did the rail recover within 1ms after load step?

If all 3 pass — capture is PASS
If any one fails — capture is FAIL

---

## CSV Output Format

Each capture gets logged to CSV with these columns:
- timestamp
- rail name
- capture number
- measured voltage
- ripple in mV
- recovery time in ms
- pass or fail result

---

## Note on Simulation Mode

SIMULATION_MODE = True is set at the top of the script.

This means the script runs without needing physical instruments.
When running on actual bench, set SIMULATION_MODE = False
and update VISA addresses to match your instrument connections.

---

## Files in This Repo

| File | Description |
|---|---|
| pdn_clean.py | Main test script |
| README.md | This documentation |
