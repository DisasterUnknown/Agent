from playwright.sync_api import sync_playwright


def duckduckgo_search(query: str):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--window-position=-10000,0",  
                "--window-size=800,600", 
            ],
        )
        page = browser.new_page()

        page.goto(f"https://html.duckduckgo.com/html/?q={query}")
        page.wait_for_selector(".result")

        items = page.query_selector_all("a.result__a")

        for i, item in enumerate(items, start=0):
            if i >= 10:
                break

            link = item.get_attribute("href")

            snippet_tag = item.query_selector(
                "xpath=../../..//a[@class='result__snippet']"
            )
            snippet = (
                snippet_tag.inner_text().strip()
                if snippet_tag
                else "No description available"
            )

            results.append({"id": i, "link": link, "search_description": snippet})

        browser.close()

    return results
