# Stablecoin Addresses Scraper

[This script](https://github.com/jonthnoz/stablecoins-scrapper/blob/master/scraper.py) can be used to scrape the addresses of stablecoins from the [CoinGecko](https://www.coingecko.com/) website.

You can use the [second script](https://github.com/jonthnoz/stablecoins-scrapper/blob/master/filter.py) to filter the addresses of stablecoins for a particular blockchain in a JSON file.

Since some addresses have been removed from the CoinGecko website for unknown reasons, you can check a previously computed list [here](https://github.com/jonthnoz/stablecoins-scrapper/blob/master/oldList.json). The community is welcome to contribute to this list.

It's not perfect, but it's a good start.

---

### Known Issues

-   Frax: The ticker is the same for another token, so the data is inaccurate for this coin currently (at the last commit time).
-   The 'main' chain is not always Ethereum, and it's hard to identify which one it is for some coins.
