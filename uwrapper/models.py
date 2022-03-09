"""Classes that represents the models in the website"""

from requests import get # GET request function
from lxml import html # HTML parsing library

class Manga:
    """
    Class that represents a manga
    
    [Attrs]
     exists: bool
        True if the manga exists, False otherwise.
         
     *ALL ATTRIBUTES ARE NULL BY DEFAULT*        
     name: str
        The name of the manga.

     rate: float
        The rate of the manga.

     thumbnaill: str
        The url of the manga's thumbnail.

     votes: int
        The number of votes the manga has.
        
     length: int
        The length of the manga in chapters.

     alt_names: list
        A list of alternative names of the manga.
            
     genres: list
        A list of manga's genres.
            
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
    """

    def __init__(self, name):
        """
        Initializes the class with the name of the manga
        ---

        [Params]
         name: str
            The name of the manga.

        [Returns]
         Manga
            The manga object.
        """

        self.exists = False
        self.alt_names, self.genres = [], []
        self.author = self.artist = self.status = None
        self.name = self.rate = self.description = None
        self.thumbnail = self.votes = self.length = None

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
            self.home = html.fromstring(home.content)
            self.url = url

            # Information about the manga itself
            self.exists = True
            self.name = self.home.xpath('//div[@class="col-md-12"]/h2/text()')[0]
            self.thumbnail = self.home.xpath('//img[@class="img-thumbnail"]/@src')[0]
            self.length = len(self.home.xpath('//div[@class="col-xs-6 col-md-6"]'))
            self.rate = float(self.home.xpath(desc_x.format(1, '/h2/text()'))[0].strip("# "))
            self.votes = int(self.home.xpath(desc_x.format(1, '/h2/small/strong/text()'))[0])
            self.alt_names = self.home.xpath(desc_x.format(2, "/h4/text()"))[0].strip().split(", ")
            self.genres = self.home.xpath(desc_x.format(3, "/h4/a/text()"))
            self.author = self.home.xpath(desc_x.format(4, "/h4/text()"))[0].strip()
            self.artist = self.home.xpath(desc_x.format(5, "/h4/text()"))[0].strip()
            self.status = self.home.xpath(desc_x.format(6, "/h4/span/text()"))[0]
            self.description = self.home.xpath(desc_x.format(8, "/div/div/text()"))[0].strip()

    def __len__(self):
        """Defines the return of the len() function"""  
        return self.length

    def __repr__(self):
        """Defines the return of the repr() function"""
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        """Defines the return of the str() function"""
        return f"<{self.__class__.__name__}: {self.name}>" 
    
    def __lt__(self, other):
        """Check if the manga length is less than the other"""
        if not hasattr(other, "__len__"): return False
        
        return len(self) < len(other)
    
    def __le__(self, other):
        """Check if the manga length is less or equal than the other"""
        if not hasattr(other, "__len__"): return False
        
        return len(self) <= len(other)
    
    def __eq__(self, other):
        """Check if the manga is equal to the other"""
        if not isinstance(other, Manga): return False

        sd = self.__dict__.copy()
        od = other.__dict__.copy()
        sd.pop("home")
        od.pop("home")
        
        return sd == od

    def __ne__(self, other):
        """Check if the manga is not equal to the other"""
        if not hasattr(other, "__len__"): return False
        
        return not self.__eq__(other)
    
    def __gt__(self, other):
        """Defines the return of the > operator"""
        if not hasattr(other, "__len__"): return False
        
        return len(self) > len(other)

    def __ge__(self, other):
        """Defines the return of the >= operator"""
        if not hasattr(other, "__len__"): return False
        
        return len(self) >= len(other)
