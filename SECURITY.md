# Security Policy

## Supported versions

This is a learning-oriented cookbook. Fixes are applied to the latest `main` and
the most recent tagged release.

| Version | Supported |
|---------|-----------|
| latest `main` | ✅ |
| older tags | ❌ |

## Reporting a vulnerability

Please **do not** open a public issue for security problems. Use GitHub's private
reporting instead:

1. Open the **Security** tab of this repository.
2. Click **Report a vulnerability** (GitHub Private Vulnerability Reporting).

If private reporting is not enabled yet, open a regular issue asking the
maintainer to turn it on — without including any sensitive details.

## Scope

These recipes run a simulator and bridge topics. The main practical risk is
running **untrusted SDF, world, model or launch files**, which can load plugins
that execute code on your machine. Treat third-party world/model files like any
other untrusted code, and review them before running.
