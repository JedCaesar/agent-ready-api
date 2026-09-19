from __future__ import annotations
import hashlib, json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

class PermissionDenied(Exception): pass
class InvalidTask(Exception): pass

@dataclass(frozen=True)
class Capability:
    name:str; description:str; required_scope:str; input_schema:dict[str,str]

class AgentService:
    def __init__(self,audit_path=None):
        self.audit_path=Path(audit_path) if audit_path else None; self.results={}
        self.capabilities={
            "quote.create":Capability("quote.create","Create a non-binding quote","quotes:write",{"sku":"string","quantity":"integer"}),
            "order.status":Capability("order.status","Read an order status","orders:read",{"order_id":"string"})}
    def manifest(self):
        return {"service":"agent-ready-api","version":"1.0","principles":["least privilege","idempotent writes","auditable actions"],"capabilities":[asdict(x) for x in self.capabilities.values()]}
    def execute(self,capability,payload,scopes,idempotency_key):
        definition=self.capabilities.get(capability)
        if not definition: raise InvalidTask(f"Unknown capability: {capability}")
        if definition.required_scope not in scopes: raise PermissionDenied(f"Missing scope: {definition.required_scope}")
        missing=set(definition.input_schema)-set(payload)
        if missing: raise InvalidTask(f"Missing fields: {', '.join(sorted(missing))}")
        task_id=hashlib.sha256(f"{capability}:{idempotency_key}".encode()).hexdigest()[:16]
        if task_id in self.results: return self.results[task_id]
        if capability=="quote.create":
            output={"sku":payload["sku"],"quantity":int(payload["quantity"]),"currency":"USD","total":int(payload["quantity"])*49.0,"binding":False}
        else: output={"order_id":payload["order_id"],"status":"processing"}
        result={"task_id":task_id,"capability":capability,"status":"completed","output":output,"created_at":datetime.now(UTC).isoformat()}
        self.results[task_id]=result
        if self.audit_path:
            with self.audit_path.open("a",encoding="utf-8") as f: f.write(json.dumps(result,sort_keys=True)+"\n")
        return result

if __name__=="__main__":
    service=AgentService("audit.jsonl")
    print(json.dumps(service.manifest(),indent=2))
    print(json.dumps(service.execute("quote.create",{"sku":"AI-101","quantity":2},{"quotes:write"},"demo-1"),indent=2))
