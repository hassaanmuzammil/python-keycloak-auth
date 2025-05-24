#!/bin/bash
# This script retrieves an access token from Keycloak using either client credentials or password grant type.

# Using client credentials grant type. Retrieves an access token for a client.
# curl -X POST "http://localhost:8080/realms/realm-1/protocol/openid-connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "client_id=client-1" \
#      -d "client_secret=I0wVz0OuX1V5zPBHppkhXJYkrqIdOdE2" \
#      -d "grant_type=client_credentials"

# Using password grant type with a specific user. Retrieves an access token for a user.
# curl -X POST "http://localhost:8080/realms/realm-1/protocol/openid-connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "client_id=$KEYCLOAK_CLIENT" \
#      -d "client_secret=$KEYCLOAK_CLIENT_SECRET" \
#      -d "username=email-1@gmail.com" \
#      -d "password=password-1" \
#      -d "grant_type=password"