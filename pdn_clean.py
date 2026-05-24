import csv
import time
import random
from datetime import datetime

SIMULATION_MODE = True

RAILS = {
    "+3V6": {"nominal_voltage": 3.6, "tolerance_percent": 5, "max_current": 2.5},
    "+1V8": {"nominal_voltage": 1.8, "tolerance_percent": 5, "max_current": 3.0},
    "+3V3": {"nominal_voltage": 3.3, "tolerance_percent": 5, "max_current": 3.0},
    "+2V5": {"nominal_voltage": 2.5, "tolerance_percent": 5, "max_current": 1.5},
}

MAX_RIPPLE_MV = 50
MAX_RECOVERY_MS = 1.0
NUM_CAPTURES = 10

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
CSV_FILE = "PDN_Test_Log_" + timestamp + ".csv"
REPORT_FILE = "PDN_Test_Report_" + timestamp + ".txt"


def simulate_voltage(nominal):
    variation = random.uniform(-1.5, 1.5)
    return round(nominal + (nominal * variation / 100), 4)


def simulate_ripple(rail_name):
    if rail_name == "+3V3":
        if random.random() < 0.3:
            return round(random.uniform(55, 80), 2)
    return round(random.uniform(20, 45), 2)


def simulate_recovery(ripple):
    rec = random.uniform(0.2, 0.8)
    if ripple > MAX_RIPPLE_MV:
        rec += random.uniform(0.5, 1.2)
    return round(rec, 3)


def run_test():
    print("=" * 50)
    print("DIGANTARA PDN LOAD TRANSIENT TEST")
    print("=" * 50)
    print("Start Time:", datetime.now())
    print("Mode: SIMULATION")
    print()

    all_results = []
    csv_rows = []

    for rail_name, cfg in RAILS.items():
        nominal = cfg["nominal_voltage"]
        tol = nominal * cfg["tolerance_percent"] / 100
        max_curr = cfg["max_current"]
        low_curr = round(max_curr * 0.5, 2)
        high_curr = round(max_curr * 1.0, 2)

        print("-" * 50)
        print("Rail:", rail_name)
        print("Nominal:", nominal, "V")
        print("Load Step:", low_curr, "A ->", high_curr, "A")
        print("-" * 50)

        rail_results = []

        for cap in range(1, NUM_CAPTURES + 1):
            meas_v = simulate_voltage(nominal)
            ripple = simulate_ripple(rail_name)
            recovery = simulate_recovery(ripple)

            v_pass = abs(meas_v - nominal) <= tol
            r_pass = ripple <= MAX_RIPPLE_MV
            rec_pass = recovery <= MAX_RECOVERY_MS
            result = "PASS" if (v_pass and r_pass and rec_pass) else "FAIL"

            print("Cap", cap, "| V =", meas_v, "V | Ripple =", ripple,
                  "mV | Recovery =", recovery, "ms | Result =", result)

            row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rail": rail_name,
                "capture": cap,
                "voltage_V": meas_v,
                "ripple_mV": ripple,
                "recovery_ms": recovery,
                "result": result,
            }
            rail_results.append(row)
            csv_rows.append(row)
            time.sleep(0.05)

        passes = sum(1 for r in rail_results if r["result"] == "PASS")
        print("Rail Summary:", passes, "/", NUM_CAPTURES, "PASS")
        print()
        all_results.append((rail_name, rail_results))

    save_csv(csv_rows)
    generate_report(all_results)


def save_csv(rows):
    fields = ["timestamp", "rail", "capture", "voltage_V", "ripple_mV", "recovery_ms", "result"]
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print("CSV saved:", CSV_FILE)


def generate_report(all_results):
    lines = []
    lines.append("=" * 50)
    lines.append("DIGANTARA PDN TEST REPORT")
    lines.append("Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("=" * 50)
    lines.append("")
    lines.append("Acceptance Criteria:")
    lines.append("  DC Voltage  : within +/-5% of nominal")
    lines.append("  Ripple      : < 50 mV p-p")
    lines.append("  Recovery    : < 1.0 ms")
    lines.append("")

    board_pass = True

    for rail_name, results in all_results:
        passes = sum(1 for r in results if r["result"] == "PASS")
        fails = NUM_CAPTURES - passes
        ripples = [r["ripple_mV"] for r in results]
        avg_ripple = round(sum(ripples) / len(ripples), 2)
        max_ripple = round(max(ripples), 2)
        status = "PASS" if fails == 0 else "FAIL"
        if fails > 0:
            board_pass = False
        lines.append("Rail: " + rail_name)
        lines.append("  Pass: " + str(passes) + "/" + str(NUM_CAPTURES))
        lines.append("  Fail: " + str(fails) + "/" + str(NUM_CAPTURES))
        lines.append("  Avg Ripple: " + str(avg_ripple) + " mV")
        lines.append("  Max Ripple: " + str(max_ripple) + " mV")
        lines.append("  Status: " + status)
        lines.append("")

    lines.append("-" * 50)
    lines.append("OVERALL BOARD RESULT: " + ("PASS" if board_pass else "FAIL"))
    lines.append("-" * 50)

    report = "\n".join(lines)
    print()
    print(report)

    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print("Report saved:", REPORT_FILE)


if __name__ == "__main__":
    run_test()
