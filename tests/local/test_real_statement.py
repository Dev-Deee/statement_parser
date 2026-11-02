"""Tests against real statements on this machine. Skipped unless the path is set."""

import os

import pdfplumber
import pytest

from statement_parser.parsers.gtbank import parse_pdf
from statement_parser.pipeline.validate import check_statement

GTBANK_STATEMENT = os.environ.get("GTBANK_STATEMENT_PDF")


@pytest.mark.skipif(not GTBANK_STATEMENT, reason="Set GTBANK_STATEMENT_PDF to run")
def test_real_gtbank_statement_reconciles():
    with pdfplumber.open(GTBANK_STATEMENT) as pdf:
        statement = parse_pdf(pdf)

    summary = statement.summary
    assert len(statement.transactions) == summary.debit_count + summary.credit_count
    assert check_statement(summary, statement.transactions) == []
