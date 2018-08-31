import json
import requests
import urllib.parse

from bs4 import BeautifulSoup


class HyperLink:
    """This class is used to keep store a hyperlink returned from a query."""
    def __init__(self, text, link):
        self.text = text
        self.link = link


class Retriever:
    """This class is used to retrieve search results from roll20. It is not
    responsible for processing the results.
    """
    def __init__(self):
        self.base_url = 'https://roll20.net'
        self.list_search_url = self.base_url + \
            '/compendium/compendium/globalsearch/dnd5e?terms='
        self.full_search_url = self.base_url + \
            '/compendium/dnd5e/searchbook/?terms='

    def get_list_results(self, search_term):
        """Build url by adding escaped version of search term, convert string
        response to a list of dicts, extract the value of the key called
        'value' from each dict, build a list with those values and return it.
        This method alone is not useful, but could be combined with other
        methods to generate more detailed queries (e.g. pass response terms
        from this method to get_result_obj() method and combine them).

        Args:
            search_term (str): The term(s) to search the compendium for
        Returns:
            (list<str>): Returns a list of strings
        """
        url = self.list_search_url + urllib.parse.quote(search_term)

        return [result['value'] for result in requests.get(url).json()]

    def get_result_obj(self, search_term):
        """Searching the compendium either returns a page, or a list of links
        to search results. This method returns either the response object for
        the former, or a list of HyperLink objects.

        Args:
            search_term (str): The term(s) to search the compendium for
        Returns:
            response (requests.models.Response): Returns the response if the
            user is redirected to a different page.
            get_result_links(response): Returns a call to get_result_links()
            with the response passed as an argument if the user is not
            redirected.
        """
        url = self.full_search_url + urllib.parse.quote(search_term)

        response = requests.get(url)

        if not response.status_code == 200:
            raise Exception('(Expected 200 response status code, received '
                            f'{response.status_code} instead.)')

        if response.url != url:  # Redirected to new page with content
            # DEBUG:
            print(f'(Redirected to {response.url})')

            return response

        else:  # Redirected to page with list of result hyperlinks
            return self.get_result_links(response, search_term)

    def get_result_links(self, response, search_term):
        """
        Takes a response object as an argument and finds all <li> tags. Then
        parses each one to check if it returns a URI and checks the text of
        the tag to see if it matches the original search term. If it does,
        the function returns a response object of that page. If not, each tag
        is added to a list of HyperLink objects that contain the URI and
        associated text.

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
            if self.has_uri(li):  # List item contains a URI
                text = li.contents[1].get_text()
                uri = li.a.get('href')
                # If one of the links matches the search term, return it
                if text.lower() == search_term.lower():
                    return requests.get(li.url)
                # Otherwise, add the resource to a list to return
                response_links.append(HyperLink(text=text, link=uri))

        # DEBUG:
        print(f'(Unable to find an exact match for {search_term}.)')

        return response_links

    @staticmethod
    def has_uri(tag):
        """Checks if a tag contains a URI.

        Args:
            tag (bs4.element.Tag): A markup tag extracted from a BeautifulSoup
            object.
        Returns:
            bool: True if tag contains an href that is a URI rather than a full
            URL, False otherwise.
        """
        return 'href="/' in tag.decode_contents()


class Parser:
    """This class is used to process search results. It is not responsible for
    retrieving search results.
    """
    def __init__(self, response_obj):
        """Takes a response object as an argument to form soup."""
        self.response_obj = response_obj
        self.soup = BeautifulSoup(response_obj.content, features="html.parser")
        self.details = {'title': self.soup.title.string}

    def add_attribute(self, key, value):
        """Add an attribute from page to dictionary to construct object."""
        self.details[key] = value

    def gather_attributes(self):
        """If response object passed to constructor has an Attributes section,
        this method will parse it.
        """
        attribute_soup = self.soup.find(id='pageAttrs')
        all_keys = attribute_soup.find_all('div', class_='col-md-3 attrName')
        all_values = attribute_soup.find_all('div',  class_='value')

        for i in range(len(all_keys)):
            self.add_attribute(all_keys[i].string, all_values[i].string)


class DungeonBuddy:
    """This class represents the public interface for the API. It has a single
    method, get_result().
    """
    def __init__(self):
        self.base_url = 'https://roll20.net'

    def get_result(self, search_term):
        """Takes a search term as an argument and returns a JSON formatted
        string. There should be 3 possible non-error results:
        - A single JSON object     (when search returns a single result)
        - An array of JSON objects (when search returns multiple results)
        - An empty JSON object     (when search returns no results)

        Args:
            search_term (str): Any string
        Returns:
            json.dumps()
        """
        if not isinstance(search_term, str):
            raise TypeError('result_obj() expected str, got '
                            f'{type(search_term)}')

        r = Retriever()
        result_obj = r.get_result_obj(search_term)

        # Single result or match
        if isinstance(result_obj, requests.models.Response):
            p = Parser(result_obj)
            p.gather_attributes()
            return json.dumps(p.details)  # Return JSON formatted string

        # Multiple results or no match
        elif isinstance(result_obj, list):
            data = []
            for result in result_obj:
                name = result.text
                content = requests.get(self.base_url + result.link)
                parsed_content = Parser(content)
                parsed_content.gather_attributes()
                data.append(dict({name: parsed_content.details}))
            return json.dumps(data)

        # result_obj should always be of type Response or list
        raise Exception('An unknown error occurred.')
