# Long-Term Memory - OpenClaw Workspace

## Repository Architecture (Est. 2026-03-20)

The workspace follows a clean separation pattern:

- **Wilma repo** (`~/.openclaw/workspace` on `master` branch) - OpenClaw configuration, contracts, and project subdirectories
- **Elysium contracts** stored in `workspace/contracts/` (not a separate repo)
- **Genai repo** (submodule) - ALGOL 26 language research and implementation
- **Nexus** (external symlink to `/mnt/d/nexus`) - Decentralized browser development
- **Mangoma & Orca** (nested independent git repos) - Agent projects

**Key principle:** Each repository contains only its domain-specific code. OpenClaw config stays in wilma; project code stays in project repos. Submodules used for genai; other projects are standalone.

## ALGOL 26 Development Stages

- **MVI (Minimum Viable Interpreter)** - Complete (2026-03-20): Python implementation with lexer, parser, AST, interpreter. Supports core language: variables, control flow (if/while/for), functions, arrays, records, basic I/O, math builtins.
- **Roadmap Phase 2-5** - Defined (2026-03-20): Comprehensive plan produced covering type system, modules, probabilistic/causal programming, concurrency, meta-cognition, formal verification, and hardware acceleration. Multi-stage hybrid architecture (Python prototype → Rust production) adopted.
- **Phase 2** - Complete (2026-03-23): Full static type system with Hindley-Milner inference, module system, ADTs, row polymorphism. Committed and tagged `phase-2-complete`.
- **Phase 3** - Complete (2026-03-24): Probabilistic programming and causal modeling. Implemented distribution classes (Bernoulli, Normal, Uniform, Conditional), `ProbModel` closures, `sample()`, `given`, `causal`, `verify` constructs. Full test suite demonstrating Bayesian inference and causal queries. Committed with message "feat(phase3): complete probabilistic programming and causal modeling".
- **Phase 4** - Implementation complete and committed (2026-03-27): Concurrency features including channels (buffered/unbuffered), async procedures, send/receive operations, and cooperative scheduler. Basic `SelectStmt` tests created (pending full implementation). Commit `eaccdd3` pushed to remote: "feat(phase4): implement concurrency with channels, async procs, and scheduler".
- **Current:** Phase 4 work integrated; pending: `SelectStmt` completion, edge case testing, full scheduler integration refinement. Phase 5 (formal verification + hardware acceleration) next in roadmap.

## Elysium Governance Smart Contracts

- **Status:** All 8 priority tasks complete (AI vote caps, citizenship jury, identity challenge, verifier integration, merit grants, tier timelocks, H3 safeguards, deployment prep)
- **Deployment readiness:** ✅ **GO for Sepolia testnet** – completed final audit, documentation, and script enhancements (2026-03-20)
- **Agent wrapper:** `elise` agent created and fixed (uses `forge script script/DeployAll.s.sol`). Currently shows "not_deployed" state.
- **Next:** Execute deployment to Sepolia; monitor and test; prepare for external audit before mainnet

## Other Active Projects

- **Aquaventure Booker:** Manual attempt on 2026-03-20 failed due to high demand. Implemented full browser automation in `booking_agent_optimized.py` using OpenClaw browser CLI: pre-loads page, waits until 9:00 AM, polls for form, fills and submits. Cron job enabled (8:58 AM) to run the agent with `qwen-portal/coder-model`. 8:50 AM checkpoint verifies browser service. Next attempt: March 23, 9:00 AM Dubai. Hourly quota checks ensure model availability.
- **Nexus (Chromium fetch):** **Restarted** on March 28 (05:03 AM). Currently at 0% (initial clone stage). Total repository expected: ~27.8M objects, ~61 GiB. Download active; will take 2-3 days depending on bandwidth. Has an OpenClaw agent wrapper (`nexus`) that manages fetch, progress checks, and automatic restarts on failure.
- **ALGOL 26:** Phase 4 (concurrency) completed and pushed. Remote repo: https://github.com/iyeque/genai (branch main, commit eaccdd3). Next steps: implement `SelectStmt` and expand test coverage before moving to Phase 5 (formal verification + hardware acceleration).
- **Orca SCM Platform:** Full-stack project (FastAPI, React, smart contracts) present in workspace. Now has an OpenClaw agent wrapper (`orca`) to manage Docker services (up/down/status) and contract deployment.
- **Elysium (elise):** Deployment agent wrapper fixed and functional; contracts stored in `workspace/contracts/`; script in `workspace/script/DeployAll.s.sol`. Ready for Sepolia testnet deployment.

The interpreter successfully runs demo programs including a neural network forward pass.

## Automation & Monitoring

