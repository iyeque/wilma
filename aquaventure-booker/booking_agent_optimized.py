#!/usr/bin/env python3
"""
Aquaventure Waterpark Booking Agent - Optimized v3
Target: Sub-3-second reaction and checkout from 9:00:00.
"""

import time
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
import subprocess
import sys

LOG_DIR = Path("/home/iyeque/.openclaw/workspace/aquaventure-booker/aquaventure-memory")
LOG_DIR.mkdir(parents=True, exist_ok=True)
TODAY = datetime.now(timezone(timedelta(hours=4))).strftime("%Y-%m-%d")
LOG_FILE = LOG_DIR / f"{TODAY}.md"

def log_message(level, message):
    timestamp = datetime.now(timezone(timedelta(hours=4))).strftime("%H:%M:%S.%f")[:-3]
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

def append_summary(section, content):
    with open(LOG_FILE, "a") as f:
        f.write(f"\n### {section}\n{content}\n")

def call_openclaw(action, **kwargs):
    """Helper to call OpenClaw CLI tools."""
    cmd = ["openclaw", "browser", action]
    for k, v in kwargs.items():
        cmd.extend([f"--{k}", str(v)])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise RuntimeError(f"openclaw browser {action} failed: {result.stderr}")
        return result.stdout
    except Exception as e:
        log_message("ERROR", f"OpenClaw call failed: {e}")
        raise

BOOKING_INFO = {
    "name": "MAX MURAYA",
    "email": "mmmuraya@outlook.com",
    "phone": "+971581518024",
    "party_size": {"adults": 3, "child": 1},
    "preferred_date": "2026-03-21",
    "fallback_dates": ["2026-03-20", "2026-03-22"],
    "card": {
        "number": "4251996048727389",
        "exp": "08/28",
        "cvv": "484"
    }
}

URL = "https://booking.aquaventureworld.com/experiences/waterpark-day-passes"

