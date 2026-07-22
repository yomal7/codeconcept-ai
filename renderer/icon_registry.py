"""Icon registry: real Lucide icon geometry (https://lucide.dev, ISC license),
baked in at build time so there is no Node/npm runtime dependency -- just
this one Python file. Each entry is the INNER markup of a Lucide SVG (its
<svg viewBox="0 0 24 24" stroke="currentColor" ...> wrapper is applied by
renderer/svg_diagram.py instead, so icons inherit the theme's accent color).

Curated subset of ~75 icons covering common educational/tech content.
Planner Agent should only request names from ICON_NAMES; any other name
(or a typo) safely falls back to "circle-help" -- see get_icon().
"""

_ICONS: dict[str, str] = {
    "server": "<rect width='20' height='8' x='2' y='2' rx='2' ry='2' /> <rect width='20' height='8' x='2' y='14' rx='2' ry='2' /> <line x1='6' x2='6.01' y1='6' y2='6' /> <line x1='6' x2='6.01' y1='18' y2='18' />",
    "database": "<ellipse cx='12' cy='5' rx='9' ry='3' /> <path d='M3 5V19A9 3 0 0 0 21 19V5' /> <path d='M3 12A9 3 0 0 0 21 12' />",
    "cloud": "<path d='M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z' />",
    "cpu": "<path d='M12 20v2' /> <path d='M12 2v2' /> <path d='M17 20v2' /> <path d='M17 2v2' /> <path d='M2 12h2' /> <path d='M2 17h2' /> <path d='M2 7h2' /> <path d='M20 12h2' /> <path d='M20 17h2' /> <path d='M20 7h2' /> <path d='M7 20v2' /> <path d='M7 2v2' /> <rect x='4' y='4' width='16' height='16' rx='2' /> <rect x='8' y='8' width='8' height='8' rx='1' />",
    "package": "<path d='M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z' /> <path d='M12 22V12' /> <polyline points='3.29 7 12 12 20.71 7' /> <path d='m7.5 4.27 9 5.15' />",
    "shield": "<path d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z' />",
    "shield-check": "<path d='M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z' /> <path d='m9 12 2 2 4-4' />",
    "globe": "<circle cx='12' cy='12' r='10' /> <path d='M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20' /> <path d='M2 12h20' />",
    "lock": "<rect width='18' height='11' x='3' y='11' rx='2' ry='2' /> <path d='M7 11V7a5 5 0 0 1 10 0v4' />",
    "lock-open": "<rect width='18' height='11' x='3' y='11' rx='2' ry='2' /> <path d='M7 11V7a5 5 0 0 1 9.9-1' />",
    "network": "<rect x='16' y='16' width='6' height='6' rx='1' /> <rect x='2' y='16' width='6' height='6' rx='1' /> <rect x='9' y='2' width='6' height='6' rx='1' /> <path d='M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3' /> <path d='M12 12V8' />",
    "container": "<path d='M22 7.7c0-.6-.4-1.2-.8-1.5l-6.3-3.9a1.72 1.72 0 0 0-1.7 0l-10.3 6c-.5.2-.9.8-.9 1.4v6.6c0 .5.4 1.2.8 1.5l6.3 3.9a1.72 1.72 0 0 0 1.7 0l10.3-6c.5-.3.9-1 .9-1.5Z' /> <path d='M10 21.9V14L2.1 9.1' /> <path d='m10 14 11.9-6.9' /> <path d='M14 19.8v-8.1' /> <path d='M18 17.5V9.4' />",
    "monitor": "<rect width='20' height='14' x='2' y='3' rx='2' /> <line x1='8' x2='16' y1='21' y2='21' /> <line x1='12' x2='12' y1='17' y2='21' />",
    "smartphone": "<rect width='14' height='20' x='5' y='2' rx='2' ry='2' /> <path d='M12 18h.01' />",
    "laptop": "<path d='M18 5a2 2 0 0 1 2 2v8.526a2 2 0 0 0 .212.897l1.068 2.127a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45l1.068-2.127A2 2 0 0 0 4 15.526V7a2 2 0 0 1 2-2z' /> <path d='M20.054 15.987H3.946' />",
    "key": "<path d='m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4' /> <path d='m21 2-9.6 9.6' /> <circle cx='7.5' cy='15.5' r='5.5' />",
    "terminal": "<path d='M12 19h8' /> <path d='m4 17 6-6-6-6' />",
    "code": "<path d='m16 18 6-6-6-6' /> <path d='m8 6-6 6 6 6' />",
    "git-branch": "<path d='M15 6a9 9 0 0 0-9 9V3' /> <circle cx='18' cy='6' r='3' /> <circle cx='6' cy='18' r='3' />",
    "git-commit": "<circle cx='12' cy='12' r='3' /> <line x1='3' x2='9' y1='12' y2='12' /> <line x1='15' x2='21' y1='12' y2='12' />",
    "git-pull-request": "<circle cx='18' cy='18' r='3' /> <circle cx='6' cy='6' r='3' /> <path d='M13 6h3a2 2 0 0 1 2 2v7' /> <line x1='6' x2='6' y1='9' y2='21' />",
    "layers": "<path d='M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z' /> <path d='M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12' /> <path d='M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17' />",
    "box": "<path d='M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z' /> <path d='m3.3 7 8.7 5 8.7-5' /> <path d='M12 22V12' />",
    "boxes": "<path d='M2.97 12.92A2 2 0 0 0 2 14.63v3.24a2 2 0 0 0 .97 1.71l3 1.8a2 2 0 0 0 2.06 0L12 19v-5.5l-5-3-4.03 2.42Z' /> <path d='m7 16.5-4.74-2.85' /> <path d='m7 16.5 5-3' /> <path d='M7 16.5v5.17' /> <path d='M12 13.5V19l3.97 2.38a2 2 0 0 0 2.06 0l3-1.8a2 2 0 0 0 .97-1.71v-3.24a2 2 0 0 0-.97-1.71L17 10.5l-5 3Z' /> <path d='m17 16.5-5-3' /> <path d='m17 16.5 4.74-2.85' /> <path d='M17 16.5v5.17' /> <path d='M7.97 4.42A2 2 0 0 0 7 6.13v4.37l5 3 5-3V6.13a2 2 0 0 0-.97-1.71l-3-1.8a2 2 0 0 0-2.06 0l-3 1.8Z' /> <path d='M12 8 7.26 5.15' /> <path d='m12 8 4.74-2.85' /> <path d='M12 13.5V8' />",
    "workflow": "<rect width='8' height='8' x='3' y='3' rx='2' /> <path d='M7 11v4a2 2 0 0 0 2 2h4' /> <rect width='8' height='8' x='13' y='13' rx='2' />",
    "alert-triangle": "<path d='m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3' /> <path d='M12 9v4' /> <path d='M12 17h.01' />",
    "check-circle": "<path d='M21.801 10A10 10 0 1 1 17 3.335' /> <path d='m9 11 3 3L22 4' />",
    "x-circle": "<circle cx='12' cy='12' r='10' /> <path d='m15 9-6 6' /> <path d='m9 9 6 6' />",
    "check": "<path d='M20 6 9 17l-5-5' />",
    "x": "<path d='M18 6 6 18' /> <path d='m6 6 12 12' />",
    "zap": "<path d='M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z' />",
    "wifi": "<path d='M12 20h.01' /> <path d='M2 8.82a15 15 0 0 1 20 0' /> <path d='M5 12.859a10 10 0 0 1 14 0' /> <path d='M8.5 16.429a5 5 0 0 1 7 0' />",
    "hard-drive": "<path d='M10 16h.01' /> <path d='M2.212 11.577a2 2 0 0 0-.212.896V18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5.527a2 2 0 0 0-.212-.896L18.55 5.11A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z' /> <path d='M21.946 12.013H2.054' /> <path d='M6 16h.01' />",
    "memory-stick": "<path d='M12 12v-2' /> <path d='M12 18v-2' /> <path d='M16 12v-2' /> <path d='M16 18v-2' /> <path d='M2 11h1.5' /> <path d='M20 18v-2' /> <path d='M20.5 11H22' /> <path d='M4 18v-2' /> <path d='M8 12v-2' /> <path d='M8 18v-2' /> <rect x='2' y='6' width='20' height='10' rx='2' />",
    "folder": "<path d='M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z' />",
    "file-text": "<path d='M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z' /> <path d='M14 2v5a1 1 0 0 0 1 1h5' /> <path d='M10 9H8' /> <path d='M16 13H8' /> <path d='M16 17H8' />",
    "file-code": "<path d='M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z' /> <path d='M14 2v5a1 1 0 0 0 1 1h5' /> <path d='M10 12.5 8 15l2 2.5' /> <path d='m14 12.5 2 2.5-2 2.5' />",
    "users": "<path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2' /> <path d='M16 3.128a4 4 0 0 1 0 7.744' /> <path d='M22 21v-2a4 4 0 0 0-3-3.87' /> <circle cx='9' cy='7' r='4' />",
    "user": "<path d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2' /> <circle cx='12' cy='7' r='4' />",
    "settings": "<path d='M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915' /> <circle cx='12' cy='12' r='3' />",
    "wrench": "<path d='M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z' />",
    "search": "<path d='m21 21-4.34-4.34' /> <circle cx='11' cy='11' r='8' />",
    "eye": "<path d='M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0' /> <circle cx='12' cy='12' r='3' />",
    "clock": "<circle cx='12' cy='12' r='10' /> <path d='M12 6v6l4 2' />",
    "calendar": "<path d='M8 2v4' /> <path d='M16 2v4' /> <rect width='18' height='18' x='3' y='4' rx='2' /> <path d='M3 10h18' />",
    "refresh-cw": "<path d='M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8' /> <path d='M21 3v5h-5' /> <path d='M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16' /> <path d='M8 16H3v5' />",
    "rotate-cw": "<path d='M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8' /> <path d='M21 3v5h-5' />",
    "arrow-right": "<path d='M5 12h14' /> <path d='m12 5 7 7-7 7' />",
    "arrow-left": "<path d='m12 19-7-7 7-7' /> <path d='M19 12H5' />",
    "arrow-up": "<path d='m5 12 7-7 7 7' /> <path d='M12 19V5' />",
    "arrow-down": "<path d='M12 5v14' /> <path d='m19 12-7 7-7-7' />",
    "circle-help": "<circle cx='12' cy='12' r='10' /> <path d='M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3' /> <path d='M12 17h.01' />",
    "message-square": "<path d='M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z' />",
    "mail": "<path d='m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7' /> <rect x='2' y='4' width='20' height='16' rx='2' />",
    "send": "<path d='M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z' /> <path d='m21.854 2.147-10.94 10.939' />",
    "download": "<path d='M12 15V3' /> <path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' /> <path d='m7 10 5 5 5-5' />",
    "upload": "<path d='M12 3v12' /> <path d='m17 8-5-5-5 5' /> <path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' />",
    "bug": "<path d='M12 20v-9' /> <path d='M14 7a4 4 0 0 1 4 4v3a6 6 0 0 1-12 0v-3a4 4 0 0 1 4-4z' /> <path d='M14.12 3.88 16 2' /> <path d='M21 21a4 4 0 0 0-3.81-4' /> <path d='M21 5a4 4 0 0 1-3.55 3.97' /> <path d='M22 13h-4' /> <path d='M3 21a4 4 0 0 1 3.81-4' /> <path d='M3 5a4 4 0 0 0 3.55 3.97' /> <path d='M6 13H2' /> <path d='m8 2 1.88 1.88' /> <path d='M9 7.13V6a3 3 0 1 1 6 0v1.13' />",
    "sparkles": "<path d='M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z' /> <path d='M20 2v4' /> <path d='M22 4h-4' /> <circle cx='4' cy='20' r='2' />",
    "rocket": "<path d='M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5' /> <path d='M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09' /> <path d='M9 12a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.4 22.4 0 0 1-4 2z' /> <path d='M9 12H4s.55-3.03 2-4c1.62-1.08 5 .05 5 .05' />",
    "brain": "<path d='M12 18V5' /> <path d='M15 13a4.17 4.17 0 0 1-3-4 4.17 4.17 0 0 1-3 4' /> <path d='M17.598 6.5A3 3 0 1 0 12 5a3 3 0 1 0-5.598 1.5' /> <path d='M17.997 5.125a4 4 0 0 1 2.526 5.77' /> <path d='M18 18a4 4 0 0 0 2-7.464' /> <path d='M19.967 17.483A4 4 0 1 1 12 18a4 4 0 1 1-7.967-.517' /> <path d='M6 18a4 4 0 0 1-2-7.464' /> <path d='M6.003 5.125a4 4 0 0 0-2.526 5.77' />",
    "bot": "<path d='M12 8V4H8' /> <rect width='16' height='12' x='4' y='8' rx='2' /> <path d='M2 14h2' /> <path d='M20 14h2' /> <path d='M15 13v2' /> <path d='M9 13v2' />",
    "map-pin": "<path d='M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0' /> <circle cx='12' cy='10' r='3' />",
    "route": "<circle cx='6' cy='19' r='3' /> <path d='M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15' /> <circle cx='18' cy='5' r='3' />",
    "signpost": "<path d='M12 13v8' /> <path d='M12 3v3' /> <path d='M2.354 10.354a1.207 1.207 0 0 1 0-1.708l2.06-2.06A2 2 0 0 1 5.828 6h12.344a2 2 0 0 1 1.414.586l2.06 2.06a1.207 1.207 0 0 1 0 1.708l-2.06 2.06a2 2 0 0 1-1.414.586H5.828a2 2 0 0 1-1.414-.586z' />",
    "credit-card": "<rect width='20' height='14' x='2' y='5' rx='2' /> <line x1='2' x2='22' y1='10' y2='10' />",
    "shopping-cart": "<circle cx='8' cy='21' r='1' /> <circle cx='19' cy='21' r='1' /> <path d='M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12' />",
    "link": "<path d='M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71' /> <path d='M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71' />",
    "sliders": "<path d='M10 8h4' /> <path d='M12 21v-9' /> <path d='M12 8V3' /> <path d='M17 16h4' /> <path d='M19 12V3' /> <path d='M19 21v-5' /> <path d='M3 14h4' /> <path d='M5 10V3' /> <path d='M5 21v-7' />",
    "fingerprint": "<path d='M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4' /> <path d='M14 13.12c0 2.38 0 6.38-1 8.88' /> <path d='M17.29 21.02c.12-.6.43-2.3.5-3.02' /> <path d='M2 12a10 10 0 0 1 18-6' /> <path d='M2 16h.01' /> <path d='M21.8 16c.2-2 .131-5.354 0-6' /> <path d='M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2' /> <path d='M8.65 22c.21-.66.45-1.32.57-2' /> <path d='M9 6.8a6 6 0 0 1 9 5.2v2' />",
    "gauge": "<path d='m12 14 4-4' /> <path d='M3.34 19a10 10 0 1 1 17.32 0' />",
    "activity": "<path d='M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2' />",
    "trending-up": "<path d='M16 7h6v6' /> <path d='m22 7-8.5 8.5-5-5L2 17' />",
    "shuffle": "<path d='m18 14 4 4-4 4' /> <path d='m18 2 4 4-4 4' /> <path d='M2 18h1.973a4 4 0 0 0 3.3-1.7l5.454-8.6a4 4 0 0 1 3.3-1.7H22' /> <path d='M2 6h1.972a4 4 0 0 1 3.6 2.2' /> <path d='M22 18h-6.041a4 4 0 0 1-3.3-1.8l-.359-.45' />",
    "repeat": "<path d='m17 2 4 4-4 4' /> <path d='M3 11v-1a4 4 0 0 1 4-4h14' /> <path d='m7 22-4-4 4-4' /> <path d='M21 13v1a4 4 0 0 1-4 4H3' />",
}

ICON_NAMES: list[str] = sorted(_ICONS.keys())

_FALLBACK = "circle-help"


def get_icon(name: str | None) -> str:
    """Return inner SVG markup for an icon name, or the circle-help fallback
    if the name is missing/unrecognized. Never returns empty -- a slide
    should never render an icon-shaped hole."""
    return _ICONS.get((name or "").strip().lower(), _ICONS[_FALLBACK])


def get_icon_svg(name: str | None, *, size: int = 20) -> str:
    """Same as get_icon, but wrapped as a standalone <svg> for embedding
    directly in HTML (e.g. a bullet's leading icon), rather than as a
    fragment placed inside an already-open diagram <svg> canvas."""
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" class="icon">{get_icon(name)}</svg>'