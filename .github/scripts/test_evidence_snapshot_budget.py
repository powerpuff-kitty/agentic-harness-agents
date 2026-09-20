"""Failed text validation must not evade the selected-evidence read budget."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_evidence_snapshot import helper


class EvidenceSnapshotBudget(unittest.TestCase):
    def test_failed_nontext_reads_consume_total_budget(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / 'AGENTS.md').write_text('Keep required evidence.\n')
            before = helper.capture(root, ['AGENTS.md'], 'fixture')
            names = ['bad' + str(i) for i in range(4)]
            for name in names:
                (root / name).write_bytes(b'\0' * 20)
            with patch.object(helper, 'MAX_TOTAL_BYTES', 64):
                result = helper.compare(root, names, 'fixture', before)
            self.assertEqual(result['measurement']['hashed_source_bytes'], 0)
            self.assertEqual(result['measurement']['read_source_bytes'], 60)
            self.assertEqual(result['unavailable'][-1]['reason'], 'input-limit')
            self.assertEqual(result['status'], 'refresh-required')


if __name__ == '__main__':
    unittest.main()
