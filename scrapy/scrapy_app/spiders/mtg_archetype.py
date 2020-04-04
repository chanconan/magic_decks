import scrapy

class MtgArchetypeSpider(scrapy.Spider):
    name = "mtg_archetype"

    def start_requests(self):
        urls = ['http://mtgtop8.com/format?f=ST']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # Extracts all the HTML information beneath Meta Breakdown from the homepage for standard MTG decks.
    # Generate a file for all of the deck archetypes in different Spider to crawl
    def parse(self, response):
        xpath_string = '/html/body/div[3]/div/table' 
        item = response.xpath(xpath_string)
        cont = str(item.extract())
        cont = cont.split('archetype?a=')
        archetypes = [arch[:3] for arch in cont[1:]] #get the archetype ID 
        with open('deck_archetype.txt','w') as f:
            contents = '\n'.join(['http://mtgtop8.com/archetype?a='+a+'&meta=52&f=ST' for a in archetypes])
            f.write(contents)