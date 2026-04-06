# File: c:\Users\under\OneDrive\Desktop\HONEYBOMBV2\cowrie_full_session_report.py
#!/usr/bin/env python3
import json
from datetime import datetime, timedelta
from pathlib import Path
import glob
import argparse # Import argparse

# Define the log file pattern
LOG_FILE_PATTERN = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json.2025-*"

# Find the latest log file based on the pattern
log_files = sorted(glob.glob(LOG_FILE_PATTERN))
LOG_PATH = Path(log_files[-1]) if log_files else None

# Modified summarize_sessions to accept either a file path or a list of entries
def summarize_sessions(source_data):
    """
    Summarizes Cowrie sessions from either a log file path or a list of log entries.
    """
    summary = {
        "total_sessions": 0,
        "ips": {},
        "commands": [],
        "usernames": [],
        "passwords": [],
        "sessions": []
    }

    entries_to_process = []

    # Determine if source_data is a file path or a list of entries
    if isinstance(source_data, (str, Path)):
        log_file_path = Path(source_data)
        if not log_file_path.exists():
            # Return an error message if the file doesn't exist
            return f"Error: Cowrie log not found at {log_file_path}."
        try:
            with open(log_file_path, 'r') as f:
                for line in f:
                    try:
                        entries_to_process.append(json.loads(line))
                    except json.JSONDecodeError:
                        # Skip lines that are not valid JSON, print a warning
                        print(f"Warning: Skipping invalid JSON line in {log_file_path}: {line.strip()}")
                        continue
        except Exception as e:
             # Return an error message for file reading issues
             return f"Error reading log file {log_file_path}: {e}"

    elif isinstance(source_data, list):
        entries_to_process = source_data
    else:
        # Return an error message for invalid input type
        return "Error: Invalid data source provided to summarize_sessions."

    # Process the collected entries
    for entry in entries_to_process:
        try:
            if entry.get("eventid") == "cowrie.session.connect":
                summary["total_sessions"] += 1
                ip = entry.get("src_ip")
                if ip:
                    summary["ips"][ip] = summary["ips"].get(ip, 0) + 1
            elif entry.get("eventid") == "cowrie.command.input":
                summary["commands"].append(entry.get("input", ""))
            elif entry.get("eventid") == "cowrie.login.failed":
                summary["usernames"].append(entry.get("username", ""))
                summary["passwords"].append(entry.get("password", ""))
            # Add other event types you want to summarize here
        except Exception as e:
            # Catch errors during processing a specific entry, print a warning
            print(f"Warning: Error processing entry: {entry}. Error: {e}")
            continue

    # --- Generate Report String ---
    report_lines = []
    report_lines.append(f"=== Cowrie Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===") # Added time to timestamp
    # Indicate if the report is filtered
    if isinstance(source_data, list):
         report_lines.append(f"Filtered entries processed: {len(entries_to_process)}")
         # Add timeframe info if available (requires passing args or delta) - keeping it simple for now
         # report_lines.append(f"Timeframe: Last {days} days, {minutes} minutes")


    report_lines.append(f"Total Sessions (connect events): {summary['total_sessions']}")
    report_lines.append("Top IPs:")
    if summary["ips"]:
        # Sort IPs by count descending and take top 5
        sorted_ips = sorted(summary["ips"].items(), key=lambda x: x[1], reverse=True)[:5]
        for ip, count in sorted_ips:
            report_lines.append(f" - {ip}: {count} attempts")
    else:
        report_lines.append(" - No IP data available in the selected timeframe/source.")

    # You can add summaries for commands, usernames, and passwords here if desired
    # report_lines.append(f"Total Commands Executed: {len(summary['commands'])}")
    # report_lines.append(f"Total Failed Login Attempts: {len(summary['usernames'])}")

    return "\n".join(report_lines) # Join lines into a single string

