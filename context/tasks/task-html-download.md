implement html download scripts to download js-rendered HTML pages and their resources, using `playwright` python library.

the created script is named `download-html.py` and is located in the `scripts` directory. it can has the following options:
- `--url` or `-u`: the URL of the page to download, this is REQUIRED.
- `--output` or `-o`: 
  - it can be the output file name, default is a named generated file based on the URL.
  - it can be a directory, in that case, the script will create a file named `downloaded.html` in that directory.
- `--with-all`: if specified, the script will download all resources (images, stylesheets, etc.) and save them in a subdirectory named after the URL's domain. Otherwise, it will only download the HTML content.
- `--with-images`: if specified, the script will download the html as well as all images, but not other resources.

in `playwright`, we will use chromium browser for rendering the page.

see `context\hints\howto-use-playwright-to-download-website-content.md` for guidelines on how to use `playwright` to download website content.