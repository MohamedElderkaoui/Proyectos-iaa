import json
import unittest
from pathlib import Path


PWA_ROOT = Path(__file__).resolve().parent / "mobile_pwa"


class MobilePwaTests(unittest.TestCase):
    def test_manifest_has_installable_app_fields_and_local_icons(self):
        manifest = json.loads((PWA_ROOT / "manifest.webmanifest").read_text("utf-8"))

        self.assertEqual(manifest["display"], "standalone")
        self.assertTrue(manifest["start_url"])
        icon_sizes = {icon["sizes"] for icon in manifest["icons"]}
        self.assertIn("192x192", icon_sizes)
        self.assertIn("512x512", icon_sizes)
        for icon in manifest["icons"]:
            self.assertTrue((PWA_ROOT / icon["src"]).is_file())

    def test_shell_links_its_manifest_and_registers_local_service_worker(self):
        html = (PWA_ROOT / "index.html").read_text("utf-8")
        script = (PWA_ROOT / "app.js").read_text("utf-8")

        self.assertIn('rel="manifest" href="./manifest.webmanifest"', html)
        self.assertIn('src="./app.js"', html)
        self.assertIn('register("./sw.js")', script)

    def test_reverse_proxy_serves_pwa_and_forwards_streamlit_on_one_host(self):
        config = (PWA_ROOT / "Caddyfile.example").read_text("utf-8")

        self.assertIn("handle_path /mobile_pwa/*", config)
        self.assertIn("root * ./mobile_pwa", config)
        self.assertIn("reverse_proxy 127.0.0.1:8501", config)


if __name__ == "__main__":
    unittest.main()
