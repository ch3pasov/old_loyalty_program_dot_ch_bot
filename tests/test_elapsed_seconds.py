"""Synthetic epoch arithmetic; no bot/module imports or live timestamps."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import unittest


SOURCE = Path(__file__).resolve().parents[1] / 'lib/useful_lib.py'
PROBE = '''import ast, json, sys, time
from datetime import datetime, timezone
time.tzset()
tree = ast.parse(open(sys.argv[1]).read())
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == 'seconds_between_timestamps')
namespace = {'datetime': datetime, 'timezone': timezone}
exec(compile(ast.Module(body=[function], type_ignores=[]), '<synthetic>', 'exec'), namespace)
cases = json.loads(sys.argv[2])
results = []
for after, before in cases:
    try:
        results.append(namespace['seconds_between_timestamps'](after, before))
    except (ValueError, OverflowError, OSError, TypeError) as error:
        results.append({'error': type(error).__name__})
print(json.dumps(results))
'''


def elapsed_in_zone(zone, cases):
    environment = os.environ.copy()
    environment['TZ'] = zone
    result = subprocess.run([sys.executable, '-B', '-c', PROBE, str(SOURCE), json.dumps(cases)],
                            env=environment, capture_output=True, text=True, timeout=5)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class ElapsedSecondsTest(unittest.TestCase):
    def test_fall_back_repeated_hour_is_one_elapsed_hour(self):
        # 2023-10-29 00:30 and 01:30 UTC both map to 02:30 at the local fall-back.
        self.assertEqual(elapsed_in_zone('CET-1CEST,M3.5.0/2,M10.5.0/3',
                                        [[1698543000, 1698539400]]), [3600])

    def test_spring_forward_is_one_elapsed_hour(self):
        # 2023-03-26 00:30 and 01:30 UTC map to local 01:30 and 03:30.
        self.assertEqual(elapsed_in_zone('CET-1CEST,M3.5.0/2,M10.5.0/3',
                                        [[1679794200, 1679790600]]), [3600])

    def test_reversed_transition_preserves_negative_seconds(self):
        self.assertEqual(elapsed_in_zone('CET-1CEST,M3.5.0/2,M10.5.0/3',
                                        [[1698539400, 1698543000], [1679790600, 1679794200]]),
                         [-3600, -3600])

    def test_fractional_zero_and_long_intervals_match_epoch_difference(self):
        cases = [[100.125, 99.375], [99.375, 100.125], [100, 100],
                 [200000.5, 1.25], [1698543000.75, 1698539400.25]]
        expected = [after - before for after, before in cases]
        for zone in ['UTC0', 'CET-1CEST,M3.5.0/2,M10.5.0/3', 'EST5']:
            with self.subTest(zone=zone):
                self.assertEqual(elapsed_in_zone(zone, cases), expected)

    def test_existing_datetime_rounding_and_invalid_value_errors_are_preserved(self):
        cases = [[100.123456789, 99.987654321], [float('nan'), 0],
                 [float('inf'), 0], [1e20, 0], ['invalid', 0]]
        expected = []
        for after, before in cases:
            try:
                expected.append((datetime.fromtimestamp(after, timezone.utc)
                                 - datetime.fromtimestamp(before, timezone.utc)).total_seconds())
            except (ValueError, OverflowError, OSError, TypeError) as error:
                expected.append({'error': type(error).__name__})
        self.assertEqual(elapsed_in_zone('UTC0', cases), expected)
        self.assertNotEqual(expected[0], cases[0][0] - cases[0][1])


if __name__ == '__main__':
    unittest.main()
