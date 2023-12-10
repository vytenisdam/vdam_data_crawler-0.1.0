from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

from lxml.etree import HTML
from requests import get

visited_pages = set()
visited_articles = set()

pages_queue = Queue()
articles_queue = Queue()


def query_to_url(query: str) -> str:
    return f"https://www.lrytas.lt/search?q={query}"


def process_page(page_url: str) -> str:
    print(page_url)
    try:
        response = get(page_url)
        tree = HTML(response.text)
        for page_link in tree.xpath(
                "//a[contains(@class, 'LPagination__button')]/@href"
        ):
            full_page_url = "https://www.lrytas.lt" + page_link
            if full_page_url not in visited_pages:
                pages_queue.put(full_page_url)
                visited_pages.add(full_page_url)
        for article_link in tree.xpath("//a[@class='LPostContent__anchor']/@href"):
            article_url = "https://www.lrytas.lt" + article_link
            if article_url not in visited_articles:
                visited_articles.add(article_url)
                articles_queue.put(article_url)

    except Exception as e:
        print("Error retrieving url", e)


if __name__ == "__main__":
    initial_url = query_to_url("rytas")
    pages_queue.put(initial_url)
    visited_pages.add(initial_url)
    with ThreadPoolExecutor(10) as executor:
        futures = set()
        while not pages_queue.empty() and len(futures) < 10:
            page = pages_queue.get()
            future = executor.submit(process_page, page)
            futures.add(future)
        done = as_completed(futures, timeout=None)
        for future in done:
            futures.remove(future)
    print("Finished processing all pages.")