import random

def get_environmental_data():
    """Simulates reading temperature and humidity from a sensor."""
    data = {
        "temperature": round(random.uniform(20.0, 35.0), 1), # Temperature in Celsius
        "humidity": round(random.uniform(60.0, 95.0), 1),    # Humidity percentage
        "soil_moisture": "Dry"                               # Example: Simulated reading
    }
    return data