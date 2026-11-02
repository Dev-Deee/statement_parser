from datetime import date

import pytest

from statement_parser.data.models.enums.statuses import Channel, Direction
from statement_parser.parsers.gtbank import parse_row

DATE = "04\xadMay\xad\n2026"

TRANSFER_OUT = [
    DATE,
    "'GTW",
    DATE,
    "2,000.00",
    "",
    "250,818.19",
    "NIBSS Instant Payment\nOutward\n000013260504180333000…\nLAUNDRY TO OPAY \xad\nJANE\nDOE",
]
TRANSFER_IN = [
    "05\xadMay\xad\n2026",
    "'10000400000000000001NIP",
    "05\xadMay\xad\n2026",
    "",
    "1,500.00",
    "251,307.44",
    "TRANSFER BETWEEN\nCUSTOMERS\n100004000000000000001…\nMISCELLANEOUS\xadOPAY\xad\nJOHN\nROE",
]
AIRTIME = [
    DATE,
    "'1234567890AIR",
    DATE,
    "1,000.00",
    "",
    "249,807.44",
    "Airtime Purchase VIA\nAIRTIME VIA USSD\xadMTN\n101CT0000000001234567…\nFROM DOE, JOHN\nTO MTN",
]
SMS_CHARGE = [
    DATE,
    "'",
    DATE,
    "486.09",
    "",
    "252,861.10",
    "SMS CHARGE SMS ALERT\nCHARGE FOR 29MAR2026\nto 27APR2026 Recover\nPartial Charges",
]
NIP_COMMISSION = [
    DATE,
    "'GTW",
    DATE,
    "10.00",
    "",
    "250,808.19",
    "Commission on NIP\nTransfer CHARGES",
]
VAT_ON_CHARGE = [DATE, "'GTW", DATE, ".75", "", "250,807.44", "VAT CHARGES"]
TRUNCATED_REFERENCE = [
    DATE,
    "'00000000001234567890G…",
    DATE,
    "500.00",
    "",
    "237,059.06",
    "TRANSFER BETWEEN\nCUSTOMERS VIA\nGTWORLD FOOD FROM\nDOE, JOHN",
]


def test_outward_transfer():
    transaction = parse_row(TRANSFER_OUT)

    assert transaction.transaction_date == date(2026, 5, 4)
    assert transaction.value_date == date(2026, 5, 4)
    assert transaction.direction == Direction.DEBIT
    assert transaction.amount_kobo == 200_000
    assert transaction.balance_after_kobo == 25_081_819
    assert transaction.channel == Channel.TRANSFER_OUT
    assert transaction.bank_reference is None  # 'GTW is a type code, not an ID
    assert transaction.narration == (
        "NIBSS Instant Payment Outward 000013260504180333000… LAUNDRY TO OPAY - JANE DOE"
    )
    assert transaction.narration_truncated is True


def test_inward_transfer_keeps_its_reference():
    transaction = parse_row(TRANSFER_IN)

    assert transaction.direction == Direction.CREDIT
    assert transaction.amount_kobo == 150_000
    assert transaction.channel == Channel.TRANSFER_IN
    assert transaction.bank_reference == "10000400000000000001NIP"


def test_airtime_purchase():
    transaction = parse_row(AIRTIME)

    assert transaction.channel == Channel.AIRTIME
    assert transaction.bank_reference == "1234567890AIR"


def test_sms_charge_with_empty_reference():
    transaction = parse_row(SMS_CHARGE)

    assert transaction.amount_kobo == 48_609
    assert transaction.bank_reference is None
    assert transaction.channel == Channel.BANK_CHARGE
    assert transaction.narration_truncated is False


@pytest.mark.parametrize(("row", "kobo"), [(NIP_COMMISSION, 1_000), (VAT_ON_CHARGE, 75)])
def test_transfer_charges_are_bank_charges_not_transfers(row, kobo):
    transaction = parse_row(row)

    assert transaction.channel == Channel.BANK_CHARGE
    assert transaction.amount_kobo == kobo


def test_truncated_reference_is_not_used_as_an_id():
    assert parse_row(TRUNCATED_REFERENCE).bank_reference is None


def test_rejects_row_with_both_debit_and_credit():
    row = TRANSFER_OUT.copy()
    row[4] = "100.00"
    with pytest.raises(ValueError):
        parse_row(row)


def test_rejects_row_with_neither_debit_nor_credit():
    row = TRANSFER_OUT.copy()
    row[3] = ""
    with pytest.raises(ValueError):
        parse_row(row)


def test_rejects_row_with_wrong_column_count():
    with pytest.raises(ValueError):
        parse_row(TRANSFER_OUT[:6])
