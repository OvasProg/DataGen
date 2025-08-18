from faker import Faker
import random
import rstr

faker = Faker()

def ensure_unique(field, value, generator_func, unique_fields, max_retries=100):
    """Optimized uniqueness checking with retry limit"""
    if field not in unique_fields:
        return value
    
    retries = 0
    while value in unique_fields[field] and retries < max_retries:
        value = generator_func()
        retries += 1
    
    if retries >= max_retries:
        # If we can't generate a unique value after max retries, 
        # append a counter to make it unique
        counter = 1
        original_value = value
        while value in unique_fields[field]:
            value = f"{original_value}_{counter}"
            counter += 1
    
    unique_fields[field].add(value)
    return value

def generate_unique_values(field_type, config, count, unique_fields):
    """Pre-generate unique values for better performance"""
    if not config.get("unique"):
        return None
    
    field_name = config.get("field_name", "unknown")
    unique_values = set()
    
    if field_type == "int":
        min_val = config.get("min", 0)
        max_val = config.get("max", 100)
        capacity = max_val - min_val + 1
        
        if count > capacity:
            # If we need more values than possible, use the full range
            values = list(range(min_val, max_val + 1))
            random.shuffle(values)
            return values[:count]
        else:
            # Generate random unique integers
            while len(unique_values) < count:
                unique_values.add(random.randint(min_val, max_val))
            return list(unique_values)
    
    elif field_type == "email":
        while len(unique_values) < count:
            unique_values.add(faker.email())
        return list(unique_values)
    
    elif field_type == "uuid":
        while len(unique_values) < count:
            unique_values.add(faker.uuid4())
        return list(unique_values)
    
    elif field_type == "username":
        while len(unique_values) < count:
            unique_values.add(faker.user_name())
        return list(unique_values)
    
    elif field_type == "ip":
        while len(unique_values) < count:
            unique_values.add(faker.ipv4())
        return list(unique_values)
    
    return None

def generate_mock_data(schema: dict, count: int = 10):
    """Generate raw mock data as list[dict]. No formatting."""
    results = []
    unique_fields = {}
    pre_generated_values = {}

    # Pre-generate unique values for better performance
    for field, config in schema.items():
        if config.get("unique"):
            field_type = config.get("type", "string")
            config["field_name"] = field  # Add field name for reference
            pre_generated = generate_unique_values(field_type, config, count, unique_fields)
            if pre_generated:
                pre_generated_values[field] = pre_generated
            else:
                unique_fields[field] = set()

    for i in range(count):
        first_name, last_name = "", ""
        item = {}
        
        for field, config in schema.items():
            field_type = config.get("type", "string")

            # Use pre-generated values if available
            if field in pre_generated_values:
                item[field] = pre_generated_values[field][i]
                continue

            if field_type == "string":
                pattern = config.get("pattern")
                if pattern:
                    value = rstr.xeger(pattern)
                    value = ensure_unique(field, value, lambda: rstr.xeger(pattern), unique_fields)
                    item[field] = value
                else:
                    value = faker.word()
                    value = ensure_unique(field, value, faker.word, unique_fields)
                    item[field] = value
            elif field_type == "int":
                min_val = config.get("min", 0)
                max_val = config.get("max", 100)
                value = random.randint(min_val, max_val)
                value = ensure_unique(field, value, lambda: random.randint(min_val, max_val), unique_fields)
                item[field] = value
            elif field_type == "float":
                min_val = config.get("min", 0)
                max_val = config.get("max", 100)
                value = round(random.uniform(min_val, max_val), 2)
                value = ensure_unique(field, value, lambda: round(random.uniform(min_val, max_val), 2), unique_fields)
                item[field] = value
            elif field_type == "bool":
                value = faker.boolean()
                value = ensure_unique(field, value, faker.boolean, unique_fields)
                item[field] = value
            elif field_type == "date":
                value = faker.date()
                value = ensure_unique(field, value, faker.date, unique_fields)
                item[field] = value
            elif field_type == "uuid":
                value = faker.uuid4()
                value = ensure_unique(field, value, faker.uuid4, unique_fields)
                item[field] = value
            elif field_type == "email":
                value = faker.email()
                value = ensure_unique(field, value, faker.email, unique_fields)
                item[field] = value
            elif field_type == "name":
                if not first_name:
                    first_name = faker.first_name()
                    first_name = ensure_unique(field, first_name, faker.first_name, unique_fields)
                if not last_name:
                    last_name = faker.last_name()
                    last_name = ensure_unique(field, last_name, faker.last_name, unique_fields)
                item[field] = f"{first_name} {last_name}"
            elif field_type == "first_name":
                if not first_name:
                    first_name = faker.first_name()
                    first_name = ensure_unique(field, first_name, faker.first_name, unique_fields)
                item[field] = first_name
            elif field_type == "last_name":
                if not last_name:
                    last_name = faker.last_name()
                    last_name = ensure_unique(field, last_name, faker.last_name, unique_fields)
                item[field] = last_name
            elif field_type == "text":
                length = config.get("length", 200)
                value = faker.text(max_nb_chars=length)
                value = ensure_unique(field, value, lambda: faker.text(max_nb_chars=length), unique_fields)
                item[field] = value
            elif field_type == "username":
                value = faker.user_name()
                value = ensure_unique(field, value, faker.user_name, unique_fields)
                item[field] = value
            elif field_type == "password":
                length = config.get("length", 12)
                value = faker.password(length=length)
                value = ensure_unique(field, value, lambda: faker.password(length=length), unique_fields)
                item[field] = value
            elif field_type == "city":
                value = faker.city()
                value = ensure_unique(field, value, faker.city, unique_fields)
                item[field] = value
            elif field_type == "country":
                value = faker.country()
                value = ensure_unique(field, value, faker.country, unique_fields)
                item[field] = value
            elif field_type == "zipcode":
                value = faker.postcode()
                value = ensure_unique(field, value, faker.postcode, unique_fields)
                item[field] = value
            elif field_type == "address":
                value = faker.address()
                value = ensure_unique(field, value, faker.address, unique_fields)
                item[field] = value
            elif field_type == "phone":
                value = faker.phone_number()
                value = ensure_unique(field, value, faker.phone_number, unique_fields)
                item[field] = value
            elif field_type == "url":
                value = faker.url()
                value = ensure_unique(field, value, faker.url, unique_fields)
                item[field] = value
            elif field_type == "ip":
                value = faker.ipv4()
                value = ensure_unique(field, value, faker.ipv4, unique_fields)
                item[field] = value
            elif field_type == "price":
                value = round(random.uniform(1.0, 1000.0), 2)
                value = ensure_unique(field, value, lambda: round(random.uniform(1.0, 1000.0), 2), unique_fields)
                item[field] = value
            elif field_type == "credit_card":
                value = faker.credit_card_number()
                value = ensure_unique(field, value, faker.credit_card_number, unique_fields)
                item[field] = value
            else:
                item[field] = f"Unsupported type: {field_type}"

        results.append(item)

    return results