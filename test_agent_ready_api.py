import tempfile, unittest
from pathlib import Path
from agent_ready_api import AgentService, PermissionDenied

class AgentServiceTests(unittest.TestCase):
    def test_manifest(self):
        names={x["name"] for x in AgentService().manifest()["capabilities"]}
        self.assertEqual(names,{"quote.create","order.status"})
    def test_scoped_idempotent_audited_task(self):
        with tempfile.TemporaryDirectory() as directory:
            audit=Path(directory)/"audit.jsonl"; service=AgentService(audit)
            first=service.execute("quote.create",{"sku":"AI-101","quantity":2},{"quotes:write"},"request-1")
            second=service.execute("quote.create",{"sku":"AI-101","quantity":2},{"quotes:write"},"request-1")
            self.assertEqual(first,second); self.assertEqual(len(audit.read_text().splitlines()),1)
    def test_missing_scope(self):
        with self.assertRaises(PermissionDenied): AgentService().execute("order.status",{"order_id":"1"},set(),"a")

if __name__=="__main__": unittest.main()
