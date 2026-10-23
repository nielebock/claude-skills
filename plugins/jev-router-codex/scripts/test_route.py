import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('route', Path(__file__).with_name('route.py'))
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)

class RouterTests(unittest.TestCase):
    def run_hook(self, prompt, tier='tiny', confidence=.95, context=.05, fail=False):
        response = {'answers': {'tier': {'choice': tier, 'confidence': confidence}, 'needs_context': {'noul': context}}}
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {'JEV_ROUTER_HOME': temp}), patch.object(sys, 'stdin', io.StringIO(json.dumps({'prompt': prompt}))), patch.object(route, 'ask', side_effect=OSError('offline') if fail else None, return_value=response) as ask:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                route.main()
            log = Path(temp, 'log.jsonl')
            rows = log.read_text() if log.exists() else ''
            self.assertTrue(all(set(json.loads(line)) <= {'ts', 'action', 'tier', 'conf', 'ctx', 'secs', 'cost'} for line in rows.splitlines()))
            return output.getvalue(), rows, ask.call_count

    def test_model_routes(self):
        for tier, model in [('tiny', 'gpt-6-luna'), ('everyday', 'gpt-6-sol'), ('large', 'gpt-6-astra')]:
            with self.subTest(tier=tier):
                output, _, calls = self.run_hook('A fictional standalone task for routing.', tier=tier)
                context = json.loads(output)['hookSpecificOutput']['additionalContext']
                self.assertIn(model, context)
                self.assertIn('fork_turns="none"', context)
                self.assertEqual(calls, 1)

    def test_private_short_and_commands_never_call_api(self):
        for prompt in ['short', '/graphify fictional content', '!a command with enough characters', 'This fictional private message #privado', '[privado] Another fictional private message']:
            output, _, calls = self.run_hook(prompt)
            self.assertEqual((output, calls), ('', 0))

    def test_uncertain_context_hardest_and_failure_do_not_delegate(self):
        for args in [{'confidence': .4}, {'context': .9}, {'tier': 'hardest'}, {'fail': True}]:
            output, _, _ = self.run_hook('A fictional standalone task for routing.', **args)
            self.assertEqual(output, '')

    def test_off_does_not_call_api(self):
        with patch.object(route, 'enabled', return_value=False):
            _, _, calls = self.run_hook('A fictional standalone task for routing.')
            self.assertEqual(calls, 0)

if __name__ == '__main__':
    unittest.main()
