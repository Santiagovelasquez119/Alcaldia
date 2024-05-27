#coding:utf-8
import datetime

import pandas as pd
def CEDULA_CATASTRAL(cedcatast:str):
    dic = {'MUNICIPIO': {212: 'COPACABANA'},
           'SECTOR': {1: 'Urbano', 2: 'Rural'},
           'BARRIO': {1: 'SAN JUAN', 2: 'MARIA', 3: 'TABLAZO-CANOAS', 4: 'EL MOJON', 5: 'FATIMA', 6: 'LA PEDRERA',
                      7: 'SAN FRANCISCO', 8: 'MIRAFLORES', 9: 'CRISTO REY', 10: 'EL RECREO', 11: 'EL OBRERO',
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
                                                                     'Clasificacion': i[5]}
        return usos_del_suelo
    else:
        for i in BD.values:
            if resultado_busqueda[1] == i[0]:
                return {resultado_busqueda[1]: {'Principal': i[1], 'Complementario': i[2],
                                                                   'Restringido': i[3], 'Prohibido': i[4],
                                                                   'Clasificacion': i[5]}}

def estudio_solicitud(ciiu:list, usos_del_suelo:dict):
    BD_usosuelo = pd.DataFrame(
        pd.read_excel(
            r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\Clasificacion_suelos.xlsx'),
        columns=['Sector', 'Principal', 'Complementario', 'Restringido', 'Prohibido', 'Clasificacion', 'Articulos'])

    BD_ciiu = pd.DataFrame(pd.read_excel(
        r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\cod_actividad.xlsx'),
                           columns=['Codigo', 'Descripcion', 'Tipo'])
    resp = {}
    for a in usos_del_suelo:
        principal = list()
        complementario = list()
        restringido = list()
        prohibido = list()

        for b in BD_usosuelo.values:
            if a == b[0]:
                principal, complementario, restringido, prohibido = b[1].split(', '), b[2].split(', '), b[3].split(', '), b[4].split(', ')

        dic_ciiu = {}
        for c in ciiu:
            for d in BD_ciiu.values:
                if c == d[0]:
                    for e in d[2].split(', '):
                        if e not in prohibido:
                            if 'Multiple' in restringido:
                                dic_ciiu[c] = 'APROBADO USO RESTRINGIDO'
                                break
                            elif e in restringido:
                                dic_ciiu[c] = 'APROBADO USO RESTRINGIDO'
                                break
                            elif 'Multiple' in complementario:
                                dic_ciiu[c] = 'APROBADO USO COMPLEMENTARIO'
                                break
                            elif e in complementario:
                                dic_ciiu[c] = 'APROBADO USO COMPLEMENTARIO'
                                break
                            elif 'Multiple' in principal:
                                dic_ciiu[c] = 'APROBADO USO PRINCIPAL'
                                break
                            elif e in principal:
                                dic_ciiu[c] = 'APROBADO USO PRINCIPAL'
                                break
                        else:
                            dic_ciiu[c] = 'NO APROBADO'
        resp[a] = dic_ciiu
    return resp

def setciiuNoAprobado(dic_ciiu:dict):
    ciiu_den = input('Ingrese los codigos de actividad: ').split(', ')
    if len(dic_ciiu) >= 2:
        usos = input('Ingrese los usos del suelo: ').split(', ')
        for a in usos:
            for b in ciiu_den:
                dic_ciiu[a][int(b)] = 'NO APROBADO'
    return pd.DataFrame(dic_ciiu)


def excepciones(usos_del_suelo:dict, ciiu_dict:dict):
    casos = input('Ingrese las restricciones: ').split(', ')
    BD_Articulos = pd.DataFrame(
        pd.read_excel(r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\Articulos.xlsx'),
        columns=['Numero', 'Articulo', 'CIIU'])
    exceptions = ''
    for a in casos:
        for b in BD_Articulos.values:
            if a == b[0]:
                pass


def llenar_formato(nombre_usuario:str, Id:str, celular:str, direccion_notif:str, mail:str, num_rad:str,
                   fecha_rad:datetime.time, ced_catast:str, matr_inm:str, direccion:str, razon_social:str,
                   uso_del_suelo:dict, resp_ciiu:dict):
    from docxtpl import DocxTemplate
    formato = DocxTemplate(r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Formatos\Formato_Comercial.docx')
    arts = ''
    replace = {'usos_del_suelo':pd.DataFrame(uso_del_suelo),
               'resp_ciiu': pd.DataFrame(resp_ciiu)}
    formato.render(replace)
    formato.save(
        rf'C:\Users\Santiago\OneDrive - Universidad Nacional de Colombia\Escritorio\Alcaldía de Copacabana\2024\USOS DE SUELOS\UsoSueloComercial_{nombre_usuario}_{num_rad}.docx')



##Información de notificación del usuario
nombre_usuario = 'PEPITO PEREZ'
Id = '1001016888'
Celular = '3023302896'
Direccion_notif = 'CR 64 N 47-81'
Mail = 'SANTIAGOVELAS119@GMAIL.COM'
Radicado = '4563'
fecha_rad = datetime.date(2024, 3, 4)

## Informacion del predio objeto de la solicitud ##
Cedula_Catastral = '212-2-001-000-0013-00025-00000-00000'
Matricula = '012-35669'
Direccion_predio = 'VDA EL NORAL'

## Informacion de la actividad y razon social
Servicio = [7490, 7320]
Razon_social = 'RAZON SOCIAL'

uso_suelo = searchforsoilusestable(Cedula_Catastral)
estudio = estudio_solicitud(Servicio, uso_suelo.keys())
print(uso_suelo)
print(estudio)
llenar_formato(nombre_usuario, Id, Celular, Direccion_notif, Mail, Radicado, fecha_rad, Cedula_Catastral, Matricula,
               Direccion_predio, Razon_social, uso_suelo, estudio)




