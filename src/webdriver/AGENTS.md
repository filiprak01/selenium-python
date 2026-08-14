# WebDriver Guidance

Keep browser/session construction here. Browser selection must remain configurable,
while Chrome is the only supported implementation in this slice. Prefer Selenium's
built-in driver management and keep browser-specific options isolated in
`chrome_options.py`.

When adding new elements, update this `AGENTS.md` and the parent framework guidance.
