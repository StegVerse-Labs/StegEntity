import unittest

from tools import verify_activation_manifest


class ActivationManifestVerifierTests(unittest.TestCase):
    def test_activation_manifest_verifier_main_returns_zero(self):
        self.assertEqual(verify_activation_manifest.main(), 0)


if __name__ == "__main__":
    unittest.main()
