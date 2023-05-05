from app.models.planet import Planet
from werkzeug.exceptions import HTTPException
from app.routes import validate_id
import pytest

# test to_dict method
def test_to_dict_no_missing_data_returns_expected_dictionary(one_planet):
    result = one_planet.to_dict()
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] == "Mars"
    assert result["description"] == "Roman god of war, aka Ares."
    assert result["number_of_moons"] == 2

def test_to_dict_missing_id_returns_expected_dictionary_with_id_None():
    test_data = Planet(name="Mars",
                    description="Roman god of war, aka Ares.",
                    number_of_moons= 2)
    result = test_data.to_dict()
    assert len(result) == 4
    assert result["id"] is None
    assert result["name"] == "Mars"
    assert result["description"] == "Roman god of war, aka Ares."
    assert result["number_of_moons"] == 2

def test_to_dict_missing_name_returns_expected_dictionary_with_name_None():
    test_data = Planet(id=1,
                    description="Roman god of war, aka Ares.",
                    number_of_moons= 2)
    result = test_data.to_dict()
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] is None
    assert result["description"] == "Roman god of war, aka Ares."
    assert result["number_of_moons"] == 2

def test_to_dict_missing_description_returns_expected_dictionary_with_description_None():
    test_data = Planet(id=1,
                    name="Mars",
                    number_of_moons= 2)
    result = test_data.to_dict()
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] == "Mars"
    assert result["description"] is None
    assert result["number_of_moons"] == 2

def test_to_dict_missing_number_of_moons_returns_expected_dictionary_with_number_of_moons_None():
    test_data = Planet(id=1,
                    name="Mars",
                    description="Roman god of war, aka Ares.")
    result = test_data.to_dict()
    assert len(result) == 4
    assert result["id"] == 1
    assert result["name"] == "Mars"
    assert result["description"] == "Roman god of war, aka Ares."
    assert result["number_of_moons"] is None

# test from_dict method
def test_from_dict_returns_planet():
    test_data = {
                "name" : "Jupiter",
                "description": "King of the Roman gods, aka Zeus.",
                "number_of_moons": 79}
    new_planet = Planet.from_dict(test_data)
    assert new_planet.name == "Jupiter"
    assert new_planet.description == "King of the Roman gods, aka Zeus."

def test_from_dict_with_no_name(): ########################## How can I check if I get a KeyError
    test_data = {
                "description": "King of the Roman gods, aka Zeus.",
                "number_of_moons": 79}
    # new_planet = Planet.from_dict(test_data)
    # assert new_planet.name == "Jupiter"
    # assert new_planet.description == "King of the Roman gods, aka Zeus."

    with pytest.raises(KeyError, match = 'name'):
        new_planet = Planet.from_dict(test_data)
        

# def test_from_dict_with_no_description():
#     test_data = {
#                 "name" : "Jupiter",
#                 "number_of_moons": 79}
#     with pytest.raises(KeyError, match = 'description'):
#         new_book = Planet.from_dict(test_data)

# def test_from_dict_with_extra_keys():
#     test_data = {
#         "extra": "some stuff",
#         "title": "New Book",
#         "description": "The Best!",
#         "another": "last value"
#     }
#     new_planet = Planet.from_dict(test_data)
#     assert new_planet.title == "New Book"
#     assert new_planet.description == "The Best!"

#================================================
def test_validate_id(one_planet):
    result_book = validate_id("1")
    assert result_book.id == 1
    assert result_book.name== "Mars"
    assert result_book.description == "Roman god of war, aka Ares."
    assert result_book.number_of_moons == 2

def test_validate_id_missing_record_raises_eception(one_planet):
    with pytest.raises(HTTPException):
        result_planet = validate_id("3")
    
def test_validate_id_invalid_id_raises_exception(one_planet):
    with pytest.raises(HTTPException):
        result_book = validate_id("cat")
