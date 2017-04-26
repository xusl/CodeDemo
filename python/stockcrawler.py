# This scripts shows how to crawl a site without settings up a complete project.
#
# Note: the `crawler.start()` can't be called more than once due twisted's reactor limitation.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Rolando Espinoza La fuente
#
# Changelog:
#     24/07/2011 - updated to work with scrapy 13.0dev
#     25/08/2010 - initial version. works with scrapy 0.9

from scrapy.contrib.loader import XPathItemLoader
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.crawler import Crawler
from scrapy import log, signals
from twisted.internet import reactor
class QuestionItem(Item):
    """Our SO Question Item"""
    title = Field()
    summary = Field()
    tags = Field()

    user = Field()
    posted = Field()

    votes = Field()
    answers = Field()
    views = Field()


class MySpider(CrawlSpider):
    """Our ad-hoc spider"""
    name = "myspider"
    start_urls = ["http://stackoverflow.com/"]
    allowed_domains = ["stackoverflow.com"]

    question_list_xpath = '//div[@id="content"]//div[contains(@class, "question-summary")]'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        self.log( "parse %s \n %s xxxxxxxxxxx" %( response.url, "*" *78))

        for qxs in hxs.select(self.question_list_xpath):
            loader = XPathItemLoader(QuestionItem(), selector=qxs)
            loader.add_xpath('title', './/h3/a/text()')
            loader.add_xpath('summary', './/h3/a/@title')
            loader.add_xpath('tags', './/a[@rel="tag"]/text()')
            loader.add_xpath('user', './/div[@class="started"]/a[2]/text()')
            loader.add_xpath('posted', './/div[@class="started"]/a[1]/span/@title')
            loader.add_xpath('votes', './/div[@class="votes"]/div[1]/text()')
            loader.add_xpath('answers', './/div[contains(@class, "answered")]/div[1]/text()')
            loader.add_xpath('views', './/div[@class="views"]/div[1]/text()')

            yield loader.load_item()

SPIDER = MySpider()

crawler_num = 0
def spider_finished():
    global crawler_num
    print "spider finished =================================="
    crawler_num -= 1
    if crawler_num <= 0:
        reactor.stop()

def main():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    def catch_item(sender, item, **kwargs):
        print "Got:", item

    #dispatcher.connect(catch_item, signal=signals.item_passed)

    from scrapy.utils.project import get_project_settings
    settings = get_project_settings()
    # shut off log
    settings.set('LOG_ENABLED', True)

    # set up crawler
    crawler = Crawler(settings)
    crawler.configure()

    # schedule spider
    crawler.crawl(MySpider())
    crawler.signals.connect(spider_finished, signal=signals.spider_closed)

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print "ENGINE STOPPED"


if __name__ == '__main__':
    main()
    log.start(None, "DEBUG")
    reactor.run()

# Snippet imported from snippets.scrapy.org (which no longer works)
# author: darkrho
# date  : Aug 25, 2010

