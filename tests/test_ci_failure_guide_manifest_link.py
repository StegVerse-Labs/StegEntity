import json
import unittest
from pathlib import Path


class CIFailureGuideManifestLinkTests(unittest.TestCase):
    def test_ci_failure_guide_is_registered_and_present(self):
        manifest = json.loads(Path("activation_manifest.json").read_text(encoding="utf-8"))
        documents = manifest["documents"]

        self.assertIn("ci_failure_guide", documents)
        self.assertEqual(documents["ci_failure_guide"], "docs/STEGENTITY_CI_FAILURE_GUIDE.md")
        self.assertTrue(Path(documents["ci_failure_guide"]).exists())


if __name__ == "__main__":
    unittest.main()
