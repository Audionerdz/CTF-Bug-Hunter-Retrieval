# Usage Examples - Real-World Workflows

Complete, copy-paste ready examples for all Telegram integration scenarios.

## Example 1: Send Quick Message

```bash
# Notify task completion
stt message "Buffer overflow exploit successful - root shell obtained"

# Send status update
stt message "🔓 FACTS machine compromised. Next: GAVEL machine"
```

## Example 2: Send Exploit Script

```bash
# Send malicious file with description
stt file /root/exploits/lfi_bypass.py "LFI filter bypass - PHP null bytes"

# Send compiled binary
stt file /tmp/rootkit.elf "Compiled privilege escalation"
```

## Example 3: Send Directory with Extracted Data

```bash
# Send entire loot directory
stt directory /root/loot "Extracted files and credentials"

# Send sensitive data
stt directory /home/user/ssh_keys "SSH keys from compromised machine"

# Send memory dump
stt directory /tmp/memory_dumps "RAM dumps for analysis"
```

## Example 4: Search RAG + Send Results

```bash
# Basic search - top 5 results from all machines
stt rag "LFI exploitation techniques"

# Specific number of results
stt rag "privilege escalation" 10

# Filter by machine
stt rag "YAML injection" 5 facts

# GAVEL machine only
stt rag "API endpoint bypass" 20 gavel
```

## Example 5: Send RAG Results as ZIP

```bash
# Compress and send search results
stt rag-zip "buffer overflow" 15 facts

# Large result set as ZIP
stt rag-zip "exploitation" 50

# Specific machine, specific count
stt rag-zip "privilege escalation" 25 facts
```

## Example 6: Multi-Phase Attack Workflow

```bash
# Phase 1: Initial access
stt message "🎯 Phase 1: Reconnaissance started..."
sst rag "initial access" 5 facts
sst message "✓ Recon complete. Found web vulnerability."

# Phase 2: Exploitation
stt message "🔓 Phase 2: Exploitation started..."
stt file /root/exploits/web_rce.py "Web RCE exploit"
stt message "✓ Initial access obtained. Reverse shell active."

# Phase 3: Privilege Escalation
stt message "🚀 Phase 3: Privilege escalation..."
stt rag "privilege escalation" 10 facts
stt message "✓ Root access obtained!"

# Phase 4: Post-exploitation
stt directory /root/loot "All extracted data"
stt message "✅ Mission complete!"
```

## Example 7: Batch Queries for Different Techniques

```bash
#!/bin/bash
# Search for multiple exploitation techniques

techniques=(
    "LFI exploitation"
    "RCE techniques"
    "SQL injection"
    "XXE attacks"
    "privilege escalation"
)

for technique in "${techniques[@]}"; do
    echo "Searching for: $technique"
    stt rag "$technique" 5 facts
    sleep 2  # Avoid rate limiting
done

stt message "✅ All searches complete"
```

## Example 8: Organized Attack Documentation

```bash
# Create comprehensive attack report
stt message "═══════════════════════════════════════════════════════════"
stt message "🎯 ATTACK REPORT - FACTS MACHINE"
stt message "═══════════════════════════════════════════════════════════"

# Reconnaissance
stt message "\n📡 RECONNAISSANCE PHASE"
stt rag "port scanning" 3 facts
stt rag "service enumeration" 3 facts
stt rag "web application analysis" 3 facts

# Exploitation
stt message "\n🔓 EXPLOITATION PHASE"
stt rag "authentication bypass" 3 facts
sst rag "RCE" 3 facts
stt rag "privilege escalation" 3 facts

# Post-exploitation
stt message "\n💾 POST-EXPLOITATION PHASE"
stt rag "data exfiltration" 3 facts
stt directory /root/loot "Extracted credentials and data"

stt message "\n✅ ATTACK COMPLETE"
stt message "═══════════════════════════════════════════════════════════"
```

## Example 9: Automated Daily Knowledge Sync

```bash
#!/bin/bash
# Sync RAG knowledge to Telegram daily

echo "Daily RAG Knowledge Sync - $(date)"
stt message "📚 Daily RAG Knowledge Sync Started"

# Update on all major techniques
topics=(
    "LFI"
    "RCE"
    "SQLi"
    "SSRF"
    "XXE"
    "CSRF"
    "XSS"
    "Deserialization"
)

for topic in "${topics[@]}"; do
    echo "Syncing: $topic"
    stt rag "$topic" 3  # Top 3 results
    sleep 1
done

stt message "✅ Daily sync complete"
```

## Example 10: Error Handling & Logging

```bash
#!/bin/bash
# Safe script with error handling

log_file="/tmp/stt_log_$(date +%Y%m%d_%H%M%S).log"

# Function to send message with logging
send_with_log() {
    local msg="$1"
    echo "[$(date +%H:%M:%S)] $msg" >> "$log_file"
    stt message "$msg" || {
        echo "ERROR: Failed to send message" >> "$log_file"
        return 1
    }
}

# Send initial message
send_with_log "🚀 Attack script started" || exit 1

# Send results with error checking
if stt rag "vulnerability" 5; then
    send_with_log "✓ RAG search successful"
else
    send_with_log "✗ RAG search failed"
fi

# Send files if they exist
if [ -f "/root/exploit.py" ]; then
    stt file "/root/exploit.py" "Exploit" || send_with_log "Failed to send exploit"
else
    send_with_log "⚠️ Exploit file not found"
fi

send_with_log "✅ Script complete"
echo "Logs saved to: $log_file"
```

## Command Quick Reference

| Task | Command |
|------|---------|
| Message | `stt message "text"` |
| File | `stt file /path` |
| Directory | `stt directory /path` |
| Search RAG | `stt rag "query"` |
| Search + ZIP | `stt rag-zip "query"` |
| Help | `stt help` |

## Best Practices

### ✅ Do

- Use `stt rag-zip` for large result sets (>10 results)
- Add descriptive captions to files and directories
- Use message updates to track attack progress
- Filter by machine when possible (faster, focused)
- Space out API calls to avoid rate limiting

### ❌ Don't

- Send files larger than 50MB to Telegram
- Query without top_k limit (can be slow)
- Send sensitive data without encryption
- Overload Telegram API with rapid requests
- Use stt without proper error handling in scripts

---

**Next: [Troubleshooting](troubleshooting.md)**
