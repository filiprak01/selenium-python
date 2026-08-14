# Test Context

This directory contains pytest fixtures and behavior-focused tests. Tests must use `UIClient`, page objects, and flows rather than direct Selenium calls.

Framework capabilities should be verified through browser tests against the configured
test URL. Start with the Sauce Demo home-page smoke test and add broader application
test cases incrementally.

When adding a new test area, fixture, marker, or test-data convention, update this file and the nearest relevant `AGENTS.md` file.
