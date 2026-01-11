# Example: anime.js Skill

This is a complete example of a skill generated from the `juliangarnier/anime` GitHub repository.

## Generated SKILL.md

```markdown
---
name: anime-js
description: Create smooth JavaScript animations with anime.js. Use this skill when the user asks to "animate elements", "create CSS animations", "tween properties", "build animation sequences", "animate SVG", or work with motion graphics and timeline-based animations in web applications.
---

# anime.js Animation Library

anime.js is a lightweight JavaScript animation library with a simple, yet powerful API. It works with CSS properties, SVG, DOM attributes and JavaScript objects, making it versatile for any web animation need.

## When to Use This Skill

Use this skill when:
- Animating CSS properties (transform, opacity, colors)
- Creating SVG animations and morphing
- Building complex animation sequences with timelines
- Tweening JavaScript object values
- Adding motion to web interfaces
- Creating scroll-triggered animations
- Building interactive animation systems

## Installation

### npm
```bash
npm install animejs
```

### yarn
```bash
yarn add animejs
```

### CDN
```html
<script src="https://cdn.jsdelivr.net/npm/animejs@3.2.1/lib/anime.min.js"></script>
```

### ES6 Import
```javascript
import anime from 'animejs/lib/anime.es.js';
```

## Quick Start

### Basic Animation
```javascript
import anime from 'animejs';

// Animate a single element
anime({
  targets: '.box',
  translateX: 250,
  rotate: '1turn',
  backgroundColor: '#FFF',
  duration: 800
});
```

### Multiple Properties
```javascript
anime({
  targets: '.element',
  translateX: 250,
  scale: 2,
  opacity: 0.5,
  duration: 1000,
  easing: 'easeInOutQuad'
});
```

## Core API Reference

### anime(params)

Create an animation instance.

```javascript
const animation = anime({
  targets: '.element',
  // ... animation parameters
});
```

**Parameters:**

| Property | Type | Description |
|----------|------|-------------|
| `targets` | String/Element/Array | Elements to animate (CSS selector, DOM element, or array) |
| `duration` | Number | Animation duration in milliseconds. Default: 1000 |
| `delay` | Number/Function | Delay before animation starts. Default: 0 |
| `easing` | String | Easing function. Default: 'easeOutElastic(1, .5)' |
| `loop` | Boolean/Number | Number of loops or true for infinite. Default: false |
| `direction` | String | 'normal', 'reverse', or 'alternate'. Default: 'normal' |
| `autoplay` | Boolean | Start animation automatically. Default: true |

**Returns:** Animation instance with control methods

### Animation Controls

```javascript
const anim = anime({ targets: '.el', translateX: 250 });

anim.play();      // Start/resume animation
anim.pause();     // Pause animation
anim.restart();   // Restart from beginning
anim.reverse();   // Reverse direction
anim.seek(500);   // Jump to 500ms
```

### Easing Functions

Built-in easing options:
- Linear: `'linear'`
- Ease: `'easeInQuad'`, `'easeOutQuad'`, `'easeInOutQuad'`
- Elastic: `'easeInElastic'`, `'easeOutElastic'`
- Bounce: `'easeInBounce'`, `'easeOutBounce'`
- Spring: `'spring(mass, stiffness, damping, velocity)'`

## Examples

### Example 1: Basic CSS Animation

Animate a button on hover effect:

```javascript
// Hover animation
const button = document.querySelector('.cta-button');

button.addEventListener('mouseenter', () => {
  anime({
    targets: button,
    scale: 1.1,
    boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
    duration: 300,
    easing: 'easeOutCubic'
  });
});

button.addEventListener('mouseleave', () => {
  anime({
    targets: button,
    scale: 1,
    boxShadow: '0 5px 15px rgba(0,0,0,0.2)',
    duration: 300,
    easing: 'easeOutCubic'
  });
});
```

### Example 2: Timeline Sequence

Create a coordinated animation sequence:

```javascript
// Create timeline
const timeline = anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
});

// Add animations to timeline
timeline
  .add({
    targets: '.logo',
    opacity: [0, 1],
    translateY: [-50, 0]
  })
  .add({
    targets: '.menu-item',
    opacity: [0, 1],
    translateX: [-30, 0],
    delay: anime.stagger(100)  // Stagger each item by 100ms
  }, '-=500')  // Start 500ms before previous ends
  .add({
    targets: '.hero-text',
    opacity: [0, 1],
    translateY: [30, 0]
  }, '-=400');
```

### Example 3: SVG Path Animation

Animate SVG drawing:

```javascript
// Animate SVG path drawing
anime({
  targets: '.line-drawing path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 1500,
  delay: (el, i) => i * 250,
  direction: 'alternate',
  loop: true
});
```

### Example 4: Staggered Grid Animation

Animate grid items with stagger effect:

```javascript
anime({
  targets: '.grid-item',
  scale: [
    { value: 0.1, easing: 'easeOutSine', duration: 500 },
    { value: 1, easing: 'easeInOutQuad', duration: 1200 }
  ],
  delay: anime.stagger(200, { grid: [14, 5], from: 'center' })
});
```

## Configuration Options

### Property Parameters

Properties can have individual parameters:

```javascript
anime({
  targets: '.element',
  translateX: {
    value: 250,
    duration: 800
  },
  rotate: {
    value: 360,
    duration: 1800,
    easing: 'easeInOutSine'
  },
  scale: {
    value: 2,
    duration: 1600,
    delay: 800,
    easing: 'easeInOutQuart'
  }
});
```

### Callbacks

```javascript
anime({
  targets: '.element',
  translateX: 250,
  begin: (anim) => console.log('Animation started'),
  update: (anim) => console.log(`Progress: ${anim.progress}%`),
  complete: (anim) => console.log('Animation completed'),
  loopBegin: (anim) => console.log('Loop started'),
  loopComplete: (anim) => console.log('Loop completed')
});
```

## Safety and Limitations

### Limitations
- Does not support CSS Grid or Flexbox animations directly
- Performance may degrade with 1000+ simultaneous animations
- SVG support varies across browsers
- No built-in scroll-trigger (use Intersection Observer)

### Best Practices
- Use `will-change` CSS for smoother animations
- Prefer `transform` and `opacity` for GPU acceleration
- Clean up animations when components unmount
- Use timeline for complex sequences instead of nested callbacks

### Performance Tips
- Limit targets per animation to <100 elements
- Use `anime.remove(targets)` to clean up
- Prefer CSS transforms over layout properties

## How It Works

anime.js uses requestAnimationFrame for smooth 60fps animations. It calculates intermediate values between start and end states using easing functions, then applies those values to target properties on each frame.

For CSS properties, it reads initial values from computed styles and interpolates to target values. For transforms, it decomposes the transform matrix for individual property control.

## Required Tools and Permissions

- **Tools needed**: Write (to create files), Bash (to run npm commands)
- **Environment**: Node.js 12+ or modern browser
- **Permissions**: None required

## Additional Resources

- [Official Documentation](https://animejs.com/documentation/)
- [GitHub Repository](https://github.com/juliangarnier/anime)
- [CodePen Examples](https://codepen.io/collection/XLebem)
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
