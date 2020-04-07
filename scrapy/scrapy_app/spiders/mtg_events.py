import scrapy

class MtgEvents(scrapy.Spider):
    name = "mtg_event"
    event_list = []

    def start_requests(self):
        archetype_file = open("deck_archetype.txt", "r")
        archetypes = archetype_file.readlines()
        urls = []
        for archetype in archetypes:
            urls.append(archetype)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        self.write_to_file(self.event_list)
    
    def parse(self, response):
        xpath_string = "/html/body/div[3]/div/table"
        item = response.xpath(xpath_string)
        cont = str(item.extract())
        cont = cont.split('event?e=')
        events = [event[:5] for event in cont[1:]] #get the archetype ID 
        event_dict = dict.fromkeys(self.event_list)
        event_dict.update(dict.fromkeys(events))
        self.event_list = list(event_dict)

    
    def write_to_file(self, events):
        with open('deck_events.txt','a') as f:
            contents = '\n'.join(['http://mtgtop8.com/events?e='+e+'&f=ST' for e in events])
            f.write(contents)