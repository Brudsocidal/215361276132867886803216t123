import json
import tempfile
import unittest
from pathlib import Path
import app as api

class ApiSmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_base = api.BASE
        api.BASE = Path(self.temp.name)
        (api.BASE / "whitelist.json").write_text("[]", encoding="utf-8")
        (api.BASE / "games.json").write_text(json.dumps({"gta":{"released":True,"module_name":"gta_module"}}), encoding="utf-8")
        (api.BASE / "version.json").write_text(json.dumps({"latest_version":"1.0.0","download_url":"","checksum":"","release_notes":""}), encoding="utf-8")
        api.SESSIONS.clear()
        self.client = api.app.test_client()
    def tearDown(self):
        api.BASE = self.old_base
        self.temp.cleanup()
    def test_health(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)
    def test_version(self):
        self.assertEqual(self.client.get("/api/version").json["latest_version"], "1.0.0")
    def test_game_status(self):
        self.assertTrue(self.client.get("/api/game/gta/status").json["released"])
    def test_admin_denied_without_token(self):
        self.assertEqual(self.client.post("/api/broadcast", json={"message":"hello"}).status_code, 403)

if __name__ == "__main__": unittest.main()
