# How to Use Marp Layout Techniques

This guide covers commonly used layout techniques in Marp (Markdown presentation ecosystem) for creating professional and visually appealing slide presentations.

## Table of Contents

1. [Basic Layout Structure](#basic-layout-structure)
2. [Slide Size and Dimensions](#slide-size-and-dimensions)
3. [Split Layout Techniques](#split-layout-techniques)
4. [Multi-Column Layouts](#multi-column-layouts)
5. [Content Alignment](#content-alignment)
6. [Header and Footer Positioning](#header-and-footer-positioning)
7. [Background Layout Techniques](#background-layout-techniques)
8. [CSS Grid and Flexbox in Marp](#css-grid-and-flexbox-in-marp)
9. [Responsive Design Patterns](#responsive-design-patterns)
10. [Advanced Layout Examples](#advanced-layout-examples)

## Basic Layout Structure

### Default Slide Structure

```markdown
---
theme: default
---

# Slide Title

Content goes here

---

## Next Slide

More content
```

### Custom Container Structure

```css
/* @theme custom */

section {
  width: 1280px;
  height: 720px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
```

## Slide Size and Dimensions

### Standard 16:9 Format (Default)

```css
section {
  width: 1280px;
  height: 720px;
}
```

### Classic 4:3 Format

```css
section {
  width: 960px;
  height: 720px;
}
```

### Custom Aspect Ratios

```css
/* Square format */
section {
  width: 720px;
  height: 720px;
}

/* Ultrawide format */
section {
  width: 1920px;
  height: 720px;
}
```

## Split Layout Techniques

### Left-Right Split with Background Images

```markdown
![bg left](image-left.jpg)

# Right Side Content

This content appears on the right side while the image occupies the left half.
```

### Right-Left Split

```markdown
![bg right](image-right.jpg)

# Left Side Content

This content appears on the left side while the image occupies the right half.
```

### Custom Split Ratios

```markdown
![bg left:33%](image.jpg)

# 67% Content Area

The image takes 33% of the width, content gets the remaining 67%.
```

### CSS-Based Split Layout

```css
section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.left-column {
  padding-right: 1rem;
}

.right-column {
  padding-left: 1rem;
}
```

```markdown
<div class="left-column">

# Left Content

- Point 1
- Point 2
- Point 3

</div>

<div class="right-column">

# Right Content

- Feature A
- Feature B
- Feature C

</div>
```

## Multi-Column Layouts

### Two-Column Layout with CSS Grid

```css
/* @theme two-column */

section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 40px;
}

.column {
  display: flex;
  flex-direction: column;
}
```

### Three-Column Layout

```css
section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
```

### Flexible Column Layout

```css
section {
  display: flex;
  gap: 2rem;
}

.column {
  flex: 1;
  min-width: 0; /* Prevents overflow */
}
```

### Using CSS Columns for Text

```css
.multi-column-text {
  column-count: 2;
  column-gap: 2rem;
  column-rule: 1px solid #ddd;
}
```

```markdown
<div class="multi-column-text">

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

</div>
```

## Content Alignment

### Vertical Centering

```css
section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
```

### Horizontal Alignment Options

```css
/* Left aligned (default) */
section {
  text-align: left;
}

/* Center aligned */
section {
  text-align: center;
}

/* Right aligned */
section {
  text-align: right;
}
```

### Custom Alignment Classes

```css
.center {
  text-align: center;
}

.right {
  text-align: right;
}

.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

```markdown
<!-- _class: center -->

# Centered Title

This entire slide is center-aligned.
```

## Header and Footer Positioning

### Global Header and Footer

```markdown
---
header: 'Presentation Title'
footer: 'Company Name | Date'
---
```

### Custom Header/Footer Styling

```css
header,
footer {
  position: absolute;
  left: 50px;
  right: 50px;
  height: 20px;
  font-size: 14px;
}

header {
  top: 30px;
  border-bottom: 1px solid #ccc;
}

footer {
  bottom: 30px;
  border-top: 1px solid #ccc;
}
```

### Advanced Header Layout

```css
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  font-weight: bold;
}

.header-right {
  font-style: italic;
}
```

## Background Layout Techniques

### Multiple Backgrounds (Horizontal)

```markdown
![bg](background1.jpg)
![bg](background2.jpg)
![bg](background3.jpg)

# Content Over Multiple Backgrounds
```

### Multiple Backgrounds (Vertical)

```markdown
![bg vertical](background1.jpg)
![bg](background2.jpg)
![bg](background3.jpg)
```

### Background Size Control

```markdown
![bg cover](image.jpg)    <!-- Fill entire slide -->
![bg contain](image.jpg)  <!-- Fit within slide -->
![bg 50%](image.jpg)      <!-- Custom size -->
![bg auto](image.jpg)     <!-- Original size -->
```

### Gradient Backgrounds

```markdown
<!-- backgroundImage: "linear-gradient(45deg, #667eea 0%, #764ba2 100%)" -->

# Gradient Background Slide
```

## CSS Grid and Flexbox in Marp

### Grid-Based Slide Layout

```css
section {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar content aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: 60px 1fr 40px;
  gap: 1rem;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }
```

### Flexbox Card Layout

```css
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: space-between;
}

.card {
  flex: 1 1 calc(33.333% - 1rem);
  min-width: 200px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
```

### Responsive Grid

```css
.responsive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
```

## Responsive Design Patterns

### Media Query Example

```css
section {
  padding: 40px;
}

@media (max-width: 768px) {
  section {
    padding: 20px;
    font-size: 24px;
  }
  
  .desktop-only {
    display: none;
  }
}
```

### Responsive Typography

```css
section {
  font-size: clamp(16px, 2.5vw, 28px);
}

h1 {
  font-size: clamp(24px, 4vw, 48px);
}

h2 {
  font-size: clamp(20px, 3vw, 36px);
}
```

### Container Queries (Modern Browsers)

```css
.container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .content {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

## Advanced Layout Examples

### Dashboard-Style Layout

```css
/* @theme dashboard */

section {
  display: grid;
  grid-template-areas:
    "title title title"
    "metric1 metric2 metric3"
    "chart chart sidebar"
    "footer footer footer";
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 80px 120px 1fr 40px;
  gap: 1rem;
  padding: 1rem;
}

.title { grid-area: title; }
.metric1 { grid-area: metric1; }
.metric2 { grid-area: metric2; }
.metric3 { grid-area: metric3; }
.chart { grid-area: chart; }
.sidebar { grid-area: sidebar; }
.footer { grid-area: footer; }
```

### Magazine-Style Layout

```css
.magazine-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: auto 1fr auto;
  gap: 2rem;
  height: 100%;
}

.feature-article {
  grid-column: 1;
  grid-row: 1 / 3;
}

.sidebar-content {
  grid-column: 2;
  grid-row: 1;
}

.advertisement {
  grid-column: 2;
  grid-row: 2;
}
```

### Masonry-Style Layout

```css
.masonry {
  column-count: 3;
  column-gap: 1rem;
  column-fill: balance;
}

.masonry-item {
  break-inside: avoid;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}
```

### Timeline Layout

```css
.timeline {
  position: relative;
  padding-left: 3rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 1rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #333;
}

.timeline-item {
  position: relative;
  margin-bottom: 2rem;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -2.5rem;
  top: 0.5rem;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #007acc;
}
```

## Best Practices

### 1. Consistent Spacing

```css
/* Use consistent spacing variables */
:root {
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;
}
```

### 2. Semantic Layout Classes

```css
.slide-title { /* ... */ }
.slide-subtitle { /* ... */ }
.slide-content { /* ... */ }
.slide-footer { /* ... */ }
```

### 3. Accessibility Considerations

```css
/* Ensure sufficient contrast */
section {
  color: #333;
  background: #fff;
}

/* Focus styles for navigation */
:focus {
  outline: 2px solid #007acc;
  outline-offset: 2px;
}
```

### 4. Performance Optimization

```css
/* Use efficient selectors */
.slide-container > .content {
  /* More specific than universal selectors */
}

/* Minimize expensive properties */
.animated-element {
  transform: translateX(0); /* Better than changing layout properties */
}
```

## Related Resources

- [Marp Official Documentation](https://marp.app/)
- [Marpit Theme CSS Documentation](https://marpit.marp.app/theme-css)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Modern CSS Layout Techniques](https://web.dev/learn/css/layout/)

## Common Layout Patterns Quick Reference

| Pattern | CSS Property | Use Case |
|---------|-------------|----------|
| Split Layout | `grid-template-columns: 1fr 1fr` | Two-column content |
| Card Grid | `display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))` | Responsive cards |
| Center Content | `display: flex; justify-content: center; align-items: center` | Centered slide content |
| Header/Footer | `position: absolute; top/bottom: value` | Fixed header/footer |
| Sidebar Layout | `grid-template-columns: 200px 1fr` | Navigation + content |
| Stack Layout | `display: flex; flex-direction: column` | Vertical stacking |

This guide provides a comprehensive overview of layout techniques available in Marp. Experiment with these patterns and combine them to create unique and professional presentations.
