"""
A module that contains multiple CSS stylesheets for use in HTML documents.

Has the following classes:
- SemanticCSS
    - Useful for adding semantic CSS stylesheets to HTML documents.
    
Credit to https://github.com/troxler/awesome-css-frameworks for the list of CSS 
frameworks.
"""
from typing import Literal

from rapidhtml.tags import Link

class SemanticCSS:
    @classmethod
    def mvp(self) -> Link:
        """A minimalist stylesheet for HTML elements
        
        https://andybrewer.github.io/mvp/

        Returns:
            Link: A link tag that points to the MVP.css stylesheet.
        """
        return Link(rel="stylesheet", href="https://unpkg.com/mvp.css")
    
    @classmethod
    def sakura(self, flavour: Literal["dark-solarized", "dark", "earthly", "ink", "pink", "radical", "vader"] = None) -> Link:
        """A minimal classless css framework
        
        Args:
            flavour (Literal[
                    "dark-solarized", 
                    "dark", 
                    "earthly", 
                    "ink", 
                    "pink", 
                    "radical",
                    "vader"
                    ], optional): 
                The flavour of the Sakura CSS framework. Defaults to None.
        
        https://oxal.org/projects/sakura/

        Returns:
            Link: A link tag that points to the Sakura.css stylesheet.
        """
        if flavour:
            return Link(rel="stylesheet", href=f"https://unpkg.com/sakura.css/css/sakura-{flavour}.css")
        return Link(rel="stylesheet", href="https://unpkg.com/sakura.css/css/sakura.css")
    
    @classmethod
    def simple(self) -> Link:
        return Link(rel="stylesheet", href="https://cdn.simplecss.org/simple.min.css")
    
    @classmethod
    def tacit(self) -> Link:
        return Link(rel="stylesheet", href="https://cdn.jsdelivr.net/gh/yegor256/tacit@gh-pages/tacit-css-1.8.1.min.css")
    
    @classmethod
    def pico(self) -> Link:
        return Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")

