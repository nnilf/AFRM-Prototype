import pytest

from validation import check_number, validate_inputs


def test_fr01_accepts_valid_inputs():
    assert validate_inputs("6000", 2400, 1200, 800, 1875) == (6000, 2400, 1200, 800, 1875)


def test_fr01_rejects_negative():
    with pytest.raises(ValueError):
        check_number("fuel", -1)


def test_fr01_rejects_zero_fuel_flow():
    with pytest.raises(ValueError):
        validate_inputs(6000, 0, 1200, 800, 1875)


def test_fr01_rejects_zero_groundspeed():
    with pytest.raises(ValueError):
        validate_inputs(6000, 2400, 1200, 0, 1875)


def test_fr01_rejects_zero_protected():
    with pytest.raises(ValueError):
        validate_inputs(6000, 2400, 1200, 800, 0)


def test_fr01_rejects_non_numeric():
    with pytest.raises(ValueError):
        check_number("fuel", "abc")


def test_fr01_rejects_nan():
    with pytest.raises(ValueError):
        check_number("fuel", float("nan"))


def test_fr01_rejects_infinity():
    with pytest.raises(ValueError):
        check_number("fuel", float("inf"))
