# Example: anime.js Skill

This is a complete example of a skill generated from the `juliangarnier/anime` GitHub repository.

## Generated SKILL.md

```markdown
---
name: anime-js
description: Create smooth JavaScript animations with anime.js. Use when asked to "animate elements", "tween properties", "build animation timelines", "animate SVG paths", or "create motion graphics" in web apps.
---

# anime.js

anime.js is a lightweight JavaScript animation library for DOM, SVG, and object tweening. Use it to build smooth UI motion and timeline-driven sequences in web applications.

## Quick Start

### npm
```bash
npm install animejs
```

### CDN
```html
<script src="https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js"></script>
```

```javascript
import anime from 'animejs';

anime({
  targets: '.box',
  translateX: 250,
  duration: 800,
  easing: 'easeInOutQuad'
});
```

## Core Tasks

### Task: Animate DOM properties
Goal: Move, fade, or scale elements with GPU-friendly properties.
Steps:
1. Select targets with a CSS selector or DOM node.
2. Use `translate`, `scale`, or `opacity` for performance.
3. Add easing and duration for motion feel.

Example:
```javascript
anime({
  targets: '.card',
  translateY: [-12, 0],
  opacity: [0, 1],
  duration: 500,
  easing: 'easeOutCubic'
});
```

### Task: Build timeline sequences
Goal: Coordinate multiple animations in order.
Steps:
1. Create a timeline with shared defaults.
2. Add steps with offsets or overlaps.
3. Use `anime.stagger` for groups.

Example:
```javascript
const tl = anime.timeline({ easing: 'easeOutExpo', duration: 600 });
tl.add({ targets: '.logo', opacity: [0, 1], translateY: [-20, 0] })
  .add({ targets: '.nav-item', opacity: [0, 1], translateX: [-12, 0],
         delay: anime.stagger(80) }, '-=200');
```

### Task: Animate SVG paths
Goal: Draw or reveal SVG strokes.
Steps:
1. Set `strokeDashoffset` using `anime.setDashoffset`.
2. Animate to 0 for a drawing effect.

Example:
```javascript
anime({
  targets: '.line path',
  strokeDashoffset: [anime.setDashoffset, 0],
  duration: 1200,
  easing: 'easeInOutSine'
});
```

## API Cheat Sheet (optional)
- `anime({...})`: Create an animation instance.
- `anime.timeline({...})`: Sequence multiple animations.
- `anime.stagger(step)`: Stagger delays or values across targets.
- `anime.setDashoffset(el)`: Compute SVG dash offsets.

## Pitfalls and Limits
- Avoid animating layout properties (top, left); prefer transforms.
- Large target sets can impact performance.
- No built-in scroll triggers; use IntersectionObserver.

## Companion Skills (optional)
- `frontend-design`: Shape the UI layout and styling around animation-heavy interfaces.
- `webapp-testing`: Validate animation behavior and timing in a real browser.

## Resources
- See `references/api-reference.md` for full API details.
- See `examples/` for runnable snippets.
- [Official Documentation](https://animejs.com/documentation/)
- [GitHub Repository](https://github.com/juliangarnier/anime)
- License: MIT
```

## File Structure

```
anime-js/
├── SKILL.md                    # Main skill file (shown above)
├── references/
│   └── api-reference.md        # Detailed API documentation
└── examples/
    ├── basic-animations.js     # Basic animation examples
    └── timeline-example.js     # Timeline usage examples
```

## Validation Output

```json
{
  "valid": true,
  "skill_path": "anime-js",
  "name": "anime-js",
  "description": "Create smooth JavaScript animations with anime.js...",
  "errors": [],
  "warnings": []
}
```
