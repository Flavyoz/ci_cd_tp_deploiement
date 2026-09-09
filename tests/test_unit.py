import pytest
from src.password_validator import validate_password

def test_length_password():
    res = validate_password("bla")

    expected = "Le mot de passe doit contenir au moins 8 caractères."
    assert expected in res.get("errors")
    assert not res.get("valid")

def test_maj():
    res = validate_password("bla")

    expected = "Le mot de passe doit contenir au moins une majuscule."
    assert expected in res.get("errors")
    assert not res.get("valid")

def test_min():
    res = validate_password("BLA")

    expected = "Le mot de passe doit contenir au moins une minuscule."
    assert expected in res.get("errors")
    assert not res.get("valid")

def test_number():
    res = validate_password("bla")

    expected = "Le mot de passe doit contenir au moins un chiffre."
    assert expected in res.get("errors")
    assert not res.get("valid")

def test_special_character():
    res = validate_password("bla")

    expected = "Le mot de passe doit contenir au moins un chiffre."
    assert expected in res.get("errors")
    assert not res.get("valid")

def test_good_password():
    res = validate_password("GoodPassword123*")

    expected = []
    assert expected == res.get("errors")
    assert res.get("valid")
