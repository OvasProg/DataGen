from data_generator import generate_mock_data


def test_generate_basic_schema_count():
    schema = {
        "id": {"type": "int", "min": 1, "max": 10},
        "name": {"type": "string"},
        "is_active": {"type": "bool"},
    }
    data = generate_mock_data(schema, count=5)
    assert isinstance(data, list)
    assert len(data) == 5
    assert all(isinstance(row, dict) for row in data)
    assert set(data[0].keys()) == {"id", "name", "is_active"}


def test_generate_respects_int_bounds():
    schema = {"n": {"type": "int", "min": 3, "max": 3}}
    data = generate_mock_data(schema, count=4)
    assert all(row["n"] == 3 for row in data)


def test_generate_unique_int_feasible():
    schema = {"uid": {"type": "int", "min": 1, "max": 100, "unique": True}}
    data = generate_mock_data(schema, count=50)
    values = [row["uid"] for row in data]
    assert len(values) == len(set(values))


def test_generate_pattern_string():
    schema = {"code": {"type": "string", "pattern": "[A-Z]{2}-[0-9]{3}"}}
    data = generate_mock_data(schema, count=3)
    assert all(isinstance(row["code"], str) for row in data)


def test_unique_int_exact_capacity():
    # capacity = max - min + 1 = 5
    schema = {"uid": {"type": "int", "min": 1, "max": 5, "unique": True}}
    data = generate_mock_data(schema, count=5)
    values = [row["uid"] for row in data]
    assert sorted(values) == sorted(list(range(1, 6)))


def test_text_length_respected():
    schema = {"bio": {"type": "text", "length": 50}}
    data = generate_mock_data(schema, count=10)
    assert all(len(row["bio"]) <= 50 for row in data)


def test_password_length_respected():
    schema = {"pwd": {"type": "password", "length": 16}}
    data = generate_mock_data(schema, count=5)
    assert all(isinstance(row["pwd"], str) and len(row["pwd"]) == 16 for row in data)


def test_username_unique_when_requested():
    schema = {"username": {"type": "username", "unique": True}}
    data = generate_mock_data(schema, count=50)
    values = [row["username"] for row in data]
    assert len(values) == len(set(values))


def test_float_range_respected():
    schema = {"rating": {"type": "float", "min": 1.5, "max": 2.5}}
    data = generate_mock_data(schema, count=20)
    for row in data:
        assert 1.5 <= row["rating"] <= 2.5


