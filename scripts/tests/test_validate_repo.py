from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_repo.py"
SPEC = importlib.util.spec_from_file_location("validate_repo", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class RepositoryValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        skill = self.root / "example-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: example-skill\ndescription: Example validation fixture.\n---\n\n# Example\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def messages(self) -> list[str]:
        return [finding.message for finding in VALIDATOR.run(self.root)]

    def test_valid_minimal_repository_passes(self) -> None:
        self.assertEqual(self.messages(), [])

    def test_broken_local_link_is_rejected(self) -> None:
        (self.root / "README.md").write_text("[missing](missing.md)\n", encoding="utf-8")
        self.assertTrue(any("本地链接目标不存在" in message for message in self.messages()))

    def test_private_key_marker_is_rejected_without_echoing_secret(self) -> None:
        (self.root / "leaked.txt").write_text(
            "-----" + "BEGIN PRIVATE KEY-----\nfixture\n",
            encoding="utf-8",
        )
        findings = VALIDATOR.run(self.root)
        self.assertTrue(any("疑似真实 private key" in item.message for item in findings))
        self.assertFalse(any(("BEGIN" + " PRIVATE KEY") in item.render() for item in findings))

    def test_environment_file_is_rejected_but_example_is_allowed(self) -> None:
        (self.root / ".env.production").write_text("TOKEN=fixture\n", encoding="utf-8")
        self.assertTrue(any("高风险凭据文件" in message for message in self.messages()))
        (self.root / ".env.production").unlink()
        (self.root / ".env.example").write_text("TOKEN=replace-me\n", encoding="utf-8")
        self.assertEqual(self.messages(), [])

    def test_private_identity_is_rejected_without_echoing_name(self) -> None:
        real_name = "张" + "硕"
        (self.root / "README.md").write_text(f"Maintained by {real_name}.\n", encoding="utf-8")
        findings = VALIDATOR.run(self.root)
        self.assertTrue(any("真实中文姓名" in item.message for item in findings))
        self.assertFalse(any(real_name in item.render() for item in findings))


if __name__ == "__main__":
    unittest.main()
