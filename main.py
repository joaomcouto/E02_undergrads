import sys
# URLS
from BUSCA_URLS import fact_check_url_collector as FC_Class
from BUSCA_URLS.fact_check_url_collector import collect_all

# CHECAGENS
from COLETORES.IMPLEMENTADOS.CHECAGENS.AOSFATOS.AOSFATOSScraper import AosFatosScraper
from COLETORES.IMPLEMENTADOS.CHECAGENS.BOATOS.BOATOSScraper import BoatosScraper
from COLETORES.IMPLEMENTADOS.CHECAGENS.COMPROVA import COMPROVAScrapper as CMPRV
from COLETORES.IMPLEMENTADOS.CHECAGENS.ESTADAO_VERIFICA import ESTADAOVERIFICAScrapper as ESTDVER
from COLETORES.IMPLEMENTADOS.CHECAGENS.FATOOUFAKE.FATOOUFAKEScraper import FatoOuFakeScraper
from COLETORES.IMPLEMENTADOS.CHECAGENS.LUPA.LUPAScraper import LupaScraper

# NOTICIAS
from COLETORES.IMPLEMENTADOS.NOTICIAS.ADVENTISTAS.ADVENTISTAS_scrapper import ADVENTISTASScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.ALIADOSBRASIL.ALIADOSBRASIL_scrapper import ALIADOSBRASILScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.ATROMBETA.ATROMBETA_scrapper import ATROMBETAScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.BBC.BBC_scrapper import BBCScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.CARTAPIAUI.CARTAPIAUI_scrapper import CARTAPIAUIScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.CONEXAOAMAZONAS.CONEXAOAMAZONAS_scrapper import CONEXAOAMAZONASScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.CRITICANACIONAL.CRITICANACIONAL_scrapper import CRITICANACIONALScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.DIARIODOPODER.DIARIODOPODER_scrapper import DIARIODOPODERScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.ESTIBORDO.ESTIBORDO_scrapper import ESTIBORDOScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.ESTUDOSNACIONAIS.ESTUDOSNACIONAIS_scrapper import ESTUDOSNACIONAISScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.FOLHADAPOLITICA.FOLHADAPOLITICA_scrapper import FOLHADAPOLITICAScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.FOLHADAREPUBLICA.FOLHADAREPUBLICA_scrapper import FOLHADAREPUBLICAScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.FOLHAMAX.FOLHAMAX_scrapper import FOLHAMAXScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.G1.g1_scrapper import G1Scrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.GAZETABRASIL.GAZETABRASIL_scrapper import GAZETABRASILScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.JORNAL21BRASIL.JORNAL21BRASIL_scrapper import JORNAL21BRASILScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.JORNALDACIDADE.JORNALDACIDADE_scrapper import JORNALDACIDADEScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.LUISCARDOSO.LUISCARDOSO_scrapper import LUISCARDOSOScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.OGRITOCENSURADO.OGRITOCENSURADO_scrapper import OGRITOCENSURADOScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.OLHOABERTOPR.OLHOABERTOPR_scrapper import OLHOABERTOPRScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.QUESTIONESE.QUESTIONESE_scrapper import QUESTIONESEScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.REVISTAAMAZONIA.REVISTAAMAZONIA_scrapper import REVISTAAMAZONIAScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.REVISTAOESTE.REVISTAOESTE_scrapper import REVISTAOESTEScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.RSAGORA.RSAGORA_scrapper import RSAGORAScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.TERCALIVRE.TERCALIVRE_scrapper import TERCALIVREScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.TERRABRASIL.TERRABRASIL_scrapper import TERRABRASILScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.TIERRAPURA.TIERRAPURA_scrapper import TIERRAPURAScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.TRIBUNANACIONAL.TRIBUNANACIONAL_scrapper import TRIBUNANACIONALScrapper
from COLETORES.IMPLEMENTADOS.NOTICIAS.UOL.UOL_scrapper import UOLScrapper



