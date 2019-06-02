import scrapy
import json
import time
from scrapy.spiders import CrawlSpider


class LinkCheckerSpider(CrawlSpider):
    name = 'link_checker'
    domain = 'https://rankedboost.com/league-of-legends/counter/'
    json_file = 'championsStats.json'
    json_data = open(json_file)
    dataset = json.load(json_data)
    
    def start_requests(self):
        for data in self.dataset:            
            championId = data['id']
            # file = open("counters.txt", 'a')
            # file.write('----------------------------')
            # file.write(championName.upper() + '\r\n')
            # file.close()
            request = scrapy.Request(url = self.domain + data['localized_name'].lower(),callback = self.parse)
            request.meta['championId'] = championId
            yield request

    def parse(self, response):
        a_selectors = response.css("#weak-against p.RecommendedCounterName::text").extract()        
        championId = response.meta['championId']
        # Loop on each tag
        # print(a_selectors)
        fileCreation = open('counters/' + championId + ".txt", 'w+')
        fileCreation.close()
        file = open('counters/' + championId + ".txt", 'a')
        for selector in a_selectors:            
            file.write(selector + '\r\n')            
        file.close()    