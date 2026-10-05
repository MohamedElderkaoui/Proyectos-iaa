import os
import tempfile
import unittest
from pathlib import Path

from accessai_checkpoint import find_latest_four_class_checkpoint


class FindLatestFourClassCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.project = self.root / "project"
        self.home = self.root / "home"
        self.project.mkdir()
        self.home.mkdir()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def checkpoint(self, base: Path, run_name: str, modified_at: int) -> Path:
        path = base / "runs" / "detect" / run_name / "weights" / "best.pt"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"checkpoint")
        os.utime(path, (modified_at, modified_at))
        return path.resolve()

    def test_selects_newest_four_class_checkpoint_across_project_and_home(self):
        older = self.checkpoint(
            self.home, "AccessAI_Proto3_yolo26n_4clases", 100
        )
        newest = self.checkpoint(
            self.project, "AccessAI_YOLO26s_4clases_RTX4060_FAST", 200
        )

        result = find_latest_four_class_checkpoint(self.project, self.home)

        self.assertEqual(result, newest)
        self.assertNotEqual(result, older)

    def test_ignores_newer_checkpoint_without_four_class_marker(self):
        valid = self.checkpoint(
            self.project, "AccessAI_YOLO26s_4clases_RTX4060_FAST", 100
        )
        self.checkpoint(self.home, "AccessAI_YOLO26x_25clases", 200)

        result = find_latest_four_class_checkpoint(self.project, self.home)

        self.assertEqual(result, valid)


if __name__ == "__main__":
    unittest.main()
