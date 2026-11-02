import tempfile
import unittest
from pathlib import Path

from ecoacao import create_app


class EcoAcaoTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_dir.name) / "test.sqlite3"
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": str(database_path),
                "SECRET_KEY": "test-secret",
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_home_shows_empty_dashboard(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Minhas a\xc3\xa7\xc3\xb5es", response.data)
        self.assertIn(b"0%", response.data)

    def test_create_action_and_update_progress(self):
        response = self.client.post(
            "/actions",
            data={
                "title": "Levar sacola reutilizável",
                "description": "No mercado",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Levar sacola reutiliz\xc3\xa1vel", response.data)
        self.assertIn(b"0%", response.data)

        response = self.client.post("/actions/1/complete", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"A\xc3\xa7\xc3\xa3o conclu\xc3\xadda", response.data)
        self.assertIn(b"100%", response.data)
        self.assertNotIn(b"Concluir", response.data)

    def test_blank_title_is_rejected(self):
        response = self.client.post(
            "/actions", data={"title": "   "}, follow_redirects=True
        )

        self.assertIn(b"Informe um nome para a a\xc3\xa7\xc3\xa3o.", response.data)
        self.assertIn(b"Suas a\xc3\xa7\xc3\xb5es aparecem aqui.", response.data)

    def test_title_over_limit_is_rejected(self):
        response = self.client.post(
            "/actions", data={"title": "a" * 81}, follow_redirects=True
        )

        self.assertIn(b"O nome deve ter at\xc3\xa9 80 caracteres.", response.data)

    def test_unknown_action_does_not_change_dashboard(self):
        response = self.client.post("/actions/999/complete", follow_redirects=True)

        self.assertIn(b"A\xc3\xa7\xc3\xa3o n\xc3\xa3o encontrada", response.data)
        self.assertIn(b"0%", response.data)


if __name__ == "__main__":
    unittest.main()
