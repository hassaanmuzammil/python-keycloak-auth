import requests
from jose import jwt
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



def get_keycloak_public_key():
    """
    Retrieve the public key from Keycloak for JWT verification.
    """
    url = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
    jwks = requests.get(url).json()
    for key in jwks["keys"]:
        if key["alg"] == "RS256" and key["use"] == "sig":
            return key
    raise Exception("No valid RSA signing key found.")


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
    
    email = user_data.get("email")
    username = user_data.get("username")

    keycloak_user = get_user_keycloak(token, username=username, email=email)
    # If user already exists, enable the user if it is disabled
    if keycloak_user:
        enable_disable_user_keycloak(
            token=token, 
            keycloak_user_id=keycloak_user["id"],
            enable=True
        )
        # TODO: change user password if provided
        return keycloak_user["id"]

    # If user does not exist, create a new one
    response = requests.post(url, json=user_data, headers=headers)
    
    if response.status_code not in [201, 204]:
        raise Exception(f"Failed to create user in Keycloak: {response.text}")

    # Retrieve Keycloak User ID
    keycloak_user_id = response.headers.get("Location", "").split("/")[-1]
    if not keycloak_user_id:
        raise Exception("Failed to extract Keycloak user ID from response headers.")

    return keycloak_user_id


def get_user_keycloak(token: str, username: str = None, email: str = None):
    """
    Retrieve a user from Keycloak by username or email.
    """
    url = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if email:
        params = {"email": email}
    elif username:
        params = {"username": username}
    else:
        raise ValueError("Either 'username' or 'email' must be provided to search for a user.")
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to search user in Keycloak: {response.text}")
    users = response.json()
    return users[0] if users else None


def enable_disable_user_keycloak(
    token: str, 
    keycloak_user_id: str,
    enable: bool = True
):
    url = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users/{keycloak_user_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {"enabled": True if enable else False}

    response = requests.put(url, headers=headers, json=payload)
    if response.status_code not in [204, 200]:
        raise Exception(f"Failed to {'enable' if enable else 'disable'} user in Keycloak: {response.text}")

    return {"msg": f"User {'enabled' if enable else 'disabled'} successfully"}


def send_email_verification_link(
    token: str,
    user_id: str,
    redirect_url: str = None
):
    """
    Send an email verification link to the user.
    """
    url = f"{KEYCLOAK_SERVER_URL}/admin/realms/{KEYCLOAK_REALM}/users/{user_id}/execute-actions-email"
    params = {"redirect_uri": redirect_url} if redirect_url else {}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = ["VERIFY_EMAIL"]

    response = requests.put(url, params=params, headers=headers, json=data)
    response.raise_for_status()
    return response.status_code


if __name__ == "__main__":

    from app.config import (
        KEYCLOAK_SERVER_URL,
        KEYCLOAK_REALM,
        KEYCLOAK_CLIENT_ID,
        KEYCLOAK_CLIENT_SECRET,
    )

    # token = get_token_standard_flow(
    #     username="username-1", 
    #     password="password-1"
    # )

    # token = get_token()

    # print(token)
    
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

    # print(get_user_keycloak(
    #     token=token["access_token"],
    #     username="username-9"
    # ))

    # disable_user_keycloak(
    #     token=token["access_token"], 
    #     keycloak_user_id="6c032a59-5a95-440a-84da-49a223f8397e"
    # )

    print(get_keycloak_public_key())