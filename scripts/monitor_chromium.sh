#!/bin/bash
# Chromium Download Monitoring Script
# Checks progress and logs status

LOG_FILE="/tmp/nexus-fetch.log"
NEXUS_DIR="/mnt/d/nexus"
OUTPUT_FILE="/home/iyeque/.openclaw/workspace/chromium_progress_$(date +%Y-%m-%d).log"

echo "=== Chromium Download Status Check ===" | tee -a "$OUTPUT_FILE"
echo "Time: $(date)" | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

# Check if process is running
echo "Process Status:" | tee -a "$OUTPUT_FILE"
ps aux | grep fetch_chromium | grep -v grep | tee -a "$OUTPUT_FILE"
if [ $? -ne 0 ]; then
    echo "⚠️  fetch_chromium process not found!" | tee -a "$OUTPUT_FILE"
fi
echo "" | tee -a "$OUTPUT_FILE"

# Check disk usage
echo "Disk Usage on /mnt/d:" | tee -a "$OUTPUT_FILE"
df -h /mnt/d 2>/dev/null | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

# Check Nexus directory size
echo "Nexus Directory Size:" | tee -a "$OUTPUT_FILE"
du -sh "$NEXUS_DIR" 2>/dev/null | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

# Check if src/ exists and its size
if [ -d "$NEXUS_DIR/src" ]; then
    echo "Chromium src/ directory:" | tee -a "$OUTPUT_FILE"
    du -sh "$NEXUS_DIR/src" 2>/dev/null | tee -a "$OUTPUT_FILE"
    echo "Contents of src/:" | tee -a "$OUTPUT_FILE"
    ls -la "$NEXUS_DIR/src" 2>/dev/null | head -20 | tee -a "$OUTPUT_FILE"
else
    echo "src/ directory not yet created" | tee -a "$OUTPUT_FILE"
fi
echo "" | tee -a "$OUTPUT_FILE"

# Tail recent log entries
echo "Recent log entries (last 10 lines):" | tee -a "$OUTPUT_FILE"
tail -10 "$LOG_FILE" 2>/dev/null | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

# Summary
echo "=== Summary ===" | tee -a "$OUTPUT_FILE"
if ps aux | grep -v grep | grep -q fetch_chromium; then
    echo "✅ Process is running" | tee -a "$OUTPUT_FILE"
else
    echo "❌ Process is NOT running" | tee -a "$OUTPUT_FILE"
fi
echo "Log location: $LOG_FILE" | tee -a "$OUTPUT_FILE"
echo "Full output saved to: $OUTPUT_FILE" | tee -a "$OUTPUT_FILE"
