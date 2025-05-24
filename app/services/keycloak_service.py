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
    return response.json()


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
    return response.json()


def refresh_access_token(
    refresh_token: str
):
    """
    Refresh an access token using a refresh token.
    """
    url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    
    payload = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(url, data=payload, headers=headers)
    return response.json()


def invalidate_token(
    refresh_token: str
):
    """
    Invalidate a refresh token in Keycloak.
    """
    logout_url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/logout"

    data = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "refresh_token": refresh_token
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(logout_url, data=data, headers=headers)
    if response.status_code in [200, 204]:
        return {"msg": "Logout successful"}
    else:
        return {"msg": "Invalid refresh token"}


def check_token_validity(token: str):
    """
    Introspect a token using Keycloak to check if it's active.
    """
    introspect_url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"

    data = {
        "token": token,
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(introspect_url, data=data, headers=headers)

    return response.json()


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
        username="username-1", 
        password="password-1"
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