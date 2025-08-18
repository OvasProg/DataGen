from flask import Flask, request, jsonify, Response, make_response
from werkzeug.exceptions import HTTPException
from data_generator import generate_mock_data
from format_utils import convert_to_csv, convert_to_xml, convert_to_sql, convert_to_html
import os

def create_app():
    app = Flask(__name__)

    # Production-friendly JSON behavior
    app.config["JSON_AS_ASCII"] = False
    app.config["JSON_SORT_KEYS"] = False

    # Request limits (16 MB)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    # --- Simple security headers on every response ---
    @app.after_request
    def set_security_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "no-referrer")
        resp.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        # CORS – allow your Netlify app origin via env var (fallback: *)
        allow_origin = os.getenv("CORS_ALLOW_ORIGIN", "*")
        resp.headers.setdefault("Access-Control-Allow-Origin", allow_origin)
        resp.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        resp.headers.setdefault("Access-Control-Allow-Headers", "Content-Type,Authorization")
        return resp

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Welcome to DataGen API",
            "endpoints": ["/healthz", "/info", "/example", "/generate"]
        })

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return jsonify({"status": "ok"}), 200

    @app.route('/info', methods=['GET'])
    def get_info():
        return jsonify({
            "supported_data_types": {
                "string": {"description": "Random string value", "parameters": {"pattern": "Regex pattern for custom string generation (optional)", "unique": "Boolean to ensure unique values (optional)"}},
                "int": {"description": "Random integer value", "parameters": {"min": "Minimum value (default: 0)", "max": "Maximum value (default: 100)", "unique": "Boolean to ensure unique values (optional)"}},
                "float": {"description": "Random float value", "parameters": {"min": "Minimum value (default: 0)", "max": "Maximum value (default: 100)", "unique": "Boolean to ensure unique values (optional)"}},
                "bool": {"description": "Random boolean value", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "date": {"description": "Random date value", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "uuid": {"description": "Random UUID value", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "email": {"description": "Random email address", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "name": {"description": "Random full name (first + last)", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "first_name": {"description": "Random first name", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "last_name": {"description": "Random last name", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "text": {"description": "Random text content", "parameters": {"length": "Maximum number of characters (default: 200)", "unique": "Boolean to ensure unique values (optional)"}},
                "username": {"description": "Random username", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "password": {"description": "Random password", "parameters": {"length": "Password length (default: 12)", "unique": "Boolean to ensure unique values (optional)"}},
                "city": {"description": "Random city name", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "country": {"description": "Random country name", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "zipcode": {"description": "Random postal code", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "address": {"description": "Random full address", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "phone": {"description": "Random phone number", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "url": {"description": "Random URL", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "ip": {"description": "Random IPv4 address", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "price": {"description": "Random price value (1.0 to 1000.0)", "parameters": {"unique": "Boolean to ensure unique values (optional)"}},
                "credit_card": {"description": "Random credit card number", "parameters": {"unique": "Boolean to ensure unique values (optional)"}}
            },
            "global_parameters": {"count": "Number of records to generate (default: 10, max: 10000)", "format": "Output format (default: json)"},
            "supported_output_formats": ["json", "csv", "xml", "sql", "html"],
            "performance_notes": {"max_recommended_count": 10000, "unique_fields_impact": "Fields with unique constraints may slow down generation", "format_impact": "CSV and SQL formats are fastest for large datasets"}
        })

    @app.route('/example', methods=['GET'])
    def get_example():
        return jsonify({
            "message": "Example schema configurations for DataGen API",
            "examples": {
                "user_profile": {"description": "Complete user profile with various field types", "count": 50, "format": "json",
                                 "schema": {"user_id": {"type": "int", "min": 1000, "max": 9999, "unique": True},
                                            "username": {"type": "username", "unique": True},
                                            "email": {"type": "email", "unique": True},
                                            "password": {"type": "password", "length": 16},
                                            "first_name": {"type": "first_name"},
                                            "last_name": {"type": "last_name"},
                                            "full_name": {"type": "name", "unique": True},
                                            "age": {"type": "int", "min": 18, "max": 80},
                                            "bio": {"type": "text", "length": 300},
                                            "is_active": {"type": "bool"},
                                            "signup_date": {"type": "date"},
                                            "last_login": {"type": "date"},
                                            "profile_uuid": {"type": "uuid", "unique": True}}},
                "ecommerce_product": {"description": "E-commerce product catalog", "count": 100, "format": "csv",
                                      "schema": {"product_id": {"type": "int", "min": 1, "max": 10000, "unique": True},
                                                 "sku": {"type": "string", "pattern": "[A-Z]{2}-[0-9]{4}-[A-Z]{2}", "unique": True},
                                                 "product_name": {"type": "string", "pattern": "[A-Z][a-z]+ [A-Z][a-z]+"},
                                                 "description": {"type": "text", "length": 500},
                                                 "price": {"type": "price"},
                                                 "cost": {"type": "float", "min": 5.0, "max": 200.0},
                                                 "stock_quantity": {"type": "int", "min": 0, "max": 1000},
                                                 "category": {"type": "string", "pattern": "(Electronics|Clothing|Books|Home|Sports)"},
                                                 "is_featured": {"type": "bool"},
                                                 "created_date": {"type": "date"},
                                                 "product_url": {"type": "url"}}},
                "customer_order": {"description": "Customer order with shipping information", "count": 75, "format": "xml",
                                   "schema": {"order_id": {"type": "int", "min": 100000, "max": 999999, "unique": True},
                                              "customer_email": {"type": "email", "unique": True},
                                              "customer_name": {"type": "name"},
                                              "phone": {"type": "phone"},
                                              "shipping_address": {"type": "address"},
                                              "city": {"type": "city"},
                                              "state": {"type": "string", "pattern": "[A-Z]{2}"},
                                              "zipcode": {"type": "zipcode"},
                                              "country": {"type": "country"},
                                              "order_total": {"type": "float", "min": 10.0, "max": 2000.0},
                                              "tax_amount": {"type": "float", "min": 0.0, "max": 200.0},
                                              "shipping_cost": {"type": "float", "min": 0.0, "max": 50.0},
                                              "order_date": {"type": "date"},
                                              "estimated_delivery": {"type": "date"},
                                              "order_status": {"type": "string", "pattern": "(Pending|Processing|Shipped|Delivered|Cancelled)"},
                                              "tracking_number": {"type": "string", "pattern": "[A-Z]{2}[0-9]{9}[A-Z]{2}", "unique": True}}},
                "system_log": {"description": "System log entries with various data types", "count": 200, "format": "sql",
                               "schema": {"log_id": {"type": "int", "min": 1, "max": 1000000, "unique": True},
                                          "timestamp": {"type": "date"},
                                          "level": {"type": "string", "pattern": "(INFO|WARNING|ERROR|DEBUG|CRITICAL)"},
                                          "service": {"type": "string", "pattern": "(web|api|database|auth|payment)"},
                                          "user_id": {"type": "int", "min": 1, "max": 10000},
                                          "ip_address": {"type": "ip"},
                                          "user_agent": {"type": "string", "pattern": "Mozilla/[0-9.]+ \\([^)]+\\) [A-Za-z]+/[0-9.]+"},
                                          "request_url": {"type": "url"},
                                          "response_code": {"type": "int", "min": 200, "max": 599},
                                          "response_time": {"type": "float", "min": 0.01, "max": 10.0},
                                          "message": {"type": "text", "length": 200},
                                          "session_id": {"type": "uuid"},
                                          "is_error": {"type": "bool"}}},
                "simple_contact": {"description": "Simple contact list with basic fields", "count": 25, "format": "html",
                                   "schema": {"id": {"type": "int", "min": 1, "max": 1000, "unique": True},
                                              "name": {"type": "name"},
                                              "email": {"type": "email"},
                                              "phone": {"type": "phone"},
                                              "city": {"type": "city"},
                                              "notes": {"type": "text", "length": 100}}}
            }
        })

    @app.route('/generate', methods=['POST', 'OPTIONS'])
    def generate():
        # Handle CORS preflight quickly
        if request.method == 'OPTIONS':
            return make_response(('', 204))

        try:
            body = request.get_json(silent=True)
            if not body or not isinstance(body, dict):
                return jsonify({"error": "No JSON data provided"}), 400

            count = body.get("count", 10)
            out_format = body.get("format", "json")

            if not isinstance(count, int) or count <= 0:
                return jsonify({"error": "Count must be a positive integer"}), 400
            if count > 10000:
                return jsonify({"error": "Count cannot exceed 10000 for performance reasons"}), 400

            # Build schema from remaining keys
            schema = {k: body[k] for k in body.keys() if k not in ["count", "format"]}
            if not schema:
                return jsonify({"error": "No schema fields provided"}), 400
            if not isinstance(schema, dict):
                return jsonify({"error": "Schema must be an object/dict"}), 400

            data = generate_mock_data(schema, count)

            fmt = str(out_format).lower()
            if fmt == "json":
                return jsonify(data), 200
            elif fmt == "csv":
                csv_data = convert_to_csv(data)
                return Response(csv_data, mimetype='text/csv',
                                headers={'Content-Disposition': 'attachment; filename=generated_data.csv'})
            elif fmt == "xml":
                xml_data = convert_to_xml(data)
                return Response(xml_data, mimetype='application/xml',
                                headers={'Content-Disposition': 'attachment; filename=generated_data.xml'})
            elif fmt == "sql":
                sql_data = convert_to_sql(data)
                return Response(sql_data, mimetype='text/plain',
                                headers={'Content-Disposition': 'attachment; filename=generated_data.sql'})
            elif fmt == "html":
                html_data = convert_to_html(data)
                return Response(html_data, mimetype='text/html',
                                headers={'Content-Disposition': 'attachment; filename=generated_data.html'})
            else:
                return jsonify({"error": f"Unsupported format: {out_format}"}), 400

        except Exception as e:
            # Generic catch: emit safe message; logs in server
            return jsonify({"error": "Request failed"}), 400

    # Friendly errors (incl. 413 from MAX_CONTENT_LENGTH)
    @app.errorhandler(413)
    def too_large(_e):
        return jsonify({"error": "Payload too large"}), 413

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_exception(_e):
        return jsonify({"error": "Unexpected server error"}), 500

    return app

# WSGI entrypoint for Gunicorn, etc.
app = create_app()

if __name__ == "__main__":
    # Dev-only run. Use Gunicorn in production.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))