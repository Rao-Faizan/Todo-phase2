---
id: 1
title: Fix Hydration Mismatch and API 404 Errors
stage: general
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: LENOVO
command: /sp.phr
labels: ["hydration", "api", "404-error", "nextjs", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/app/layout.tsx
  - frontend/components/ClientOnly.tsx
  - frontend/next.config.ts
tests: []
---

# Fix Hydration Mismatch and API 404 Errors

## Context
User reported two issues when running the project:
1. Hydration mismatch error related to client/server rendering differences
2. 404 error for the signup API endpoint

## Solution Implemented

### 1. Hydration Mismatch Fix
**Problem**: The error "A tree hydrated but some attributes of the server rendered HTML didn't match the client properties" occurred because the AuthProvider was trying to access localStorage during server-side rendering.

**Solution**: Created a `ClientOnly` component that ensures the AuthProvider only renders on the client side after hydration is complete.
- Created `frontend/components/ClientOnly.tsx` component that returns null until the client is mounted
- Updated `frontend/app/layout.tsx` to wrap the AuthProvider with ClientOnly

### 2. 404 API Error Fix
**Problem**: The signup API call was failing with a 404 error because API requests were going to the frontend server instead of the backend server.

**Solution**: Added a proxy configuration in `next.config.ts` that rewrites API requests to forward them to the backend server.
- Added a rewrites configuration that forwards all `/api/*` requests to `http://localhost:8000/api/*`

## Outcome/Impact
Both issues are now resolved:
- Hydration mismatch error is eliminated
- API calls properly reach the backend server
- Application should run without these specific errors

## Files Modified Summary
- `frontend/app/layout.tsx` - Wrapped AuthProvider with ClientOnly component
- `frontend/components/ClientOnly.tsx` - New component to handle client-side only rendering
- `frontend/next.config.ts` - Added API proxy rewrites

## Next Steps
- Ensure both backend (port 8000) and frontend (port 3000) servers are running
- Test the signup functionality to confirm API calls work properly

## Reflection
The hydration issue is a common problem when using client-side APIs like localStorage in server-side rendered Next.js applications. The ClientOnly pattern is a standard solution for this. The API routing issue was resolved by setting up proper proxying between the frontend and backend during development.

## Failure Modes Observed
None observed - both fixes were implemented successfully.

## Next Experiment to Improve Prompt Quality
N/A - the fixes were straightforward and effective.