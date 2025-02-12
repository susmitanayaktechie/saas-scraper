from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import pandas as pd
import time
import random
import logging
import dns.resolver
import ssl
import socket
import requests
from typing import List, Dict
import json
import re

class SaaSAttributeScraper:
    def __init__(self, headless: bool = True):
        self.logger = self._setup_logging()
        self.chrome_options = self._setup_chrome_options(headless)
        self.driver = None

    def _setup_logging(self) -> logging.Logger:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def _setup_chrome_options(self, headless: bool) -> Options:
        options = Options()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        ua = UserAgent()
        options.add_argument(f'user-agent={ua.random}')
        return options

    def start_browser(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def _extract_vendor_attributes(self, url: str) -> Dict:
        attrs = {}
        attrs['app_name'] = self.driver.title
        attrs['app_domains'] = url
        attrs['vendor_name'] = self._find_company_name()
        attrs['linkedin_url'] = self._find_social_links().get('linkedin')
        attrs['employee_count'] = self._extract_employee_count()
        attrs['founded'] = self._extract_founding_date()
        attrs['headquarters_location'] = self._extract_location()
        attrs['holding_type'] = self._determine_holding_type()
        attrs['category'] = self._extract_category()
        attrs['type_of_service'] = self._extract_service_type()
        return attrs

    def _find_company_name(self) -> str:
        try:
            element = self.driver.find_element(By.TAG_NAME, 'h1')
            return element.text.strip()
        except:
            return "Unknown"

    def _find_social_links(self) -> Dict:
        links = {}
        try:
            social_elements = self.driver.find_elements(By.TAG_NAME, 'a')
            for elem in social_elements:
                href = elem.get_attribute('href')
                if href:
                    if 'linkedin.com' in href:
                        links['linkedin'] = href
        except:
            pass
        return links

    def _extract_employee_count(self) -> str:
        return "Not available"
    
    def _extract_founding_date(self) -> str:
        return "Not available"
    
    def _extract_location(self) -> str:
        return "Not available"

    def _determine_holding_type(self) -> str:
        return "Private"
    
    def _extract_category(self) -> str:
        return "AI"

    def _extract_service_type(self) -> str:
        return "SaaS"
    
    def _extract_compliance_attributes(self) -> Dict:
        compliance_attrs = {}
        compliance_keywords = ['gdpr', 'hipaa', 'soc 2', 'iso 27001', 'pci dss', 'fedramp', 'ccpa', 'nist']
        page_text = self.driver.page_source.lower()
        for keyword in compliance_keywords:
            compliance_attrs[keyword] = keyword in page_text
        return compliance_attrs
    
    def _check_security_headers(self, url: str) -> Dict:
        headers = {}
        try:
            response = requests.head(url)
            headers['strict_transport_security'] = 'Strict-Transport-Security' in response.headers
            headers['x_content_type_options'] = 'X-Content-Type-Options' in response.headers
            headers['x_frame_options'] = 'X-Frame-Options' in response.headers
            headers['content_security_policy'] = 'Content-Security-Policy' in response.headers
        except:
            pass
        return headers

    def analyze_site(self, url: str) -> Dict:
        try:
            self.start_browser()
            self.driver.get(url)
            time.sleep(random.uniform(2, 5))
            attributes = {}
            attributes.update(self._extract_vendor_attributes(url))
            attributes.update(self._extract_compliance_attributes())
            attributes.update(self._check_security_headers(url))
            return attributes
        except:
            return {}
        finally:
            self.close_browser()

    def analyze_multiple_sites(self, urls: List[str]) -> pd.DataFrame:
        results = []
        for url in urls:
            self.logger.info(f"Analyzing {url}")
            attributes = self.analyze_site(url)
            attributes['url'] = url
            results.append(attributes)
            time.sleep(random.uniform(2.0, 5.0))
        return pd.DataFrame(results)

    def save_results(self, df: pd.DataFrame, filename: str):
        df.to_csv(f"{filename}.csv", index=False)
        df.to_json(f"{filename}.json", orient='records', indent=2)
        self.logger.info(f"Results saved to {filename}.csv and {filename}.json")

def main():
    ai_websites = [
        "https://openai.com",
        "https://anthropic.com",
        "https://stability.ai",
        "https://www.jasper.ai",
        "https://www.grammarly.com",
        "https://www.copy.ai",
        "https://www.writesonic.com"
    ]
    
    scraper = SaaSAttributeScraper(headless=True)
    results_df = scraper.analyze_multiple_sites(ai_websites)
    scraper.save_results(results_df, "ai_saas_attributes")
    
    print("\nAttribute coverage statistics:")
    print(results_df.notna().mean().sort_values(ascending=False))

if __name__ == "__main__":
    main()
