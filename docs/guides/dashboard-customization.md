# Customization

## Add a new technique badge

1. Create a CSS class `.badge-<name>` with a matte color and blur:

```css
.badge-my-tech {
    background: rgba(120, 80, 200, 0.35);
    backdrop-filter: blur(8px);
    color: #fff;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}
```

2. Ensure `getTechBadge(tech)` normalizes names correctly:

```javascript
tech.toLowerCase().replace(/\s+/g, '-')
```

The function maps normalized technique names to badge classes.

## Difficulty and OS badges

These are applied automatically from spreadsheet values:

- **Windows** → blue badge
- **Linux** → orange badge
- **Easy / Intermediate / Hard / Insane** → green / yellow / red / purple

## Reverse table order

By default the table keeps Excel row order. To show newest entries first, reverse the JSON array before rendering:

```javascript
json.reverse()
```

Edit the relevant section in `index.html` where rows are prepared for `createTable()`.

## Font

The dashboard uses **Hack Nerd Font** from `assets/HackNerdFont-Regular.ttf` for a terminal aesthetic. Replace the file or update the `@font-face` rule in `index.html` to use a different typeface.

## See also

- [Features](dashboard-features.md) — what each column shows
- [Development](dashboard-development.md) — full data loading flow
