# STT CLI Wrapper - Bash Script

**File**: `/usr/local/bin/send-to-telegram`  
**Alias**: `stt`  
**Lines**: 224  
**Purpose**: User-friendly command-line interface for Telegram integration

## Complete Annotated Script

```bash
#!/bin/bash
# ════════════════════════════════════════════════════════════════════════════
# Telegram Sender Quick Utility Script
# Handles messages, files, directories, and RAG queries
# Updated: 2026-02-09 - Full STT integration with RAG system
# ════════════════════════════════════════════════════════════════════════════

# Exit on error - stop script if any command fails
set -e

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════

# Path to RAG system root directory
RAG_PATH="/home/kali/Desktop/RAG"

# Path to Python virtual environment
# All scripts run within this venv to have dependencies isolated
RAG_VENV="$RAG_PATH/.venv"

# ════════════════════════════════════════════════════════════════════════════
# COLOR DEFINITIONS
# ════════════════════════════════════════════════════════════════════════════

# ANSI color codes for terminal output
GREEN='\033[0;32m'      # Success messages
BLUE='\033[0;34m'       # Info messages
RED='\033[0;31m'        # Error messages
YELLOW='\033[1;33m'     # Warning messages
NC='\033[0m'            # No Color (reset)

# ════════════════════════════════════════════════════════════════════════════
# FUNCTION: activate_venv()
# Purpose: Activate the Python virtual environment
# Returns: Exit code 1 if venv not found
# ════════════════════════════════════════════════════════════════════════════

activate_venv() {
    # Check if venv directory exists
    if [ ! -d "$RAG_VENV" ]; then
        # Print error message in red
        echo -e "${RED}RAG venv not found at $RAG_VENV${NC}"
        # Exit script with error code
        exit 1
    fi
    
    # Activate the virtual environment by sourcing the activation script
    # This adds venv's python/pip to PATH and sets up environment
    source "$RAG_VENV/bin/activate"
}

# ════════════════════════════════════════════════════════════════════════════
# FUNCTION: send_rag_query()
# Purpose: Execute RAG query and send results to Telegram
# Arguments:
#   $1 - query string (required)
#   $2 - top_k results (optional, default: 5)
#   $3 - machine filter (optional, default: all machines)
# ════════════════════════════════════════════════════════════════════════════

send_rag_query() {
    # Capture function arguments
    local query="$1"              # The search query
    local top_k="${2:-5}"         # Number of results (default 5)
    local machine="${3:-}"        # Machine filter (empty = all)
    
    # Print what we're doing
    echo -e "${BLUE}RAG Query: $query${NC}"
    echo -e "${BLUE}Top-K: $top_k${NC}"
    # Only show machine if provided
    [ -n "$machine" ] && echo -e "${BLUE}Machine: $machine${NC}"
    
    # Activate Python virtual environment
    activate_venv
    
    # Run Python script in subshell to isolate environment
    # The subshell ensures venv activation doesn't affect parent shell
    (
        # Change to RAG directory where the script is located
        cd "$RAG_PATH"
        
        # Execute rag_to_telegram.py with different argument sets
        # based on whether machine filter was provided
        if [ -n "$machine" ]; then
            # With machine filter: pass 4 arguments
            # Arguments: query, top_k, machine
            python3 "rag_to_telegram.py" "$query" "$top_k" "$machine"
        else
            # Without machine filter: pass 2 arguments
            # Arguments: query, top_k (machine defaults to all)
            python3 "rag_to_telegram.py" "$query" "$top_k"
        fi
    )
}

# ════════════════════════════════════════════════════════════════════════════
# FUNCTION: send_rag_query_zip()
# Purpose: Execute RAG query and send results as ZIP file to Telegram
# Arguments: Same as send_rag_query(), plus --zip flag to Python script
# ════════════════════════════════════════════════════════════════════════════

send_rag_query_zip() {
    # Capture function arguments (same signature as send_rag_query)
    local query="$1"              # The search query
    local top_k="${2:-5}"         # Number of results (default 5)
    local machine="${3:-}"        # Machine filter (empty = all)
    
    # Print what we're doing
    echo -e "${BLUE}RAG Query ZIP: $query${NC}"
    echo -e "${BLUE}Top-K: $top_k${NC}"
    [ -n "$machine" ] && echo -e "${BLUE}Machine: $machine${NC}"
    echo -e "${YELLOW}Creating ZIP file...${NC}"
    
    # Activate Python virtual environment
    activate_venv
    
    # Run Python script in subshell
    (
        # Change to RAG directory
        cd "$RAG_PATH"
        
        # Execute rag_to_telegram.py with --zip flag to create ZIP output
        if [ -n "$machine" ]; then
            # With machine filter and ZIP flag
            python3 "rag_to_telegram.py" "$query" "$top_k" "$machine" --zip
        else
            # Without machine filter, with ZIP flag
            python3 "rag_to_telegram.py" "$query" "$top_k" --zip
        fi
    )
}

# ════════════════════════════════════════════════════════════════════════════
# FUNCTION: send_message()
# Purpose: Send a text message to Telegram
# Arguments:
#   $1 - message text (required)
# ════════════════════════════════════════════════════════════════════════════

send_message() {
    # Capture the message text
    local message="$1"
    
    # Print status
    echo -e "${BLUE}Sending message...${NC}"
    
    # Activate Python virtual environment
    activate_venv
    
    # Run telegram_sender.py with the message as argument
    # The script will handle chunking if message is too long
    python3 "$RAG_PATH/telegram_sender.py" "$message"
}

# ════════════════════════════════════════════════════════════════════════════
# FUNCTION: send_file()
# Purpose: Send a file to Telegram
# Arguments:
#   $1 - file path (required)
#   $2 - caption (optional)
# ════════════════════════════════════════════════════════════════════════════

send_file() {
    # Capture function arguments
    local file_path="$1"          # Path to file to send
    local caption="${2:-}"        # Optional caption (empty string if not provided)
    
    # Validate file exists before attempting to send
    if [ ! -f "$file_path" ]; then
        # File not found - print error and exit
        echo -e "${RED}File not found: $file_path${NC}"
        exit 1
    fi
    
    # Print what file we're sending
    echo -e "${BLUE}Sending file: $(basename "$file_path")${NC}"
    
    # Activate Python virtual environment
    activate_venv
    
    # Send file using telegram_sender.py with different argument sets
    # based on whether caption was provided
    if [ -n "$caption" ]; then
        # Send file WITH caption
        # Arguments: --file, file_path, caption_text
        python3 "$RAG_PATH/telegram_sender.py" --file "$file_path" "$caption"
    else
        # Send file WITHOUT caption
        # Arguments: --file, file_path (only)
        python3 "$RAG_PATH/telegram_sender.py" --file "$file_path"
    fi
}

# ════════════════════════════════════════════════════════════════════════════
# FUNCTION: send_directory()
# Purpose: ZIP a directory and send it to Telegram
# Arguments:
#   $1 - directory path (required)
#   $2 - caption (optional, default: "Directory archive")
# ════════════════════════════════════════════════════════════════════════════

send_directory() {
    # Capture function arguments
    local dir_path="$1"                           # Path to directory to send
    local caption="${2:-Directory archive}"       # Caption with sensible default

    # Validate directory exists before attempting to send
    if [ ! -d "$dir_path" ]; then
        # Directory not found - print error and exit
        echo -e "${RED}Directory not found: $dir_path${NC}"
        exit 1
    fi
    
    # Print what directory we're sending
    echo -e "${BLUE}Sending directory: $(basename "$dir_path")${NC}"
    
    # Activate Python virtual environment
    activate_venv
    
    # Run send_directory.py to ZIP and send the directory
    # Arguments: directory_path, caption_text
    python3 "$RAG_PATH/send_directory.py" "$dir_path" "$caption"
}

# ════════════════════════════════════════════════════════════════════════════
# FUNCTION: show_help()
# Purpose: Display usage information and examples
# ════════════════════════════════════════════════════════════════════════════

show_help() {
    # Print title
    echo -e "${BLUE}Telegram Sender - STT Command${NC}"
    echo ""
    
    # Print usage section
    echo -e "${GREEN}Usage:${NC}"
    echo "  stt rag \"query\" [top_k] [machine]       Search RAG and send results"
    echo "  stt rag-zip \"query\" [top_k] [machine]   Search RAG and send as ZIP"
    echo "  stt message \"text\"                      Send text message"
    echo "  stt file /path/to/file [caption]        Send file"
    echo "  stt directory /path/to/dir [caption]    Send directory as ZIP"
    echo "  stt /path/to/file                       Send file directly"
    echo ""
    
    # RAG usage examples
    echo -e "${GREEN}RAG Examples:${NC}"
    echo "  stt rag \"LFI exploitation\"              # 5 results, all machines"
    echo "  stt rag \"RCE techniques\" 10             # 10 results"
    echo "  stt rag \"privesc\" 5 facts               # Only FACTS machine"
    echo "  stt rag \"yaml injection\" 5 gavel        # Only GAVEL machine"
    echo ""
    
    # RAG ZIP examples
    echo -e "${GREEN}RAG ZIP Examples:${NC}"
    echo "  stt rag-zip \"LFI exploitation\"          # 5 results as ZIP"
    echo "  stt rag-zip \"RCE techniques\" 10         # 10 results as ZIP"
    echo "  stt rag-zip \"privesc\" 5 facts           # FACTS results as ZIP"
    echo ""
    
    # Other command examples
    echo -e "${GREEN}Other Examples:${NC}"
    echo "  stt message \"Task completed\""
    echo "  stt file /root/exploit.py \"Exploit script\""
    echo "  stt directory /root/loot \"Extracted files\""
    echo ""
    
    # Show index statistics
    echo -e "${YELLOW}Index Statistics:${NC}"
    echo "  Index:     rag-canonical-v1-emb3large"
    echo "  Model:     text-embedding-3-large (3072D)"
    echo "  FACTS:     105 chunks (92%)"
    echo "  GAVEL:       9 chunks (8%)"
    echo ""
    
    # Show configuration
    echo -e "${YELLOW}Configuration:${NC}"
    echo "  RAG Path:     $RAG_PATH"
    echo "  RAG Venv:     $RAG_VENV"
    echo "  Telegram:     /root/.openskills/env/telegram.env"
    echo "  Pinecone:     /root/.openskills/env/pinecone.env"
    echo "  OpenAI:       /root/.openskills/env/openai.env"
}

# ════════════════════════════════════════════════════════════════════════════
# MAIN LOGIC - Case statement for command routing
# ════════════════════════════════════════════════════════════════════════════

# Parse the first argument to determine which operation to perform
case "$1" in
    # ════════════════════════════════════════════════════════════════════════
    # COMMAND: stt rag "query" [top_k] [machine]
    # Searches RAG and sends results to Telegram
    # ════════════════════════════════════════════════════════════════════════
    rag)
        # Validate that at least query is provided
        if [ $# -lt 2 ]; then
            # Print error message with correct usage
            echo -e "${RED}Usage: stt rag \"query\" [top_k] [machine]${NC}"
            echo ""
            echo "Examples:"
            echo "  stt rag \"LFI exploitation\""
            echo "  stt rag \"RCE techniques\" 10"
            echo "  stt rag \"privesc\" 5 gavel"
            exit 1
        fi
        # Call function: pass query, optional top_k (default 5), optional machine
        send_rag_query "$2" "${3:-5}" "${4:-}"
        ;;
    
    # ════════════════════════════════════════════════════════════════════════
    # COMMAND: stt rag-zip "query" [top_k] [machine]
    # Searches RAG and sends results as ZIP file to Telegram
    # ════════════════════════════════════════════════════════════════════════
    rag-zip)
        # Validate that at least query is provided
        if [ $# -lt 2 ]; then
            # Print error message with correct usage
            echo -e "${RED}Usage: stt rag-zip \"query\" [top_k] [machine]${NC}"
            echo ""
            echo "Examples:"
            echo "  stt rag-zip \"LFI exploitation\""
            echo "  stt rag-zip \"RCE techniques\" 10"
            echo "  stt rag-zip \"privesc\" 5 facts"
            exit 1
        fi
        # Call function: pass query, optional top_k (default 5), optional machine
        send_rag_query_zip "$2" "${3:-5}" "${4:-}"
        ;;
    
    # ════════════════════════════════════════════════════════════════════════
    # COMMAND: stt message "text"
    # Sends plain text message to Telegram
    # ════════════════════════════════════════════════════════════════════════
    message)
        # Validate that message text is provided
        if [ $# -lt 2 ]; then
            # Print error message with correct usage
            echo -e "${RED}Usage: stt message \"Your message\"${NC}"
            exit 1
        fi
        # Call function with message text
        send_message "$2"
        ;;
    
    # ════════════════════════════════════════════════════════════════════════
    # COMMAND: stt file /path/to/file [caption]
    # Sends a file to Telegram
    # ════════════════════════════════════════════════════════════════════════
    file)
        # Validate that at least file path is provided
        if [ $# -lt 2 ]; then
            # Print error message with correct usage
            echo -e "${RED}Usage: stt file /path/to/file [caption]${NC}"
            exit 1
        fi
        # Call function: pass file path, optional caption
        send_file "$2" "${3:-}"
        ;;
    
    # ════════════════════════════════════════════════════════════════════════
    # COMMAND: stt directory /path/to/dir [caption]
    # ZIPs and sends a directory to Telegram
    # ════════════════════════════════════════════════════════════════════════
    directory)
        # Validate that at least directory path is provided
        if [ $# -lt 2 ]; then
            # Print error message with correct usage
            echo -e "${RED}Usage: stt directory /path/to/dir [caption]${NC}"
            exit 1
        fi
        # Call function: pass directory path, optional caption
        send_directory "$2" "${3:-}"
        ;;
    
    # ════════════════════════════════════════════════════════════════════════
    # COMMAND: stt help / stt --help / stt -h
    # Displays help information
    # ════════════════════════════════════════════════════════════════════════
    help|--help|-h)
        # Call help function
        show_help
        ;;
    
    # ════════════════════════════════════════════════════════════════════════
    # DEFAULT: stt /path/to/file
    # If argument is a file path (not a recognized command), send it directly
    # This is a convenience feature for quick file sending
    # ════════════════════════════════════════════════════════════════════════
    *)
        # Check if the first argument is an existing file
        if [ $# -ge 1 ] && [ -f "$1" ]; then
            # It's a file - send it with optional caption (2nd argument)
            send_file "$1" "${2:-}"
        else
            # Not a recognized command and not a file - show help
            show_help
            exit 1
        fi
        ;;
esac

# ════════════════════════════════════════════════════════════════════════════
# COMPLETION MESSAGE
# ════════════════════════════════════════════════════════════════════════════

# Print success message in green
echo -e "${GREEN}Done!${NC}"
```

