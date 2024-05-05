# Shopping Cart API Documentation

This documentation provides an overview of the endpoints and their respective functionalities for the Shopping Cart API.
# Test

To run the tests for the Cart API, you can use the following command:

```shell
make test
```

There is also a postman collection provided that can be used to play with the project.

# Run
To run the server for the Cart API, you can use the following command:

```shell
make run
```

## Designing the Data Model

The data model was designed to support complex interactions between users, products, carts, and orders. Relationships are defined to allow efficient data retrieval and manipulation, supporting the core functionalities of an e-commerce platform.

The data model is implemented in the Python files located in the `store/models` directory. These files define the structure and behavior of the different entities in the system, such as `User`, `Product`, `Cart`, and `Order`. The relationships between these entities are established using Django's ORM (Object-Relational Mapping) features, ensuring data consistency and integrity.

For example, the `User` model defines fields like `username`, `first_name`, `last_name`, and `email`, while the `Product` model includes attributes such as `name`, `description`, and `price`. The `Cart` model represents a user's shopping cart and is associated with a specific user through a foreign key relationship. Similarly, the `Order` model represents a completed order and is linked to a user and the products in the order.

By organizing the data model in this way, the system can efficiently handle operations like adding items to the cart, placing orders, and retrieving user information. The relationships between entities enable seamless navigation and manipulation of data, providing a solid foundation for the e-commerce platform's functionality.

## Integrating Business Logic

Business logic was integrated to handle scenarios typical of shopping environments, such as cart management, order processing, and payment transactions. Special attention was given to ensuring transactions are handled atomically to avoid data inconsistencies.

### Integration test
Test the flow of adding items to the cart, placing orders, and listing orders.

This test case performs the following steps:
1. Registers a user with the provided username, password, first name, last name, and email.
2. Logs in the user using the registered username and password.
3. Retrieves the user's profile information.
4. Adds two products to the cart with their respective name, description, and price.
5. Lists the available products.
6. Adds items to the cart and clears the cart.
7. Adds items to the cart, places an order, and cancels the order.
8. Adds items to the cart, places an order, and completes the payment.
9. Adds items to the cart and places an order.
10. Lists the user's orders.

This test case ensures that the cart flow, order placement, and order listing functionalities are working correctly in the store application.


## API Implementation

The API was implemented using Django REST Framework for its robustness and ease of use in building RESTful APIs. Serializers validate and structure incoming data, while viewsets and routers provide the logic and routing needed for endpoint functionality.

## Decisions Made

The project is structured in a modular fashion, adhering to Django's convention of separating concerns into distinct applications. The main applications in this project are `shopping_cart` and `store`.

The `shopping_cart` application handles the configuration and routing for the project, while the `store` application contains the business logic and data models for the shopping cart functionality.

The `store` application is further divided into several modules:

- `models`: This module contains the data models for the application, including `User`, `Product`, `Cart`, and `Order`. These models define the structure of the database tables and the relationships between them.

- `views`: This module contains the view functions for the application. These functions handle HTTP requests and responses, utilizing the serializers and models to interact with the database.

- `serializers`: This module contains the serializers for the application. These serializers handle the conversion between complex data types and Python native datatypes, which can then be easily rendered into JSON or other content types.

- `tests`: This module contains the test cases for the application. These tests ensure that the application's functionality is working as expected.

The system design follows a typical three-tier architecture, with a presentation layer (the API endpoints), a business logic layer (the view functions and serializers), and a data storage layer (the database models). This separation of concerns allows for easier maintenance and scalability of the application.

# API Endpoint Documentation

## Register

Endpoint: `/store/register`
Method: `POST`
Description: Registers a new user.

Request body:
```json
{
	"username": "a",
    "first_name": "A",
    "last_name": "B",
	"password": "b",
	"email": "a@b.com"
}
```

## Login

Endpoint: `/store/login`
Method: `POST`
Description: Authenticates a user and generates an access token.
Request body:
```json
{
	"username": "a",
    "password": "b"
}
```

## Get User

Endpoint: `/store/user/`
Method: `GET`
Description: Retrieves the details of the authenticated user.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Add Product

Endpoint: `/store/product/`
Method: `POST`
Description: Adds a new product to the system.
Request body:
```json
{
    "name": "LAPTOP",
    "description": "RTX 3090",
    "price": 1200
}
```


## List Products

Endpoint: `/store/product/`
Method: `GET`
Description: Retrieves a list of all available products.

## Add to Cart

Endpoint: `/store/cart/`
Method: `POST`
Description: Adds a product to the user's cart.
Request Body:
```json
{
    "product_id": 1,
    "quantity": 2
}
```

Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Get Cart

Endpoint: `/store/cart`
Method: `GET`
Description: Retrieves the user's cart.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Clear Cart

Endpoint: `/store/cart`
Method: `DELETE`
Description: Clears the user's cart.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Place Order

Endpoint: `/store/orders`
Method: `PUT`
Description: Places an order for the products in the user's cart.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Get Order

Endpoint: `/store/order/{order_id}`
Method: `GET`
Description: Retrieves the details of a specific order.
Parameters:
- `order_id` (string): The ID of the order to retrieve.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Get Order Payment Details

Endpoint: `/store/orders/{order_id}`
Method: `GET`
Description: Retrieves the payment details of a specific order.
Parameters:
- `order_id` (string): The ID of the order to retrieve payment details for.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Pay for Order

Endpoint: `/store/payment/{payment_id}`
Method: `POST`
Description: Initiates the payment process for a specific order.
Parameters:
- `payment_id` (string): The ID of the order to make payment for.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## Cancel Payment

Endpoint: `/store/payment/{payment_id}`
Method: `DELETE`
Description: Cancels the payment for a specific order.
Parameters:
- `payment_id` (string): The ID of the order to cancel payment for.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.

## List Orders

Endpoint: `/store/orders`
Method: `GET`
Description: Retrieves a list of all orders placed by the user.
Headers:
- `Authorization` (string): Bearer token obtained from the login endpoint.