from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

class DOMTools:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_text(self) -> str:
        return self.soup.get_text()

    def find_elements(self, selector: str) -> List[Dict[str, Any]]:
        elements = []
        for tag in self.soup.select(selector):
            element_info = {
                "tag": tag.name,
                "text": tag.get_text(strip=True),
                "attrs": tag.attrs
            }
            elements.append(element_info)
        return elements

    def get_element_attribute(self, selector: str, attribute: str) -> Optional[str]:
        element = self.soup.select_one(selector)
        if element:
            return element.get(attribute)
        return None

    def simplify_dom(self) -> str:
        # Remove script and style tags
        for script_or_style in self.soup(["script", "style"]):
            script_or_style.decompose()
        
        # Remove comments
        for comment in self.soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Remove excessive whitespace
        for tag in self.soup.find_all(True):
            if tag.string:
                tag.string = ' '.join(tag.string.split())
        
        return str(self.soup)

# Example usage (for testing purposes)
if __name__ == "__main__":
    html = """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Hello, World!</h1>
        <p id="intro">This is an <a href="#">example</a> paragraph.</p>
        <div class="container">
            <button class="btn" data-action="click">Click Me</button>
            <span style="display:none;">Hidden text</span>
        </div>
        <!-- A comment -->
        <script>alert('hi');</script>
    </body>
    </html>
    """
    dom_tools = DOMTools(html)
    
    print("--- Extracted Text ---")
    print(dom_tools.extract_text())
    
    print("\n--- Find H1 Elements ---")
    print(dom_tools.find_elements("h1"))
    
    print("\n--- Get Button Action Attribute ---")
    print(dom_tools.get_element_attribute(".btn", "data-action"))

    print("\n--- Simplified DOM ---")
    print(dom_tools.simplify_dom())
