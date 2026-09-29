import pytest
from parser import parse

def test_single_condition_with_number():
    result = parse("price>10")
    assert result["condition1"]["field"] == "price"
    assert result["condition1"]["operator"] == ">"
    assert result["condition1"]["value"] == "10"

def test_single_condition_with_string():
    result = parse("name=fortnite")
    assert result["condition1"]["field"] == "name"
    assert result["condition1"]["operator"] == "="
    assert result["condition1"]["value"] == "fortnite"

def test_implied_and():
    result = parse("app_id>10 release_date=10-10-2020")
    assert len(result) == 3
    assert result["condition1"]["field"] == "app_id"
    assert result["logic_op"] == "and"
    assert result["condition2"]["field"] == "release_date"

def test_explicit_and():
    result = parse("price>10 and name=minecraft")
    assert len(result) == 3
    assert result["condition1"]["field"] == "price"
    assert result["condition2"]["field"] == "name"

def test_explicit_or():
    result = parse("price>10 or name=minecraft")
    assert len(result) == 3
    assert result["condition1"]["field"] == "price"
    assert result["logic_op"] == "or"
    assert result["condition2"]["field"] == "name"

def test_not_equal():
    result = parse("metacritic_url!=www.google.com")
    assert result["condition1"]["field"] == "metacritic_url"
    assert result["condition1"]["operator"] == "!="
    assert result["condition1"]["value"] == "www.google.com"

def test_empty_string():
    result = parse("")
    assert result is None

def test_invalid_field():
    result = parse("fish=10")
    assert result is None

def test_invalid_operator():
    result = parse("name===deep_rock_galactic")
    assert result is None

def test_missing_field():
    result = parse("=deep_rock_galactic")
    assert result is None

def test_missing_operator():
    result = parse("namedeep_rock_galactic")
    assert result is None

def test_missing_value():
    result = parse("name=")
    assert result is None

def test_missing_condition2():
    result = parse("name=fortnite or")
    assert result is None

def test_improper_case():
    result = parse("nAme=fortnite")
    assert result is None

def test_leading_whitespace():
    result = parse("     name=fortnite")
    assert result["condition1"]["field"] == "name"
    assert result["condition1"]["operator"] == "="
    assert result["condition1"]["value"] == "fortnite"

def test_trailing_whitespace():
    result = parse("name=fortnite                ")
    assert result["condition1"]["field"] == "name"
    assert result["condition1"]["operator"] == "="
    assert result["condition1"]["value"] == "fortnite"

def test_implied_and_whitespace():
    result = parse("app_id>10             release_date=10-10-2020")
    assert len(result) == 3
    assert result["condition1"]["field"] == "app_id"
    assert result["logic_op"] == "and"
    assert result["condition2"]["field"] == "release_date"