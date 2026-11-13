# Notes: AI answer panel test

- Product: workplace search, sold to companies (tenants) by seat.
- Test: 2026-09-01 to 2026-09-28. Users were randomized 50/50 to control or treatment (the panel) inside every tenant. 412 tenants, about 180,000 active users.
- Success: a search session with a click that dwells 30 seconds or more, or an answer copied.
- Session logs go back to 2026-06-01.

## Tables

- search_sessions(session_id, user_id, tenant_id, arm, date, success, used_3p_result)
- users(user_id, tenant_id, arm, signup_date)
- tenants(tenant_id, seats, segment): segment is '3P power' or 'standard', set by sales from how many connectors the tenant has installed. 61 tenants are '3P power'.

## Open

- Tenants vary from 5 to 9,000 seats.
- Sales and the PM both talk about "3P power" customers.
