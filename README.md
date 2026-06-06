# Cent Mira Backend

Cent Mira Backend is a learning-focused Flask API for an ecommerce project.

The goal of this project is not to rush straight into launching a finished store. The goal is to learn backend development by building the project layer by layer: app setup, database models, authentication, products, carts, orders, and eventually tests and production-ready improvements.

At this stage, the backend can:

- start a Flask server
- connect to a SQLite database with SQLAlchemy
- create database tables from models
- register users
- log users in
- generate JWT access tokens
- protect routes with JWT authentication
- create, read, update, and delete products

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Cors
- SQLite for local development

## Project Structure

```txt
cent_mira_backend/
  README.md
  requirements.txt
  run.py
  app/
    __init__.py
    config.py
    extensions.py
    models/
      __init__.py
      user.py
      product.py
      cart.py
      order.py
      order_item.py
    blueprints/
      auth/
        __init__.py
        routes.py
      products/
        __init__.py
        routes.py
      carts/
        __init__.py
        routes.py
      orders/
        __init__.py
        routes.py
```

Some files are intentionally still empty because we are building the backend one milestone at a time.

## Important Concepts Learned So Far

### App Factory

The Flask app is created inside `create_app()` in `app/__init__.py`.

This pattern keeps setup organized as the project grows. Instead of creating everything directly in `run.py`, the project creates the app in one place, loads config, initializes extensions, and registers blueprints.

### Extensions

The shared Flask extensions live in `app/extensions.py`.

```python
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
```

They are created once, then connected to the Flask app inside `create_app()`.

This keeps imports cleaner and helps avoid circular import problems.

### Config

The app settings live in `app/config.py`.

The current config includes:

- `SECRET_KEY`
- `SQLALCHEMY_DATABASE_URI`
- `SQLALCHEMY_TRACK_MODIFICATIONS`
- `JWT_SECRET_KEY`

For now, the project uses development fallback values. Later, real secrets should come from environment variables.

### Models

Models describe database tables using Python classes.

So far, the project has:

- `User`
- `Product`

Each model inherits from `db.Model`, which tells SQLAlchemy that the class should map to a database table.

### Blueprints

Blueprints group related routes together.

So far, the project has active blueprints for:

- authentication routes under `/auth`
- product routes under `/products`

The cart and order blueprints exist in the folder structure, but we have not built them yet.

## Setup

From the project root, install dependencies:

```powershell
pip install -r requirements.txt
```

If the `flask` command is not recognized on Windows, use:

```powershell
python -m flask
```

instead of:

```powershell
flask
```

## Running The Server

Start the backend with:

```powershell
python run.py
```

The server should run at:

```txt
http://127.0.0.1:5000
```

Keep this terminal open while testing API requests from another terminal.

## Creating Database Tables

Whenever a new model is added, run:

```powershell
python -m flask --app run.py create-db
```

This runs `db.create_all()` and creates any missing tables.

For this learning stage, `create-db` is enough. Later, when the database schema starts changing often, the project should move to migrations with Flask-Migrate or Alembic.

## Current API Routes

### Health Check

```txt
GET /health
```

Checks that the backend is running.

Example:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/health -Method GET
```

Expected response:

```json
{
  "service": "cent-mira-api",
  "status": "ok"
}
```

## Authentication

Authentication routes live under:

```txt
/auth
```

### Register

```txt
POST /auth/register
```

Creates a new user account.

Example:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/auth/register `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"name":"Test User","email":"test@example.com","password":"password123"}'
```

What this route does:

- reads JSON from the request body
- checks that name, email, and password were provided
- normalizes the email
- checks if the email is already registered
- hashes the password
- saves the user to the database
- returns the new user without exposing the password hash

### Login

```txt
POST /auth/login
```

Logs a user in and returns a JWT access token.

Example:

```powershell
$login = Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/auth/login `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"email":"test@example.com","password":"password123"}'
```

To view the token:

```powershell
$login.access_token
```

The token is proof that the user is logged in. It is sent with protected requests using the `Authorization` header.

### Current User

```txt
GET /auth/me
```

Returns the logged-in user's information.

This route is protected with `@jwt_required()`, so it needs a valid token.

