## copy and paste script for example here: https://www.online-python.com/
## and you can test it online

import datetime

MAX_TX_DELAY = 29

def calculate_delay(payload_bytes):
    """
    Replicates the C algorithm:
    1. XOR all payload bytes together.
    2. Take result modulo (MAX_TX_DELAY + 1).
    """
    payload_hash = 0
    for b in payload_bytes:
        payload_hash ^= b
    return payload_hash % (MAX_TX_DELAY + 1)

def compute_formation_time(arrival_time, payload_hex):
    """
    Given an arrival datetime and the payload as a hex string,
    returns the estimated datetime when the payload was formed.
    """
    payload_bytes = bytes.fromhex(payload_hex)
    delay_sec = calculate_delay(payload_bytes)
    return arrival_time - datetime.timedelta(seconds=delay_sec), delay_sec

if __name__ == "__main__":
    # Example usage:
    payload_hex = "03419471FEE7D8D40000000000000002"
    arrival_str = "2025-06-08 12:00:00"
    arrival_time = datetime.datetime.strptime(arrival_str, "%Y-%m-%d %H:%M:%S")

    formation_time, delay_seconds = compute_formation_time(arrival_time, payload_hex)
    print(f"Computed delay: {delay_seconds} seconds")
    print(f"Estimated payload formation time: {formation_time}")
