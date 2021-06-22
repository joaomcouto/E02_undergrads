from selenium.webdriver.common.by import By
from datetime import datetime

from crawler.custom_scraper import CustomScraper


class AosFatosScraper(CustomScraper):

    def __init__(self):
        super(AosFatosScraper, self).__init__()

    def get_title(self):
        """
        Get title of AosFatos URL.
        """
        title = self.wrapper.find_element(By.TAG_NAME, 'h1').text
        return title

    def get_subtitle(self):
        """
        AosFatos page has no subtitles.
        """
        return ''

    def get_date(self):
        """
        Treat date found on AosFato's website
        example: "11 de maio de 2021, 12h40"
        """

        date = self.wrapper.find_element(By.CLASS_NAME, 'publish_date').text
        aosfatos_date_time = date.split(',')
        aosfatos_time = aosfatos_date_time[1].split('h')
        aosfatos_date = aosfatos_date_time[0].split(' de ')
        mapper = {
                'janeiro': 1,
                'fevereiro': 2,
                'março': 3,
                'abril': 4,
                'maio': 5,
                'junho': 6,
                'julho': 7,
                'agosto': 8,
                'setembro': 9,
                'outubro': 10,
                'novembro': 11,
                'dezembro': 12
            }
        return datetime(
            year=int(aosfatos_date[2]),
            month=mapper[aosfatos_date[1]],
            day=int(aosfatos_date[0]),
            hour=int(aosfatos_time[0]),
            minute=int(aosfatos_time[1])
            )

    def get_authors(self):
        """
        The page either has no author or is arranged in the following format:
        "Por joao dolores, roberto massafera e juliana arrudas coelos"
        """
        try:
            authors = self.wrapper.find_element(By.CLASS_NAME, 'author').text
            authors = authors.replace('Por ', '').replace(',', ' e').split(' e ')
        except:
            authors = ''
        return authors

    def get_text(self, year):
        text_list_raw = self.wrapper.find_elements(By.TAG_NAME, 'p')
        text_list = text_list_raw[2:]
        text_list = [v.text for v in text_list]
        text = '\n'.join(text_list)
        return text

    def get_categories(self):
        """
        Aos fatos has no category on page
        """
        pass

    def get_tags(self):
        """
        Aos fatos has no tags
        """
        return []

    def get_veredicts(self):
        veredicts = []
        possible_veredicts = [
            'EXAGERADO',
            'IMPRECISO',
            'INSUSTENTÁVEL',
            'INSUSTENTAVEL',
            'FALSO',
            'VERDADEIRO',
            'DISTORCIDO',
            'CONTRADITÓRIO',
            'CONTRADITORIO',
            'DESVIRTUADO'
        ]
        try:
            # Logic for most 2021
            veredict_candidates = self.wrapper.find_elements(By.XPATH, '*//img[string-length(@data-image-id)>0]')
            for candidate in veredict_candidates:
                veredict_attr = candidate.get_attribute('data-image-id')
                veredict = veredict_attr[:-4] # remove .png
                if veredict.upper() in possible_veredicts:
                    veredicts.append(veredict.lower())

            if not veredicts:
                raise Exception('Has no veredict.')
        except:
            try:
                # Logic for most 2020
                veredict_candidates = self.wrapper.find_elements(By.TAG_NAME, 'figcaption')
                for candidate in veredict_candidates:
                    veredict = candidate.text
                    veredict = veredict.replace(' ', '')
                    if veredict.upper() in possible_veredicts:
                        veredicts.append(veredict.lower())
                if not veredicts:
                    raise Exception('Has no veredict.')
            except:
                try:
                    # Logic for most 2019/18
                    veredict_candidates = self.wrapper.find_elements(By.XPATH, "//p[contains(@style, 'text-align: center;')]")
                    for candidate in veredict_candidates:
                        veredict = candidate.text
                        if veredict.upper() in possible_veredicts:
                            veredicts.append(veredict.lower())
                except:
                    raise Exception('Has no veredict.')
        if not veredicts:
            raise Exception('Has no veredict.')
        return veredicts

    def get_image(self):
        """
        Searches and treats the disposal of the image source on
        AosFatos page, which varies depending on the year of publication.
        """
        not_main_image = [
            # Falso symbol
            "https://cdn-images-2.medium.com/max/800/1*-a-QEpowbRqGUPG5-aihLw.png",
            # Falso symbol variation
            "https://lh4.googleusercontent.com/RIq1MXpFMHm_Nh2v1KetiY05A8seiUx7CY9k7j11f1oLL-DBi9GXl06Wk7dBddc2U3yRiDj1HMr_v50pA1h7toqoE67zBYZ3-NLQ2uR8bFo5TjjkGu1a8jQjlcNMxMhntK1XC1Df",
            # Falso symbol with veredict
            "https://static.aosfatos.org/static/images/stamps/falso.png",
            # Verdadeiro symbol
            "https://cdn-images-2.medium.com/max/800/1*Gz2sag5FYyNoYO9g9fp7Qw.png",
            # Verdadeiro symbol variation
            "https://lh3.googleusercontent.com/g4boZ623E1SW1iJHNrQTckH-X6MlD8JpNulN9IflbQldKoAwODLqG2Ejt_eoxZn7eZ63Nt3D7AdhCtYY6BwRPW4HBiKNoOTiP5MVCE7839jEMLx5ck-qc2LgUE3jeMZR2Og_zD4A",
            # Verdadeiro symbol with veredict
            "https://static.aosfatos.org/static/images/stamps/verdadeiro.png"
            # Impreciso symbol
            "https://static.aosfatos.org/media/cke_uploads/2016/07/28/3_impreciso_gde.png",
            # Impreciso symbol with veredict
            "https://static.aosfatos.org/static/images/stamps/impreciso.png",
            # Insustentável symbol
            "https://cdn-images-2.medium.com/max/800/1*bJppYC2dlhFhxVz-XJoeJw.png",
            # Insustentavel symbol variation
            "https://lh6.googleusercontent.com/iN_rgDv85g-lcaXtPdAPDgGk90KebAsK4v30084gxjU6Z5hYPDHVi8V22fTOFk_1WNGfqHgIut7av-VvJhLJkZM3ey3EZm8funL4TmfDy03klaGt2cJLRBfaev-pl2yO3lQk_PCQ",
            # Insustentável symbol with veredict
            "https://static.aosfatos.org/static/images/stamps/insustentavel.png",
            # Exagerado symbol
            "https://cdn-images-2.medium.com/max/800/1*dN4W3IAJt6Vs-6G6GuZzkA.png",
            # Exagerado Symbol variation
            "https://lh5.googleusercontent.com/_x_NmwDflBCTRoYhpvR4UqP15FlM0I7_jXP4j9J7gk8F3FJ5ZXojeBwEcbjz_GCIoD_XjC6iBHbj5RipMtqtZzmIVQ4Hfw9WjhQw73tXHjTktZdwlINyTk6e9FOKeQj1tPoOEknb",
            # Exagerado symbol with veredict
            "https://static.aosfatos.org/static/images/stamps/exagerado.png",
            # Desvirtuado symbol
            "https://lh5.googleusercontent.com/_vnyeDKPlWkTkroWNXvUvuTpld5D11ZR-C7TE_h7lfira8EOHmev8Gn4XEY3U1WWClgD931lYSZna08UVUugq-9FPXMOTUN3OztMI_3YAZMZ5sxw5Y_4oinca_E46Ki7r95NE4905X8",
            # Distorcido symbol with veredict
            "https://static.aosfatos.org/static/images/stamps/distorcido.png",
            # Contradiório symbol
            "https://static.aosfatos.org/media/cke_uploads/2017/09/05/6_contraditorio_gde.png",
            # Contradiório symbol with veredict
            "https://static.aosfatos.org/static/images/stamps/contraditorio.png",
            # Selo
            "https://static.aosfatos.org/static/images/selo-ifcn-v1597271148.png"
        ]
        img = ''
        try:
            # Logic for 2021
            img = self.wrapper.find_element(By.CLASS_NAME, 'responsive-article-image').get_attribute('src')
            if img in not_main_image or '.svg' in img or img == '':
                raise Exception('Image not found yet')
        except:
            try:
                image_candidates = self.wrapper.find_elements(By.XPATH, "//img[contains(@alt, '')]")
                limit = 2
                for idx, candidate in enumerate(image_candidates):
                    if idx >= limit:
                        break
                    current_img = candidate.get_attribute('src')
                    if current_img not in not_main_image and '.svg' not in current_img:
                        img = current_img
                        break
            except:
                img = ''

        return img

    def get_video(self):
        return ''

    def get_html(self):
        return self.driver.page_source

    def execute(self, url, category=[]):
        try_cnt = 0
        last_exception = None
        while try_cnt < self.try_rate:
            try:
                self.driver.get(url)
                self.wrapper = self.driver.find_element(By.CLASS_NAME, 'ck-article')
                date = self.get_date()
                result = {
                    'url': url,
                    'source_name': 'aos fatos',
                    'title':  self.get_title(),
                    'subtitle': self.get_subtitle(),
                    'publication_date': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'text_news': self.get_text(date.year),
                    'image_link': self.get_image(),
                    'video_link': self.get_video(),
                    'authors': self.get_authors(),
                    'categories': category,
                    'tags': self.get_tags(),
                    'obtained_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    'rating': self.get_veredicts(),
                    'raw_file_name': self.get_html_file_value(url)
                    }
                return date.year, date.month, result, self.get_html()
            except Exception as e:
                try_cnt += 1
                last_exception = e
        raise last_exception
