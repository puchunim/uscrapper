"""Classes that represents the models in the website"""

from os import (
    makedirs, # Function to create dirs
    listdir, # Function to list files
    path # Module to get path information
)
from requests import get # GET request function
from lxml import html # HTML parsing library
from json import (
    dump, # Save to json function
    load  # Load from json function
)

class Manga:
    """
    Class that represents a manga
    
    [Attrs]
     exists: bool
        True if the manga exists, False otherwise.
         
     *ALL ATTRIBUTES ARE NULL BY DEFAULT*
     __name : str
        The name of the manga, without spaces and with dashes,
        come from the user.
          
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
        self.__name = name.lower().replace(" ", "-")
        self.alt_names, self.genres = [], []
        self.author = self.artist = self.status = None
        self.name = self.rate = self.description = None
        self.thumbnail = self.votes = self.length = None
        
        # Loads the manga's information from
        # a cached index.json file
        # TODO: Add a more robust and optional caching system
        try:
            if self.__name in listdir("./uscrapper/data/"):
                self.exists = True
                self.__dict__.update(self.__from_json("index"))
                if self.status == "Ativo":
                    self.home = html.fromstring(get(self.url, allow_redirects=False).content)
                return
        
        except FileNotFoundError:
            pass

        # Temporary home and url variables, this vars
        # will be replaced by the real ones when the
        # manga exists.
        url = "https://unionleitor.top/pagina-manga/{}".format(self.__name)
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

        sd = self.__dict__.copy()
        sd["home"] = None
        self.__to_json("index", sd)

    def __len__(self):
        """Defines the return of the len() function"""  
        return self.length

    def __repr__(self):
        """Defines the return of the repr() function"""
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        """Defines the return of the str() function"""
        return f"<{self.__class__.__name__}: {self.name}>" 
    
    # TODO: Compatibility with int and float values on operations
    # TODO: Decide how magic methods will work properly
    def __lt__(self, other):
        """Check if the manga length is less than the other"""
        if not isinstance(other, Manga):
            raise TypeError(f"Comparisons only work with two 'Manga' objects, other's type == {type(other)}")

        
        return len(self) < len(other)
    
    def __le__(self, other):
        """Check if the manga length is less or equal than the other"""
        if not isinstance(other, Manga):
            raise TypeError(f"Comparisons only work with two 'Manga' objects, other's type == {type(other)}")
        
        return len(self) <= len(other)
    
    def __eq__(self, other):
        """Check if the manga is equal to the other"""
        if not isinstance(other, Manga):
            raise TypeError(f"Comparisons only work with two 'Manga' objects, other's type == {type(other)}")


        sd = self.__dict__.copy()
        od = other.__dict__.copy()
        sd.pop("home")
        od.pop("home")
        
        return sd == od

    def __ne__(self, other):
        """Check if the manga is not equal to the other"""
        if not isinstance(other, Manga):
            raise TypeError(f"Comparisons only work with two 'Manga' objects, other's type == {type(other)}")

        return not self.__eq__(other)
    
    def __gt__(self, other):
        """Defines the return of the > operator"""
        if not isinstance(other, Manga):
            raise TypeError(f"Comparisons only work with two 'Manga' objects, other's type == {type(other)}")

        return len(self) > len(other)

    def __ge__(self, other):
        """Defines the return of the >= operator"""
        if not isinstance(other, Manga):
            raise TypeError(f"Comparisons only work with two 'Manga' objects, other's type == {type(other)}")
        
        return len(self) >= len(other)

    def __from_json(self, jname, _path="./uscrapper/data/"):
        """
        Loads the manga's information from a .json file
        ---
        
        [Params]
         jname: str
            The name of the json file.
         
         path: str
            The path where the file is saved.
        
        [Returns]
         dict
            The dictionary with the manga's information, or None if the file doesn't exist.
        """

        if path.isfile((p := f"{_path}{self.__name}/{jname}.json")):                
            with open(p, "r", encoding="utf8") as jf:
                return load(jf)
            
        return {}

    def __to_json(self, jname, obj, _path="./uscrapper/data/"):
        """
        Saves the manga's information in a .json file
        ---
        
        [Params]
         jname: str
            The name of the file.
                
         obj: dict
            The object to be saved.

         path: str
            The path where the file will be saved.
        
        [Returns]
         None
        """

        if not self.exists:
            return False    # TODO: Raise custom exception
        
        makedirs((p := f"{_path}{self.__name}"), exist_ok=True)
        with open(f"{p}/{jname}.json", "w+", encoding="utf8") as jf:
            dump(obj, jf, indent=4)

    def get_chapters(self, _path="./uscrapper/data/"):
        """
        Gets the chapters of the manga
        ---
        
        [Params]
         path: str
            The path where the file is saved.
        
        [Returns]
         None
        """

        if not self.exists:
            return False    # TODO: Raise custom exception
        
        chapters = {}
        if (jf := self.__from_json("chapters", _path)):
            chapters.update(jf)

        else:
            if not self.home:
                self.home = html.fromstring(get(self.url).content)

            c_urls = self.home.xpath('//div[@class="col-xs-6 col-md-6"]/a/@href')
            c_urls.sort()
            for url in c_urls:
                c_page = html.fromstring(get(url).content)
                chapters[url.split("/")[-1]] = c_page.xpath('//div[@class="col-sm-12 text-center"]/img/@src')[2:]
            
            self.__to_json("chapters", chapters, _path)
        
        return chapters
