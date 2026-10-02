"""
Cold Chain Logistics - AI Assistant
File: db/seed_data.py

Kaam:
  Database mein test ke liye fake data daalta hai:
    - 3 Shipments (alag alag cargo aur temp limits ke saath)
    - Har shipment ki kuch Telemetry readings (GPS + temperature)
      jisme ek shipment jaan-boojh kar apni limit CROSS karti hai
      (taaki hum "breach detect" karna test kar sakein)

Run karne ke liye:
  python db/seed_data.py
"""

from datetime import datetime, timedelta
from connection import get_connection   # connection.py wali file se


def seed():
    conn = get_connection()
    cursor = conn.cursor()

    print("Purana test data saaf kar rahe hain (agar hai to)...")
    # Pehle Telemetry delete karo (foreign key hai, isliye pehle child table)
    cursor.execute("DELETE FROM Telemetry WHERE ShipmentID IN ('A42', 'B17', 'C09')")
    cursor.execute("DELETE FROM Shipments WHERE ShipmentID IN ('A42', 'B17', 'C09')")
    conn.commit()

    # --------------------------------------------------------
    # 1. Shipments daalo
    # --------------------------------------------------------
    print("Shipments daal rahe hain...")
    shipments = [
        # ShipmentID, TruckID, Origin, Destination, CargoType, MinTemp, MaxTemp, Status
        ("A42", "TRK-101", "Los Angeles", "Long Beach", "Frozen Vaccines", -22.0, -18.0, "in_transit"),
        ("B17", "TRK-205", "San Diego", "Los Angeles", "Fresh Seafood", 0.0, 4.0, "in_transit"),
        ("C09", "TRK-310", "Fresno", "Sacramento", "Dairy Products", 2.0, 6.0, "in_transit"),
    ]

    insert_shipment = """
        INSERT INTO Shipments
            (ShipmentID, TruckID, OriginCity, DestinationCity, CargoType, MinTempC, MaxTempC, Status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_shipment, shipments)
    conn.commit()
    print(f"  -> {len(shipments)} shipments daal di.")

    # --------------------------------------------------------
    # 2. Telemetry readings daalo
    # Har shipment ke liye 5 readings, 10-10 minute ke gap par
    # --------------------------------------------------------
    print("Telemetry readings daal rahe hain...")
    now = datetime.utcnow()

    telemetry_rows = []

    # --- Shipment A42: NORMAL rehti hai (-22 se -18 ke beech), koi breach nahi
    a42_temps = [-20.5, -20.3, -20.8, -19.9, -20.1]
    a42_coords = [(45.10, -122.40), (45.05, -122.35), (45.00, -122.30),
                  (44.95, -122.25), (44.90, -122.20)]
    for i, (temp, (lat, lon)) in enumerate(zip(a42_temps, a42_coords)):
        recorded_at = now - timedelta(minutes=(len(a42_temps) - i) * 10)
        telemetry_rows.append(("A42", lat, lon, temp, recorded_at))

    # --- Shipment B17: BREACH hoti hai! limit hai 0-4C, par last reading 7.2C
    b17_temps = [2.1, 2.5, 3.0, 5.8, 7.2]   # aakhri do readings limit todti hain
    b17_coords = [(32.71, -117.16), (32.80, -117.10), (32.90, -117.05),
                  (33.00, -117.00), (33.10, -116.95)]
    for i, (temp, (lat, lon)) in enumerate(zip(b17_temps, b17_coords)):
        recorded_at = now - timedelta(minutes=(len(b17_temps) - i) * 10)
        telemetry_rows.append(("B17", lat, lon, temp, recorded_at))

    # --- Shipment C09: NORMAL rehti hai (2 se 6 ke beech)
    c09_temps = [3.5, 3.8, 4.0, 3.9, 3.6]
    c09_coords = [(36.75, -119.77), (36.85, -119.80), (36.95, -119.85),
                  (37.05, -119.90), (37.15, -119.95)]
    for i, (temp, (lat, lon)) in enumerate(zip(c09_temps, c09_coords)):
        recorded_at = now - timedelta(minutes=(len(c09_temps) - i) * 10)
        telemetry_rows.append(("C09", lat, lon, temp, recorded_at))

    insert_telemetry = """
        INSERT INTO Telemetry (ShipmentID, Latitude, Longitude, TempC, RecordedAt)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_telemetry, telemetry_rows)
    conn.commit()
    print(f"  -> {len(telemetry_rows)} telemetry readings daal di.")

    # --------------------------------------------------------
    # 3. Confirm karo
    # --------------------------------------------------------
    cursor.execute("SELECT ShipmentID, CargoType, MinTempC, MaxTempC FROM Shipments")
    print("\nShipments ab database mein:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} (limit: {row[2]}C to {row[3]}C)")

    print("\nNote: Shipment B17 ki aakhri readings (5.8C, 7.2C) uski limit")
    print("(0C-4C) se zyada hain - yeh jaan-boojh kar ek 'breach' scenario hai,")
    print("taaki aage hum agent ka alert/warning logic test kar sakein.")

    cursor.close()
    conn.close()
    print("\nDone! Seed data daal diya gaya.")


if __name__ == "__main__":
    seed()