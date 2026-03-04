## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: workflow had legacy trigger mix and no explicit write permission declaration.
- Fixes made: switched to schedule + manual dispatch, upgraded action versions, and added `permissions: contents: write`.
- Validation: checked updater sequence (`make`, `make clean`) and commit target (`data/`).
- Known blockers: none identified in this remediation pass.
