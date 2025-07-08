import asyncio
from typing import List, Dict
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import re
from app.models import ProductResult
from app.search_engines import get_currency
import json

async def extract_structured_data(html: str) -> List[dict]:
    """Extract JSON-LD structured data from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'Product':
                results.append(data)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('@type') == 'Product':
                        results.append(item)
        except:
            continue
    
    return results

async def scrape_site(url: str, country: str, site_name: str) -> List[ProductResult]:
    results = []
    try:
        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url, bypass_cache=True)
            
            # Try structured data first
            structured_data = await extract_structured_data(result.html)
            
            for product in structured_data[:10]:
                try:
                    name = product.get('name', '')
                    offers = product.get('offers', {})
                    if isinstance(offers, list):
                        offers = offers[0] if offers else {}
                    
                    price = offers.get('price')
                    if price and name:
                        results.append(ProductResult(
                            link=product.get('url', url),
                            price=str(price),
                            currency=offers.get('priceCurrency', get_currency(country)),
                            productName=name[:100],
                            source=site_name
                        ))
                except:
                    continue
            
            # If no structured data, try basic HTML parsing
            if not results:
                soup = BeautifulSoup(result.html, 'html.parser')
                
                # Find all links with product-like text
                links = soup.find_all('a', href=True)
                
                for link in links[:50]:  # Check first 50 links
                    text = link.get_text(strip=True)
                    href = link['href']
                    
                    # Skip if text is too short or doesn't contain query terms
                    if len(text) < 20 or 'iphone' not in text.lower():
                        continue
                    
                    # Look for price near this link
                    parent = link.parent
                    if parent:
                        parent_text = parent.get_text()
                        price_matches = re.findall(r'[$]?\s*(\d{1,4}(?:[,.]?\d{3})*(?:\.\d{2})?)', parent_text)
                        
                        for price_match in price_matches:
                            price = price_match.replace(',', '').replace('$', '')
                            try:
                                if float(price) > 100 and float(price) < 5000:  # Reasonable price range
                                    full_url = href
                                    if not href.startswith('http'):
                                        if href.startswith('/'):
                                            base_url = '/'.join(url.split('/')[:3])
                                            full_url = base_url + href
                                        else:
                                            continue
                                    
                                    results.append(ProductResult(
                                        link=full_url,
                                        price=price,
                                        currency=get_currency(country),
                                        productName=text[:100],
                                        source=site_name
                                    ))
                                    break
                            except:
                                continue
                    
                    if len(results) >= 10:
                        break
    except Exception as e:
        print(f"Error scraping {site_name}: {e}")
    
    return results

async def fetch_prices(country: str, query: str, search_urls: List[Dict[str, str]]) -> List[ProductResult]:
    # Only use sites we can reliably scrape
    reliable_sites = ['Google Shopping', 'Amazon', 'eBay']
    filtered_urls = [s for s in search_urls if s['name'] in reliable_sites]
    
    tasks = []
    for search_data in filtered_urls:
        tasks.append(scrape_site(search_data["url"], country, search_data["name"]))
    
    results = await asyncio.gather(*tasks)
    
    # Flatten and filter
    all_results = []
    query_terms = query.lower().split()
    
    for result_list in results:
        for result in result_list:
            # Basic relevance check
            product_lower = result.productName.lower()
            # Check if at least one major query term is in product name
            if any(term in product_lower for term in query_terms if len(term) > 3):
                all_results.append(result)
    
    # Remove duplicates based on product name similarity
    unique_results = []
    seen_names = set()
    
    for result in all_results:
        name_key = result.productName[:30].lower()
        if name_key not in seen_names:
            seen_names.add(name_key)
            unique_results.append(result)
    
    # Sort by price
    unique_results.sort(key=lambda x: float(x.price))
    
    return unique_results[:20]