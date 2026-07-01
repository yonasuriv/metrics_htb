# Usage

All examples assume you run from the repo root or have `htbctrl` on your PATH.

## General

```bash
htbctrl                  # Show help menu
htbctrl --help           # Same
```

---

## Machines

```bash
# List active machines
htbctrl machines

# List retired machines (VIP)
htbctrl machines --retired

# Search by name (active + retired)
htbctrl machines --search "Sau"

# Filter by OS and difficulty
htbctrl machines --os linux --diff Easy

# Show only unowned machines
htbctrl machines --pending

# Show only fully owned machines
htbctrl machines --owned

# Limit results
htbctrl machines --limit 10

# Force refresh (ignore cache)
htbctrl machines --refresh
```

---

## Machine info

```bash
# Detailed view with avatar (Kitty), difficulty, rating, tags, solves
htbctrl machine --id 573
```

---

## Submit flags

```bash
# Submit flag (auto-detects user or root based on owned state)
htbctrl submit --id 573 --flag abc123...def456

# Submit explicitly as root
htbctrl submit --id 573 --flag abc123...def456 --type root

# With perceived difficulty (1–10 scale, like HTB)
htbctrl submit --id 573 --flag abc123...def456 --diff 4
```

> [!TIP]
> **Auto-detection:** If you already own the user flag, the next submit goes as root automatically. If both are owned, you get a warning instead of a failure.

---

## Lab control

```bash
# Start a machine
htbctrl spawn --id 573

# Use VIP server
htbctrl spawn --id 573 --vip

# Show active machine + IP
htbctrl active

# Stop (auto-detects active machine)
htbctrl stop

# Reset
htbctrl reset
```

---

## Profile

```bash
# Show your profile stats
htbctrl profile
```

---

## Cache

```bash
# Show cache status
htbctrl cache

# Clear cache
htbctrl cache --clear
```

## See also

- [Configuration](configuration.md) — config paths and avatar sizing
- [Troubleshooting](cli-troubleshooting.md) — common errors
