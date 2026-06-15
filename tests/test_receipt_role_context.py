import unittest

from src.stegentity.receipts import make_receipt


class ReceiptRoleContextTests(unittest.TestCase):
    def test_receipt_omits_role_context_when_absent(self):
        receipt = make_receipt(
            receipt_type="execution",
            capsule_hash="sha256:test",
            capsule_id="capsule-test",
            actor_receipt_id="receipt-test",
            authority_token_id="token-test",
            adapter="local_fs",
            target="demo_target",
            result={"status": "ok"},
        )
        self.assertNotIn("role_context", receipt)
        self.assertIn("receipt_hash", receipt)

    def test_receipt_includes_role_context_when_present(self):
        receipt = make_receipt(
            receipt_type="execution",
            capsule_hash="sha256:test",
            capsule_id="capsule-test",
            actor_receipt_id="receipt-test",
            authority_token_id="token-test",
            adapter="local_fs",
            target="demo_target",
            result={"status": "ok"},
            role_context={
                "actor_role": "StegAgent",
                "counterparty_role": "StegEntity",
                "role_transition": "RT-002",
            },
        )
        self.assertEqual(receipt["role_context"]["actor_role"], "StegAgent")
        self.assertEqual(receipt["role_context"]["counterparty_role"], "StegEntity")
        self.assertIn("receipt_hash", receipt)


if __name__ == "__main__":
    unittest.main()
