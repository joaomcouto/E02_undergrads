import sys
# ULRS
from COLETORES.COLETORES_URL import fact_check_url_collector as FC_Class
from COLETORES.COLETORES_URL.fact_check_url_collector import collect_all

from COLETORES.IMPLEMENTADOS.ADVENTISTAS.ADVENTISTAS_scrapper import ADVENTISTASScrapper
from COLETORES.IMPLEMENTADOS.ALIADOSBRASIL.ALIADOSBRASIL_scrapper import ALIADOSBRASILScrapper
from COLETORES.IMPLEMENTADOS.ATROMBETA.ATROMBETA_scrapper import ATROMBETAScrapper
from COLETORES.IMPLEMENTADOS.BBC.BBC_scrapper import BBCScrapper
from COLETORES.IMPLEMENTADOS.CARTAPIAUI.CARTAPIAUI_scrapper import CARTAPIAUIScrapper
from COLETORES.IMPLEMENTADOS.CONEXAOAMAZONAS.CONEXAOAMAZONAS_scrapper import CONEXAOAMAZONASScrapper
from COLETORES.IMPLEMENTADOS.CRITICANACIONAL.CRITICANACIONAL_scrapper import CRITICANACIONALScrapper
from COLETORES.IMPLEMENTADOS.DIARIODOPODER.DIARIODOPODER_scrapper import DIARIODOPODERScrapper
from COLETORES.IMPLEMENTADOS.ESTIBORDO.ESTIBORDO_scrapper import ESTIBORDOScrapper
from COLETORES.IMPLEMENTADOS.ESTUDOSNACIONAIS.ESTUDOSNACIONAIS_scrapper import ESTUDOSNACIONAISScrapper
from COLETORES.IMPLEMENTADOS.FOLHADAPOLITICA.FOLHADAPOLITICA_scrapper import FOLHADAPOLITICAScrapper
from COLETORES.IMPLEMENTADOS.FOLHADAREPUBLICA.FOLHADAREPUBLICA_scrapper import FOLHADAREPUBLICAScrapper
from COLETORES.IMPLEMENTADOS.FOLHAMAX.FOLHAMAX_scrapper import FOLHAMAXScrapper
from COLETORES.IMPLEMENTADOS.G1.g1_scrapper import G1Scrapper
from COLETORES.IMPLEMENTADOS.GAZETABRASIL.GAZETABRASIL_scrapper import GAZETABRASILScrapper
from COLETORES.IMPLEMENTADOS.JORNAL21BRASIL.JORNAL21BRASIL_scrapper import JORNAL21BRASILScrapper
from COLETORES.IMPLEMENTADOS.JORNALDACIDADE.JORNALDACIDADE_scrapper import JORNALDACIDADEScrapper
from COLETORES.IMPLEMENTADOS.LUISCARDOSO.LUISCARDOSO_scrapper import LUISCARDOSOScrapper
from COLETORES.IMPLEMENTADOS.OGRITOCENSURADO.OGRITOCENSURADO_scrapper import OGRITOCENSURADOScrapper
from COLETORES.IMPLEMENTADOS.OLHOABERTOPR.OLHOABERTOPR_scrapper import OLHOABERTOPRScrapper
from COLETORES.IMPLEMENTADOS.QUESTIONESE.QUESTIONESE_scrapper import QUESTIONESEScrapper
from COLETORES.IMPLEMENTADOS.REVISTAAMAZONIA.REVISTAAMAZONIA_scrapper import REVISTAAMAZONIAScrapper
from COLETORES.IMPLEMENTADOS.REVISTAOESTE.REVISTAOESTE_scrapper import REVISTAOESTEScrapper
from COLETORES.IMPLEMENTADOS.RSAGORA.RSAGORA_scrapper import RSAGORAScrapper
from COLETORES.IMPLEMENTADOS.TERCALIVRE.TERCALIVRE_scrapper import TERCALIVREScrapper
from COLETORES.IMPLEMENTADOS.TERRABRASIL.TERRABRASIL_scrapper import TERRABRASILScrapper
from COLETORES.IMPLEMENTADOS.TIERRAPURA.TIERRAPURA_scrapper import TIERRAPURAScrapper
from COLETORES.IMPLEMENTADOS.TRIBUNANACIONAL.TRIBUNANACIONAL_scrapper import TRIBUNANACIONALScrapper
from COLETORES.IMPLEMENTADOS.UOL.UOL_scrapper import UOLScrapper



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
            if (agency == '-estadao_verifica'):
                collector_obj = FC_Class.Estadao_verifica()
            elif (agency == '-boatos'):
                collector_obj = FC_Class.Boatos()
            elif (agency == '-comprova'):
                collector_obj = FC_Class.Comprova()
            elif (agency == '-aos_fatos'):
                collector_obj = FC_Class.Aos_fatos()
            elif (agency == '-lupa'):
                collector_obj = FC_Class.Lupa()
            elif (agency == '-fato_fake'):
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
        if source == 'ADVENTISTAS':
            t = ADVENTISTASScrapper(0)

        elif source == 'ALIADOSBRASIL':
            t = ALIADOSBRASILScrapper(0)

        elif source == 'ATROMBETA':
            t = ATROMBETAScrapper(0)

        elif source == 'BBC':
            t = BBCScrapper(0)

        elif source == 'CARTAPIAUI':
            t = CARTAPIAUIScrapper(0)

        elif source == 'CONEXAOAMAZONAS':
            t = CONEXAOAMAZONASScrapper(0)

        elif source == 'CRITICANACIONAL':
            t = CRITICANACIONALScrapper(0)

        elif source == 'DIARIODOPODER':
            t = DIARIODOPODERScrapper(0)

        elif source == 'ESTIBORDO':
            t = ESTIBORDOScrapper(0)

        elif source == 'ESTUDOSNACIONAIS':
            t = ESTUDOSNACIONAISScrapper(0)

        elif source == 'FOLHADAPOLITICA':
            t = FOLHADAPOLITICAScrapper(0)

        elif source == 'FOLHADAREPUBLICA':
            t = FOLHADAREPUBLICAScrapper(0)

        elif source == 'FOLHAMAX':
            t = FOLHAMAXScrapper(0)

        elif source == 'G1':
            t = G1Scrapper(0)

        elif source == 'GAZETABRASIL':
            t = GAZETABRASILScrapper(0)

        elif source == 'JORNAL21BRASIL':
            t = JORNAL21BRASILScrapper(0)

        elif source == 'JORNALDACIDADE':
            t = JORNALDACIDADEScrapper(0)

        elif source == 'LUISCARDOSO':
            t = LUISCARDOSOScrapper(0)

        elif source == 'OGRITOCENSURADO':
            t = OGRITOCENSURADOScrapper(0)

        elif source == 'OLHOABERTOPR':
            t = OLHOABERTOPRScrapper(0)

        elif source == 'QUESTIONESE':
            t = QUESTIONESEScrapper(0)

        elif source == 'REVISTAAMAZONIA':
            t = REVISTAAMAZONIAScrapper(0)

        elif source == 'REVISTAOESTE':
            t = REVISTAOESTEScrapper(0)

        elif source == 'RSAGORA':
            t = RSAGORAScrapper(0)

        elif source == 'TERCALIVRE':
            t = TERCALIVREScrapper(0)

        elif source == 'TERRABRASIL':
            t = TERRABRASILScrapper(0)

        elif source == 'TIERRAPURA':
            t = TIERRAPURAScrapper(0)

        elif source == 'TRIBUNANACIONAL':
            t = TRIBUNANACIONALScrapper(0)

        elif source == 'UOL':
            t = UOLScrapper(0)

        # Caso a busca seja por várias URLs vindas de um arquivo
        if argv[2] == "-busca_em_arquivo":
            pass
        # Caso a busca seja por URL única passada como parâmetro
        else:
            url = argv[2]
            data = t.scrap_article(url)
            t.append_article_to_txt(data)
        t.driver.quit()


if __name__ == "__main__":
    main(sys.argv[1:])
