CheckSeptic
---

### Setup

Copy the contents of `example.env` to `.env` and update values appropriately

```bash
cp example.env .env
```

If using a HouseCanary base url other than 'https://api.housecanary.com/v2' add it to the .env file under `HOUSE_CANARY_BASE_URL`

Set up local environment:


Run `docker-compose up`

or run without docker by:

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