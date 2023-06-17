# Hopper Bacco

Hopper-Bacco (Oh perbacco) is a simple utility that forward requests changing IP and User Agent to avoid bans.

## Quick start

### Configure Hopper Bacco

Create a copy of `.example.env` and rename it to `.env`.

```bash
cp .example.env .env
```

Then edit it based on your needs.

```bash
ENVIRONMENT=production
PORT=10000
LOG_LEVEL=info
ALLOWED_HOSTS=["*"]

API_KEY_HEADER=x-api-key
API_KEY=your_api_key

REQUESTS_TIMEOUT_SECONDS=10
PROXY_COUNTRIES=["IT", "DE"]  # List of countries to use for proxy
```

### Run with docker-compose

```bash
docker-compose up --build -d
```

### Use Hopper Bacco

Hopper Bacco exposes a REST API to forward requests rotating the `User Agent` and using a random `proxy` to avoid bans.
You can check the API documentation at `http://localhost:10000/docs` or `http://localhost:10000/redoc`.
Hopper Bacco is protected by an API key that you can set in the `.env` file.
The `/hop` endpoint accepts the following parameters:

- `url`: (String) the url to forward the request to;
- `method`: (String) the HTTP method to use;
- `params`: (Optional key value dictionary) the query string parameters;
- `data`: (Optional String) the data of the request (used to send `xml` data type);
- `body`: (Optional key value dictionary) the body of the request;
- `headers`: (Optional key value dictionary) the headers of the request.
- `type`: (Optional string) request content response type. For example `application/json` or `application/xml`.
  Default: `application/json`.

Note that `type` parameter is used to return as the defined media type, it does not change the response content
structure.
#### Request Example

```bash
curl --location 'http://localhost:10000/api/v1/hop' \
--header 'x-api-key: {{your_api_key}}' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://postman-echo.com/get",
    "method": "GET",
    "params": {
        "foo1": "bar1",
        "foo2": "bar2"
    },
    "body": {
        "foo3": "foo3",
        "foo4": "foo4"
    },
    "headers": {
        "x-custom-header": "custom header value"
    },
    "type": "application/json"
}'
```