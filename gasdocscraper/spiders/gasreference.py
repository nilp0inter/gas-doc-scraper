import re

import scrapy


fnregex = re.compile('(?P<name>[a-zA-Z_][a-zA-Z_0-9]*)\((?P<params>[^)]*)\)')


def get_function_info(s):
    if (match := fnregex.match(s)) is not None:
        r = match.groupdict()
        return (r['name'], [p.strip() for p in r['params'].split(',') if p])


def get_methods(response):
    cells = response.xpath('//table[contains(@class, "function") and contains(@class, "members") ]//td')
    col1, col2, col3 = cells[::3], cells[1::3], cells[2::3]
    methods_with_parnames = col1.xpath('./code/a/text()')
    methods_with_partypes = col1.xpath('./code/a/@href')
    returns = col2.xpath('./code//text()')
    descriptions = col3
    for mpn, mpt, r, ds in zip(methods_with_parnames,
                               methods_with_partypes,
                               returns,
                               descriptions):
        method_with_parnames = mpn.extract()
        method_with_partypes = mpt.extract()

        # Because it's an anchor
        method_with_partypes = method_with_partypes[method_with_partypes.index('#')+1:]

        fname, par_names = get_function_info(method_with_parnames)
        _, par_types = get_function_info(method_with_partypes)

        r = r.extract()
        d = ''.join(ds.xpath('.//text()').extract())
        yield {'name': fname,
               'parameters': [{'name': p[0], 'type': p[1]}
                              for p in zip(par_names, par_types)],
               'result': r,
               'description': d}


def get_properties(response):
    cells = response.xpath('//table[contains(@class, "property") and contains(@class, "members") ]//td')
    col1, col2, col3 = cells[::3], cells[1::3], cells[2::3]
    properties = col1.xpath('./code')
    types = col2.xpath('./code')
    descriptions = col3
    for ps, t, ds in zip(properties, types, descriptions):
        p = ''.join(ps.xpath('.//text()').extract())
        d = ''.join(ds.xpath('.//text()').extract())
        yield {'name': p,
               'type': ''.join(t.xpath('.//text()').extract()),
               'url': t.xpath('.//a/@href').extract_first() or "",
               'description': d}


class GasreferenceSpider(scrapy.Spider):
    name = 'gasreference'
    allowed_domains = ['developers.google.com']
    # start_urls = ['https://developers.google.com/apps-script/reference/document/element']
    start_urls = ['https://developers.google.com/apps-script/reference/document/attribute']

    def parse(self, response):
        gt = dict()
        gt['url'] = response.request.url
        gt['name'] = response.xpath('//span[@itemprop="name"]/text()').get()
        gt['type'] = response.xpath('//h1[contains(@class, "devsite-page-title")]/text()').get().lower().split()[0]
        gt['methods'] = list(get_methods(response))
        gt['properties'] = list(get_properties(response))
        yield gt

        links = response.xpath('//a[contains(@href, "apps-script/reference/")]/@href').extract()
        for l in links:
            yield scrapy.Request(response.urljoin(l))
