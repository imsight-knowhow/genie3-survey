# How to Adjust Margins in Marp Presentations

This guide covers various techniques for adjusting margins, spacing, and positioning of elements in Marp (Markdown Presentation Ecosystem) slides.

## Table of Contents

1. [Understanding Marp Layout Structure](#understanding-marp-layout-structure)
2. [Basic Margin Adjustment Techniques](#basic-margin-adjustment-techniques)
3. [Element Positioning Methods](#element-positioning-methods)
4. [Slide-Specific Margin Control](#slide-specific-margin-control)
5. [Advanced Spacing Techniques](#advanced-spacing-techniques)
6. [Common Use Cases and Solutions](#common-use-cases-and-solutions)
7. [Theme-Level Margin Configuration](#theme-level-margin-configuration)
8. [Troubleshooting Margin Issues](#troubleshooting-margin-issues)

## Understanding Marp Layout Structure

### Marp Section Element
In Marp, each slide is contained within a `<section>` element that acts as the viewport:

```css
section {
  width: 1280px;
  height: 720px;
  padding: 40px; /* Default slide padding */
}
```

### Root Context
Marp uses `:root` pseudo-class to refer to each `<section>` element:

```css
:root {
  /* These apply to each slide section */
  padding: 2rem;
  margin: 0;
}
```

## Basic Margin Adjustment Techniques

### 1. CSS Margin Properties

#### Standard Margin Control
```css
<style scoped>
h1 {
  margin-top: 2rem;
  margin-bottom: 1rem;
  margin-left: 0;
  margin-right: 0;
}

/* Shorthand syntax */
h2 {
  margin: 1rem 0 0.5rem 0; /* top right bottom left */
}
</style>
```

#### Negative Margins for Tighter Spacing
```css
<style scoped>
h1 {
  margin-top: -1rem; /* Moves element closer to top */
  margin-bottom: -0.5rem; /* Reduces space below */
}
</style>
```

### 2. Padding vs Margin
```css
<style scoped>
/* Padding: Space inside the element */
.content-box {
  padding: 2rem; /* Internal spacing */
}

/* Margin: Space outside the element */
.content-box {
  margin: 1rem; /* External spacing */
}
</style>
```

## Element Positioning Methods

### 1. Relative Positioning (Recommended)
This is the most reliable method for adjusting element positions in Marp:

```css
<style scoped>
h1 {
  position: relative;
  top: -2rem; /* Move up by 2rem */
}

h2 {
  position: relative;
  top: 1rem; /* Move down by 1rem */
  left: 2rem; /* Move right by 2rem */
}
</style>
```

#### Moving Title Closer to Top
```markdown
---
<!-- _class: -->

<style scoped>
h2:first-of-type {
  position: relative;
  top: -1.5em;
  margin-bottom: -1em;
}
</style>

## Your Slide Title

Content starts here...
```

### 2. Absolute Positioning
Use sparingly, as it removes elements from normal flow:

```css
<style scoped>
.corner-element {
  position: absolute;
  top: 20px;
  right: 20px;
}

.bottom-note {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
}
</style>
```

### 3. Transform-Based Positioning
Useful for fine-tuning without affecting layout:

```css
<style scoped>
.shifted-content {
  transform: translateY(-20px); /* Move up 20px */
}

.slight-adjustment {
  transform: translate(10px, -5px); /* Right 10px, up 5px */
}
</style>
```

## Slide-Specific Margin Control

### Using Scoped Styles
Apply margin adjustments to individual slides:

```markdown
---

<style scoped>
section {
  padding: 20px; /* Reduce default padding */
}

h1 {
  margin-top: 0; /* Remove top margin from title */
}

ul {
  margin-left: 2rem; /* Increase list indentation */
}
</style>

# Your Slide Title

- List item 1
- List item 2
```

### Class-Based Margin Control
```markdown
---
<!-- _class: tight-margins -->

<style scoped>
.tight-margins h1 {
  margin: 0.5rem 0;
}

.tight-margins p {
  margin: 0.25rem 0;
}
</style>

# Tightly Spaced Title

Content with reduced margins.
```

### Theme Override for Specific Slides
```markdown
---
<!-- _class: custom-spacing -->

<style scoped>
.custom-spacing {
  padding: 60px 80px; /* Override theme padding */
}

.custom-spacing h1 {
  margin-top: -20px; /* Pull title up */
}
</style>
```

## Advanced Spacing Techniques

### 1. Flexbox-Based Spacing
```css
<style scoped>
section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* Consistent spacing between elements */
}

.content-area {
  flex: 1;
  margin: 0; /* Remove default margins */
}
</style>
```

### 2. Grid-Based Spacing
```css
<style scoped>
section {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 2rem;
  padding: 2rem;
}

.header { margin: 0; }
.content { margin: 0; }
.footer { margin: 0; }
</style>
```

### 3. CSS Custom Properties for Consistent Spacing
```css
<style scoped>
:root {
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
}

h1 { margin: 0 0 var(--spacing-lg) 0; }
h2 { margin: var(--spacing-md) 0 var(--spacing-sm) 0; }
p { margin: 0 0 var(--spacing-sm) 0; }
</style>
```

## Common Use Cases and Solutions

### 1. Reducing Title Top Margin
**Problem**: Title appears too far from the top of the slide.

**Solution**:
```css
<style scoped>
h1 {
  position: relative;
  top: -1.5rem;
  margin-bottom: -1rem;
}
</style>
```

### 2. Centering Content with Custom Margins
**Problem**: Need to center content with specific spacing.

**Solution**:
```css
<style scoped>
section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 4rem;
}

.centered-content {
  margin: 2rem auto;
  text-align: center;
}
</style>
```

### 3. Adjusting List Indentation
**Problem**: Default list margins don't match design requirements.

**Solution**:
```css
<style scoped>
ul, ol {
  margin: 1rem 0;
  padding-left: 2rem;
}

li {
  margin: 0.5rem 0;
}
</style>
```

### 4. Creating Sidebar Layouts with Controlled Margins
**Problem**: Need different margin settings for sidebar content.

**Solution**:
```css
<style scoped>
section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin: 0;
}

.main-content {
  margin: 0 2rem 0 0;
}

.sidebar {
  margin: 0;
  padding: 1rem;
  background: #f5f5f5;
}
</style>
```

### 5. Footer Positioning with Margins
**Problem**: Need to position footer content at bottom with proper spacing.

**Solution**:
```css
<style scoped>
section {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.content {
  flex: 1;
  margin: 0 0 2rem 0;
}

.footer {
  margin-top: auto;
  margin-bottom: 0;
}
</style>
```

## Theme-Level Margin Configuration

### Creating Custom Theme with Default Margins
```css
/* @theme custom-margins */

section {
  padding: 30px 50px; /* Custom slide padding */
}

h1, h2, h3, h4, h5, h6 {
  margin: 1rem 0 0.5rem 0;
}

p {
  margin: 0 0 1rem 0;
}

ul, ol {
  margin: 1rem 0;
  padding-left: 2rem;
}

blockquote {
  margin: 1.5rem 2rem;
  padding: 1rem;
}
```

### Using Theme in Markdown
```markdown
---
marp: true
theme: custom-margins
---

# Your Presentation

Content with custom margin settings.
```

## Troubleshooting Margin Issues

### 1. Margins Not Applied
**Issue**: CSS margins don't seem to work.

**Debugging Steps**:
```css
<style scoped>
/* Add visible borders to debug */
h1 {
  border: 1px solid red;
  margin: 2rem 0;
}

/* Check if element is affected by flexbox/grid */
section {
  border: 1px solid blue;
}
</style>
```

### 2. Margin Collapse
**Issue**: Vertical margins between elements collapse.

**Solution**:
```css
<style scoped>
/* Prevent margin collapse with padding or border */
.content-block {
  border-top: 1px solid transparent;
  margin: 2rem 0;
}

/* Or use flexbox gap instead */
.container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
</style>
```

### 3. Responsive Margin Issues
**Issue**: Margins don't scale properly on different screen sizes.

**Solution**:
```css
<style scoped>
h1 {
  margin: clamp(1rem, 3vw, 3rem) 0;
}

section {
  padding: clamp(20px, 5vw, 60px);
}
</style>
```

### 4. Theme Override Problems
**Issue**: Theme styles override custom margins.

**Solution**:
```css
<style scoped>
/* Use higher specificity */
section h1 {
  margin: 2rem 0 !important;
}

/* Or reset and reapply */
h1 {
  all: unset;
  display: block;
  font-size: 2rem;
  font-weight: bold;
  margin: 2rem 0;
}
</style>
```

## Best Practices

### 1. Use Consistent Units
```css
/* Prefer rem for consistency */
h1 { margin: 2rem 0 1rem 0; }

/* Use em for proportional spacing */
p { margin: 0 0 1em 0; }

/* Use px for precise control */
.precise-element { margin-top: 23px; }
```

### 2. Mobile-First Responsive Margins
```css
<style scoped>
/* Mobile first */
section {
  padding: 1rem;
}

h1 {
  margin: 1rem 0 0.5rem 0;
}

/* Desktop adjustments */
@media (min-width: 768px) {
  section {
    padding: 2rem;
  }
  
  h1 {
    margin: 2rem 0 1rem 0;
  }
}
</style>
```

### 3. Semantic Spacing Variables
```css
<style scoped>
:root {
  --title-margin: 2rem 0 1rem 0;
  --paragraph-margin: 0 0 1rem 0;
  --section-padding: 2rem;
}

h1 { margin: var(--title-margin); }
p { margin: var(--paragraph-margin); }
section { padding: var(--section-padding); }
</style>
```

## Quick Reference

| Technique | CSS Property | Use Case |
|-----------|-------------|----------|
| Move element up | `position: relative; top: -Xpx` | Adjust title position |
| Reduce spacing | `margin: 0` or negative margins | Tight layouts |
| Increase spacing | `margin: Xrem` | Loose, readable layouts |
| Consistent gaps | `display: flex; gap: Xrem` | Even spacing between elements |
| Override theme | `margin: X !important` | Force specific margins |
| Responsive margins | `clamp(min, preferred, max)` | Scalable spacing |

## Related Resources

- [CSS Margin - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/margin)
- [Marp Theme CSS Documentation](https://marpit.marp.app/theme-css)
- [CSS Box Model Guide](https://web.dev/learn/css/box-model/)
- [Flexbox Gap Property](https://developer.mozilla.org/en-US/docs/Web/CSS/gap)
- [GitHub Issue: Move Title Up/Down](https://github.com/marp-team/marp-core/issues/177)

## Example: Complete Slide with Custom Margins

```markdown
---
<!-- _class: custom-slide -->

<style scoped>
.custom-slide {
  padding: 30px 40px;
}

.custom-slide h2:first-of-type {
  position: relative;
  top: -1em;
  margin-bottom: -0.5em;
}

.custom-slide h3 {
  margin: 1.5rem 0 0.5rem 0;
}

.custom-slide ul {
  margin: 0.5rem 0 1rem 2rem;
}

.custom-slide li {
  margin: 0.25rem 0;
}
</style>

## Custom Spaced Slide

### Section 1

- Point A
- Point B  
- Point C

### Section 2

More content with controlled spacing.
```

This guide provides comprehensive techniques for controlling margins and spacing in Marp presentations. Remember to test your margin adjustments across different export formats (HTML, PDF, PPTX) to ensure consistency.
