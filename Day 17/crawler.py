import asyncio
import os
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

async def main():
    # Configure a deep crawl with max 200 pages
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            max_pages=200,
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun("https://www.wikipedia.org", config=config)

        print(f"Crawled {len(results)} pages in total")

        # Create results directory if it doesn't exist
        results_dir = "crawl_results"
        os.makedirs(results_dir, exist_ok=True)
        
        # Generate timestamp for file names
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # File paths
        md_filename = os.path.join(results_dir, f"crawl_results_{timestamp}.md")
        txt_filename = os.path.join(results_dir, f"crawl_results_{timestamp}.txt")
        json_filename = os.path.join(results_dir, f"crawl_results_{timestamp}.json")
        
        # Write to markdown file
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(f"# Web Crawling Results\n\n")
            md_file.write(f"**Crawl Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            md_file.write(f"**Total Pages Crawled:** {len(results)}\n")
            md_file.write(f"**Max Pages Limit:** 200\n")
            md_file.write(f"**Starting URL:** https://www.wikipedia.org\n\n")
            md_file.write("---\n\n")
            
            for i, result in enumerate(results, 1):
                md_file.write(f"## Page {i}\n\n")
                md_file.write(f"**URL:** {result.url}\n")
                md_file.write(f"**Depth:** {result.metadata.get('depth', 0)}\n")
                md_file.write(f"**Status Code:** {result.status_code}\n")
                md_file.write(f"**Content Length:** {len(result.cleaned_html) if result.cleaned_html else 0} characters\n\n")
                
                if result.cleaned_html:
                    # Add first 500 characters of content as preview
                    content_preview = result.cleaned_html[:500] + "..." if len(result.cleaned_html) > 500 else result.cleaned_html
                    md_file.write(f"**Content Preview:**\n```\n{content_preview}\n```\n\n")
                
                md_file.write("---\n\n")
        
        # Write to text file
        with open(txt_filename, 'w', encoding='utf-8') as txt_file:
            txt_file.write("WEB CRAWLING RESULTS\n")
            txt_file.write("=" * 50 + "\n\n")
            txt_file.write(f"Crawl Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            txt_file.write(f"Total Pages Crawled: {len(results)}\n")
            txt_file.write(f"Max Pages Limit: 200\n")
            txt_file.write(f"Starting URL: https://www.wikipedia.org\n\n")
            txt_file.write("-" * 50 + "\n\n")
            
            for i, result in enumerate(results, 1):
                txt_file.write(f"PAGE {i}\n")
                txt_file.write(f"URL: {result.url}\n")
                txt_file.write(f"Depth: {result.metadata.get('depth', 0)}\n")
                txt_file.write(f"Status Code: {result.status_code}\n")
                txt_file.write(f"Content Length: {len(result.cleaned_html) if result.cleaned_html else 0} characters\n\n")
                
                if result.cleaned_html:
                    # Add first 500 characters of content as preview
                    content_preview = result.cleaned_html[:500] + "..." if len(result.cleaned_html) > 500 else result.cleaned_html
                    txt_file.write(f"Content Preview:\n{content_preview}\n\n")
                
                txt_file.write("-" * 50 + "\n\n")
        
        # Write to JSON file
        json_data = {
            "crawl_info": {
                "crawl_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "total_pages_crawled": len(results),
                "max_pages_limit": 200,
                "starting_url": "https://www.wikipedia.org"
            },
            "results": []
        }
        
        for i, result in enumerate(results, 1):
            page_data = {
                "page_number": i,
                "url": result.url,
                "depth": result.metadata.get('depth', 0),
                "status_code": result.status_code,
                "content_length": len(result.cleaned_html) if result.cleaned_html else 0,
                "title": result.metadata.get('title', ''),
                "description": result.metadata.get('description', ''),
                "content_preview": result.cleaned_html[:500] + "..." if result.cleaned_html and len(result.cleaned_html) > 500 else result.cleaned_html or "",
                "links_found": len(result.links.get('internal', [])) if hasattr(result, 'links') and result.links else 0,
                "images_found": len(result.media.get('images', [])) if hasattr(result, 'media') and result.media else 0
            }
            json_data["results"].append(page_data)
        
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=2, ensure_ascii=False)
        
        print(f"Results saved to:")
        print(f"  Markdown: {md_filename}")
        print(f"  Text: {txt_filename}")
        print(f"  JSON: {json_filename}")

        # Access individual results (keeping original functionality)
        for result in results[:3]:  # Show first 3 results
            print(f"URL: {result.url}")
            print(f"Depth: {result.metadata.get('depth', 0)}")

if __name__ == "__main__":
    asyncio.run(main())