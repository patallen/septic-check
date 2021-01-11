CheckSeptic
---

### Setup for Docker

Copy the contents of `example.env` to `.env` and update values appropriately

```bash
cp example.env .env
```

If using a HouseCanary base url other than https://api.housecanary.com/v2 add it to the `.env` file under `HOUSE_CANARY_BASE_URL`

Run container: `docker-compose up`

### Set up local environment:

```bash
python3 -m venv .virtualenv
source .virtualenv/bin/activate
pip install -r dev-requirements.txt

HOUSE_CANARY_API_KEY=<string> \
HOUSE_CANARY_API_SECRET=<string> \
./manage.py runserver
```

Try it:
```
curl https://localhost:8000/check-septic?address=<address>&zipcode=<zipcode>
```

## API Documentation
The following query parameters are required: address, zipcode.

Status Codes:
---
200 -> Request completed successfully and true/false determination was made

204 -> Request completed successfully; but true/false determination could not be made

400 -> Request was improperly formatted or has an invalid set of arguments

500 -> Request failed due internal error: I.e. Could not connect to external API

Response Formats
---
200 OK:
```
Content-Type: application/json
{
    "result": <bool>
}
```

non-200 OK:
```
Content-Type: application/json
{
    "message": <string>,
    "data": [<supporting datas>]
}
```

Example:
```
GET => /check-septic?address=18 Haskell Rd&zipcode=03087
<= 200 OK
Content-Type: application/json
{
    "result": true
}
```

### Notes & Next Steps
Scalability
  - Really good canditate for async - (feature/async branch)
  - Proper load balancing
  - Webserver such as uwsgi/gunicorn can handle many concurrent open connections
  - No memory concerns, but response time/open connection time will be dependent on call to external API
  - Caching would not be very effective - would be rare to call this endpoint multiple times with same inputs.
  - Reasonable timeouts should be used to limit the potential request duration

Security
  - Auth should be properly controlled within the VPC using IAM
  - Additional request-level auth such as HMAC or oauthM2M can be utilized
  - If this is a public service, we need to integrate with existing user auth service
  - API credentials and application secrets should be managed with a key management service
  - Separate configurations across deployment stages (DEBUG=False in production)

