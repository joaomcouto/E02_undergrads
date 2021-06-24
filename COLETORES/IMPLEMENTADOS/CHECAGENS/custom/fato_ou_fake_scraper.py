from selenium.webdriver.common.by import By
from datetime import datetime
import time

from crawler.custom_scraper import CustomScraper


class FatoOuFakeScraper(CustomScraper):

    def __init__(self):
        super(FatoOuFakeScraper, self).__init__()

    def get_title(self):
        try:
            title = self.wrapper.find_element(By.CLASS_NAME, 'title').text
        except:
            raise Exception('Has no title.')
        return title

    def get_subtitle(self):
        try:
            subtitle = self.wrapper.find_element(By.CLASS_NAME, 'subtitle').find_element(By.TAG_NAME, 'h2').text
        except:
            subtitle = ''
        return subtitle

    def get_date(self):
        """
        Treat date found on fato-ou-fake's website
        example: "16/09/2020 17h48"
        """
        try:
            date = self.wrapper.find_element(By.TAG_NAME, 'time').text
            fato_ou_fake_date_time = date.split(' ')
            hour, minute = fato_ou_fake_date_time[1].split('h')
            day, month, year = fato_ou_fake_date_time[0].split('/')
            return datetime(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minute=int(minute)
                )
        except:
            raise Exception('Has no Date.')

    def get_authors(self):
        try:
            authors_raw = self.wrapper.find_element(By.CLASS_NAME, 'content-publication-data__from').get_attribute('title')
            authors_splitted_e = authors_raw.split(' e ')
            authors = authors_splitted_e[0].split(', ')
            if len(authors_splitted_e) > 1:
                authors.append(authors_splitted_e[1])
            return authors
        except:
            return []

    def get_text(self, year):
        try:
            text_parts = self.wrapper.find_elements(By.CLASS_NAME, 'content-text')
            text = ''
            for text_part in text_parts:
                text += text_part.text
            return text
        except:
            return ''

    def get_categories(self):
        try:
            category = self.driver.find_element(By.CLASS_NAME, 'area-subeditoria').text
        except:
            category = ''
        return category

    def get_tags(self):
        return []

    def get_veredicts(self):
        """
        Verdicts are arranged as images on the page.
        """
        veredicts = []
        veredicts_images_candidates = []
        # Get img tags
        try:
            veredicts_images_candidates = self.wrapper.find_elements(By.TAG_NAME, 'img')
        except:
            raise Exception('Has no veredict.')
        # Get Veredicts
        for candidate in veredicts_images_candidates:
            try:
                candidate_src = candidate.get_attribute('src')
                # Verify fake image
                if candidate_src == 'https://s2.glbimg.com/o9tqwzdNCBentLDOcpGb1C4CxfE=/0x0:1600x400/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2020/e/b/ImkcwXR0KMZarxAHzZIw/header-materia-fato-ou-fake.jpg':
                    veredicts.append('fake')
                # Verify veredict on src of image
                elif 'selo-' in candidate_src:
                    veredict = candidate_src.split('selo-')[1][:-4] #get final part and remove '.jpg'
                    veredict = ''.join([i for i in veredict if not i.isdigit()]) # removing numbers
                    veredict = veredict.replace('-', ' ')
                    veredicts.append(veredict)
                elif candidate_src == 'https://s2.glbimg.com/aen-sBxMZXDC1jKHjRcgvXW-PxM=/0x0:1600x267/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2018/q/N/CDZclxR4OGnIQYJwYgmA/selo-fato.jpg':
                    veredicts.append('fato')
            except:
                pass
        # Verify for empty veredicts
        if not veredicts:
            raise Exception('Has no veredict.')
        return veredicts

    def get_image(self):
        not_main_images = [
                # Fato ou fake image
                "https://s2.glbimg.com/AoiHBQDVMc2LywJhO-skTe93DFk=/0x0:1600x407/924x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2018/T/j/hXh7qjRFuJBlEq11hNvg/fato-ou-fake-header.png",
                # Fato image:
                "https://s2.glbimg.com/kpYDMp4va2acwZ1HZwnu6Nu_Wtg=/0x0:1600x267/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2019/r/x/NcVillTuyBA8k2kn6G3A/selo-fake.jpg",
                # Fake image
                "'https://s2.glbimg.com/o9tqwzdNCBentLDOcpGb1C4CxfE=/0x0:1600x400/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2020/e/b/ImkcwXR0KMZarxAHzZIw/header-materia-fato-ou-fake.jpg'"
            ]
        img = ''
        try:
            img_parent = self.wrapper.find_element(By.CLASS_NAME, 'content-featured-image')
            img = img_parent.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except:
            return ''
        # Logic for 2019:
        if img in not_main_images:
            try:
                main_images_candidates = self.wrapper.find_elements(By.TAG_NAME, 'img')
                for candidate in main_images_candidates:
                    img_src = candidate.get_attribute('src')
                    if img_src not in not_main_images:
                        img = img_src
                        break
            except:
                pass
        return img

    def get_video(self):
        try:
            video = self.wrapper.find_element(By.XPATH, "//div[contains(@class, 'block-youtube')]/iframe").get_attribute('src')
        except:
            video = ''
        return video

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
                time.sleep(3)
                self.slowly_scroll_down_page()
                self.wrapper = self.driver.find_element(By.TAG_NAME, 'main')
                date = self.get_date()
                result = {
                    'url': url,
                    'source_name': 'fato-ou-fake',
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
                # Adds to the count of attempts:
                try_cnt += 1
                last_exception = e
        raise last_exception

    def slowly_scroll_down_page(self):
        """
        Scroll slowly down the page to load all the content
        """
        try:
            page_scroll_height = 1000
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            for timer in range(0,50):
                self.driver.execute_script("window.scrollTo(0, "+str(page_scroll_height)+")")
                if page_scroll_height % 1000 >= page_height % 1000:
                    break
                page_scroll_height += 1000
                time.sleep(.8)
        except:
            raise Exception('Unable to slowly scroll down the page.')
