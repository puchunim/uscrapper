"""Classes that represents the models in the website"""

from requests import get # GET request function
from lxml import html # HTML parsing library

class Manga:
    """Class that represents a manga"""
    def __init__(self, name):
        """
        Initializes the class with the name of the manga
        ---

        [Params]
         name: str
            The name of the manga.

        [Attrs]
         *ALL ATTRIBUTES ARE NULL BY DEFAULT*
         exists: bool
            True if the manga exists, False otherwise.
        
         name: str     *Dont confuse with param name*
            The name of the manga.

         rate: float
            The rate of the manga.

         alt_names: list
            A list of alternative names of the manga.
            
         genders: list
            A list of manga's genders.
            
         author: str
            Manga's author name.
         
         artist: str
            Manga's artist name.
        
         status: str
            Manga's release status.
        
         description: str
            Manga's description.
        
         home: lxml.html.HtmlElement
            The HTML element of the manga's home page.

         url: str
            The URL of the manga's home page.

        [Returns]
         Manga
            The manga object.
        """

        self.exists = False
        self.alt_names, self.genders = [], []
        self.author, self.artist, self.status = None, None, None
        self.name, self.rate, self.description = None, None, None

        # Temporary home and url variables, this vars
        # will be replaced by the real ones when the
        # manga exists.
        url = "https://unionleitor.top/pagina-manga/{}".format(name.lower().replace(" ", "-"))
        home = get(url, allow_redirects=False)

        if home.status_code not in [404, 302]:
            # Xpaths to get the additional information of the manga,
            # from the home page.
            desc_x = '//div[@class="col-md-8 col-xs-12"][{}]{}'

            # Intrinsic attributes
            self.exists = True
            self.home = html.fromstring(home.content)
            self.url = url
            
            # Information about the manga itself
            self.name = self.home.xpath('//div[@class="col-md-12"]/h2/text()')[0]
            self.rate = float(self.home.xpath(desc_x.format(1, '/h2/text()'))[0].strip("# "))
            self.alt_names = self.home.xpath(desc_x.format(2, "/h4/text()"))[0].strip().split(", ")
            self.genders = self.home.xpath(desc_x.format(3, "/h4/a/text()"))
            self.author = self.home.xpath(desc_x.format(4, "/h4/text()"))[0].strip()
            self.artist = self.home.xpath(desc_x.format(5, "/h4/text()"))[0].strip()
            self.status = self.home.xpath(desc_x.format(6, "/h4/span/text()"))[0]
            self.description = self.home.xpath(desc_x.format(8, "/div/div/text()"))[0].strip()
