# -*- coding: utf-8 -*-
# filename: crawler.py

#import sqlite3
import urllib.request, urllib.error, urllib.parse  
from html.parser import HTMLParser  
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from browseapp.models import MaterialWebProcesado

class HREFParser(HTMLParser):  
    """
    Parser that extracts hrefs
    """
    hrefs = set()
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            dict_attrs = dict(attrs)
            if dict_attrs.get('href'):
                self.hrefs.add(dict_attrs['href'])


def get_local_links(html, domain, current_path):  
    """
    Read through HTML content and returns a tuple of links
    internal to the given domain
    """
    hrefs = set()
    parser = HREFParser()
    parser.feed(html)
    for href in parser.hrefs:
        u_parse = urlparse(href)
        if href.startswith('/'):
            # purposefully using path, no query, no hash
            hrefs.add(u_parse.path)
        # only keep the local urls
        elif u_parse.netloc == domain:
            hrefs.add(u_parse.path)
        else:
            if len(u_parse.netloc)==0:
                hrefs.add('/'.join(current_path.split('/')[:-1])+'/'+u_parse.path)
    return hrefs

class CrawlerCache(object):
    """
    Filtra el texto desde el objeto BeautiFulSoup4 'dirty_soup'
    """
    def clean(self, dirty_soup):
        for script in dirty_soup(["script", "style", "head", "a"]):
            script.extract()
        texto_filtrado = dirty_soup.get_text()
        lines = (line.strip() for line in texto_filtrado.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        texto_filtrado = '\n'.join(chunk for chunk in chunks if chunk)
        return texto_filtrado
    """
    Crawler data caching per relative URL and domain.
    """
    def set(self, domain, url, data):
        """
        store the content for a given domain and relative url
        """
        if not MaterialWebProcesado.objects.filter(dominio=domain, url=url):
            soup = BeautifulSoup(data, 'html.parser', )
            title = soup.find("title").string
            #language = soup.find("html")['lang']
            contenido = self.clean(soup)
            nuevo = MaterialWebProcesado(dominio=domain, url=url, titulo=title, idioma='', tipo_aprendizaje='', contenido=contenido, codigo_fuente=data)
            nuevo.save()

    def get(self, domain, url):
        """
        return the content for a given domain and relative url
        """
        q = MaterialWebProcesado.objects.filter(dominio=domain, url=url)
        if q:
            return q[0]

    def get_urls(self, domain):
        """
        return all the URLS within a domain
        """
        q=MaterialWebProcesado.url.filter(dominio=domain)
        # could use fetchone and yield but I want to release
        # my cursor after the call. I could have create a new cursor tho.
        # ...Oh well
        return [row[0] for row in q]


class Crawler(object):  
    def __init__(self, cache=None, depth=2):
        """
        depth: how many time it will bounce from page one (optional)
        cache: a basic cache controller (optional)
        """
        self.depth = depth
        self.content = {}
        self.cache = cache

    def crawl(self, url, no_cache=None):
        """
        url: where we start crawling, should be a complete URL like
        'http://www.intel.com/news/'
        no_cache: function returning True if the url should be refreshed
        """


        u_parse = urlparse(url)
        self.domain = u_parse.netloc
        self.content[self.domain] = {}
        self.scheme = u_parse.scheme
        self.no_cache = no_cache
        self._crawl([u_parse.path], self.depth)

    def set(self, url, html):
        self.content[self.domain] = html
        if self.is_cacheable(url) and len(html)>0:
            self.cache.set(self.domain, url, html)

    def get(self, url):
        page = None
        if self.is_cacheable(url):
          page = self.cache.get(self.domain, url)
        if page is None:
          page = self.curl(url)
          return page
        else:
          print("URL ya explorada: [%s] %s" % (self.domain, url))
        return page.codigo_fuente
        #return page.codigo_fuente

    def is_cacheable(self, url):
        return self.cache and self.no_cache \
            and not self.no_cache(url)

    def _crawl(self, urls, max_depth):
        n_urls = set()
        if max_depth:
            for url in urls:
                # do not crawl twice the same page
                if url not in self.content.values():
                    html = self.get(url)
                    self.set(url, html)
                    n_urls = n_urls.union(get_local_links(html, self.domain, url))
            self._crawl(n_urls, max_depth-1)


    def curl(self, url):
        """
        return content at url.
        return empty string if response raise an HTTPError (not found, 500...)
        """
        try:
            print("Explorando URL: [%s] %s" % (self.domain, url))
            req = urllib.request.Request('%s://%s%s' % (self.scheme, self.domain, url))
            response = urllib.request.urlopen(req)
            #if len(response.read().decode('ascii', 'ignore'))==0:
            #    return ''
            return response.read().decode('ascii', 'ignore')
        except urllib.error.HTTPError as e:
            print("error [%s] %s: %s" % (self.domain, url, e))
            return ''
