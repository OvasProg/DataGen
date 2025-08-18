import csv
import io
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Dict


def convert_to_csv(data: List[Dict]) -> str:
    if not data:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def convert_to_xml(data: List[Dict]) -> str:
    if not data:
        return "<?xml version='1.0' encoding='UTF-8'?><data></data>"

    root = ET.Element("data")
    for item in data:
        record = ET.SubElement(root, "record")
        for key, value in item.items():
            field = ET.SubElement(record, key)
            field.text = str(value)

    rough_string = ET.tostring(root, 'unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def convert_to_sql(data: List[Dict], table_name: str = "generated_data") -> str:
    if not data:
        return ""

    columns = list(data[0].keys())
    sql_statements = []

    for item in data:
        values = []
        for column in columns:
            value = item[column]
            if isinstance(value, str):
                escaped_value = str(value).replace("'", "''")
                value = f"'{escaped_value}'"
            else:
                value = str(value)
            values.append(value)

        sql_statements.append(
            f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
        )

    return "\n".join(sql_statements)


def convert_to_html(data: List[Dict]) -> str:
    if not data:
        return "<html><body><table></table></body></html>"

    html = ["<html>", "<body>", "<table border='1'>", "<thead>", "<tr>"]

    for key in data[0].keys():
        html.append(f"<th>{key}</th>")
    html.append("</tr>")
    html.append("</thead>")
    html.append("<tbody>")

    for item in data:
        html.append("<tr>")
        for value in item.values():
            html.append(f"<td>{value}</td>")
        html.append("</tr>")

    html.append("</tbody>")
    html.append("</table>")
    html.append("</body>")
    html.append("</html>")

    return "\n".join(html)


