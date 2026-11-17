"""Exercise the published Python helper without network access or extra packages."""

import contextlib
import io
from pathlib import Path
import re
import sys
import types
import unittest
from unittest.mock import Mock, patch
import warnings


SOURCE = Path(__file__).resolve().parents[2] / "src/examples/proteins-api.qmd"
SETUP = re.search(r"```\{pyodide\}\n(.*?)\n```", SOURCE.read_text(), re.DOTALL).group(1)


class ProteinSearchOutputTests(unittest.TestCase):
    def setUp(self):
        self.namespace = {"__name__": "protein_example"}
        # The helper's HTTP result is supplied below; importing requests must not
        # require installing it just to exercise the example's output behaviour.
        with patch.dict(sys.modules, {"requests": types.ModuleType("requests")}):
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(SETUP, "<setup-cell>", "exec"), self.namespace)

    def test_every_capped_cell_run_displays_incompleteness(self):
        hits = [{"mgyp": "MGYP000000000001"}, {"mgyp": "MGYP000000000002"}]
        self.namespace["get_json"] = Mock(return_value=hits)
        cell = compile(
            'hits = search_proteins(pfam_accession="PF00005", limit=2)',
            "<search-cell>",
            "exec",
        )
        # Reuse the caller and globals, but replace output each time, as the
        # browser does. A default-filtered warnings.warn only appears once.
        with warnings.catch_warnings():
            warnings.simplefilter("default")
            for run in range(2):
                output = io.StringIO()
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    exec(cell, self.namespace)
                self.assertIn("results may be incomplete", output.getvalue(), f"Run {run + 1}")
                self.assertIs(self.namespace["hits"], hits)

    def test_short_response_does_not_report_a_reached_limit(self):
        hits = [{"mgyp": "MGYP000000000001"}]
        self.namespace["get_json"] = Mock(return_value=hits)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = self.namespace["search_proteins"](pfam_accession="PF00005", limit=2)
        self.assertNotIn("results may be incomplete", output.getvalue())
        self.assertIs(result, hits)


if __name__ == "__main__":
    unittest.main()
