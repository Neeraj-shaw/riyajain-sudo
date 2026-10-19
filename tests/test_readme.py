"""Run with: python3 -m unittest discover -s tests -v."""
from pathlib import Path
import re
import unittest
from urllib.parse import parse_qs, urlsplit

README = Path(__file__).resolve().parents[1] / "README.md"


class ProfileReadmeTests(unittest.TestCase):
    def test_stats_images_have_valid_login_and_alt_text(self):
        text = README.read_text(encoding="utf-8")
        images = re.findall(r"!\[([^\]]*)\]\((https://[^)]+)\)", text)
        cards = [(alt, url) for alt, url in images if urlsplit(url).hostname in {
            "github-readme-stats.shion.dev", "streak-stats.demolab.com", "komarev.com"
        }]
        self.assertEqual(len(cards), 4)
        for alt, url in cards:
            with self.subTest(url=url):
                self.assertTrue(alt.strip())
                self.assertFalse(any(char.isspace() for char in url))
                query = parse_qs(urlsplit(url).query)
                self.assertEqual(query.get("username", query.get("user")), ["riyajain-sudo"])

    def test_direct_activity_fallback_is_available(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("https://github.com/riyajain-sudo?tab=overview", text)
        self.assertIn("third-party services", text)


if __name__ == "__main__":
    unittest.main()
