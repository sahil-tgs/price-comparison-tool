from typing import Dict, List

SEARCH_ENGINES = {
    "US": [
        {"name": "Google Shopping", "url": "https://www.google.com/search?tbm=shop&q="},
        {"name": "Amazon", "url": "https://www.amazon.com/s?k="},
        {"name": "eBay", "url": "https://www.ebay.com/sch/i.html?_nkw="},
        {"name": "Walmart", "url": "https://www.walmart.com/search?q="},
        {"name": "BestBuy", "url": "https://www.bestbuy.com/site/searchpage.jsp?st="}
    ],
    "IN": [
        {"name": "Google Shopping", "url": "https://www.google.co.in/search?tbm=shop&q="},
        {"name": "Amazon India", "url": "https://www.amazon.in/s?k="},
        {"name": "Flipkart", "url": "https://www.flipkart.com/search?q="},
        {"name": "Myntra", "url": "https://www.myntra.com/"},
        {"name": "Snapdeal", "url": "https://www.snapdeal.com/search?keyword="}
    ],
    "UK": [
        {"name": "Google Shopping", "url": "https://www.google.co.uk/search?tbm=shop&q="},
        {"name": "Amazon UK", "url": "https://www.amazon.co.uk/s?k="},
        {"name": "eBay UK", "url": "https://www.ebay.co.uk/sch/i.html?_nkw="},
        {"name": "Argos", "url": "https://www.argos.co.uk/search/"}
    ],
    "DEFAULT": [
        {"name": "Google Shopping", "url": "https://www.google.com/search?tbm=shop&q="}
    ]
}

CURRENCY_MAP = {
    "US": "USD",
    "IN": "INR", 
    "UK": "GBP",
    "CA": "CAD",
    "AU": "AUD",
    "EU": "EUR"
}

def get_search_urls(country: str, query: str) -> List[Dict[str, str]]:
    engines = SEARCH_ENGINES.get(country.upper(), SEARCH_ENGINES["DEFAULT"])
    return [{"name": engine["name"], "url": engine["url"] + query.replace(" ", "+")} for engine in engines]

def get_currency(country: str) -> str:
    return CURRENCY_MAP.get(country.upper(), "USD")