import markdown
from bs4 import BeautifulSoup

class MarkdownParser:
    # Function to read the Markdown file
    def read_markdown_file(self,filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            md_content = file.read()
        return md_content

    # Function to convert Markdown to HTML
    def convert_md_to_html(self,md_content):
        return markdown.markdown(md_content)

    # Function to parse HTML and extract data
    def parse_html(self,html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        # print(soup)
        headers = [header.get_text() for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        paragraphs = [para.get_text() for para in soup.find_all('p')]
        # print(headers)
        return headers, paragraphs

    # Main function to process the Markdown file
    def process_markdown_file(self,filepath):
        md_content = self.read_markdown_file(filepath)
        html_content = self.convert_md_to_html(md_content)
        headers, paragraphs = self.parse_html(html_content)
        
        # print("Headers:")
        # for header in headers:
        #     print(header)
        
        # print("\nParagraphs:")
        # for paragraph in paragraphs:
        #     print(paragraph)
        return paragraphs