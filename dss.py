#!/usr/bin/env python3
"""CISO DSS optimizer aligned with NICE Framework.

Commands:
- plan: build an optimized workforce plan under budget.
- gap: compare current vs target workforce and report missing capabilities.

This is the main entry point. The logic has been refactored into modules
under dss_modules/ for better organization and maintainability.
"""

from dss_modules.cli import main


if __name__ == "__main__":
    main()
