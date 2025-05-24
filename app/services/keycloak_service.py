import requests
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection

from app.config import KEYCLOAK_SERVER_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET


def get_token():
    
    url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    payload = {   
        "grant_type": "client_credentials",
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error: {response.text}")


def get_token_standard_flow(
    username: str,
    password: str
):
    url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    payload = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error: {response.text}")

def create_user_keycloak(
    token: str,
    user_data: dict
):
    """
    Create a new user in Keycloak.
    """
    url = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=user_data, headers=headers)
    
    if response.status_code not in [201, 204]:
        raise Exception(f"Failed to create user in Keycloak: {response.text}")

    # Retrieve Keycloak User ID
    keycloak_user_id = response.headers.get("Location", "").split("/")[-1]
    if not keycloak_user_id:
        raise Exception("Failed to extract Keycloak user ID from response headers.")

    return keycloak_user_id


if __name__ == "__main__":

    from app.config import (
        KEYCLOAK_SERVER_URL,
        KEYCLOAK_REALM,
        KEYCLOAK_CLIENT_ID,
        KEYCLOAK_CLIENT_SECRET,
        KEYCLOAK_ADMIN,
        KEYCLOAK_ADMIN_PASSWORD
    )

    token = get_token_standard_flow(
        username="username", 
        password="password"
    )

    # token = get_token()

    print(token)
    
    # i = 3
    # user_data = {
    #     "username": f"username-{i}",
    #     "firstName": f"firstname-{i}",
    #     "lastName": f"lastname-{i}",
    #     "email": f"email-{i}@gmail.com",
    #     "enabled": True,
    #     "credentials": [{"type": "password", "value": f"password-{i}", "temporary": False}]
    # }

    # user_id = create_user(
    #     token="ncbdksvhufw904rh2fbkad",
    #     user_data
    # )
    # print(user_id)