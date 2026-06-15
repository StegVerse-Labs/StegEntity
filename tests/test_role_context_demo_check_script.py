import unittest

import tools.check_role_context_demo as role_context_demo_check


class RoleContextDemoCheckScriptTests(unittest.TestCase):
    def test_main_returns_zero_for_clean_demo(self):
        result_code = role_context_demo_check.main()
        self.assertEqual(result_code, 0)


if __name__ == "__main__":
    unittest.main()
