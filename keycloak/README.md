# Keycloak Setup with Docker Compose

A simple Docker Compose setup for running Keycloak with a PostgreSQL database.

## 🚀 Getting Started

### 1️⃣ Start Services

Run the following command to start Keycloak and PostgreSQL in detached mode:

```sh
docker compose up -d
```

### 2️⃣ Access Keycloak

Once the services are running, you can access Keycloak at:

🔗 [http://localhost:8080](http://localhost:8080)

Login using the credentials set in the `docker-compose.yml` file. Default values:

- **Username:** `admin`
- **Password:** `admin`

## 🔧 Configuring Keycloak

### 1️⃣ Create a Realm

A realm is an isolated space in Keycloak that manages users, roles, and clients.

### 2️⃣ Create a Client

Within your realm, create a client that represents the application using Keycloak for authentication.

### 3️⃣ Update Client Settings

In the client settings, enable the following options:

✅ **Client authentication**\
✅ **Standard flow** (for browser-based login)\
✅ **Direct access grants** (for password-based authentication)\
✅ **Service account roles** (for machine-to-machine authentication)

### 4️⃣ Store Client Secret

Once the client is created, copy the **client secret** and store it securely. This secret is needed for authentication.

## 📜 Viewing Logs

To monitor Keycloak logs in real-time, run:

```sh
docker compose logs -f
```

## ⏹️ Stopping Services

To stop and remove running containers:

```sh
docker compose down
```

To also remove associated volumes, add the `-v` flag:

```sh
docker compose down -v
```

## 🔑 Obtaining an Access Token

Use the following `curl` command to obtain an access token using client credentials:

```sh
export SERVER_URL="http://localhost:8080"
export REALM="realm"
export CLIENT="client"
export CLIENT_SECRET="client-secret"

curl -X POST "$SERVER_URL/realms/$REALM/protocol/openid-connect/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id=$CLIENT" \
     -d "client_secret=$CLIENT_SECRET" \
     -d "grant_type=client_credentials"
```

---

✅ **Now your Keycloak setup is ready!** 🎉

