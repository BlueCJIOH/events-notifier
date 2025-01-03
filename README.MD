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
   docker-compose up --build
   ```

## Usage

To emit an event, send a POST request to the appropriate endpoint with the event data. The service will handle the rest, ensuring the event is published to RabbitMQ.

## Documentation

API documentation is available at `/api/docs/` and `/api/redoc/` endpoints, providing detailed information about the available endpoints and their usage.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.