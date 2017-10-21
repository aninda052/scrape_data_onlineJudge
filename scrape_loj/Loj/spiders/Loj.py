# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


count = 1

class LojSpider(scrapy.Spider):
    name = 'Loj'
    allowed_domains = ['lightoj.com']
    start_urls = ['http://lightoj.com/login_main.php']
    next_url = 'http://lightoj.com/volume_usersubmissions.php'
    loj_file = open("loj_solve_list.txt","a")

    def parse(self, response) :
        return scrapy.FormRequest.from_response(
            response,
            formdata={'myuserid': '***', 'mypassword': '***'},
            callback=self.after_login
        )
        self.loj_file.close()


    def after_login(self, response):
    	# check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        print ('yahoo',':D'*20)
        yield scrapy.Request(self.next_url,callback = self.all_submissions )


    def all_submissions(self,response):
    	return scrapy.FormRequest.from_response(
            response,
            formdata={'user_password': '***'},
            callback = self.final_page
        )


    def final_page(self, response):
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        rows = response.css('#mytable3 tr')
        for row in rows[1:] :
        	tmp = row.css('div::text').re('A.*d')
        	if (len(tmp)) :
        		tmp1 = row.css('th [href]').re('href="(\S*)"')
        		yield response.follow((tmp1[0]),callback = self.final_code)
        


    def final_code(self,response):
    	global count 
    	soup = BeautifulSoup(response.text,'html5lib')
    	code = soup.find('textarea').text
    	name = soup.find('table' , id='mytable3').find_all('tr')[1].find_all('td')[2].text.strip()
    	file =open('{}'.format(name)+'.cpp','w')
    	file.write(code)
    	file.close()
    	line ='{}.   '.format(count) + name + '\n'
    	self.loj_file.write(line)
    	count += 1

    	




        
        

