from selenium.webdriver.common.by import By
from datetime import datetime
import pytesseract
from PIL import Image
from urllib.request import urlopen
import re

from COLETORES.IMPLEMENTADOS.CHECAGENS.custom_scraper import CustomScraper


class BoatosScraper(CustomScraper):

    def __init__(self):
        super(BoatosScraper, self).__init__()
        self.source = 'BOATOS'

    def get_title(self):
        try:
            title = self.wrapper.find_element(By.CLASS_NAME, 'entry-title').text
        except:
            raise Exception('Has no title.')
        return title

    def get_subtitle(self):
        try:
            subtitle = self.wrapper.find_element(By.XPATH, "//p[1]/strong").text
        except:
            subtitle = ''
        return subtitle

    def get_date(self):
        """
        Treat date found on boato's website
        example: "2016-08-17T01:31:14-03:00"
        Therefore, date already comes in ISO 8601 format
        """
        try:
            boatos_datetime = self.wrapper.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
            boatos_date, boatos_time = boatos_datetime.replace('-03:00', '').split('T')
            hour, minute, seconds = boatos_time.split(':')
            year, month, day = boatos_date.split('-')
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
            # Not one factchecking found with more than one author:
            authors = [self.wrapper.find_element(By.CSS_SELECTOR, '.author > a').text]
            return authors
        except:
            return []

    def get_text(self, subtitle):
        try:
            text_parts_candidates = self.wrapper.find_elements(By.XPATH, "//*[local-name()='p' or local-name()='h2']")
            # Remove empty text parts
            text_parts = []
            import re
            for text_part in text_parts_candidates:
                if re.search('[a-zA-Z]', text_part.text):
                    text_parts.append(text_part)
            # Remove subtitle if appears
            if subtitle != '':
                # Removes first part
                text_parts.pop(0)
            text = ''
            for text_part in text_parts:
                text += text_part.text
            return text
        except:
            return ''

    def get_categories(self):
        try:
            category = self.wrapper.find_elements(By.CSS_SELECTOR, '.cat-links > a')[-1].text
        except:
            category = ''
        return category

    def get_tags(self, img):
        tags = []
        if img != '':
            # Get words from image
            tag_condensed = pytesseract.image_to_string(Image.open(urlopen(img)))
            # Remove stamp
            tag_condensed = tag_condensed.split('\nBoatos')[0]
            tag_condensed_treated = tag_condensed.replace('\n','').replace(' ', '').replace('\x0c', '')
            tags_candidates = tag_condensed_treated.split('#')
            for tag_candidate in tags_candidates:
                # Remove empty candidates
                if re.search('[a-zA-Z]', tag_candidate):
                    tags.append(tag_candidate)
        return tags

    def get_veredicts(self, tags, subtitle, title):
        """
        Verdicts are vereified on tags, subtitle or title, in that order.
        """
        veredicts = []
        if len(tags) >= 1:
            if 'boato' in tags[0].lower():
                veredicts.append('boato')
        elif subtitle != '':
            if 'boato' in subtitle.lower():
                veredicts.append('boato')
        elif 'boato' in title.lower():
            veredicts.append('boato')
        # Verify for empty veredicts
        if not veredicts:
            raise Exception('Has no veredict.')
        return veredicts

    def get_image(self):
        try:
            img_class = self.wrapper.find_element(By.CLASS_NAME, 'featured-image')
            img_tag = img_class.find_element(By.TAG_NAME, 'img')
            img = img_tag.get_attribute('src')
        except:
            img = ''
        return img

    def get_video(self):
        try:
            video_tag_candidate = self.wrapper.find_element(By.XPATH, "//iframe[@allowfullscreen='allowfullscreen']")
            video_src_candidate = video_tag_candidate.get_attribute('src')
            if 'youtube' in video_src_candidate:
                video = video_src_candidate
            else:
                video = ''
        except:
            video = ''
        return video

    def get_html(self):
        try:
            return self.driver.page_source
        except:
            raise Exception('Problem on loading HTML to be saved on file.')

    def execute(self, url):
        # Execute scraper
        try_cnt = 0
        last_exception = None
        not_finished = True
        while try_cnt < self.try_rate and not_finished:
            try:
                self.driver.get(url)
                self.wrapper = self.driver.find_element(By.ID, 'content')
                date = self.get_date()
                # On this class order matters
                img = self.get_image()
                tags = self.get_tags(img)
                subtitle = self.get_subtitle()
                text = self.get_text(subtitle)
                title = self.get_title()
                veredicts = self.get_veredicts(tags, subtitle, title)
                result = {
                    'url': url,
                    'source_name': 'boatos',
                    'title':  title,
                    'subtitle': subtitle,
                    'publication_date': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'text_news': text,
                    'image_link': img,
                    'video_link': self.get_video(),
                    'authors': self.get_authors(),
                    'categories': self.get_categories(),
                    'tags': tags,
                    'obtained_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    'rating': veredicts,
                    'raw_file_name': self.get_html_file_value(url)
                    }
                # Insert collected data into database
                self.insert(
                    type='checking',
                    collected_data=result,
                    html=self.get_html(),
                    year=date.year,
                    month=date.month
                    )
                not_finished = False
            except Exception as e:
                try_cnt += 1
                last_exception = e

            if not_finished:
                # If a exception is raised during the research, the Exception
                # is saved with the url as keY.
                self.insert(
                    type='error',
                    collected_data={url: str(last_exception)}
                    )
