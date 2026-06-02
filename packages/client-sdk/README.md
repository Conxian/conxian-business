# `@conxian/client-sdk`

Internal client helpers for the BOS control plane.

This package is the future home for admin-facing clients that talk to trusted runtime services such as `conxian-nexus`.

## Initial functions
- health bootstrap helper
- placeholder list functions for release artifacts, audit events, governance actions, and environments
- bootstrap write helpers for release approval requests and governance decisions

## Current behavior
The write helpers currently return accepted bootstrap responses and are intended to be replaced with real admin/runtime calls.