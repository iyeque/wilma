# Aquaventure Booker Memory

This directory contains logs and state for the Aquaventure Waterpark ticket booking agent.

## Strategy
- Target: https://booking.aquaventureworld.com/experiences/waterpark-day-passes
- Release: Daily 9:00 AM UAE time (UTC+4)
- Priority: MAX MURAYA (3 adults + 1 child, prefer 21 March 2026)
- Contact: mmmuraya@outlook.com, +971581518024
- Card: 4251996048727389 (Exp 08/28, CVV 484) - stored in memory only

## Plan
1. Starting 19 March: Attempt daily at exactly 9:00 AM UAE time
2. Retry: brute-force 5-second interval, no time limit, until success or sold out
3. Stop condition: Success on any date (prefer 21st), or site declares sold out

## Notes
- Today is Thursday, March 18, 2026
- Current time: ~05:24 UAE (before 9 AM release)
- First attempt should be 9:00 AM Friday, March 19, 2026
- March 21-22 is weekend - harder to get, be persistent