Example:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/auth/me `
  -Method GET `
  -Headers @{ Authorization = "Bearer $($login.access_token)" }
```

Important note: do not manually paste a shortened token with `...`. A real JWT must be copied completely.

## Products

Product routes live under:

```txt
/products
```

The product API currently supports full basic CRUD:

- create product
- list products
- get one product
- update product
- delete product

For now, product creation, update, and deletion are open so we can focus on learning CRUD. Later, these should be protected and limited to admin users.

### Product Fields

The `Product` model currently has:

- `id`
- `name`
- `description`
- `price`
- `stock`
- `image_url`
- `created_at`

Current note about money: `price` uses `Float` for learning simplicity. Later, it is better to store money as an integer amount, such as kobo or cents, to avoid floating-point issues.

### Create Product

```txt
POST /products
```

Example:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/products `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"name":"Classic T-Shirt","description":"Soft cotton Cent Mira tee","price":12000,"stock":25,"image_url":"https://example.com/tshirt.jpg"}'
```

What this route does:

- reads product data from JSON
- requires `name` and `price`
- rejects negative price values
- rejects negative stock values
- saves the product to the database
- returns the created product

### List Products

```txt
GET /products
```

Example:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/products -Method GET
```

This returns all products currently stored in the database.

### Get One Product

```txt
GET /products/<product_id>
```

Example:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/products/1 -Method GET
```

If the product does not exist, Flask returns a 404 response.

### Update Product

```txt
PUT /products/<product_id>
```

Example:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/products/1 `
  -Method PUT `
  -ContentType "application/json" `
  -Body '{"name":"Premium T-Shirt","price":15000,"stock":18}'
```

This route supports partial updates. That means the request only needs to include the fields that should change.

For example, this is also valid:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:5000/products/1 `
  -Method PUT `
  -ContentType "application/json" `
  -Body '{"stock":10}'
```

### Delete Product

```txt
DELETE /products/<product_id>
```

Example:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/products/1 -Method DELETE
```

This removes the product from the database.

## HTTP Status Codes We Have Seen

Some common responses during development:

- `200 OK`: request worked
- `201 Created`: a new record was created
- `400 Bad Request`: required data is missing or invalid
- `401 Unauthorized`: token is missing or invalid
- `404 Not Found`: requested record does not exist
- `405 Method Not Allowed`: route exists, but the wrong HTTP method was used
- `409 Conflict`: user email already exists

Example: visiting `/auth/login` in the browser sends a `GET` request, but login expects `POST`, so Flask returns `405 Method Not Allowed`.

## Current Learning Milestones Completed

1. Created the Flask app factory.
2. Added app config.
3. Added Flask extensions.
4. Added a health check route.
5. Added the `User` model.
6. Added password hashing.
7. Added database creation with a Flask CLI command.
8. Added auth blueprint.
9. Added user registration.
10. Added login with JWT token creation.
11. Added protected `/auth/me` route.
12. Added `Product` model.
13. Added products blueprint.
14. Added product creation.
15. Added product listing.
16. Added single-product lookup.
17. Added product update.
18. Added product deletion.

## Next Planned Milestone

The next major feature is the shopping cart.

Planned routes:

```txt
GET    /cart
POST   /cart/items
PUT    /cart/items/<item_id>
DELETE /cart/items/<item_id>
```

The cart will introduce relationships between:

- users
- products
- cart items

Unlike products, cart routes should be protected because each user should only see and modify their own cart.

## Future Improvements

These are intentionally saved for later learning milestones:

- admin-only product management
- cart item model and routes
- order and checkout flow
- better request validation
- consistent error response helpers
- database migrations
- automated tests
- pagination for product lists
- search and filtering
- environment variable setup with `.env`
- production configuration
- storing product prices as integer kobo/cents

## Development Notes

Use two terminals while testing:

1. Server terminal:

```powershell
python run.py
```

2. Request terminal:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/health -Method GET
```

The server must be running before `Invoke-RestMethod` can connect to it.

If PowerShell shows `>>`, it means it is waiting for the rest of a multi-line command. Press `Ctrl + C` to cancel and return to the normal prompt.
