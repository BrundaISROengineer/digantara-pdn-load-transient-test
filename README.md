# digantara-pdn-load-transient-test
Python automation script for PDN load transient testing using SCPI/PyVISA - Digantara assessment

# Digantara PDN Load Transient Test

## Overview

I wrote this script to automate PDN load transient testing for the
given assessment.

I tested all four rails:
- +3V6
- +1V8
- +3V3
- +2V5

The script simulates load transient captures, checks measurements
against acceptance limits, and automatically generates CSV and
report files.

---

## Instruments Considered

| Instrument | Model |
|---|---|
| DC Power Supply | Keithley 2230-30-1 |
| Electronic Load | Keithley 2380 |
| Oscilloscope | Keysight DSOX6004A |
| Multimeter | Keithley DMM6500 |

---

## What I Implemented

For each rail I:
- Applied 50% to 100% load step
- Took 10 captures
- Checked voltage regulation
- Checked ripple
- Checked recovery time
- Logged PASS/FAIL automatically

At the end the script:
- Prints rail summary
- Saves CSV log
- Saves final text report

---

## Acceptance Limits Used

| Parameter | Limit |
|---|---|
| Voltage | ±5% of nominal |
| Ripple | < 50 mV p-p |
| Recovery Time | < 1 ms |

---

## How I Ran It


python pdn_clean.py


Simulation mode is enabled inside the script so no hardware
connection is needed to execute it.

---

## Results I Observed

**+3V6 Rail**
- Pass: 10/10
- Avg Ripple: 31.51 mV
- Max Ripple: 38.56 mV
- Status: PASS

**+1V8 Rail**
- Pass: 10/10
- Avg Ripple: 34.62 mV
- Max Ripple: 43.61 mV
- Status: PASS

**+3V3 Rail**
- Pass: 6/10
- Fail: 4/10
- Avg Ripple: 44.5 mV
- Max Ripple: 69.91 mV
- Status: FAIL

Captures that failed:
- Cap 1 — Ripple 69.91 mV, Recovery 1.294 ms
- Cap 3 — Ripple 68.95 mV, Recovery 1.833 ms
- Cap 5 — Ripple 55.89 mV, Recovery 1.672 ms
- Cap 6 — Ripple 69.75 mV, Recovery 1.359 ms

**+2V5 Rail**
- Pass: 10/10
- Avg Ripple: 34.63 mV
- Max Ripple: 44.72 mV
- Status: PASS

**Overall Board Result: FAIL**

---

## My Analysis

The failures were only on +3V3 rail. All other three rails
passed all 10 captures cleanly.

During the failing captures the DC voltage was still within
tolerance. Only ripple and recovery time crossed the limit.

This tells me the converter is regulating fine under steady
state but struggling when load suddenly steps from 1.5A to 3.0A.

The failure pattern is intermittent not consistent. That rules
out a hard component failure. Something is marginal.

My assessment is the output capacitor ESR on the 3V3 stage is
borderline. As the board warms up across repeated captures the
ESR increases slightly and that degrades the transient response
enough to push ripple above 50mV.

To confirm this I would add a 47uF low ESR ceramic cap directly
across the 3V3 output terminals and rerun the test. If failures
drop to zero that confirms the ESR root cause.

---

## Files Included

| File | Purpose |
|---|---|
| pdn_clean.py | Main automation script |
| README.md | This documentation |
| output | complete output details |

---

## Notes

- Script runs in simulation mode by default
- Set SIMULATION_MODE = False for real bench use
- Update VISA addresses to match your instrument connections
- PyVISA library needed only for actual hardware run

## SCREENSHOTS
The following screenshots show the actual execution, generated output, and project structure used during PDN transient test automation.
  
<img width="1706" height="795" alt="image" src="https://github.com/user-attachments/assets/1cd68e87-1b21-4d70-8949-f49baa234288" />

<img width="1500" height="759" alt="image" src="https://github.com/user-attachments/assets/9855903f-9337-4a15-ab1c-90f4d9d77c27" />

<img width="1558" height="784" alt="image" src="https://github.com/user-attachments/assets/f16bf8de-ea8e-4330-bfe7-8efe5b7d1959" />

<img width="1707" height="813" alt="image" src="https://github.com/user-attachments/assets/cb910e97-a0c1-48e6-99f7-8173dda72e0f" />

<img width="1794" height="770" alt="image" src="https://github.com/user-attachments/assets/efedb43a-1849-4b71-a48c-9f856091a8bb" />

- 
<img width="1705" height="658" alt="image" src="https://github.com/user-attachments/assets/56a2c6e0-fd99-4cff-972b-8e884941fa30" />




