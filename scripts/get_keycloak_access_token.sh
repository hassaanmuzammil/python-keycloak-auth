# source ../.env &&

# curl -X POST "http://localhost:8080/realms/realm-1/protocol/openid-connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "client_id=client-1" \
#      -d "client_secret=I0wVz0OuX1V5zPBHppkhXJYkrqIdOdE2" \
#      -d "grant_type=client_credentials"

# curl -X POST "http://localhost:8080/realms/master/protocol/openid-connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "client_id=admin-cli" \
#      -d "username=admin" \
#      -d "password=admin" \
#      -d "grant_type=password"

# curl -X POST "http://localhost:8080/realms/realm-1/protocol/openid-connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "client_id=client-1" \
#      -d "username=email-1@gmail.com" \
#      -d "password=password-1" \
#      -d "grant_type=password"

# curl -X POST "$KEYCLOAK_SERVER_URL/realms/$KEYCLOAK_REALM/protocol/openid-connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -d "client_id=$KEYCLOAK_CLIENT" \
#      -d "client_secret=$KEYCLOAK_CLIENT_SECRET" \
#      -d "grant_type=client_credentials"