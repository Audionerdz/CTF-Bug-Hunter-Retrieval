# telegram_sender.py - Core Telegram Class

**File**: `/home/kali/Desktop/RAG/telegram_sender.py`  
**Lines**: 196  
**Class**: `TelegramSender`  
**Purpose**: Low-level Telegram Bot API communication with message chunking

## Complete Annotated Script

```python
#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
"""
Telegram Sender for RAG Results
Supports chunked messages for long content
"""
# ════════════════════════════════════════════════════════════════════════════

# Standard library imports for file and network operations
import os                    # OS file operations (file existence, size)
import requests              # HTTP requests to Telegram API
import time                  # Sleep for rate limiting
import zipfile              # Create ZIP archives of directories

# Third-party import for environment variable loading
from dotenv import load_dotenv  # Load .env files with credentials

# ════════════════════════════════════════════════════════════════════════════
# LOAD ENVIRONMENT VARIABLES
# ════════════════════════════════════════════════════════════════════════════

# Load environment variables from telegram.env file
# This file contains TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
load_dotenv("/root/.openskills/env/telegram.env")


# ════════════════════════════════════════════════════════════════════════════
# CLASS: TelegramSender
# Purpose: Handle all Telegram API communication
# ════════════════════════════════════════════════════════════════════════════

class TelegramSender:
    
    # ════════════════════════════════════════════════════════════════════════
    # __init__() - Initialize Telegram connection
    # Purpose: Load credentials from environment and validate them
    # ════════════════════════════════════════════════════════════════════════
    
    def __init__(self):
        # Load bot token from environment variable
        # This is the unique token for your Telegram bot
        # Format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz...
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        # Load chat ID from environment variable
        # This is the numeric ID of the Telegram chat to send messages to
        # Format: 123456789 (usually starts with - for groups)
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        # Validate that both credentials are present
        # If either is missing, raise error immediately
        if not self.token or not self.chat_id:
            raise ValueError("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in env")

    # ════════════════════════════════════════════════════════════════════════
    # send_message() - Send text message to Telegram
    # Purpose: Send text with automatic chunking for long messages
    # Arguments:
    #   text (str): Message content to send
    #   parse_mode (str): 'Markdown', 'HTML', or None (default plain text)
    # Returns: bool - True if all chunks sent successfully
    # ════════════════════════════════════════════════════════════════════════
    
    def send_message(self, text, parse_mode=None):
        """
        Send a text message to the configured Telegram chat.
        Automatically splits long messages (>4000 chars).

        Args:
            text (str): The message content
            parse_mode (str): 'Markdown', 'HTML', or None.
                              WARNING: Markdown is strict and errors easily with special chars.
                              Default is None (plain text) for safety with raw content.
        """
        # Telegram Bot API endpoint for sending messages
        # Uses the bot token for authentication
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        # Telegram has a hard limit of 4096 characters per message
        # We use 3500 to be safe and leave room for formatting overhead
        # (like message numbering "[1/3]")
        chunk_size = 3500

        # Split message into chunks if it exceeds the limit
        # List comprehension: create list of text segments
        # range(0, len(text), chunk_size) gives starting positions
        chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
        total_chunks = len(chunks)

        # Print progress information
        print(f"📤 Sending {total_chunks} message chunk(s) to Telegram...")

        # Process each chunk
        # enumerate(chunks, 1) gives (index, content) starting from 1
        for i, chunk in enumerate(chunks, 1):
            
            # If message was split, add chunk indicator
            if total_chunks > 1:
                # Create header showing current chunk and total
                header = f"[{i}/{total_chunks}] "
                # Combine header with chunk content
                chunk_content = f"{header}\n{chunk}"
            else:
                # No indicator needed if only 1 chunk
                chunk_content = chunk

            # Build the API request payload
            payload = {
                "chat_id": self.chat_id,    # Where to send the message
                "text": chunk_content        # Message content
            }

            # Add parse_mode if specified
            # This tells Telegram how to format the message
            if parse_mode:
                payload["parse_mode"] = parse_mode

            try:
                # Send HTTP POST request to Telegram API
                # json=payload automatically serializes Python dict to JSON
                # timeout=20 prevents hanging if API is slow
                response = requests.post(url, json=payload, timeout=20)
                
                # Raise exception if HTTP status indicates error (4xx, 5xx)
                response.raise_for_status()
                
                # Rate limiting: wait 0.5 seconds between messages
                # Prevents hitting Telegram's rate limits
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                # Network error occurred
                print(f"❌ Error sending chunk {i}: {e}")
                
                # Try to print API error response if available
                if hasattr(e, "response") and e.response:
                    print(f"Response: {e.response.text}")
                
                # Return False to indicate failure
                return False

        # All chunks sent successfully
        print(f"✅ All chunks sent successfully!")
        return True

    # ════════════════════════════════════════════════════════════════════════
    # send_document() - Send file to Telegram
    # Purpose: Upload a file to Telegram with optional caption
    # Arguments:
    #   file_path (str): Path to file to send (required)
    #   caption (str): Optional caption for the document
    # Returns: bool - True if successful
    # ════════════════════════════════════════════════════════════════════════
    
    def send_document(self, file_path, caption=""):
        """
        Send a document (file) to Telegram.

        Args:
            file_path (str): Path to file to send
            caption (str): Optional caption for the document

        Returns:
            bool: True if successful
        """
        # Check if file exists before attempting to send
        if not os.path.exists(file_path):
            # File not found - print error and return failure
            print(f"❌ File not found: {file_path}")
            return False

        # Calculate file size in MB for warning purposes
        # 1 MB = 1024 * 1024 bytes
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        # Warn if file exceeds Telegram's 50MB limit
        if file_size_mb > 50:
            print(
                f"⚠️  WARNING: File is {file_size_mb:.1f} MB. Telegram limit is 50 MB."
            )

        # Telegram Bot API endpoint for sending documents
        url = f"https://api.telegram.org/bot{self.token}/sendDocument"
        
        # Extract filename from path for display
        filename = os.path.basename(file_path)

        # Open file in binary read mode for uploading
        with open(file_path, "rb") as f:
            # Prepare multipart form data for file upload
            # files parameter tells requests to upload as multipart/form-data
            files = {"document": (filename, f)}
            
            # Additional form data (chat_id and caption)
            data = {"chat_id": self.chat_id, "caption": caption}

            try:
                # Send HTTP POST request with file
                # timeout=60 gives 60 seconds for large file upload
                response = requests.post(url, files=files, data=data, timeout=60)
                
                # Raise exception if HTTP status indicates error
                response.raise_for_status()
                
                # Parse JSON response (contains file_id if successful)
                result = response.json()
                
                # Print success message
                print(f"✅ Document sent: {filename}")
                return True
                
            except requests.exceptions.RequestException as e:
                # Error occurred during upload
                print(f"❌ Error sending document: {e}")
                return False

    # ════════════════════════════════════════════════════════════════════════
    # send_directory() - ZIP and send entire directory
    # Purpose: Create ZIP archive of directory and send to Telegram
    # Arguments:
    #   directory_path (str): Path to directory to send
    #   caption (str): Optional caption for the ZIP file
    # Returns: bool - True if successful
    # ════════════════════════════════════════════════════════════════════════
    
    def send_directory(self, directory_path, caption=""):
        """
        Create a ZIP of a directory and send it to Telegram.

        Args:
            directory_path (str): Path to directory to send
            caption (str): Optional caption

        Returns:
            bool: True if successful
        """
        # Check if directory exists
        if not os.path.isdir(directory_path):
            # Directory not found - print error and return failure
            print(f"❌ Directory not found: {directory_path}")
            return False

        # Extract directory name from path
        # .rstrip("/") removes trailing slash if present
        dirname = os.path.basename(directory_path.rstrip("/"))
        
        # Create ZIP filename in /tmp directory
        # /tmp is used as temporary storage for generated ZIP
        zip_path = f"/tmp/{dirname}.zip"

        # Create ZIP archive
        # zipfile.ZIP_DEFLATED enables compression
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Walk through directory tree
            # root: current directory path
            # dirs: subdirectories in current directory
            # files: files in current directory
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    # Build full path to file
                    file_path = os.path.join(root, file)
                    
                    # Calculate archive name (relative path within ZIP)
                    # Remove the base directory path to get relative path
                    arcname = file_path.replace(directory_path.rstrip("/") + "/", "")
                    
                    # Add file to ZIP with calculated archive name
                    zipf.write(file_path, arcname)

        # Calculate ZIP size for logging
        zip_size = os.path.getsize(zip_path) / 1024
        print(f"📦 Created ZIP: {zip_path} ({zip_size:.1f} KB)")

        # Send the created ZIP file
        # Recursively calls send_document() with the ZIP file
        return self.send_document(zip_path, caption)


# ════════════════════════════════════════════════════════════════════════════
# MAIN BLOCK - Command-line usage
# Only runs if script is executed directly (not imported)
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Import additional modules needed for CLI
    import sys                                      # sys.argv for arguments
    import argparse                                 # argparse for CLI parsing

    # Create argument parser for command-line interface
    parser = argparse.ArgumentParser(description="Send messages/files to Telegram")
    
    # Optional argument: --file / -f
    # Specify a file to send instead of a message
    parser.add_argument("--file", "-f", type=str, help="Path to file to send")
    
    # Optional argument: --directory / -d
    # Specify a directory to ZIP and send
    parser.add_argument(
        "--directory", "-d", type=str, help="Path to directory to send as ZIP"
    )
    
    # Positional argument: message
    # Remaining arguments are treated as message text or caption
    # nargs="*" means zero or more arguments
    parser.add_argument("message", nargs="*", help="Message text or caption for file")

    # Parse command-line arguments
    args = parser.parse_args()

    # Create TelegramSender instance
    # This loads credentials from environment
    sender = TelegramSender()

    # Route based on which arguments were provided
    
    if args.file:
        # --file flag was provided: send a file
        # Combine multiple message arguments into single caption string
        caption = " ".join(args.message) if args.message else ""
        sender.send_document(args.file, caption)
        
    elif args.directory:
        # --directory flag was provided: send a directory as ZIP
        # Combine multiple message arguments into single caption string
        caption = " ".join(args.message) if args.message else ""
        sender.send_directory(args.directory, caption)
        
    elif args.message:
        # No flags but message provided: send as plain text message
        # Join all message arguments into single message string
        sender.send_message(" ".join(args.message))
        
    else:
        # No arguments provided: send test message
        # Useful for verifying Telegram connection is working
        sender.send_message(
            "🤖 **RAG System Connected**\n\nTelegram integration is working correctly! ✅"
        )
```

