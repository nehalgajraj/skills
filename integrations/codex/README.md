# Codex Integration Assets

Codex does not expose Claude-style multi-event hooks (`PreToolUse`, `PostToolUse`, `Stop`) in config.

Codex supports a `notify` command that is called on `agent-turn-complete` events.
Use this folder to implement hook-like behavior for Codex.
This is most useful in interactive Codex sessions where the agent is waiting for user input.

Files:
- `notify/notify_audit.py` - logs turn-complete notifications into `docs/sessions/.audit/<thread-id>.jsonl`
- `notify/config.snippet.toml` - minimal config snippet for `~/.codex/config.toml`

Setup:
1. Edit `notify/config.snippet.toml` with your absolute repo path.
2. Add the `notify = [...]` line to `~/.codex/config.toml`.
3. Run Codex in the repo and verify JSONL entries are created under `docs/sessions/.audit/`.
