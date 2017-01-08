# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import string

#http://books.toscrape.com/
#scrapy crawl BooksSpider -o books.csv -s LOG_FILE=scrapy.log

### Built a spider using Scrapy to scrape this e-commerce website: http://books.toscrape.com/ into a CSV file.
###
### Required data:
### •Book Name (tip: there are 1000 books)
### •Category
### •Availability (Yes, No)
### •Price (incl. tax)
### •Rating
### •Image URL
### •Description
###
### Upload both your Scrapy project and CSV file to GitHub or even DropBox and send the link to the Q&A secion of this course, or at least screenshots of the project and results.
###
### Note: This task can be done with any other web scraping tool; however, using Scrapy is a must for this practicing project.


class BooksSpider(Spider):

    name = 'BooksSpider'
    allowed_domains = [ 'books.toscrape.com' ]
    start_urls = ( 'http://books.toscrape.com/', )

    def parse(self, response):

        urls = response.xpath('//article [@class="product_pod"]').xpath('.//h3/a/@href').extract()

        for url in urls:
            url_to_get = response.urljoin(url)
            print url_to_get
            yield Request(url_to_get, callback=self.parse_each_page)

        #######################################
        #  Process to next Page, Last Page Stop
        
        next_page = response.xpath('//li [@class="next"]/a/@href').extract()
        
        if next_page != []:
            next_page = response.urljoin(response.xpath('//li [@class="next"]/a/@href').extract()[0])
            print "next_page " + next_page
            yield Request(next_page, callback=self.parse)
        else:
            print "No more pages " + str(next_page)

    def parse_each_page(self, response):

        Title         = response.xpath('//li [@class="active"]/text()').extract()
        Category      = response.xpath('.//li/a/text()').extract()[2]
        table_data    = response.xpath('//table [@class="table table-striped"]/tr/td/text()').extract()
        Availability  = table_data[5]
        Price         = table_data[3]
        Rating        = response.xpath('.//p [contains(@class,"star-rating")]/@class').extract()[0]
        Rating        = Rating.split()[1]
        ImageUrl      = response.xpath('.//img/@src').extract()[0]
        Description   = response.xpath('//p/text()').extract()[10]

        yield { 'Title'        : Title,
                'Category'     : Category,
                'Availability' : Availability,
                'Price'        : Price,
                'Rating'       : Rating,
                'ImageUrl'     : ImageUrl,
                'Description'  : Description, 
              }