## How It Works

### Flow Diagram

```
User Command (stt)
      ↓
Parse argument ($1)
      ↓
  ┌───┴────────────────────────────────┐
  │ Which command?                     │
  ├────────────────────────────────────┤
  │ rag → send_rag_query()             │
  │ rag-zip → send_rag_query_zip()     │
  │ message → send_message()           │
  │ file → send_file()                 │
  │ directory → send_directory()       │
  └────────────────────────────────────┘
      ↓
Activate venv
      ↓
Execute Python script
      ↓
Send to Telegram
      ↓
Completion
```

## Key Concepts

### Variable Defaults
```bash
# Default values using ${var:-default} syntax
local top_k="${2:-5}"              # If $2 empty, use 5
local caption="${2:-}"             # If $2 empty, use empty string
local machine="${3:-}"             # If $3 empty, use empty string
```

### Subshell Execution
```bash
# Subshell ( ... ) isolates environment
(
    cd "$RAG_PATH"
    python3 script.py
)
# After subshell exits, original shell directory unchanged
```

### Conditional Execution
```bash
# Only show machine if provided
[ -n "$machine" ] && echo "Machine: $machine"

# Only add caption if provided
if [ -n "$caption" ]; then
    # with caption
else
    # without caption
fi
```

## Usage Examples

```bash
# Query RAG - return top 5 results from all machines
stt rag "LFI exploitation"

# Query FACTS only, return top 10
stt rag "privilege escalation" 10 facts

# Query GAVEL, get 15 results, send as ZIP
stt rag-zip "YAML injection" 15 gavel

# Send a message
stt message "Task completed successfully"

# Send a file with caption
stt file /root/notes.txt "My notes"

# Send a directory
stt directory /root/loot "Extracted files"

# Send file directly (no command needed)
stt /root/exploit.py
```

---

**Next: [telegram_sender.py](telegram_sender_py.md) - The core Telegram class**
