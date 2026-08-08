#!/usr/bin/env bash
# PostToolUse hook: logs edits and commands to per-session JSONL audit file.
# Receives JSON on stdin with: session_id, tool_name, tool_input, transcript_path
#
# Only logs Write, Edit, Bash, and NotebookEdit tool uses.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AUDIT_DIR="$PROJECT_ROOT/docs/sessions/.audit"
mkdir -p "$AUDIT_DIR"

# Read hook input from stdin
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('session_id','unknown'))" 2>/dev/null || echo "unknown")

# Only log file-modifying and command tools
case "$TOOL_NAME" in
    Write|Edit|Bash|NotebookEdit)
        ;;
    *)
        exit 0
        ;;
esac

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Extract a summary of the input (file path or command)
SUMMARY=$(echo "$INPUT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ti = d.get('tool_input', {})
tool = d.get('tool_name', '')
if tool == 'Edit':
    print(f\"Edit {ti.get('file_path', '?')}\")
elif tool == 'Write':
    print(f\"Write {ti.get('file_path', '?')}\")
elif tool == 'Bash':
    cmd = ti.get('command', '')
    print(f\"Bash: {cmd[:120]}\")
elif tool == 'NotebookEdit':
    print(f\"NotebookEdit {ti.get('notebook_path', '?')}\")
else:
    print(tool)
" 2>/dev/null || echo "$TOOL_NAME")

# Append to session audit log
echo "{\"ts\":\"$TIMESTAMP\",\"tool\":\"$TOOL_NAME\",\"summary\":$(echo "$SUMMARY" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))')}" >> "$AUDIT_DIR/${SESSION_ID}.jsonl"
