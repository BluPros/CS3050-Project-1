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
    assert result["condition1"]["operator"] == "=="
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
    assert result["condition1"]["operator"] == "=="
    assert result["condition1"]["value"] == "fortnite"

def test_trailing_whitespace():
    result = parse("name=fortnite                ")
    assert result["condition1"]["field"] == "name"
    assert result["condition1"]["operator"] == "=="
    assert result["condition1"]["value"] == "fortnite"

def test_implied_and_whitespace():
    result = parse("app_id>10             release_date=10-10-2020")
    assert len(result) == 3
    assert result["condition1"]["field"] == "app_id"
    assert result["logic_op"] == "and"
    assert result["condition2"]["field"] == "release_date"

def test_metacritic_url():
    result = parse("metacritic_url=https://www.metacritic.com/game/pc/off-road-redneck-racing?ftag=MCD-06-10aaa1f")
    assert result["condition1"]["value"] == "https://www.metacritic.com/game/pc/off-road-redneck-racing?ftag=MCD-06-10aaa1f"

def test_metacritic_url_and():
    result = parse("metacritic_url=https://www.metacritic.com/game/pc/off-road-redneck-racing?ftag=MCD-06-10aaa1f and price>3.33")
    assert result["condition1"]["value"] == "https://www.metacritic.com/game/pc/off-road-redneck-racing?ftag=MCD-06-10aaa1f"
    assert result["condition2"]["value"] == "3.33"

def test_underscore_replacement():
    result = parse("name=guilty_gear_strive")
    assert result["condition1"]["value"] == "guilty gear strive"

def test_double_equals():
    result1 = parse("tag=guilty_gear_strive")
    result2 = parse("tag==guilty_gear_strive")
    print(result2)
    assert result1["condition1"]["field"] == result2["condition1"]["field"]

def test_tag_vs_tags():
    result1 = parse("tag=guilty_gear_strive")
    result2 = parse("tags=guilty_gear_strive")
    assert result1["condition1"]["field"] == result2["condition1"]["field"]

def test_category_vs_categories():
    result1 = parse("category=guilty_gear_strive")
    result2 = parse("categories=guilty_gear_strive")
    assert result1["condition1"]["field"] == result2["condition1"]["field"]

def test_genre_vs_genres():
    result1 = parse("genre=guilty_gear_strive")
    result2 = parse("genres=guilty_gear_strive")
    assert result1["condition1"]["field"] == result2["condition1"]["field"]