#Log Filtering Function
def filter_logs_by_timeframe(log_file_path, days=0, minutes=0):
    """
    Returns log entries from the last X days/minutes from a given log file.
    """
    now = datetime.utcnow()
    delta = timedelta(days=days, minutes=minutes)
    filtered_entries = []

    log_file = Path(log_file_path) # Ensure it's a Path object
    if not log_file.exists():
        print(f"Error: Log file not found at {log_file}.")
        return [] # Return empty list if file not found

    with open(log_file, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                timestamp = entry.get("timestamp")
                if timestamp:
                    try:
                        # Parse timestamp and compare
                        # Use fromisoformat for Python 3.7+ or handle Z manually
                        # entry_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        # Using strptime for broader compatibility, handle potential errors
                        entry_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                        if now - entry_time <= delta:
                            filtered_entries.append(entry)
                    except ValueError:
                        print(f"Warning: Skipping line due to invalid timestamp format: {timestamp}")
                        continue
            except json.JSONDecodeError:
                # Skip lines that are not valid JSON, print a warning
                print(f"Warning: Skipping invalid JSON line: {line.strip()}")
                continue
            except Exception as e:
                # Catch other potential errors during processing a line, print a warning
                print(f"Warning: Error processing line: {e}")
                continue

    return filtered_entries

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cowrie Session Full or Filtered Report")
    parser.add_argument("--days", type=int, default=0, help="Filter logs from the last X days")
    parser.add_argument("--minutes", type=int, default=0, help="Filter logs from the last X minutes")
    # Add the new --output argument
    parser.add_argument("--output", type=str, help="Path to output file (optional)")
    args = parser.parse_args()

    # Use the latest log file found by glob, or handle if none exist
    if not LOG_PATH:
        error_message = f"Error: No Cowrie log files found matching the pattern {LOG_FILE_PATTERN}"
        if args.output:
             # If output file is specified, write the error there too
             try:
                 Path(args.output).write_text(error_message)
                 print(f"[!] Error report written to {args.output}")
             except Exception as e:
                 print(f"[!] Could not write error report to {args.output}: {e}")
             print(error_message) # Also print to console
        else:
            print(error_message)
        exit(1) # Exit with a non-zero status code to indicate an error

    # Determine the data source based on arguments
    if args.days > 0 or args.minutes > 0:
        # If filtering is requested, get the filtered entries list
        print(f"Filtering logs from the last {args.days} days and {args.minutes} minutes...")
        source_data = filter_logs_by_timeframe(LOG_PATH, days=args.days, minutes=args.minutes)
        # Check if filtering returned an empty list (e.g., file not found or no entries)
        if not source_data and Path(LOG_PATH).exists():
             print("No entries found matching the specified timeframe.")
             # Optionally generate an empty report or just exit
             report = "=== Cowrie Filtered Summary - No entries found ===\n"
             report += f"Timeframe: Last {args.days} days, {args.minutes} minutes\n"
             report += "Total Sessions (connect events): 0\n"
             report += "Top IPs:\n - No IP data available in the selected timeframe/source."
        elif not source_data and not Path(LOG_PATH).exists():
             # filter_logs_by_timeframe already printed an error, just set report to None
             report = None # Indicate no report could be generated
        else:
             # Pass the list of entries to summarize_sessions
             report = summarize_sessions(source_data)
    else:
        # If no filtering is requested, pass the file path for the full report
        print(f"Generating full report from {LOG_PATH}...")
        source_data = LOG_PATH # Set source_data to the file path
        report = summarize_sessions(source_data)

    # --- Output the report ---
    # Check if summarize_sessions returned an error string
    if report and report.startswith("Error:"):
         if args.output:
             try:
                 Path(args.output).write_text(report)
                 print(f"[!] Error report written to {args.output}")
             except Exception as e:
                 print(f"[!] Could not write error report to {args.output}: {e}")
             print(report) # Also print to console
         else:
             print(report)
         exit(1) # Exit with error status
    elif report: # If report was generated successfully (not None and not an error string)
        if args.output:
            try:
                Path(args.output).write_text(report)
                print(f"[+] Report successfully written to {args.output}")
            except Exception as e:
                print(f"[!] Error writing report to {args.output}: {e}")
                print(report) # Print to console if writing fails
                exit(1) # Exit with error status
        else:
            print(report)
    # If report is None (e.g., filter_logs_by_timeframe failed and returned []),
    # the relevant messages were already printed.
