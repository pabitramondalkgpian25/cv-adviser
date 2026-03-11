"""
tests/test_helpers.py
Unit tests for utils/helpers.py functions.
Run with: pytest tests/ -v
"""
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import truncate_text, build_download_bundle


class TestTruncateText:
    def test_short_text_unchanged(self):
        text = "Hello world"
        assert truncate_text(text, max_chars=100) == text

    def test_exact_limit_unchanged(self):
        text = "a" * 100
        assert truncate_text(text, max_chars=100) == text

    def test_long_text_truncated(self):
        text = "a" * 7000
        result = truncate_text(text, max_chars=6000)
        assert len(result) > 6000  # includes the note suffix
        assert "truncated" in result.lower()
        assert result.startswith("a" * 6000)

    def test_default_limit_is_6000(self):
        text = "b" * 7000
        result = truncate_text(text)
        assert result[:6000] == "b" * 6000


class TestBuildDownloadBundle:
    def test_bundle_contains_all_sections(self):
        bundle = build_download_bundle(
            eval_result="Eval content",
            scoring_result="Score content",
            grammar_result="Grammar content",
            skill_gap_result="Gap content",
            role="Data Scientist"
        )
        assert "CV Evaluation" in bundle
        assert "CV Scoring" in bundle
        assert "Grammar" in bundle
        assert "Skill Gap" in bundle
        assert "Data Scientist" in bundle

    def test_bundle_without_skill_gap(self):
        bundle = build_download_bundle(
            eval_result="Eval",
            scoring_result="Score",
            grammar_result="Grammar",
            skill_gap_result="",
            role="Engineer"
        )
        assert "Skill Gap" not in bundle
        assert "Eval" in bundle
