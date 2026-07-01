# Usage

All examples assume you run from the repo root. Adjust paths if you installed an alias.

## General

```bash
python htbctrl.py cli                  # Show help menu
python htbctrl.py cli --help           # Same
```

![htbcli](../../../src/htb_cli/assets/01.jpg)

---

## Machines

```bash
# List active machines
python htbctrl.py cli machines

# List retired machines (VIP)
python htbctrl.py cli machines --retired

# Search by name (active + retired)
python htbctrl.py cli machines --search "Sau"

# Filter by OS and difficulty
python htbctrl.py cli machines --os linux --diff Easy

# Show only unowned machines
python htbctrl.py cli machines --pending

# Show only fully owned machines
python htbctrl.py cli machines --owned

# Limit results
python htbctrl.py cli machines --limit 10

# Force refresh (ignore cache)
python htbctrl.py cli machines --refresh
```

![machines](../../../src/htb_cli/assets/07.jpg)
![machines-retired](../../../src/htb_cli/assets/08.jpg)

---

## Machine info

```bash
# Detailed view with avatar (Kitty), difficulty, rating, tags, solves
python htbctrl.py cli machine-info --id 573
```

![machine-info](../../../src/htb_cli/assets/11.jpg)

---

## Submit flags

```bash
# Submit flag (auto-detects user or root based on owned state)
python htbctrl.py cli submit --id 573 --flag abc123...def456

# Submit explicitly as root
python htbctrl.py cli submit --id 573 --flag abc123...def456 --type root

# With perceived difficulty (1–10 scale, like HTB)
python htbctrl.py cli submit --id 573 --flag abc123...def456 --diff 4
```

![submit](../../../src/htb_cli/assets/06.jpg)

> [!TIP]
> **Auto-detection:** If you already own the user flag, the next submit goes as root automatically. If both are owned, you get a warning instead of a failure.

---

## Lab control

```bash
# Start a machine
python htbctrl.py cli spawn --id 573

# Use VIP server
python htbctrl.py cli spawn --id 573 --vip

# Show active machine + IP
python htbctrl.py cli active

# Stop (auto-detects active machine)
python htbctrl.py cli stop

# Reset
python htbctrl.py cli reset
```

![spawn](../../../src/htb_cli/assets/05.jpg)
![active](../../../src/htb_cli/assets/09.jpg)

---

## Profile

```bash
# Show your profile stats
python htbctrl.py cli profile
```

---

## Cache

```bash
# Show cache status
python htbctrl.py cli cache

# Clear cache
python htbctrl.py cli cache --clear
```

![cache](../../../src/htb_cli/assets/12.jpg)

## See also

- [Configuration](configuration.md) — config paths and avatar sizing
- [Troubleshooting](troubleshooting.md) — common errors
