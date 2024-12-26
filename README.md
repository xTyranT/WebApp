# Web Application Backend

This is a web application built with Django for the backend, utilizing a microservices architecture. The app is served through Nginx acting as a reverse proxy, with monitoring and alerting enabled via Prometheus and Grafana.

  
  
## 🧐 Features

### 1. Robust Backend with Django

- Authentication: Secure user authentication and session management.
- API Endpoints: Exposed RESTful APIs for seamless interaction between services.
- Scalability: Designed to handle high traffic with ease using a modular microservices architecture.
### 2. Microservices Architecture
- Modularity: Each service focuses on a specific domain (e.g., user management, profile...).
- Independent Deployment: Services can be deployed, scaled, and updated independently.
- Inter-Service Communication: Services communicate effectively using well-defined APIs.
### 3. Efficient Traffic Handling with Nginx
- Reverse Proxy: Routes incoming requests to the appropriate microservices.
- Load Balancing: Ensures even distribution of traffic for improved reliability.
- Caching: Improves response times by caching static and dynamic content.

### 4. Comprehensive Monitoring and Visualization
- Prometheus Metrics: Collects system and application metrics such as request rates, response times, and error rates.
- Grafana Dashboards: Provides detailed, real-time visualizations and insights into the system’s health and performance.

### 5. Containerized Deployment
- Docker: Ensures consistent environments across development, staging, and production.
- Docker-Compose: Simplifies multi-container setups for local development and testing.

### 6. Secure and Configurable
- Secure Communication: HTTPS-ready with SSL/TLS integration.
- Configurable Settings: Environment-based configuration for flexibility across development, staging, and production.

## 🛠️ Installation Steps

First, Clone the Repository:

```
git clone https://github.com/xTyranT/xTyranT.github.io.git Application
```

Change Directory

```
cd Web Application
```

Make sure no other container is running to prevent build errors

```
make clean
```

Build the Project

```
make
```
## 🖥️ Usage

Once you’ve set up and built the **Web app** project, you can go and test the backend endpoints:

---

### 1. Access the Server
You can access the server using your browser or tools like `curl`:

- **In a browser**: Open the address `https://localhost` to see the server’s response.
- wait its just a backend so you have to fetch the endpoints, here is the list of endpoints:

## Authentication service
```
auth/register/
auth/login/
auth/login/refresh/
auth/logout/
auth/intra/register/
auth/intra/redirect/
auth/verify/
auth/intra/verify/
auth/password/reset/
auth/password/forgot/
auth/password/change/
auth/health/
```

## Profile service
```
profile/intra/create/
profile/create/
profile/me/
profile/<int:id>
profile/update
profile/friend/request/<int:rid>
profile/friend/accept/<int:sid>
profile/friend/reject/<int:sid>
profile/friend/request/list/
profile/friend/list/
profile/search/<query>
profile/health/
```
### 2. Access the monitoring tools
You can access the dashboard using your browser:

- **In a browser**: Open the address `http://localhost:3000` and login using the credentials in .env, go to menu > dashboards > Postgres_exporter

### Happy Coding!

