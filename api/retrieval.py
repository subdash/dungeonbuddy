import json
import requests
import urllib.parse

from bs4 import BeautifulSoup


class HyperLink:
    def __init__(self, text, link):
        self.text = text
        self.link = link


class Retriever:
    def __init__(self):
        """Sets the base url and urls for search methods."""
        self.base_url = 'https://roll20.net'
        self.list_search_url = self.base_url + \
            '/compendium/compendium/globalsearch/dnd5e?terms='
        self.full_search_url = self.base_url + \
            '/compendium/dnd5e/searchbook/?terms='

    def get_list_results(self, search_term):
        """
        Build url by adding escaped version of search term, convert string response
        to a list of dicts, extract the value of the key called 'value' from each
        dict, build a list with those values and return it.
        This method alone is not useful, but could be combined with other methods
        to generate more detailed queries (e.g. pass response terms from this
        method to get_result_obj() method and combine them).
        Args:
            search_term (str): The term(s) to search the comendium for
        Returns:
            response_links (:obj:`list` of :obj:`str`): Returns a list of strings
        """
        url = self.list_search_url + urllib.parse.quote(search_term)

        returned_results = []
        for result in json.loads(requests.get(url).text):
            returned_results.append(result['value'])

        return returned_results

    def get_result_obj(self, search_term):
        """
        Searching the compendium either returns a page, or a list of links to
        search results. This method returns either the response object for the
        former, or a list of HyperLink objects
        Args:
            search_term (str): The term(s) to search the comendium for
        Returns:
            response (requests.models.Response): Returns the response if the user
            is redirected to a different page.
            get_result_links(response): Returns a call to get_result_links() with
            the response passed as an argument if the user is not redirected.
        """
        url = self.full_search_url + urllib.parse.quote(search_term)

        response = requests.get(url)

        if not response.status_code == 200:
            raise Exception('Expected 200 response status code, received '
                            f'{response.status_code} instead')

        if response.url != url:  # Redirected to new page with content
            print(f'Redirected to {response.url}')
            return response
        else:  # Redirected to page with list of result hyperlinks
            return self.get_result_links(response)

    def get_result_links(self, response):
        """
        Takes a response object as an argument and finds all <li> tags. Then parses
        each one to check if it returns a URI. Then builds a list of HyperLink
        objects that contain the URI and associated text.
        Args:
            response (requests.models.Response)
        Returns:
            response_links (:obj:`list` of :obj:`HyperLink`)
        """
        # Find all <li> tags in the body of the response and wrap in list()
        list_items = list(BeautifulSoup(response.content,
                                        features="html.parser").find_all('li'))
        response_links = []

        for li in list_items:
            if self.has_uri(li):  # Returned URI
                text = li.contents[1].get_text()
                uri = li.a.get('href')
                response_links.append(HyperLink(text=text, link=uri))

        return response_links

    def has_uri(self, tag):
        """
        Args:
            tag (bs4.element.Tag): A markup tag extracted from a BeautifulSoup
            object.
        Returns:
            bool: True if tag contains an href that is a URI rather than a full
            URL, False otherwise.
        """
        return 'href="/' in tag.decode_contents()


class Parser:
    def __init__(self, response_obj):
        """Takes a response object as an argument to form soup."""
        self.response_obj = response_obj
        self.soup = BeautifulSoup(response_obj.content, features="html.parser")
        self.details = {'title': self.soup.title.string}

    def add_attribute(self, key, value):
        """Add an attribute from page to dictionary to construct object."""
        self.details[key] = value

    def gather_content(self):
        pass

    def gather_attributes(self):
        """If response object passed to constructor has an Attributes section,
        this method will parse it.
        """
        attribute_soup = self.soup.find(id='pageAttrs')
        all_keys = attribute_soup.find_all('div', class_='col-md-3 attrName')
        all_values = attribute_soup.find_all('div',  class_='value')

        for i in range(len(all_keys)):
            self.add_attribute(all_keys[i].string, all_values[i].string)
