# Data sources

| Data | Endpoint | Auth |
|------|----------|------|
| Profile + legacy rank | `GET /api/v4/profile/{PROFILE_ID}` | Public |
| Experience level | `GET /api/experience/v1/account/{ACCOUNT_ID}` | Public |
| Season league + rank | `GET /api/v4/season/user/{PROFILE_ID}/ranks` | Public |
| Machine progress (incl. OS) | `GET /api/v4/profile/progress/machines/{PROFILE_ID}` | Public |
| Challenges, fortresses, etc. | `GET /api/v4/profile/progress/*/{PROFILE_ID}` | Public |
| Activity | `GET /api/v5/user/profile/activity/{PROFILE_ID}` | Public |
| Machines catalog | `GET /api/v5/machines/` | App token |
| Tracks | `GET /api/v5/tracks/` | App token |
| Team rankings | `GET /api/v4/rankings` | App token |

Base URL: `https://labs.hackthebox.com`

## Public access

Your HTB profile must be set to **Public** (Profile → Settings → Privacy).

## Authenticated endpoints

When an app token is configured, the fetcher requests machines, tracks, and rankings. Without a token, these are **skipped** (no error).

See [Configuration → Authentication](configuration.md#authentication).

## Cache

Responses cache under `user/<profile_id>/data/`. See [Configuration → Cache](configuration.md#cache).

## Security

- Tokens are optional; passed only as `Authorization: Bearer` to auth endpoints
- Never commit tokens — use `.env` locally or GitHub Actions secrets in CI
