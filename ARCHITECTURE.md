# Architecture

## Overview

DoIt is a full-stack web application following a Client-Server architectural pattern. The backend was implemented with FastAPI providing a RESTful architecture and a React frontend. The backend uses PostgreSQL for storage, and authenticates users via JWT tokens stored in httpOnly cookies. The frontend is a Single Page Application (SPA) that communicates with the backend only over HTTP.

---
## Data Models

### User
- id (primary key)
- name
- email (unique)
- password (hashed)

### Task
- id (primary key)
- user_id (foreign key)
- title
- state (OPEN, COMPLETED, DELETED)

**Relationships:** Task.user_id → User.id

---

## Authentication Flow

1. User logs in with email and password in '/api/v1/user/auth'
2. Backend verifies credentials against the database
3. If successful, a JWT is generated and stored in an httpOnly cookie
4. On subsequent requests, the browser automatically sends the cookie
5. Backend validates the JWT on protected routes
6. On logout, `/api/v1/user/logout` clears the cookie

```
Browser                          FastAPI
  |                                |
  |  POST /auth (email, password)  |
  |------------------------------> |
  |                                | verify password & sign JWT
  |                                | 
  |  Set-Cookie: access_token      |
  | <----------------------------- |
  |                                |
  |  GET /task (cookie sent)  |
  |------------------------------> |
  |                                |
  |                                | verify JWT
  |                                |
  |  200 OK + Data                 |
  | <----------------------------- |
```

## Request Flow
React (localhost:3000)
    |
    |
    v
FastAPI (localhost:8000)
    |
    |
    v
PostgreSQL (Docker port 5433)

## CORS

The backend allows requests from: http://localhost:3000 with allow_credentials=True enabled, so that cookies are sent and recieved across two ports locally for cookie-based authentication.