## Class Diagram

```
┌─────────────────────────────────────┐
│       TelegramSender                │
├─────────────────────────────────────┤
│ Attributes:                         │
│  - token (bot token)                │
│  - chat_id (destination chat)       │
├─────────────────────────────────────┤
│ Methods:                            │
│  - __init__()                       │
│  - send_message(text, parse_mode)   │
│  - send_document(file_path, caption)│
│  - send_directory(dir_path, caption)│
└─────────────────────────────────────┘
```

## Key Features

### Message Chunking

```python
# Split messages longer than 3500 chars
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Add chunk counter
[1/3] First chunk...
[2/3] Second chunk...
[3/3] Final chunk...
```

### File Upload

```python
# Open file in binary mode and upload
with open(file_path, "rb") as f:
    files = {"document": (filename, f)}
    response = requests.post(url, files=files, data=data)
```

### Directory Compression

```python
# Walk directory tree and add all files to ZIP
for root, dirs, files in os.walk(directory_path):
    for file in files:
        zipf.write(file_path, arcname)
```

## Usage Examples

### Python Script

```python
# Direct usage
from telegram_sender import TelegramSender

sender = TelegramSender()

# Send message
sender.send_message("Task completed!")

# Send file
sender.send_document("/root/notes.txt", "My notes")

# Send directory
sender.send_directory("/root/loot", "Extracted files")
```

### Command Line

```bash
# Send message
python3 telegram_sender.py "Hello Telegram"

# Send file
python3 telegram_sender.py --file /root/exploit.py "Exploit script"

# Send directory
python3 telegram_sender.py --directory /root/loot "Extracted files"

# Test connection
python3 telegram_sender.py
```

---

**Next: [rag_to_telegram.py](rag_to_telegram_py.md) - RAG integration**
