import re
import scrapy
from urllib.parse import urljoin
from scrapy.selector import Selector


class NbaLinksSpider(scrapy.Spider):
	name = "nba_links"

	start_urls = [
	"https://www.basketball-reference.com/players/"
	]

	def parse(self,response):
		
		with_comment = response.css("div#all_alphabet.section_wrapper.alphabet").get()
		selector = Selector(text=with_comment, type="html")
		regex = re.compile(r"<!--(.*)-->", re.DOTALL)
		comment = selector.xpath('//comment()').re(regex)[0]
		comment_selector = Selector(text=comment, type="html")

		extensions = comment_selector.css('li a::attr(href)').getall()
		for ext in extensions:
			url = urljoin('https://www.basketball-reference.com/',ext)
			yield scrapy.Request(url, callback=self.parse_players)

		
	def parse_players(self,response):
		p_extensions = response.xpath('//*[@data-stat="player"]/a/@href').getall()
		for p_ext in p_extensions:
			url = urljoin('https://www.basketball-reference.com/',p_ext)
			yield scrapy.Request(url, callback=self.parse_season)

	def parse_season(self,response):
		s_extensions = response.xpath('//*[@data-stat="season"]/a/@href').getall()
		for s_ext in s_extensions:
			url = urljoin('https://www.basketball-reference.com/',s_ext)
			yield scrapy.Request(url, callback=self.parse_games)

	def parse_games(self,response):
		table = response.xpath("//div[@id='div_pgl_basic']/table/tbody/tr[contains(@id,'pgl_basic')]")
		player_name = response.css('div.nothumb').css('p').css('strong strong::text').get()
		name_verif = response.css('h1[itemprop="name"]::text').get()
		#response.xpath('//div[@id="meta"]/div[@class="nothumb"]/p/strong/strong/text()').get()
		#response.css('h1[itemprop="name"]::text').get()

		for items in table:
			yield {
				'name': player_name,
				'name_verif': name_verif,
				'game_date': items.css('td[data-stat="date_game"] a::text').get(),
				'team': items.css('td[data-stat="team_id"] a::text').get(),
				'opp': items.css('td[data-stat="opp_id"] a::text').get(),
				'game_location': items.css('td[data-stat = "game_location"]::text').get(),
				'game_result': items.css('td[data-stat = "game_result"]::text').get(),
				'game_started': items.css('td[data-stat = "game_started"]::text').get(),
				'minutes_played': items.css('td[data-stat = "mp"]::text').get(),
				'field_goals_made': items.css('td[data-stat = "fg"]::text').get(),
				'field_goals_attempted': items.css('td[data-stat = "fga"]::text').get(),
				'fg_pct': items.css('td[data-stat = "fg_pct"]::text').get(),
				'3p_made': items.css('td[data-stat = "fg3"]::text').get(),
				'3p_attempts': items.css('td[data-stat = "fg3a"]::text').get(),
				'3p_pct': items.css('td[data-stat = "fg3_pct"]::text').get(),
				'freethrows_made': items.css('td[data-stat = "ft"]::text').get(),
				'freethrows_attempted': items.css('td[data-stat = "fta"]::text').get(),
				'ft_pct': items.css('td[data-stat = "ft_pct"]::text').get(),
				'off_reb': items.css('td[data-stat = "orb"]::text').get(),
				'def_reb': items.css('td[data-stat = "drb"]::text').get(),
				'tot_reb': items.css('td[data-stat = "trb"]::text').get(),
				'assists': items.css('td[data-stat = "ast"]::text').get(),
				'steals': items.css('td[data-stat = "stl"]::text').get(),
				'blocks': items.css('td[data-stat = "blk"]::text').get(),
				'turnovers': items.css('td[data-stat = "tov"]::text').get(),
				'points': items.css('td[data-stat = "pts"]::text').get()

			}