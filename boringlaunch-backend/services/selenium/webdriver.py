from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ..logger import log

class WebDriverManager:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.driver = None

    def create_driver(self):
        """Create and configure Chrome WebDriver"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            log.info("WebDriver created successfully")
            return self.driver
        except Exception as e:
            log.error(f"Failed to create WebDriver: {str(e)}")
            raise

    def close_driver(self):
        """Close the WebDriver instance"""
        try:
            if self.driver:
                self.driver.quit()
                log.info("WebDriver closed successfully")
        except Exception as e:
            log.error(f"Failed to close WebDriver: {str(e)}")
            raise

    def __enter__(self):
        """Context manager entry"""
        return self.create_driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_driver() 