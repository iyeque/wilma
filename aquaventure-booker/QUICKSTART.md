# Aquaventure Booker - Quick Start Guide

## When to Run
- **Daily at 9:00 AM UAE time (UTC+4) sharp**
- Starting: Friday, March 19, 2026
- Until: March 22, 2026 OR success

## How to Execute
The subagent should be spawned to run the booking automation. When called at the right time:

1. The agent will use browser automation to navigate to the booking site
2. Fill the form with the following details:
   - **Name:** MAX MURAYA
   - **Email:** mmmuraya@outlook.com
   - **Phone:** +971581518024
   - **Party:** 3 adults + 1 child (2-year-old free). If only 2 adults + 1 child available, take that.
   - **Date:** Prefer March 21, 2026 (any date before March 22 works)
   - **Payment:** Card 4251996048727389 (Exp 08/28, CVV 484) - for reservation only
3. Retry with exponential backoff (30s, 60s, 120s...) for up to 20 minutes if failures occur
4. Stop as soon as booking is confirmed

## Important Notes
- Card details are stored in memory only; do not log or commit
- All actions are logged in: `/home/iyeque/.openclaw/workspace/aquaventure-booker/aquaventure-memory/YYYY-MM-DD.md`
- Weekend (March 21-22) will be more competitive - be persistent
- If the site crashes, wait and retry automatically

## Status Commands
- Check daily logs: `ls -la /home/iyeque/.openclaw/workspace/aquaventure-booker/aquaventure-memory/`
- View today's log: `cat /home/iyeque/.openclaw/workspace/aquaventure-booker/aquaventure-memory/$(date +%Y-%m-%d).md`

## Script Location
The Python automation script is at:
`/home/iyeque/.openclaw/workspace/aquaventure-booker/booking_agent.py`

(But the subagent will execute directly via browser tool, not via separate script)
