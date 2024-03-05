# web-scraping

Application require to create `.env` file based on `.env-example`. After that it can be launched using docker:

```
docker compose up
```

Application contains 3 microservices:<br />
1. mongodb - nosql database for saving scrapped informations,
2. app - presentation application based on streamlit,
3. scrapper - service responsible for crawling data from written spiders.

Application is not hosted anywhere due to lack of cloud credits.