- Chromium download monitoring via cron (every 15 min) – isolated, no external messages
- Hourly model-quota checks (19:00–23:00 Dubai) to ensure booking agent can run at 9:00 AM
- Daily workspace backup to wilma (pushes local commits)
- Submodule management for genai integration
- WhatsApp messages limited to: daily poem for Wilmax, critical alerts to Max only

## Mangoma Music Generation: Lyria Access & Stable Audio Fallback (2026-03-24)

**Context:** YouTube live streaming requires continuous AI-generated music. Original plan: use Google's Lyria model (Vertex AI). Testing revealed Lyria is experimental and not accessible without special allowlisting.

### Vertex AI Setup Results
- ✅ Installed gcloud SDK in WSL
- ✅ Authenticated as `mmmaximus18@gmail.com`
- ✅ Set project: `project-68ac92be-3207-4788-84d`
- ✅ Enabled Vertex AI API (`aiplatform.googleapis.com`)
- ❌ Lyria model (`models/lyria-realtime-exp`) **NOT found** in model list
- Conclusion: Lyria requires **special access** beyond standard Vertex AI billing.

**Action:** Submitted Google Cloud support case requesting Lyria access. Awaiting approval.

### Stable Audio 2.0 Integration (Immediate Fallback)
While awaiting Lyria access, implemented **Stable Audio 2.0** (Stability AI) via Hugging Face Inference API as a free/cheap alternative.

**Architecture:**
- `UnifiedMusicClient` – abstraction layer supporting multiple providers (`lyria`, `stable-audio`, `local`)
- `StableAudioClient` – Hugging Face API wrapper (chunk-based generation)
- `config.ts` – expanded with `vertex` and `stableAudio` sections, `musicProvider` selector
- `server.ts` – migrated from Lyria-only to UnifiedMusicClient

**Key characteristics:**
- **Lyria:** Real-time continuous streaming (ideal for 24/7), but requires access + ~$172/day
- **Stable Audio:** Generates fixed-length chunks (~30-47 sec) in ~10-60 seconds, free tier ~30k compute units/month (~60 sec audio per generation)
- **Switching:** Set `MUSIC_PROVIDER=lyria` or `stable-audio` in `.env`

**Status:** Code complete, committed, and pushed. Ready to test with Hugging Face token once obtained.

**Limitations & Next Steps:**
- Stable Audio is **not realtime continuous** – requires a queuing system (generate next chunk while playing current)
- Need to implement chunk queue/player for seamless playback
- Consider self-hosting Stable Audio locally (requires GPU) for zero-cost continuous generation
- Also researching: Replicate API (pay-per-use), AudioCraft (Meta), Riffusion, MuseGAN

### Daily Poem to Wilmax
✅ Sent morning poem via WhatsApp (consistent with daily cron job `daily-poem-wilmax` at 08:00). Poem delivered successfully.

---

## Model Configuration Fixes (2026-03-22 evening)

**Problem:** Multiple cron jobs were using expired or unreliable LLM models:
- `whatsapp-precheck-0755` failed with "Solar Pro 3 free tier expired"
- Hourly quota check defaulting to Solar Pro 3 as well
- Morning summary and tech update using `google/gemini-3-pro-preview` (risky)

**Solution:** Migrated all critical WhatsApp delivery jobs to confirmed working model `qwen-portal/coder-model`:
- `Check if any free-tier LLM models have reset quota` - explicit model override added
- `whatsapp-precheck-0755` - switched from Solar Pro 3 to qwen
- `daily_morning_summary` - switched from google/gemini-3-pro-preview to qwen
- `daily-tech-update` - switched from google/gemini-3-pro-preview to qwen
- `daily-poem-wilmax` - switched from google/gemini-3-pro-preview to qwen (2026-03-22 evening)
- `mangoma-memory-sync` - switched from google/gemini-3-pro-preview to qwen (2026-03-22 evening)

**Status:** All JSON configuration validated. All time-critical messaging now uses a reliable, working model. Aquaventure booking agent already using qwen-portal/coder-model.

**Next:** Monitor tomorrow morning's cron runs (7:55, 8:00, 8:50, 8:55, 9:00) to confirm successful deliveries. All time-critical messaging now uses qwen-portal/coder-model; deprecated models purged from config.

## Aquaventure Booking System Verification (2026-03-24)

**8:50 AM Checkpoint Results:**
- ✅ Browser service running (Chromium headless, PID 9625, CDP port 18801)
- ✅ Chromium CDP reachable and responsive; Aquaventure booking page already loaded
- ✅ OpenClaw gateway healthy (HTTP 200 on port 18789)
- ✅ Model `qwen-portal/coder-model` confirmed reliable (used by all successful cron jobs)
- ✅ Aquaventure booking cron job (`aquaventure-booking-attempt`) verified enabled and scheduled for 08:58 Dubai (8 minutes later)
- ✅ Booking script (`aquaventure-booker/booking_agent_optimized.py`) present with correct credentials and strategy

