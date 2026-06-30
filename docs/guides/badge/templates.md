# Templates

Templates use `$key$` substitution. When `hide_if_null` is enabled, missing values render as empty strings.

## Available templates

| Name | Format | Description |
|------|--------|-------------|
| `classic` | HTML | HTB dark — avatar + stats + ranking |
| `compact` | HTML | Small single-row card |
| `profile-card` | HTML | Full stats grid + rank tiers |
| `rank-card` | HTML | Legacy / level / season focus |
| `season-card` | HTML | Season league highlight |
| `terminal` | HTML | Kali terminal aesthetic |
| `hacker-red` | HTML | Black + red accent |
| `hacker-yellow` | HTML | Black + yellow accent |
| `light` | HTML | Light theme |
| `minimal` | HTML | Inline badge |
| `github-classic` | HTML | GitHub-style light card |
| `github-plugin` | HTML | GitHub dark + progress bars |
| `github-metrics.*` | SVG | GitHub metrics-style SVG variants |
| `metrics-terminal` | SVG | Terminal-style SVG |

Select with `-t` / `--template` / `HTB_TEMPLATE`.

Preview PNGs for each template are in [`examples/badges/`](../../examples/badges/) (reference only — not copied to your repo). Your generated badges go in `output/`.

## Profile & identity

| Placeholder | Description |
|-------------|-------------|
| `$user_name$` | HTB username |
| `$user_rank$` | Legacy rank title |
| `$user_avatar$` | Avatar URL (HTML) |
| `$user_avatar_b64$` | Avatar data URI (SVG) |
| `$user_country$` | Country name |
| `$account_id$` | HTB account UUID |

## Flags & stats

| Placeholder | Description |
|-------------|-------------|
| `$user_owns$` | User flags |
| `$user_system_owns$` | Root flags |
| `$user_bloods$` | User bloods |
| `$user_system_bloods$` | Root bloods |
| `$user_challenge_bloods$` | Challenge bloods |
| `$user_points$` | Points |
| `$user_respects$` | Respects |
| `$user_ranking$` | Global rank |

## Experience

| Placeholder | Description |
|-------------|-------------|
| `$level_number$` | Level |
| `$level_title$` | Level title |
| `$level_grade$` | Grade |
| `$level_xp_total$` | Total XP |
| `$level_streak$` | Streak counter |
| `$level_image_url$` | Rank badge URL |
| `$level_bg_url$` | Rank background URL |

## Season

| Placeholder | Description |
|-------------|-------------|
| `$season_name$` | Season name |
| `$season_league$` | League tier |
| `$season_rank$` | Season rank |
| `$season_rank_suffix$` | Ordinal suffix |
| `$season_points$` | Season points |
| `$season_flags_obtained$` | Flags obtained |
| `$season_flags_total$` | Flags total |

## Team

| Placeholder | Description |
|-------------|-------------|
| `$team_name$` | Team name |
| `$team_id$` | Team ID |
| `$team_ranking$` | Team rank |
| `$team_avatar$` | Team logo URL |

## Progress bars (CSS `width` %)

| Placeholder | Based on |
|-------------|----------|
| `$user_owns_bar_pct$` | User flags / 200 |
| `$user_system_owns_bar_pct$` | Root flags / 200 |
| `$season_points_bar_pct$` | Season points / 2000 |
| `$level_xp_bar_pct$` | Total XP / 150000 |

## Metadata

| Placeholder | Description |
|-------------|-------------|
| `$last_activity$` | Last activity date |
| `$last_update$` | Generation timestamp (UTC) |
