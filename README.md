# python-keycloak-auth

A custom `users` service for maintaining users and their associated features (basic information, roles, permissions, links) for an application. Authentication flow for users is managed by a 3rd party auth provider `keycloak`.

## Keycloak

### Setup

```sh
cd keycloak
docker compose up -d postgres keycloak
```

Starts a Postgres DB and a Keycloak service which can be accessed at http://localhost:8080

See [Keycloak Setup](./keycloak/README.md) for more details.

### Configuration
- Create a realm in keycloak. Realm is a space to manage a set of users, roles, and clients.
- Create a client in keycloak. Client is the application that uses keycloak to authenticate, authorize, and manage users.
- Enable the following for the client:
    - `Client Authentication`
    - `Direct Access Grants`
    - `Standard Flow`
    - `Service Account Roles`
    ![Client Settings](./docs/image.png)

    
- In the service account roles, assign `manage-users` and `view-users` roles to the client.
![Client Service Accounts Roles](./docs/image-1.png)

| Purpose                       | Flow to Use                                                                                              | Why                                                                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Creating/managing users**   | Service Accounts (Client Credentials Grant)                                                              | The client (backend app) authenticates itself with client ID & secret, gets an admin token, and calls Keycloak Admin API to create/manage users. |
| **User login/authentication** | Direct Access Grants (Resource Owner Password Credentials) or better: Standard Flow (Authorization Code) | Users provide their username/password, your app gets user tokens to allow access to the application.                                    |

## Authentication flow

1. Backend uses client credentials to create users in Keycloak realm.  
2. User logs in with username and password.  
3. Keycloak returns access token (short-lived) and refresh token (long-lived).  
4. Frontend sends access token with API requests to authenticate user.  
5. When access token expires, frontend uses refresh token to request a new access token.  
6. If refresh token is invalid or expired, user must log in again.  
7. User logs out by frontend calling logout API with refresh token to revoke session.  
8. Keycloak session deletion invalidates refresh token and access token immediately.  
9. Frontend can detect user inactivity and trigger logout to clear tokens and session.  

## Auth & Token Endpoints

- `GET /auth/token/client-credentials` — Get access token using client credentials (no user auth needed). Just for testing.
- `POST /auth/login` — Log in with username/password, get tokens.
- `POST /auth/token/refresh` — Refresh access token using refresh token.
- `POST /auth/logout` — Log out by invalidating refresh token.
- `POST /auth/token/validate` — Validate access or refresh token.

## User Endpoints
- `POST /users` — Create a new user with the provided details.
- `GET /users` — Retrieve a list of all users.
- `GET /users/{user_id}` — Retrieve details of a specific user by their ID.
- `PUT /users/{user_id}` — Update the details of a specific user by their ID.
- `DELETE /users/{user_id}` — Delete a specific user by their ID.

## MailHog

MailHog is a testing tool that acts as a `fake SMTP server`. It captures emails sent by applications and provides a web interface to view them.

### Setup

```sh
cd keycloak
docker compose up -d mailhog
```

### Details
- MailHog listens on a port (usually `1025`) like an SMTP server.
- When Keycloak sends an email via SMTP, MailHog intercepts it instead of delivering it to a real mail server. No real emails are sent.
- Captured emails can be viewed in MailHog’s web UI, typically accessible at [http://localhost:8025](http://localhost:8025).


## Run

```sh
# For debug
uvicorn main:app --reload

# For production
docker compose up -d
```