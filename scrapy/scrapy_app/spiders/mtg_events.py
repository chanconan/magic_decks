import scrapy

class MtgEvents(scrapy.Spider):
    name = "mtg_event"

    def start_requests(self):
        archetype_file = open("deck_archetype.txt", "r")
        archetypes = archetype_file.readlines()
        urls = ["http://mtgtop8.com/archetype?a=12&&meta=52&f=ST"]
        # for archetype in archetypes:
        #     urls.append(archetype)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        xpath_string = "/html/body/div[3]/div/table"
        item = response.xpath(xpath_string)
        cont = str(item.extract())
        cont = cont.split('event?e=')
        events = [event[:5] for event in cont[1:]] #get the archetype ID 
        with open('deck_events.txt','w') as f:
            contents = '\n'.join(['http://mtgtop8.com/events?e='+e+'&f=ST' for e in events])
            f.write(contents)