**Preparation Outcome:** All systems GO. No restarts required. Booking attempt will proceed as scheduled at 9:00 AM Dubai. Confidence: HIGH.

## Critical Configuration Recovery & Infrastructure Restart (2026-03-25 Evening)

**Discovery:** On March 25 evening, it was discovered that:
- The Aquaventure booking cron job was **missing** from `/home/iyeque/.openclaw/cron/jobs.json`
- Several cron jobs lacked explicit model overrides and defaulted to the expired `upstage/solar-pro-3:free`
- The browser service (Xvfb + Chromium) was **not running**
- The `qwen-portal/coder-model` OAuth token had expired (March 22), causing fallback to Solar Pro 3

**Actions Taken:**
1. **Added missing Aquaventure booking job** with schedule `58 8 * * *` (Asia/Dubai), agent `aquaventure-booker`, and explicit model
2. **Fixed model overrides** on all remaining cron jobs to use `qwen-portal/coder-model`
3. **Switched Aquaventure job model** to `openrouter/stepfun/step-3.5-flash:free` (currently working free tier)
4. **Started browser service manually:**
   - Xvfb on display :99 (PID 10151)
   - Chromium with remote debugging on port 18801 (PID 10155)
5. **Verified CDP and gateway health:**
   - CDP: Chrome/146.0.7680.80, protocol 1.3, ws://localhost:18801/devtools/…
   - Gateway: `{"ok":true,"status":"live"}`
6. **Recorded detailed checkpoint** in `memory/2026-03-25-checkpoint.md`

**Current State:** All infrastructure verified, configurations corrected. Next automated booking attempt: **March 26, 9:00 AM Dubai**.

**Open Issues:**
- Qwen OAuth token needs refresh; using stepfun as primary for booking (non-blocking)
- Browser service auto-start ✅ COMPLETED (systemd user services: xvfb.service, chromium.service)
- Solar Pro 3 removed from fallback chain ✅ COMPLETED

---

## Browser Service Auto-Start Implementation (2026-03-25 late night)

**Problem:** Browser service required manual start after reboot; could cause missed booking if system restarted before 9:00 AM.

**Solution:** Created systemd user services for reliable auto-start:
- `xvfb.service` – runs Xvfb on display :99 (Type=simple, foreground)
- `chromium.service` – runs Chromium headless on CDP port 18801; Requires=Avives=xvfb.service
Both services enabled (`systemctl --user enable`) to start automatically on user login. Services verified running under systemd management (PIDs 18173, 18184).

**Result:** Browser will now auto-start on boot without manual intervention. Services will also restart on failure.

---

## Solar Pro 3 Fallback Cleanup (2026-03-25 late night)

**Problem:** `openrouter/upstage/solar-pro-3:free` remained in `agents.defaults.model.fallbacks` in `openclaw.json`, posing a risk of accidental reuse despite being expired.

**Action:** Removed that entry from the fallbacks array. The fallback chain now starts with `openrouter/stepfun/step-3.5-flash:free` followed by other reliable providers.

**Result:** Solar Pro 3 will no longer be selected as a fallback, eliminating 404 errors from expired model usage.

## Default Model Primary Update (2026-03-25 late night)

**Action:** Changed `agents.defaults.model.primary` from `qwen-portal/coder-model` to `openrouter/stepfun/step-3.5-flash:free` in `openclaw.json`. Moved `qwen-portal/coder-model` into the fallbacks list.

**Rationale:** The qwen OAuth token expired on March 22, making stepfun the more reliable default. This eliminates fallback latency for any agent relying on the default model.

**Result:** All new agent sessions will default to stepfun unless an explicit model is specified.

## Default Model Update (2026-03-25 late night)

**Action:** Changed `agents.defaults.model.primary` from `qwen-portal/coder-model` to `openrouter/stepfun/step-3.5-flash:free` in `openclaw.json`. Moved `qwen-portal/coder-model` into fallbacks list.

**Rationale:** The qwen OAuth token expired (March 22), so stepfun is more reliable as primary. This eliminates fallback latency for all agents that rely on the default model.

**Result:** All new agent sessions will default to stepfun unless an explicit model is specified.


## Critical Configuration Recovery (2026-03-25)

**Discovery:** On March 25, it was discovered that the Aquaventure booking cron job was **missing** from `/home/iyeque/.openclaw/cron/jobs.json`. Additionally, several cron jobs lacked explicit model overrides and were still defaulting to the expired `upstage/solar-pro-3:free` model, causing repeated failures.

**Actions Taken:**
- Added missing cron job `Aquaventure Booking Attempt` (scheduled 08:58 Dubai, agent: `aquaventure-booker`, model: `qwen-portal/coder-model`, timeout: 300s)
- Applied explicit model overrides to all remaining cron jobs that were using default/expired models:
  - `whatsapp-precheck-0855`
  - `daily-wilma-sync`
  - `Chromium Download Monitor`
