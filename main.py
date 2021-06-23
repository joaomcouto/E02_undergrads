import sys
#from COLETORES.COLETORES.ADVENTISTAS.ADVENTISTAS_scrapper.py import ADVENTISTASScrapper
from COLETORES.COLETORES_URL import fact_check_url_collector as FC_Class
from COLETORES.COLETORES_URL.fact_check_url_collector import collect_all

def main(argv):
    """
    Select parameters, instanciate source
    than triggers data scraper
    """
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
        source = argv[1]
        url = argv[2]
        if source == 'adventistas':
            t = ADVENTISTASScrapper(0)

        data = t.scrap_article(url)
        t.append_article_to_txt(data)
        t.driver.quit()


if __name__ == "__main__":
    main(sys.argv[1:])
