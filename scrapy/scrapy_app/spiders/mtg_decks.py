import scrapy

class MtgDecks(scrapy.Spider):
    name = "mtg_deck"

    def start_requests(self):
        event_file = open("deck_events.txt", "r")
        events = event_file.readlines()
        urls = []
        for event in events:
            urls.append(event)

        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse)