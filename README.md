
# Storage-Optimizer - Duplicate File Management Utility


![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Automation](https://img.shields.io/badge/Automation-Scheduled%20Task-orange.svg)

> A powerful Python script that detects and removes duplicate files in a directory using checksum logic and emails a detailed log report to the specified recipient — fully automated on a scheduled basis.

---

## Features

- ✅ Recursively scans directories and subdirectories
- ✅ Detects duplicate files using **MD5 checksum**
- ✅ Deletes duplicate files automatically
- ✅ Generates a structured log file of deleted files
- ✅ Sends the log via **email (Gmail SMTP)**
- ✅ Supports scheduling with `schedule` module

---

## Technologies Used

- `os` – File and directory operations  
- `hashlib` – MD5 checksum for duplicate detection  
- `smtplib`, `email.mime` – Sending email with attachments  
- `schedule` – Periodic task execution  
- `sys`, `time` – System and time handling

---

## Installation

```bash
git clone https://github.com/premc5731/storage-optimizer.git
cd storage-optimizer
pip install schedule
```

---

## Usage

Run the script from the command line:

```bash
python delete_duplicates_with_email_log.py <DirectoryPath> <TimeIntervalInMinutes> <RecipientEmail>
```

### Example:

```bash
python delete_duplicates_with_email_log.py "C:\Users\prem\Documents" 30 receiver@example.com
```

This will:
- Scan the given directory every 30 minutes
- Remove duplicate files
- Create a log file
- Email the log to `receiver@example.com`

---

## Command Line Options

| Flag     | Description                                |
|----------|--------------------------------------------|
| `--h`    | Show help message                          |
| `--u`    | Show usage instructions                    |

---

## Log File Output

The script generates a log like this:
```
--------------------------------------------------------------------------------
This is a log file of delete_duplicate_files automation script
--------------------------------------------------------------------------------
<filepath1> deleted at : <timestamp>
<filepath2> deleted at : <timestamp>
...
Total deleted files : X
This file is created at <timestamp>
--------------------------------------------------------------------------------
```

## Email Report Format

Subject: `Delete Duplicate Files`  
Body includes:
- Start time of scan
- Total scanned files
- Total duplicate files found

Attached: Log file

---

## Automation

This script uses `schedule` to run at fixed intervals (e.g., every 30 minutes). It continuously checks for duplicate files without user interaction.

---

## Sample Output

![Sample Output](https://img.shields.io/badge/Output-Demo-blue?logo=python)

```bash
Automation Script Starting...
Total deleted files : 12
Email sent successfully
```

---

## Contributing

Pull requests are welcome!  
To contribute:
- Fork this repo

- Commit your changes
- Open a PR

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for more info.

---

## Acknowledgements

Special thanks to Python’s core modules and the open-source community.

---

## Show your support

If you like this project, give it a ⭐ on GitHub and share it!
