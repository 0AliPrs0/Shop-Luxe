# 🛍️ Shop Luxe - E-commerce API

![Python](https://img.shields.io/badge/Python-3.12-blue.svg) ![Django](https://img.shields.io/badge/Django-5.2-darkgreen.svg) ![Django REST Framework](https://img.shields.io/badge/DRF-3.15-red.svg) ![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker) ![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)

A fully containerized REST API for a modern online shop, built on Django and DRF and designed for scalability. It features a complete suite of services orchestrated by Docker Compose (PostgreSQL, Redis), asynchronous task processing with Celery, and a secure, stateless authentication system using JSON Web Tokens (JWT) with distinct user roles.

---

## 📖 Table of Contents
- [✨ Key Features](#-key-features)
- [🏗️ Architecture Overview](#️-architecture-overview)
- [🚀 Getting Started](#-getting-started)
- [🔌 API Endpoints Documentation](#-api-endpoints-documentation)
  - [👤 User & Authentication](#-user--authentication)
  - [📦 Products, Categories & Reviews](#-products-categories--reviews)
  - [🔍 Search](#-search)
  - [🛒 Shopping Cart](#-shopping-cart)
  - [💳 Orders & Payments](#-orders--payments)
- [🔮 Future Improvements](#-future-improvements)
- [📝 License](#-license)

---

## ✨ Key Features

- **Containerized Environment**: Fully containerized with **Docker** for a consistent and easy-to-manage development and production setup.
- **Asynchronous Tasks**: **Celery** and **Redis** handle background tasks like sending verification emails, ensuring a fast, non-blocking user experience.
- **High-Performance Caching**: **Redis** is used to cache frequently accessed data (products, categories) to reduce database load and improve API response times.
- **Role-Based Access Control (RBAC)**: Distinct permissions for **Customers** and **Sellers**. Sellers can manage their products, while customers have access to shopping features.
- **Secure JWT Authentication**: Stateless authentication using **JSON Web Tokens** with a complete flow including registration, email verification, login, and password reset.
- **Complete E-commerce Workflow**: Full support for a standard shopping experience, from Browse products and managing a cart to creating orders and initiating payments.
- **Image Handling**: Users can upload profile pictures, and sellers can upload multiple images for their products.

---

## 🏗️ Architecture Overview

The entire application is orchestrated by Docker Compose, consisting of four main services:

-   **`db` (PostgreSQL)**: A powerful, open-source object-relational database system.
-   **`redis`**: An in-memory data store used as both a message broker for Celery and a cache backend for Django.
-   **`backend` (Django)**: The main application server that runs the Django REST Framework API.
-   **`celery`**: A dedicated worker process that listens to the Redis queue and executes background tasks asynchronously.

---

## 🚀 Getting Started

### Prerequisites
- Git
- Docker
- Docker Compose

### Installation
1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd shop_luxe
    ```

2.  **Create the `.env` file:**
    Create a `.env` file in the project root and populate it with your credentials. You can use `env.example` as a template.
    ```bash
    cp env.example .env
    ```

3.  **Build and Run with Docker Compose:**
    This single command will build, create, and start all the necessary containers.
    ```bash
    docker-compose up --build
    ```

4.  **Apply Database Migrations:**
    In a **new terminal window**, run the migrate command to set up your database schema.
    ```bash
    docker-compose exec backend python manage.py migrate
    ```

5.  **Create a Superuser:**
    Create an admin user to access the Django admin panel.
    ```bash
    docker-compose exec backend python manage.py createsuperuser
    ```

The API is now running and accessible at `http://localhost:8000`.

---

## 🔌 API Endpoints Documentation

### 👤 User & Authentication

#### 1. Register New User
- **Endpoint:** `POST /api/auth/register/`
- **Auth:** `AllowAny`
- **Description:** Registers a new, inactive user and triggers a Celery task to send a verification email.
- **Request Body:**
  ```json
  {
      "username": "newuser",
      "email": "new@example.com",
      "password": "strongpassword123",
      "first_name": "New",
      "last_name": "User"
  }
  ```
- **Success Response (201):**
  ```json
  {
      "message": "User registered successfully. Please check your email to verify your account."
  }
  ```

#### 2. Verify Email Address
- **Endpoint:** `GET /api/accounts/verify-email/<uidb64>/<token>/`
- **Auth:** `AllowAny`
- **Description:** Activates a user's account when they click the verification link sent to their email.

#### 3. User Login
- **Endpoint:** `POST /api/auth/login/`
- **Auth:** `AllowAny`
- **Description:** Authenticates an active user and returns JWT access and refresh tokens.

#### 4. User Logout
- **Endpoint:** `POST /api/auth/logout/`
- **Auth:** `IsAuthenticated`
- **Description:** Blacklists the user's refresh token, effectively logging them out.

#### 5. User Profile (View & Update)
- **Endpoint:** `GET`, `PATCH /api/profile/me/`
- **Auth:** `IsAuthenticated`
- **Description:** Allows a user to view or update their profile, including uploading a `profile_picture` (using `multipart/form-data`).

#### 6. Password Reset
- **Endpoints:**
  - `POST /api/auth/password-reset/` (Request reset link)
  - `POST /api/auth/password-reset/confirm/` (Confirm new password)
- **Auth:** `AllowAny`
- **Description:** A two-step process to securely reset a user's password via email.

#### 7. JWT Token Management
- **Endpoints:**
  - `POST /api/token/refresh/` (Refresh access token)
  - `POST /api/token/verify/` (Verify token validity)
- **Auth:** Varies
- **Description:** Standard endpoints for managing JWT tokens.

---
### 📦 Products, Categories & Reviews

#### 8. List/Detail Categories
- **Endpoint:** `GET /api/categories/` or `GET /api/categories/<id>/`
- **Auth:** `AllowAny`
- **Description:** Retrieves a list of all categories or the details of a specific one, including nested child categories.

#### 9. List/Detail Products
- **Endpoint:** `GET /api/products/` or `GET /api/products/<id>/`
- **Auth:** `AllowAny`
- **Description:** Retrieves a list of all products or the details of a specific one, including its variants.

#### 10. Create Product
- **Endpoint:** `POST /api/products/create/`
- **Auth:** `IsSellerUser`
- **Description:** Allows a user from the 'Sellers' group to create a new product along with its variants.

#### 11. Upload Product Image
- **Endpoint:** `POST /api/products/<product_pk>/upload-image/`
- **Auth:** `IsProductOwner`
- **Description:** Allows the seller who owns the product to upload an image for it (`multipart/form-data`).

#### 12. List/Create Product Reviews
- **Endpoint:** `GET /api/products/<product_id>/reviews/` or `POST /api/products/<product_id>/reviews/add/`
- **Auth:** `AllowAny` for GET, `IsAuthenticated` for POST.
- **Description:** Allows users to view all reviews for a product or add a new one.

---
### 🔍 Search

#### 13. Global Search
- **Endpoint:** `GET /api/search/?q=<query>&type=<product|category>`
- **Auth:** `AllowAny`
- **Description:** A flexible search endpoint to find products and/or categories based on a search query.

---
### 🛒 Shopping Cart

#### 14. View/Clear Cart
- **Endpoint:** `GET`, `DELETE /api/cart/`
- **Auth:** `IsAuthenticated`
- **Description:** Get the details of the user's current cart or remove all items from it.

#### 15. Add to Cart
- **Endpoint:** `POST /api/cart/add/`
- **Auth:** `IsAuthenticated`
- **Description:** Add a product variant to the user's cart or increase its quantity if it already exists.

#### 16. Update/Remove Cart Item
- **Endpoint:** `PATCH /api/cart/update/<id>/` or `DELETE /api/cart/remove/<id>/`
- **Auth:** `IsAuthenticated`
- **Description:** Update the quantity of a specific item or remove it completely from the cart.

---
### 💳 Orders & Payments

#### 17. List/Detail Orders
- **Endpoint:** `GET /api/orders/` or `GET /api/orders/<id>/`
- **Auth:** `IsAuthenticated`
- **Description:** Get a list of the user's order history or view the details of a specific order, including all items.

#### 18. Initiate Payment
- **Endpoint:** `POST /api/payments/initiate/`
- **Auth:** `IsAuthenticated`
- **Description:** Creates a payment record and returns a simulated payment gateway URL for a specific order.

#### 19. Payment Callback
- **Endpoint:** `GET /api/payments/callback/`
- **Auth:** `AllowAny`
- **Description:** A simulated callback URL for the payment gateway to report the status of a transaction and update the order accordingly.

---

## 🔮 Future Improvements
- Integrate a real payment gateway (e.g., Stripe).
- Implement real-time notifications using Django Channels (e.g., for order status updates).
- Add product review moderation.
- Develop a comprehensive seller dashboard.

---

## 📝 License
This project is licensed under the MIT License.
