#coding:utf-8
import pandas as pd
def CEDULA_CATASTRAL(cedcatast:str):
    dic = {'MUNICIPIO': {212: 'COPACABANA'},
           'SECTOR': {1: 'Urbano', 2: 'Rural'},
           'BARRIO': {1: 'SAN JUAN', 2: 'MARIA', 3: 'TABLAZO-CANOAS', 4: 'EL MOJON', 5: 'FATIMA', 6: 'LA PEDRERA',
                      7: 'SAN FRANCISCO', 8: 'MIRAFLOREZ', 9: 'CRISTO REY', 10: 'EL RECREO', 11: 'EL OBRERO',
                      12: 'SIMON BOLIVAR', 13: 'TOBON QUINTERO', 14: 'YARUMITO', 15: 'LAS VEGAS', 16: 'LA ASUNCION',
                      17: 'LA AZULITA', 18: 'CORREDOR MULTIPLE', 19: 'PORVENIR', 20: 'EL PEDREGAL', 21: 'EL REMANSO',
                      22: 'LA MISERICORDIA', 23: 'MACHADO', 24: 'VILLANUEVA'},
           'VEREDA': {1: 'QUEBRADA ARRIBA', 2: 'SABANETA', 3: 'PEÑOLCITO', 4: 'CABUYAL', 5: 'GRANIZAL',
                      6: 'CONVENTO', 7: 'FONTIDUEÑO', 8: 'MONTAÑITA', 9: 'EL SALADO', 10: 'ALVARADO', 11: 'ANCON',
                      12: 'ZARZAL CURAZAO', 13: 'EL NORAL', 14: 'LA VETA', 15: 'ZARZAL LA LUZ'}}
    partes = cedcatast.split('-')
    municipio, sector, corregimiento = int(partes[0]), int(partes[1]), int(partes[2])
    barrio, manz_vere, predio = int(partes[3]), int(partes[4]), int(partes[5])
    edificio, und_pred = int(partes[6]), int(partes[7])

    if sector == 1:
        resp_1 = {'Municipio': dic['MUNICIPIO'][municipio], 'Sector': dic['SECTOR'][sector], 'Corregimiento': corregimiento,
                  'Barrio': dic['BARRIO'][barrio], 'Manzanda-Vereda':manz_vere, 'Predio': predio, 'Edificio':edificio,
                  'Unidad predial': und_pred}
        return resp_1

    if sector == 2:
        resp_2 = {'Municipio': dic['MUNICIPIO'][municipio], 'Sector': dic['SECTOR'][sector],
                  'Corregimiento': corregimiento, 'Barrio': dic['VEREDA'][manz_vere], 'Manzanda-Vereda':manz_vere,
                  'Predio': predio, 'Edificio': edificio, 'Unidad predial': und_pred}

        return resp_2


def searchforsoilusestable(cedula_catastral:str):
    BD = pd.DataFrame(
        pd.read_excel(r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\Clasificacion_suelos.xlsx'),
        columns=['Sector', 'Principal', 'Complementario', 'Restringido', 'Prohibido', 'Clasificacion', 'Articulos'])
    resultado_busqueda = {}
    count = 1
    for e in BD.values:
        if CEDULA_CATASTRAL(cedula_catastral)['Barrio'] in e[0]:
            resultado_busqueda[count] = e[0]
            count +=1
    print('LA BUSQUEDA ARROJO LOS SIGUIENTES RESULTADOS:')
    if len(resultado_busqueda.values()) > 1:
        for i in range(1, len(resultado_busqueda.values()) + 1):
            print(f'{i}. {resultado_busqueda[i]}')
        chosen = input('\nSeleccione los sectores de uso del suelo correspondientes: ').split(', ')
        usos_del_suelo = {}
        for e in chosen:
            for i in BD.values:
                if i[0] == resultado_busqueda[int(e)]:
                    usos_del_suelo[f'{resultado_busqueda[int(e)]}']={'Principal': i[1], 'Complementario': i[2],
                                                                     'Restringido': i[3], 'Prohibido': i[4],
                                                                     'Clasificacion': i[5], 'Articulos': i[6]}
        return usos_del_suelo
    else:
        for i in BD.values:
            if resultado_busqueda[1] == i[0]:
                return {resultado_busqueda[1]: {'Principal': i[1], 'Complementario': i[2],
                                                                   'Restringido': i[3], 'Prohibido': i[4],
                                                                   'Clasificacion': i[5], 'Articulos': i[6]}}

def verificarsolicitud(tipo:str, ciiu:list, uso_del_suelo:dict):
    if tipo == 'Estudio':
        BD_ciiu = pd.DataFrame(pd.read_excel(r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\cod_actividad.xlsx'),
                               columns=['Codigo', 'Descripcion', 'Tipo'])
        resultado_ciiu = {}
        for e in ciiu:
            for i in BD_ciiu.values:
                if e == i[0]:
                    resultado_ciiu[e] = {'Descripcion': i[1], 'Tipo': i[2]}


        usos = ["Principal", "Complementario", "Restringido", "Prohibido"]
        resultado = {}
        for i in resultado_ciiu.keys():
            eval = {}
            for j in usos:
                for w in uso_del_suelo.values():
                    for z in resultado_ciiu[i]['Tipo'].split(', '):
                        if z in w[j].split(', '):
                            eval[f'Uso_{j}'] = 'APROBADO'
                            print('ok1')
                            break
                        else:
                            eval[f'Uso_{j}'] = 'NO APROBADO'
                            #print(eval)
                        #print(j, w[j].split(', '), z)
            print('ciclo terminado')

            return eval



data = searchforsoilusestable('212-2-001-000-0013-00025-00000-00000')
print(verificarsolicitud('Estudio', [4711, 4719], data))





