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
- **Current:** Phase 2 implementation completed (2026-03-23). Phase 3 implementation underway – probabilistic programming + causal modeling. Already has AST nodes, lexer tokens, parser support for `prob {}`, `sample()`, `given`, `causal`, `verify`. Type system extended with `DistType` and effect tracking. Interpreter runtime added with distribution classes (Bernoulli, Normal, Uniform, Conditional) and ProbModel closure semantics. Test suite demonstrates working Bernoulli/normal/uniform sampling and recursive probabilistic functions.

## Elysium Governance Smart Contracts

- **Status:** All 8 priority tasks complete (AI vote caps, citizenship jury, identity challenge, verifier integration, merit grants, tier timelocks, H3 safeguards, deployment prep)
- **Deployment readiness:** ✅ **GO for Sepolia testnet** – completed final audit, documentation, and script enhancements (2026-03-20)
- **Agent wrapper:** `elise` agent created and fixed (uses `forge script script/DeployAll.s.sol`). Currently shows "not_deployed" state.
- **Next:** Execute deployment to Sepolia; monitor and test; prepare for external audit before mainnet

## Other Active Projects

- **Aquaventure Booker:** Manual attempt on 2026-03-20 failed due to high demand. Implemented full browser automation in `booking_agent_optimized.py` using OpenClaw browser CLI: pre-loads page, waits until 9:00 AM, polls for form, fills and submits. Cron job enabled (8:58 AM) to run the agent with `qwen-portal/coder-model`. 8:50 AM checkpoint verifies browser service. Next attempt: March 23, 9:00 AM Dubai. Hourly quota checks ensure model availability.
- **Nexus (Chromium fetch):** In progress (~1.6% complete, ~100 GB total). Estimated 2–3 days remaining. Now has an OpenClaw agent wrapper (`nexus`) that can manage fetch, progress checks, and restarts.
- **ALGOL 26 Phase 2:** Sub-agent spawned to implement full static type system and module system (Hindley-Milner inference, ADTs, row polymorphism, module boundaries). Running in background with Gemini Pro.
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
