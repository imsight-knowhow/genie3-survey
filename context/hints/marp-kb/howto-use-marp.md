# How to Use Marp: Create Presentations with Markdown

Marp (Markdown Presentation Ecosystem) is a powerful tool that allows you to create beautiful slide presentations using Markdown syntax. This guide covers installation, basic usage, and advanced features.

## What is Marp?

Marp provides an intuitive experience for creating slide decks using familiar Markdown syntax. You only need to focus on writing your content in a Markdown document, and Marp handles the presentation formatting.

## Installation Options

### 1. VS Code Extension (Recommended for Development)
Install the "Marp for VS Code" extension from the marketplace:
- Search for "Marp for VS Code" in the Extensions tab
- Provides live preview, export functionality, and IntelliSense

### 2. Marp CLI (Command Line Interface)
```bash
# Using npx (no installation required)
npx @marp-team/marp-cli@latest slide-deck.md

# Global installation
npm install -g @marp-team/marp-cli

# Local project installation
npm install --save-dev @marp-team/marp-cli
```

### 3. Package Managers
```bash
# macOS (Homebrew)
brew install marp-cli

# Windows (Scoop)
scoop install marp
```

## Basic Markdown Syntax for Slides

### Creating Your First Slide Deck
Create a `.md` file with the following structure:

```markdown
---
marp: true
---

# My Presentation Title

Welcome to my presentation!

---

## Slide 2: Bullet Points

- First item
- Second item
- Third item

---

## Slide 3: Code Example

```javascript
function hello() {
    console.log("Hello, Marp!");
}
```

---

## Slide 4: Images

![width:500px](path/to/image.jpg)

---

## Thank You!

Questions?
```

### Key Syntax Elements

- **`---`**: Slide separator (horizontal ruler)
- **`marp: true`**: Front-matter directive to enable Marp
- **Standard Markdown**: Headings, lists, code blocks, images work as expected

## Directives and Customization

### Global Directives (in front-matter)
```markdown
---
marp: true
title: My Presentation
theme: gaia
paginate: true
backgroundColor: #fff
author: Your Name
---
```

### Local Directives (per slide)
```markdown
<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _backgroundColor: #000 -->

# Slide with Custom Styling
```

### Built-in Themes
- **default**: Clean, minimal theme
- **gaia**: Elegant theme with gradient backgrounds
- **uncover**: Bold, high-contrast theme

```markdown
---
marp: true
theme: gaia
---
```

## Advanced Features

### Image Sizing and Positioning
```markdown
<!-- Background image -->
![bg](image.jpg)

<!-- Sized image -->
![width:400px height:300px](image.jpg)

<!-- Split layout with background -->
![bg left:40%](image.jpg)

# Content on the right side
```

### Fragmented Lists (Appear One by One)
```markdown
* Item 1
* Item 2
* Item 3
```

### Math Typesetting
```markdown
$$
f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{2 \pi i \xi x} d\xi
$$
```

### Speaker Notes
```markdown
<!-- This is a speaker note, only visible in presenter mode -->

# My Slide Title

Regular slide content here.
```

## Export Options

### Using Marp CLI

#### Export to HTML
```bash
marp slide-deck.md
marp slide-deck.md -o output.html
```

#### Export to PDF
```bash
marp --pdf slide-deck.md
marp slide-deck.md -o output.pdf
```

#### Export to PowerPoint (PPTX)
```bash
marp --pptx slide-deck.md
marp slide-deck.md -o output.pptx
```

#### Export to Images
```bash
# Multiple PNG images (one per slide)
marp --images png slide-deck.md

# Title slide only
marp --image png slide-deck.md
```

### Using VS Code Extension
1. Open your Marp Markdown file
2. Click the Marp icon in the toolbar
3. Select "Export slide deck..."
4. Choose your desired format

## Advanced CLI Features

### Watch Mode (Auto-reload)
```bash
marp -w slide-deck.md
```

### Server Mode (Live Preview)
```bash
marp -s ./slides-directory
```

### Preview Window
```bash
marp -p slide-deck.md
```

### Custom Themes
```bash
marp --theme custom-theme.css slide-deck.md
```

## Configuration File

Create `marp.config.js` for project-wide settings:

```javascript
export default {
  inputDir: './slides',
  output: './public',
  pdf: true,
  html: true,
  theme: 'gaia',
  themeSet: './themes'
}
```

## Best Practices

1. **Keep slides simple**: Focus on one concept per slide
2. **Use consistent styling**: Stick to one theme throughout
3. **Optimize images**: Use appropriate sizes and formats
4. **Test exports**: Always preview your exported presentations
5. **Use speaker notes**: Add context for yourself during presentations
6. **Version control**: Keep your Markdown files in git for easy collaboration

## Presenter Mode

When using the HTML output in a browser:
- Press `P` to open presenter view
- Shows current slide, speaker notes, and next slide preview
- Perfect for dual-monitor setups

## Common Use Cases

- **Technical presentations**: Code syntax highlighting works great
- **Educational content**: Math formulas and diagrams
- **Business presentations**: Clean, professional themes
- **Documentation**: Convert docs to presentation format
- **Workshops**: Live-reload for iterative development

## Troubleshooting

- **Preview not working**: Ensure `marp: true` is in front-matter
- **Export failures**: Check that you have Chrome/Edge/Firefox installed
- **Theme issues**: Verify theme syntax and file paths
- **Image problems**: Use relative paths or online URLs

## Resources

### Official Documentation
- [Official Marp Website](https://marp.app/)
- [Marp CLI Documentation](https://github.com/marp-team/marp-cli)
- [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
- [Marpit Framework](https://marpit.marp.app/) (underlying engine)
- [Built-in Themes](https://github.com/marp-team/marp-core/tree/main/themes)

### Context7 Library Documentation
- **Marp CLI**: `/marp-team/marp-cli` - CLI interface for converting Markdown to slides
- **Marpit Framework**: `/marp-team/marpit` - Core framework for slide creation
- Access via: Use these library IDs with context7 for comprehensive API documentation and code examples

## Quick Start Template

```markdown
---
marp: true
title: Your Presentation Title
theme: default
paginate: true
---

# Your Presentation Title
### Subtitle or Date

---

## Agenda

1. Introduction
2. Main Content
3. Conclusion
4. Questions

---

## Introduction

Your introduction content here...

---

## Thank You!

**Questions?**

Contact: your.email@example.com
```

Start with this template and customize based on your needs!