def main(argv):
    """
    Select parameters, instanciate source
    than triggers data scraper
    """
    if len(argv) < 2:
        print("Por favor entre com um número correto de parametros")
        sys.exit()

    process_type = argv[0]

    if process_type == '-url':
        agency = argv[1]
        if (agency == '-all'):
            EV = FC_Class.Estadao_verifica()
            B =  FC_Class.Boatos()
            C =  FC_Class.Comprova()
            AF = FC_Class.Aos_fatos()
            L =  FC_Class.Lupa()
            F =  FC_Class.Fato_ou_fake()
            objs_list = [EV,B,C,AF,L,F]
            for obj in objs_list:
                try:
                    collect_all(obj)
                except Exception as ex:
                    print("Ocorreu um erro! Coleta interrompida.\n")
                    print('Erro: ', ex)
        else:
            if (agency == 'ESTADAOVERIFICA'):
                collector_obj = FC_Class.Estadao_verifica()
            elif (agency == 'BOATOS'):
                collector_obj = FC_Class.Boatos()
            elif (agency == 'COMPROVA'):
                collector_obj = FC_Class.Comprova()
            elif (agency == 'AOSFATOS'):
                collector_obj = FC_Class.Aos_fatos()
            elif (agency == 'LUPA'):
                collector_obj = FC_Class.Lupa()
            elif (agency == 'FATOOUFAKE'):
                collector_obj = FC_Class.Fato_ou_fake()
            else:
                print('Argumento não definido!\n')
                return
            #coleta
            try:
                collect_all(collector_obj)
            except Exception as ex:
                print("Ocorreu um erro! Coleta interrompida.\n")
                print('Erro: ', ex)


    elif process_type == '-coletor':
        # Verificando se o número de parâmetros está correto para essa seleção
        if len(argv) < 3:
            print("Por favor entre com um número correto de parametros")
            sys.exit()

        # Instanciando coletor implementado
        source = argv[1]
        url = argv[2]
        if source == 'ADVENTISTAS':
            t = ADVENTISTASScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'ALIADOSBRASIL':
            t = ALIADOSBRASILScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'ATROMBETA':
            t = ATROMBETAScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'BBC':
            t = BBCScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'CARTAPIAUI':
            t = CARTAPIAUIScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'CONEXAOAMAZONAS':
            t = CONEXAOAMAZONASScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'CRITICANACIONAL':
            t = CRITICANACIONALScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'DIARIODOPODER':
            t = DIARIODOPODERScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'ESTIBORDO':
            t = ESTIBORDOScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'ESTUDOSNACIONAIS':
            t = ESTUDOSNACIONAISScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'FOLHADAPOLITICA':
            t = FOLHADAPOLITICAScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'FOLHADAREPUBLICA':
            t = FOLHADAREPUBLICAScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'FOLHAMAX':
            t = FOLHAMAXScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'G1':
            t = G1Scrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'GAZETABRASIL':
            t = GAZETABRASILScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'JORNAL21BRASIL':
            t = JORNAL21BRASILScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'JORNALDACIDADE':
            t = JORNALDACIDADEScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'LUISCARDOSO':
            t = LUISCARDOSOScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'OGRITOCENSURADO':
            t = OGRITOCENSURADOScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'OLHOABERTOPR':
            t = OLHOABERTOPRScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'QUESTIONESE':
            t = QUESTIONESEScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'REVISTAAMAZONIA':
            t = REVISTAAMAZONIAScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'REVISTAOESTE':
            t = REVISTAOESTEScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'RSAGORA':
            t = RSAGORAScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'TERCALIVRE':
            t = TERCALIVREScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()


        elif source == 'TERRABRASIL':
            t = TERRABRASILScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()

        elif source == 'TIERRAPURA':
            t = TIERRAPURAScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()

        elif source == 'TRIBUNANACIONAL':
            t = TRIBUNANACIONALScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()

        elif source == 'UOL':
            t = UOLScrapper(0)
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
            t.driver.quit()

        elif source == 'ESTADAOVERIFICA':
            url = argv[2]
            EV = ESTDVER.Estadao_Verifica()
            EV.scrap_check(url.strip())

        elif source == 'COMPROVA':
            url = argv[2]
            C = CMPRV.Comprova()
            C.scrap_check(url.strip())

        elif source == 'AOSFATOS':
            t = AosFatosScraper()
            t.execute(url)
            t.close_connection()

        elif source == 'BOATOS':
            t = BoatosScraper()
            t.execute(url)
            t.close_connection()

        elif source == 'FATOOUFAKE':
            t = FatoOuFakeScraper()
            t.execute(url)
            t.close_connection()

        elif source == 'LUPA':
            t = LupaScraper()
            t.execute(url)
            t.close_connection()


if __name__ == "__main__":
    main(sys.argv[1:])