class OptimizedBooker:
    def __init__(self):
        self.start_time = None
        self.success = False
        self.page_target_id = None
        self.poll_interval = 1.0  # Check every 1 second after 9:00

    def log_action(self, action, detail=""):
        log_message("INFO", f"{action} | {detail}" if detail else action)

    def open_page_early(self):
        """Open booking page BEFORE 9:00 to ensure it's loaded."""
        self.log_action("OPEN_PAGE_EARLY", URL)
        try:
            # Start/ensure browser is running
            call_openclaw("start")
            # Open the URL in the user profile (keeps cookies/session)
            output = call_openclaw("open", url=URL, profile="user")
            # Save target ID for later
            self.page_target_id = output.strip()
            self.log_action("PAGE_LOADED", f"target_id={self.page_target_id}")
            return True
        except Exception as e:
            self.log_action("OPEN_FAILED", str(e))
            return False

    def wait_until_launch(self):
        """Wait until exactly 9:00:00 UAE time."""
        now = datetime.now(timezone(timedelta(hours=4)))
        target = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now >= target:
            log_message("WARN", "Already past 9:00 AM, proceeding immediately")
            return
        sleep_seconds = (target - now).total_seconds()
        self.log_action("WAITING", f"{sleep_seconds:.1f}s until 9:00:00")
        time.sleep(sleep_seconds)

    def is_form_present(self):
        """Quickly check if booking form has appeared via DOM snapshot."""
        try:
            # Take a snapshot with aria refs for stable element identification
            output = call_openclaw("snapshot", targetId=self.page_target_id, refs="aria")
            # Parse the snapshot (JSON lines) to look for form elements
            for line in output.strip().split("\n"):
                if not line.strip():
                    continue
                snap = json.loads(line)
                # Look for date picker or quantity inputs or book button
                # This is a heuristic - adapt based on actual page structure
                if "book now" in snap.get("text", "").lower() or "add to cart" in snap.get("text", "").lower():
                    return True
                # Check for input fields that likely belong to the form
                if snap.get("role") in ("textbox", "button", "combobox") and "date" in snap.get("name", "").lower():
                    return True
            return False
        except Exception as e:
            self.log_action("FORM_CHECK_ERROR", str(e))
            return False

    def detect_form_by_dom(self):
        """Detect if the booking form is visible (not the high demand notice)."""
        # Use a more reliable check: look for 'Book Now' or 'Proceed' button
        try:
            output = call_openclaw("snapshot", targetId=self.page_target_id, refs="aria")
            texts = []
            for line in output.strip().split("\n"):
                if line.strip():
                    snap = json.loads(line)
                    texts.append(snap.get("text", "").lower())
            # Combine all visible text to check for key indicators
            all_text = " ".join(texts)
            if "book now" in all_text or "proceed to checkout" in all_text or "add to cart" in all_text:
                return True
            return False
        except Exception as e:
            self.log_action("DETECT_FORM_ERROR", str(e))
            return False

    def fill_and_submit(self):
        """Fill form and submit as fast as possible."""
        self.log_action("FILL_START")
        try:
            # 1. Select date - find date picker or directly input
            # Try to find an input for date and fill preferred date
            call_openclaw("fill", targetId=self.page_target_id, selector='input[type="date"]', value=BOOKING_INFO["preferred_date"])
            self.log_action("DATE_SELECTED", BOOKING_INFO["preferred_date"])
            time.sleep(0.1)

            # 2. Set quantity: adults and child
            # We'll try to find increment buttons or inputs
            # This is site-specific; we assume select elements or +/- buttons
            # For now, we'll attempt to set adult count
            call_openclaw("click", targetId=self.page_target_id, text="Adults")
            call_openclaw("fill", targetId=self.page_target_id, name="adults", value=str(BOOKING_INFO["party_size"]["adults"]))
            self.log_action("ADULTS_SET", str(BOOKING_INFO["party_size"]["adults"]))

            call_openclaw("click", targetId=self.page_target_id, text="Children")
            call_openclaw("fill", targetId=self.page_target_id, name="children", value=str(BOOKING_INFO["party_size"]["child"]))
            self.log_action("CHILDREN_SET", str(BOOKING_INFO["party_size"]["child"]))

            time.sleep(0.1)

            # 3. Enter name
            call_openclaw("fill", targetId=self.page_target_id, name="name", value=BOOKING_INFO["name"])
            self.log_action("NAME_ENTERED", BOOKING_INFO["name"])

            # 4. Enter email
            call_openclaw("fill", targetId=self.page_target_id, name="email", value=BOOKING_INFO["email"])
            self.log_action("EMAIL_ENTERED", BOOKING_INFO["email"])

            # 5. Enter phone
            call_openclaw("fill", targetId=self.page_target_id, name="phone", value=BOOKING_INFO["phone"])
            self.log_action("PHONE_ENTERED", BOOKING_INFO["phone"])

            # 6. Payment details - likely in an iframe; skip for now due to complexity
            # We'll log as WARN if not present
            self.log_action("PAYMENT_SKIP", "Payment automation not implemented yet")

            # 7. Submit
            call_openclaw("click", targetId=self.page_target_id, text="Book Now")
            self.log_action("SUBMIT_CLICKED", "Booking form submitted")
            return True
        except Exception as e:
            self.log_action("FILL_ERROR", str(e))
            return False

    def check_confirmation(self):
        """Detect success – look for confirmation number or success message."""
        try:
            output = call_openclaw("snapshot", targetId=self.page_target_id, refs="aria")
            for line in output.strip().split("\n"):
                if line.strip():
                    snap = json.loads(line)
                    txt = snap.get("text", "").lower()
                    if "confirmation" in txt or "success" in txt or "thank you" in txt:
                        return True
            return False
        except Exception as e:
            self.log_action("CONFIRM_CHECK_ERROR", str(e))
            return False

    def attempt_booking(self):
        """Single attempt – should be extremely fast."""
        try:
            self.log_action("ATTEMPT_START")
            if self.fill_and_submit():
                time.sleep(2)  # Wait for processing
                if self.check_confirmation():
                    return True
        except Exception as e:
            log_message("ERROR", f"Attempt exception: {e}")
        return False

    def run(self):
        self.start_time = time.time()
        log_message("INFO", "=== OPTIMIZED BOOKING SEQUENCE STARTED ===")
        log_message("INFO", f"Target: {URL}")
        log_message("INFO", f"Party: {BOOKING_INFO['party_size']['adults']} adults + {BOOKING_INFO['party_size']['child']} child")
        log_message("INFO", "Strategy: Pre-load page, wait until 9:00:00, then rapid DOM polling & submit")

        # Step 1: Open page early (8:58 or earlier)
        if not self.open_page_early():
            self.log_action("ABORT", "Failed to open page early")
            return False
        time.sleep(1)

        # Step 2: Wait until exactly 9:00:00
        self.wait_until_launch()

        # Step 3: Aggressive polling for form appearance
        self.log_action("POLLING_START", "Checking for form appearance every 1s (max 2h)")
        max_wait_seconds = 7200
        poll_interval = 1.0
        for i in range(max_wait_seconds):
            if self.detect_form_by_dom():
                self.log_action("FORM_FOUND", f"at +{i}s after 9:00")
                # Step 4: Immediately attempt booking
                if self.attempt_booking():
                    self.success = True
                    self.log_action("SUCCESS", "Booking confirmed!")
                    append_summary("RESULT", "✅ SUCCESS - Tickets secured")
                    break
                else:
                    self.log_action("WARN", "Attempt failed, continuing to poll")
                    # After a failed attempt, wait a moment before next detection cycle
                    time.sleep(2)
            else:
                time.sleep(poll_interval)

        if not self.success:
            self.log_action("FAILURE", "Form never appeared within window or all attempts failed")
            append_summary("RESULT", "❌ FAILED - No tickets today")

        self.log_action("SEQUENCE_END")
        return self.success

if __name__ == "__main__":
    booker = OptimizedBooker()
    success = booker.run()
    exit(0 if success else 1)