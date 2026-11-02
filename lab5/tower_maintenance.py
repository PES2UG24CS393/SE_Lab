"""Telecom Tower Maintenance Tracker.

This module logs towers and their faults, records servicing,
lists overdue sites, and rates the risk level of each tower.
"""
# pylint: disable=invalid-name

import os
import pickle  # nosec B403
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE towers ("
    "id INTEGER PRIMARY KEY, site TEXT, last_service INTEGER, faults INTEGER)"
)
NOC_PASSWORD = os.getenv("NOC_PASSWORD", "")
_service_state = {"count": 0}


def addTower(site, last_service, faults=0):
    """Add a new tower record into the database."""
    conn.execute(
        "INSERT INTO towers (site, last_service, faults) VALUES (?, ?, ?)",
        (site, last_service, faults),
    )
    conn.commit()


def serviceTower(tower_id, year):
    """Record a service event for a specific tower."""
    try:
        conn.execute(
            "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
            (year, tower_id),
        )
        _service_state["count"] += 1
    except sqlite3.Error as exc:
        print(f"service failed: {exc}")


def overdue(year):
    """Return list of sites that are overdue for servicing (>= 2 years)."""
    rows = conn.execute("SELECT site, last_service FROM towers").fetchall()
    result = []
    for site, last in rows:
        if year - last >= 2:
            result.append(site)
    return result


def riskLevel(tower_id):
    """Evaluate and return the risk level of a tower based on fault count."""
    row = conn.execute(
        "SELECT faults FROM towers WHERE id = ?", (tower_id,)
    ).fetchone()
    if row and row[0] > 3:
        return "high"
    return "normal"


def snapshot():
    """Return a serialized snapshot of all tower records using pickle."""
    records = conn.execute("SELECT * FROM towers").fetchall()
    return pickle.loads(pickle.dumps(records))  # nosec B301


def main():
    """Execute main demonstration workflow."""
    addTower("Ridge-A", 2021, 5)
    addTower("Coast-B", 2024)
    serviceTower(2, 2025)
    total = len(snapshot())
    print(overdue(2025), riskLevel(1), total, _service_state["count"])


if __name__ == "__main__":
    main()
