# Events Notifier Service

The Events Notifier Service is a Python-based application designed to emit events via RabbitMQ. This service is developed to facilitate the communication of events between different components of a system, ensuring that events are reliably transmitted and received.

## Features

- Emit events to RabbitMQ
- Configurable event types and payloads
- Integration with Django for easy management
- Supports JWT authentication for secure access
- OpenAPI documentation with drf-spectacular

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BlueCJIOH/events-notifier.git
   cd events-notifier
   ```

2. Build and run the services using Docker Compose:
   ```bash
   cd notifier
   docker-compose up --build -d
   docker-compose exec web python manage.py migrate && python manage.py loaddata fixtures/users.json
   ```

   ```bash
   cd another-service
   docker-compose up --build -d
   ```

3. Request to urls:
   ```bash
   curl -X POST http://localhost:8000/api/auth/sign-in/ \
     -H "Content-Type: application/json" \
     -d '{"email": "your_username", "password": "your_password"}'
   ```
   successful response:
   ```json
   {
    "access_token": "your_jwt_token",
    "refresh_token": "your_refresh_token"
   }
   ```
   ```bash
   curl -X POST http://localhost:8000/tasks/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_jwt_token" \
     -d '{
           "title": "TEXT",
           "description": "TEST"
         }'
   ```
   successful response:
   ```json
   {
    "id": 110,
    "title": "TEXT",
    "description": "TEST",
    "status": "pending",
    "created_at": "2025-01-08T10:06:25.406216Z",
    "updated_at": "2025-01-08T10:06:25.406239Z",
    "user": 1
   }
   ```

4. Connect to websocket (make sure you have wscat installed)
   ```bash
   wscat -c ws://localhost:8000/ws/tasks/
   ```

5. You have logs from notifier service in ClickHouse
   ```bash
   docker exec -it clickhouse clickhouse-client
   ```

   ```sql
   SELECT * FROM logs;
   -- to see the table logs
   ```

## Commit
   ```bash
   pip install pre-commit
   pre-commit install

   pre-commit run --all-files # if you wanna test manually
   git commit -m "Your message" --no-veriyfy # without pre-commit check
   ```

## Usage

To emit an event, send a POST request to the appropriate endpoint with the event data. The service will handle the rest, ensuring the event is published to RabbitMQ and logged by ClickHouse.

## Documentation

API documentation is available at `/api/docs/` and `/api/redoc/` endpoints, providing detailed information about the available endpoints and their usage.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
