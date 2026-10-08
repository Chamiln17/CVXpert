# Security policy

## Reporting a vulnerability

Please report security problems privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue.

Include what you found, how to reproduce it, and what an attacker could do with it.

## Supported versions

Only the latest release on the default branch receives fixes.

## What CVXpert does with your data

- CVXpert runs on your machine. It sends the CV text, and the Job Description if you give one, to OpenRouter and the chosen model's provider, using your own OpenRouter API key.
- It stores nothing beyond the report files you ask it to write. The web page writes the uploaded CV to a temporary folder and deletes it after parsing.
- Your API key is read from the environment or a local `.env` file, which is git-ignored. CVXpert never prints or logs it.

Use an OpenRouter key with a credit limit, and never commit `.env`.
