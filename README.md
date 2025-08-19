# DataGen

🚀 **[Live Demo](https://datagen-lx1m.netlify.app/)**  
Visit the demo website to explore the API with an interactive **Swagger UI**.  
On the site, you’ll find full documentation about available endpoints and data types.  
You can also send live requests directly through the Swagger interface at:

- **Website:** `https://datagen-lx1m.netlify.app/api`
- **API root:** `https://datagen-lx1m.onrender.com/`

---

**DataGen** is a flexible fake data generation API designed for developers who need realistic test data quickly. Define your own schema, set constraints, and choose from multiple output formats — all with a single API call.

## ✨ Features

* **Custom Schemas** – Define the data structure you need.
* **Multiple Data Types** – Numbers, strings, dates, city names, countries, and more.
* **Scalable** – Generate up to **10,000 rows** per request.
* **Flexible Output Formats** – JSON (default), CSV, XML, HTML, SQL.
* **Advanced Parameters:** 
  * Value ranges
  * String uniqueness
  * Pattern-based generation
  * Custom constraints

## 📦 Example Usage

### Request

`POST /generate`
```json
{
  "count": 2,
  "format": "json",
  "id": { "type": "int", "min": 1, "max": 9999 },
  "name": { "type": "name" },
  "city": { "type": "city" },
  "age": { "type": "int", "min": 18, "max": 65 }
}
```
Response (JSON)

```json
[
  { "id": 1, "name": "Alice", "city": "Berlin", "age": 34 },
  { "id": 2, "name": "Bob", "city": "Tokyo", "age": 27 }
]
```

## 🔧 Use Cases
- Seeding test databases
- Mocking API responses
- Rapid prototyping
- Data-driven UI/UX testing
