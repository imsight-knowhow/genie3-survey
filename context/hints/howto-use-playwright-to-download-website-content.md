# How to Use Playwright to Download a Website and Its Images

This guide explains how to use Playwright to open a website, download the rendered HTML (after JavaScript has been processed), and download all the images on the page.

## 1. Get the Rendered HTML

After navigating to a page, you can get the full HTML content of the page, including any modifications made by JavaScript, using the `page.content()` method.

**Source:** [Playwright Documentation](https://playwright.dev/docs/api/class-page#page-content)

### Python

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        
        # Get the entire page content
        html = await page.content()
        
        # Save the HTML to a file
        with open("page.html", "w", encoding="utf-8") as f:
            f.write(html)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript

```javascript
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');

  // Get the entire page content
  const html = await page.content();

  // Save the HTML to a file
  fs.writeFileSync('page.html', html, 'utf-8');

  await browser.close();
})();
```

## 2. Download Images

To download images, you can intercept network requests. You can listen for all responses, check if the content type is an image, and then save the image buffer.

**Source:** [Playwright Documentation - Network](https://playwright.dev/docs/network)

### Python

```python
import asyncio
import os
from playwright.async_api import async_playwright
from urllib.parse import urlparse

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Create a directory to save images
        if not os.path.exists("images"):
            os.makedirs("images")

        # Listen for all responses and save images
        async def handle_response(response):
            # Check if the response is an image
            if "image" in response.headers.get("content-type", ""):
                try:
                    # Get the image buffer
                    buffer = await response.body()
                    # Get a filename from the URL
                    parsed_url = urlparse(response.url)
                    filename = os.path.basename(parsed_url.path)
                    if not filename:
                        # if no filename, use a default
                        filename = f"image_{len(os.listdir('images'))}.jpg"
                    
                    # Save the image
                    with open(os.path.join("images", filename), "wb") as f:
                        f.write(buffer)
                    print(f"Saved image: {filename}")
                except Exception as e:
                    print(f"Could not save image {response.url}: {e}")

        page.on("response", handle_response)

        await page.goto("https://www.wikipedia.org/")
        
        # Wait for a bit for images to load
        await page.wait_for_timeout(5000)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript

```javascript
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Create a directory to save images
  if (!fs.existsSync('images')) {
    fs.mkdirSync('images');
  }

  // Listen for all responses and save images
  page.on('response', async (response) => {
    const contentType = response.headers()['content-type'];
    if (contentType && contentType.startsWith('image/')) {
      try {
        const buffer = await response.body();
        const url = new URL(response.url());
        let filename = path.basename(url.pathname);
        if (!filename || filename === '/') {
            filename = `image_${Date.now()}.${contentType.split('/')[1]}`;
        }

        fs.writeFileSync(path.join('images', filename), buffer);
        console.log(`Saved image: ${filename}`);
      } catch (e) {
        console.error(`Could not save image ${response.url()}: ${e}`);
      }
    }
  });

  await page.goto('https://www.wikipedia.org/');

  // Wait for a bit for images to load
  await new Promise(resolve => setTimeout(resolve, 5000));

  await browser.close();
})();
```

This approach allows you to capture all images loaded by the page, whether they are in `<img>` tags, CSS backgrounds, or loaded dynamically by JavaScript.