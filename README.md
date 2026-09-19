# Agent-Ready API

A reference implementation for an internet where software agents are first-class users. Agents can discover capabilities, request narrowly scoped actions, safely retry writes, and leave an audit trail.

## Core ideas

- **Discovery:** a machine-readable manifest describes tasks and input schemas
- **Least privilege:** every capability declares a required scope
- **Idempotency:** repeated requests with the same key return the original result
- **Auditability:** completed actions are written as structured JSON events
- **Human control:** quote creation is explicitly non-binding

## Run it

```bash
python agent_ready_api.py
python -m unittest test_agent_ready_api.py
```

## Architecture

`AgentService` owns capability discovery, authorization, validation, idempotency, execution, and audit logging. This keeps the policy layer easy to test and ready to sit behind FastAPI, Flask, or another transport.

## Production roadmap

- OAuth 2.1 token validation and tenant isolation
- Signed agent identity and delegated authorization
- Approval gates for binding or high-value actions
- Persistent idempotency storage and distributed locking
- OpenTelemetry traces and policy decision logs

This project is a focused architecture demonstration, not a production commerce service.
