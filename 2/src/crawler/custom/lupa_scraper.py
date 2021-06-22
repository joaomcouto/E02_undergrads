from selenium.webdriver.common.by import By
from datetime import datetime

from crawler.custom_scraper import CustomScraper


class LupaScraper(CustomScraper):

    def __init__(self):
        super(LupaScraper, self).__init__()

    def get_title(self):
        try:
            title = self.wrapper.find_element(By.XPATH, "//h2[@class='bloco-title']").text
        except:
            raise Exception('Has no title.')
        return title

    def get_subtitle(self):
        return ''

    def get_date(self):
        """
        Treat date found on Lupa's website
        example: "07.dez.2015 | 15h22"
        """
        try:
            date = self.wrapper.find_element(By.XPATH, "//div[@class='bloco-meta']").text.lower()
            lupa_date_time = date.split('|')
            lupa_time = lupa_date_time[1].split('h')
            lupa_date = lupa_date_time[0].split('.')
            mapper = {
                    'jan': 1,
                    'fev': 2,
                    'mar': 3,
                    'abr': 4,
                    'maio': 5,
                    'jun': 6,
                    'jul': 7,
                    'ago': 8,
                    'set': 9,
                    'out': 10,
                    'nov': 11,
                    'dez': 12
                }
            return datetime(
                year=int(lupa_date[2]),
                month=mapper[lupa_date[1]],
                day=int(lupa_date[0]),
                hour=int(lupa_time[0]),
                minute=int(lupa_time[1])
                )
        except:
            raise Exception('Has no Date.')

    def get_authors(self):
        try:
            authors = []
            authors_elements = self.wrapper.find_elements(By.XPATH, "//div[@class='bloco-autor']/span/strong/a")
            for author_element in authors_elements:
                authors.append(author_element.text)
            return authors
        except:
            return []

    def get_text(self, year):
        try:
            post_inner_element = self.wrapper.find_element(By.CLASS_NAME, 'post-inner')
            text_list = post_inner_element.find_elements(By.TAG_NAME, 'p')
            # Remove Notes added at the bottom of the texts after 2018
            if year > 2018:
                text_list = text_list[:-1]
            text_list = [v.text for v in text_list]
            text = '\n'.join(text_list)
            return text
        except:
            return ''

    def get_categories(self):
        return []

    def get_tags(self):
        try:
            tags = []
            tag_elements = self.wrapper.find_elements(By.XPATH, "//h4//following-sibling::ul[1]//li")
            for tag_element in tag_elements:
                tags.append(tag_element.text)
            return tags
        except:
            return []

    def get_veredicts(self):
        veredicts = []
        try:
            elements_with_veredicts = self.wrapper.find_elements(By.XPATH, "//div[@class='post-inner']/div[contains(@class, 'etiqueta')]")
            for veredict_element in elements_with_veredicts:
                veredicts.append(veredict_element.text)
            if len(veredicts) == 0:
                raise
        except:
            elements_with_veredicts = self.wrapper.find_elements(By.XPATH, "//div[@class='post-inner']//img[contains(@alt, 'RECORTES-POSTS')]")
            for veredict_element in elements_with_veredicts:
                veredicts.append(veredict_element.get_attribute('alt')[15:])

        if not veredicts:
            raise Exception('Has no veredict.')
        return veredicts

    def get_image(self):
        try:
            image = self.driver.find_element(By.CLASS_NAME, 'single-post-cover-image').find_element(By.TAG_NAME, 'img').get_attribute('srcset')
            return image
        except:
            return ''

    def get_video(self):
        return ''

    def get_html(self):
        try:
            return self.driver.page_source
        except:
            raise Exception('Problem on loading HTML to be saved on file.')


    def execute(self, url):
        try_cnt = 0
        last_exception = None
        while try_cnt < self.try_rate:
            try:
                self.driver.get(url)
                self.wrapper = self.driver.find_element(By.CLASS_NAME, 'main-content')
                self.verify_content_type()
                date = self.get_date()
                result = {
                    'url': url,
                    'source_name': 'lupa',
                    'title':  self.get_title(),
                    'subtitle': self.get_subtitle(),
                    'publication_date': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'text_news': self.get_text(date.year),
                    'image_link': self.get_image(),
                    'video_link': self.get_video(),
                    'authors': self.get_authors(),
                    'categories': self.get_categories(),
                    'tags': self.get_tags(),
                    'obtained_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    'rating': self.get_veredicts(),
                    'raw_file_name': self.get_html_file_value(url)
                    }
                return date.year, date.month, result, self.get_html()
            except Exception as e:
                # If not CHECAGEM type stop iteration:
                if 'only accepts CHECAGEM type' in str(e):
                    raise e
                # Selenium exception:
                else:
                    try_cnt += 1
                    last_exception = e
        raise last_exception

    def verify_content_type(self):
        """
        This scraper only works on CHECAGEM type or absence of type
        """
        other_content_types = [
            'análise',
            'artigo',
            'institucional',
            'podcast',
            'reportagem',
            'vídeos']
        try:
            content_type = self.wrapper.find_element(By.XPATH, "//div[contains(@class, 'post-tags')]/ul[1]/li/a").text
        except:
            content_type = ''

        if content_type.lower() in other_content_types:
            raise ValueError(f'{content_type} is not a valid content type, only accepts CHECAGEM type')
