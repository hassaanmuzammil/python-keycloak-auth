# python-keycloak-auth

A custom `users` database for maintaining users and their associated features (basic information, roles, permissions, links) for an application.
Authentication flow for users is managed by a 3rd party auth provider `keycloak`.

## Keycloak

### Setup

```
cd keycloak
docker compose up -d
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
- In the service account roles, assign `manage-users` and `view-users` roles to the client.

| Purpose                       | Flow to Use                                                                                              | Why                                                                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Creating/managing users**   | Service Accounts (Client Credentials Grant)                                                              | The client (backend app) authenticates itself with client ID & secret, gets an admin token, and calls Keycloak Admin API to create/manage users. |
| **User login/authentication** | Direct Access Grants (Resource Owner Password Credentials) or better: Standard Flow (Authorization Code) | Users provide their username/password, your app gets user tokens to allow access to the application.                                    |
