# send_directory.py - Directory Sender

**File**: `/home/kali/Desktop/RAG/send_directory.py`  
**Lines**: 151  
**Class**: `DirectorySender`  
**Purpose**: ZIP and send directories to Telegram

## Complete Annotated Script (Key Sections)

```python
#!/usr/bin/env python3
"""
Send Directory to Telegram
Creates a ZIP of a directory and sends it to Telegram.
"""

import os
import sys
import zipfile
import requests
from dotenv import load_dotenv

# Load Telegram credentials
load_dotenv("/root/.openskills/env/telegram.env")

# ════════════════════════════════════════════════════════════════════════════
# CLASS: DirectorySender
# ════════════════════════════════════════════════════════════════════════════

class DirectorySender:
    
    def __init__(self):
        # Load credentials from environment
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        # Validate credentials
        if not self.token or not self.chat_id:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

    # ════════════════════════════════════════════════════════════════════════
    # create_zip() - Compress directory
    # ════════════════════════════════════════════════════════════════════════
    
    def create_zip(self, directory, output_path=None):
        """
        Create a ZIP file from a directory.
        
        Args:
            directory (str): Path to directory to compress
            output_path (str): Output ZIP file path (auto-generated if None)
        
        Returns:
            str: Path to created ZIP file
        """
        # Validate directory exists
        if not os.path.isdir(directory):
            raise ValueError(f"Directory does not exist: {directory}")

        # Auto-generate output path if not specified
        if output_path is None:
            # Extract directory name
            dirname = os.path.basename(directory.rstrip("/"))
            # Create output path in /tmp
            output_path = f"/tmp/{dirname}.zip"

        # Create ZIP archive with compression
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Walk through directory tree
            for root, dirs, files in os.walk(directory):
                for file in files:
                    # Build full file path
                    file_path = os.path.join(root, file)
                    
                    # Calculate relative path for archive
                    arcname = file_path.replace(directory.rstrip("/") + "/", "")
                    
                    # Add file to ZIP
                    zipf.write(file_path, arcname)

        # Calculate and report ZIP size
        size_kb = os.path.getsize(output_path) / 1024
        print(f"📦 Created ZIP: {output_path} ({size_kb:.1f} KB)")
        return output_path

    # ════════════════════════════════════════════════════════════════════════
    # send_zip() - Upload ZIP to Telegram
    # ════════════════════════════════════════════════════════════════════════
    
    def send_zip(self, zip_path, caption=""):
        """
        Send a ZIP file to Telegram.
        
        Args:
            zip_path (str): Path to ZIP file
            caption (str): Optional caption
        
        Returns:
            bool: True if successful
        """
        # Validate ZIP exists
        if not os.path.exists(zip_path):
            raise ValueError(f"ZIP file not found: {zip_path}")

        # Check file size
        file_size = os.path.getsize(zip_path) / (1024 * 1024)
        if file_size > 50:
            print(f"⚠️  WARNING: File is {file_size:.1f} MB. Telegram limit is 50 MB.")

        # Telegram API endpoint
        url = f"https://api.telegram.org/bot{self.token}/sendDocument"

        # Open and send file
        with open(zip_path, "rb") as f:
            # Prepare multipart form data
            files = {"document": ("archive.zip", f, "application/zip")}
            data = {"chat_id": self.chat_id, "caption": caption}

            try:
                # POST to Telegram API
                response = requests.post(url, files=files, data=data, timeout=60)
                response.raise_for_status()
                
                # Parse result
                result = response.json()
                print(f"✅ ZIP sent successfully!")
                return True
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Error sending ZIP: {e}")
                return False

    # ════════════════════════════════════════════════════════════════════════
    # send_directory() - Complete workflow
    # ════════════════════════════════════════════════════════════════════════
    
    def send_directory(self, directory, caption=""):
        """
        Complete workflow: ZIP directory and send to Telegram.
        """
        print(f"📤 Preparing to send: {directory}")
        
        # 1. Create ZIP
        zip_path = self.create_zip(directory)
        
        # 2. Send ZIP
        success = self.send_zip(zip_path, caption)
        
        # 3. Report result
        if success:
            print(f"🎉 Directory sent to Telegram!")

        return success

# ════════════════════════════════════════════════════════════════════════════
# MAIN - Command-line interface
# ════════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 send_directory.py /path/to/directory [caption]")
        sys.exit(1)

    directory = sys.argv[1]
    caption = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    sender = DirectorySender()
    sender.send_directory(directory, caption)

if __name__ == "__main__":
    main()
```

## Workflow

```
User Input: Directory Path
      ↓
DirectorySender.__init__()
      ├─ Load TELEGRAM_BOT_TOKEN
      └─ Load TELEGRAM_CHAT_ID
      ↓
send_directory()
      ├─ Validate directory exists
      ├─ create_zip()
      │  └─ Walk directory tree
      │  └─ Add files to ZIP
      │  └─ Return ZIP path
      └─ send_zip()
         ├─ Check file size (<50MB)
         ├─ POST to Telegram API
         └─ Return success/failure
      ↓
Result
```

## Usage

### Python Script
```python
from send_directory import DirectorySender

sender = DirectorySender()

# Send directory
sender.send_directory(
    "/root/loot",
    "Extracted files from FACTS machine"
)
```

### Command Line
```bash
# Direct Python execution
python3 send_directory.py /root/loot "My notes"

# Via STT alias
stt directory /root/loot "Extracted files"
```

## Error Handling

```python
try:
    response = requests.post(url, files=files, data=data, timeout=60)
    response.raise_for_status()
    print("✅ Success")
except requests.exceptions.RequestException as e:
    print(f"❌ Error: {e}")
    # Handle error gracefully
```

---

**Next: [Usage Examples](usage-examples.md)**