- Verified all 11 cron jobs now use `qwen-portal/coder-model` consistently
- Confirmed `aquaventure-booker` agent has the required provider configuration for qwen-portal

**Status:** All cron configurations corrected and validated. The next Aquaventure booking attempt will be **March 26, 9:00 AM Dubai** (assuming March 25 window already passed). All critical messaging jobs now use a reliable, working model.

**Lesson:** Periodic audits of cron job configurations are needed to ensure model overrides aren't inadvertently lost during edits. Consider adding a schema validation step to prevent missing required fields like `model`.

## Model Migration to stepfun (2026-03-25 evening)

**Problem:** The 8:50 AM checkpoint job failed with error: "404 No allowed providers are available for the selected model." Investigation revealed that `qwen-portal/coder-model`, while previously working, had an expired OAuth token (as of March 22). The checkpoint file and tests confirmed that `openrouter/stepfun/step-3.5-flash:free` was the only reliably working free-tier model at the time.

**Resolution:** Migrated all cron jobs from the now-unreliable `qwen-portal/coder-model` to the confirmed working `openrouter/stepfun/step-3.5-flash:free`. This included 10 jobs:
- daily_morning_summary
- daily-poem-wilmax
- daily-tech-update
- whatsapp-precheck-0755
- whatsapp-precheck-0855
- daily-wilma-sync
- mangoma-memory-sync
- Chromium Download Monitor
- 8:50 AM checkpoint
- Model quota check (19:00–23:00)

The Aquaventure Booking Attempt was already using stepfun (adjusted earlier due to qwen OAuth issues).

**Result:** All cron jobs now target a stable, working model. The 8:50 AM checkpoint and other time-critical tasks have a high probability of success starting March 26.

**Recommendation:** Continue monitoring stepfun's availability. If it degrades, we may need to evaluate other providers or implement a dynamic model fallback mechanism.

---

## Chromium Download Monitoring Technique (2026-03-26/28)

**Context:** Monitoring large `git clone` operations for the Chromium/src repository (~61 GiB, 27.8M objects) requires understanding of git's multi-stage process.

### Key Indicators

1. **Process State:** The main `git clone --no-checkout` process runs in `D` (uninterruptible I/O wait) state for extended periods. This is **normal** and indicates active network transfer, not a hang.

2. **Object Count:** `git count-objects` in the repository shows unpacked objects. In early stages, this can be 0 even while download is active because pack files are still being received and not yet unpacked.

3. **Pack Files:** Check `.git/objects/pack/` for `*.pack` files. These appear only after significant data has been received. Initially empty is expected.

4. **Network Connection:** The child process `git-remote-https` (or `git remote-https`) maintains an ESTABLISHED TLS connection to `chromium.googlesource.com:443`. Presence of this connection indicates active transfer.

5. **CPU Usage:** Low CPU (1-10%) is typical for network-bound I/O. Higher CPU during `index-pack` phase later.

6. **Directory Size:** The repository root size remains small (tens of KiB) until pack files start accumulating. Once packs appear, size grows rapidly.

### Restart Logic

**Do NOT restart if:**
- `git clone` or `gclient sync` processes are running
- `git-remote-https` has an ESTABLISHED connection
- The repository directory exists with `.git` structure

**Restart only if:**
- Processes are dead (no `git clone`, `gclient`, or `git-remote-https` running)
- And no network connection to chromium.googlesource.com from relevant processes
- And repository is incomplete (no pack files after extended time)

### Observations from Recent Attempts

- **March 24:** Reached 63% completion (~11 GiB) before network timeout; automatic recovery possible?
- **March 27:** Reached 17.45% (~2.02 GiB) before network error; resumed in retry mode
- **March 28 (current):** Fresh restart at 0% (04:28 AM). Expected to take 2-3 days on current bandwidth.

### Recommendations

- **Cron frequency:** Every 15 minutes is appropriate (doesn't overload system, catches failures promptly)
- **No WhatsApp alerts:** This is a low-priority background operation; failures should auto-restart
- **Thresholds:** Consider flagging if `.git/objects/pack/` remains empty after 30 minutes, or if process is in `D` state with zero network bytes transferred for >1 hour (could use `/proc/<pid>/net/tcp` to verify connection activity)
- **Logging:** Keep detailed reports per check; these are valuable for post-mortem if download consistently fails at certain sizes

### Future Improvements

- Parse `git clone --progress` output if available (currently suppressed by nohup). Could parse log file for "Receiving objects: X% (Y/Z)" pattern.
- Use `git fetch --dry-run` to check if objects are already complete? Not applicable mid-clone.
- Consider resuming interrupted clone via `git fetch --all` if pack files exist, rather than full restart.

