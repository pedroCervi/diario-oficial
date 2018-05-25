# -*- coding: utf-8 -*-
from dateparser import parse
from urllib.parse import quote_plus
import datetime as dt
import json
import scrapy
import requests

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

MONTHS = {

}

class DfBrasiliaSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '5300108'
    name = 'df_brasilia'
    allowed_domains = ['dodf.df.gov.br']
    main_url = 'http://dodf.df.gov.br/listar'

    def parse(self, response):
        years = response.css('.nome::text').extract()

        for year in years:
            response = requests.get(main_url + '?dir=' + year)
            months = [month for month in response.json()['data']]

            for month in months:
                response = requests.get(main_url + '?dir=' + year + '/' + month)
                days = [day_folder for day_id, day_folder in response.json()['data'].items()]

                for day in days:
                    url = main_url + '?dir=' + year + '/' + month + '/' + day
                    yield scrapy.Request(url, self.parse_document)

    def parse_document(self, response):
        pdfs = [pdf for pdf in response.json()['data']]

        path = response.json()['dir']
        parsed_date = re.compile(r".+\/DODF [0-9]+ ([0-9]{2}-[0-9]{2}-[0-9]{4})$").match(path).group(1);
        date = dateparser.parse(parsed_date)

        for pdf in pdfs:
            url = main_url + '?dir=' + quote_plus(pdf)

            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                scraped_at=dt.datetime.utcnow(),
                power='executive_legislative'
            )










# start_urls[0] + '#' + folder_year + '/' + folder_month + 'DODF 016 23-01-2018'
# 'http://dodf.df.gov.br/listar#2018/01_Janeiro/DODF%20016%2023-01-2018'
#                                              'DODF%20016%2023-01-2018'
# 'http://dodf.df.gov.br/listar#2018/01_Janeiro/DODF%20008%2031-01-2018%20EDICAO%20EXTRA'
