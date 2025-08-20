from format_utils import convert_to_csv, convert_to_xml, convert_to_sql, convert_to_html


SAMPLE = [
    {"id": 1, "name": "Alice", "city": "Paris"},
    {"id": 2, "name": "Bob", "city": "Berlin"},
]


def test_convert_to_csv_basic():
    csv_text = convert_to_csv(SAMPLE)
    assert "id,name,city" in csv_text.splitlines()[0]
    # header + 2 rows
    assert len([l for l in csv_text.splitlines() if l.strip()]) == 3


def test_convert_to_xml_basic():
    xml_text = convert_to_xml(SAMPLE)
    assert "<data>" in xml_text
    assert xml_text.count("<record>") == 2
    assert "<name>Alice</name>" in xml_text or "<name>Bob</name>" in xml_text


def test_convert_to_sql_basic():
    sql_text = convert_to_sql(SAMPLE, table_name="people")
    lines = [l for l in sql_text.splitlines() if l.strip()]
    assert len(lines) == 2
    assert lines[0].startswith("INSERT INTO people (")


def test_convert_to_html_basic():
    html_text = convert_to_html(SAMPLE)
    assert "<table" in html_text and "</table>" in html_text
    assert "<th>id</th>" in html_text and "<th>name</th>" in html_text
    # header + 2 rows
    assert html_text.count("<tr>") >= 3


