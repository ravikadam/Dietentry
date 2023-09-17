import requests

BASE_API_URL = "https://your_backend_api_url"

class DietChatBot:
    def __init__(self):
        self.user_id = None

    def register_user(self, username, age, weight):
        payload = {
            "username": username,
            "age": age,
            "weight": weight
        }
        response = requests.post(f"{BASE_API_URL}/users/", json=payload)
        if response.status_code == 200:
            self.user_id = response.json().get("id")
            return self.user_id
        else:
            return None

    def authenticate_user(self, email):
        # Implement email-based authentication here
        # For simplicity, we're assuming the user is authenticated if they provide an email
        return True

    def add_diet_data(self, food, calories_burnt):
        if not self.user_id:
            print("User not registered!")
            return

        payload = {
            "user_id": self.user_id,
            "food": food,
            "calories_burnt": calories_burnt
        }
        response = requests.post(f"{BASE_API_URL}/user_data/", json=payload)
        return response.json()

    def get_recommendation(self):
        if not self.user_id:
            print("User not registered!")
            return

        response = requests.get(f"{BASE_API_URL}/recommendation/{self.user_id}")
        return response.json().get("recommendation")

    def save_recommendation(self, recommendation):
        # Assuming you have an endpoint to save recommendations
        payload = {
            "user_id": self.user_id,
            "recommendation": recommendation
        }
        response = requests.post(f"{BASE_API_URL}/save_recommendation/", json=payload)
        return response.json()

# Example usage
bot = DietChatBot()

# Registering a user
user_id = bot.register_user("JohnDoe", 25, 70.5)
if user_id:
    print(f"User registered with ID: {user_id}")

# Authenticating the user
if bot.authenticate_user("johndoe@example.com"):
    print("User authenticated!")

# Adding diet data
response = bot.add_diet_data("Pizza", 300)
print(response)

# Getting recommendation
recommendation = bot.get_recommendation()
print(f"Recommended Diet: {recommendation}")

# Saving recommendation
response = bot.save_recommendation(recommendation)
print(response)
