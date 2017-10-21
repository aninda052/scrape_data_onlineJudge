# -*- coding: utf-8 -*-
import scrapy



count = 1
problems =set ()

class UvaSpidySpider(scrapy.Spider):
    name = 'uva_spidy'
    allowed_domains = ['uva.onlinejudge.org']
    start_urls = ['https://uva.onlinejudge.org//']
    next_url = 'https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=9'
    file = open("uva_solve_list.txt","a")
    

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'username': '***', 'passwd': '***'} ,
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        print ('yahoo',':D'*10)
        yield scrapy.Request(self.next_url,callback = self.submission_page)


    def submission_page(self,response):

        global count ,problems
        tabs = response.css('table')
        subs=tabs[2].css('tr')
        for sub in subs:
            tmp = sub.css('td')
            prb_id = str(tmp[1].css('a::text').extract_first())
            if tmp[3].css('::text').extract_first() == 'Accepted' and prb_id not in problems :
                name = tmp[2].css('a::text').extract_first()
                line = '{}.  '.format(count) +  prb_id +' - ' + name + '\n'
                self.file.write(line)
                count += 1
                problems.add(prb_id)

    	# checking for next page 
    	nxt = tabs[3].css('tr')[0].css('a')
    	tmp = nxt[len(nxt)-2].css('::text').re('(\S*)')
    	if tmp[0] == 'Next' :
    		yield scrapy.Request(nxt[len(nxt)-2].css('::attr(href)').extract_first(),callback = self.submission_page)
    	else :
    		self.file.close()

