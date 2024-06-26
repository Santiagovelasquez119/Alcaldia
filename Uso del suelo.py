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
            count += 1
    print('LA BUSQUEDA ARROJO LOS SIGUIENTES RESULTADOS:')
    if len(resultado_busqueda.values()) > 1:
        for i in range(1, len(resultado_busqueda.values()) + 1):
            print(f'{i}. {resultado_busqueda[i]}')
        chosen = input('\nSeleccione los sectores de uso del suelo correspondientes: ').split(', ')
        usos_del_suelo = {}
        for e in chosen:
            for i in BD.values:
                if i[0] == resultado_busqueda[int(e)]:
                    usos_del_suelo[f'{resultado_busqueda[int(e)]}'] = {'Principal': i[1], 'Complementario': i[2],
                                                                       'Restringido': i[3], 'Prohibido': i[4],
                                                                       'Clasificacion': i[5], 'Articulos': i[6]}
        return usos_del_suelo
    else:
        for i in BD.values:
            if resultado_busqueda[1] == i[0]:
                return {resultado_busqueda[1]: {'Principal': i[1], 'Complementario': i[2],
                                                                   'Restringido': i[3], 'Prohibido': i[4],
                                                                   'Clasificacion': i[5], 'Articulos': i[6]}}


def searchforciiutable(ciiu:list):
    BD_ciiu = pd.DataFrame(pd.read_excel(
        r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\cod_actividad.xlsx'),
        columns=['Codigo', 'Descripcion', 'Tipo'])

    ciiu_result = {}
    for a in ciiu:
        for b in BD_ciiu.values:
            if a == b[0]:
                ciiu_result[a] = {'Descripcion': b[1], 'Tipo': b[2]}
    return ciiu_result

def estudio_solicitud(ciiu:list, usos_del_suelo:dict):
    resp = {}
    for a in usos_del_suelo:
        uso = {}
        for b in searchforciiutable(ciiu).keys():
            if searchforciiutable(ciiu)[b]['Tipo'] not in usos_del_suelo[a]['Prohibido'].split(', '):
                c = ['Principal', 'Complementario', 'Restringido']
                for i in c:
                    if ((searchforciiutable(ciiu)[b]['Tipo'] in usos_del_suelo[a][i].split(', ')) or
                            ('Multiple' in usos_del_suelo[a][i])):
                        uso[b] = f'APROBADO USO {i}'.upper()
                        break
                    else:
                        uso[b] = 'NO APROBADO'
            else:
                uso[b] = 'NO APROBADO USO PROHIBIDO'
        resp[a] = uso
    return resp


def setciiuNoAprobado(dic_ciiu:dict, ciiu_rest:list):
    ciiu_den = ciiu_rest
    if len(dic_ciiu) >= 2:
        usos = input('Ingrese los usos del suelo a restringir: ').split(', ')
        for a in usos:
            for b in ciiu_den:
                dic_ciiu[a][int(b)] = 'NO APROBADO'
    return pd.DataFrame(dic_ciiu)


def restricciones(usos_del_suelo:dict, ciiu_dict: dict):
    BD_Restricciones = pd.DataFrame(
        pd.read_excel(r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\Restricciones.xlsx'),
        columns=['Restriccion', 'Descripcion', 'ciiu'])
    print('Se tienen las siguientes restricciones: ')
    dic_restric = {}
    n = 1
    for a in BD_Restricciones.values:
        print(f'{n}. {a[0]}')
        dic_restric[int(n)] = [a[0], a[1], a[2]]
        n += 1
    chosen = input('Seleccione la(s) restriccion(es): ').split(', ')
    for a in chosen:
        for b in dic_restric.keys():
            print(a, b)
            if a == b:
                c = setciiuNoAprobado(ciiu, dic_restric[int(a)][2])
                return c, a[1]

def llenar_formato(nombre_usuario:str, Id:str, celular:str, direccion_notif:str, mail:str, num_rad:str,
                   fecha_rad:datetime.time, ced_catast:str, matr_inm:str, direccion:str, razon_social:str, servicios:list,
                   uso_del_suelo:dict, resp_ciiu:dict):
    from docxtpl import DocxTemplate
    formato = DocxTemplate(r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Formatos\Formato_Comercial.docx')
    BD_Articulos = pd.DataFrame(pd.read_excel(r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\Articulos.xlsx'))
    BD_ciiu = pd.DataFrame(pd.read_excel(
        r'C:\Users\Santiago\PycharmProjects\pythonProject\Alcaldia\Ensayos\Mejoras\Bases de datos\cod_actividad.xlsx'),
        columns=['Codigo', 'Descripcion', 'Tipo'])
    usos = ''
    arts = []
    for e in uso_del_suelo.keys():
        usos += f'Uso del suelo del sector: {e}\n'
        usos += f'Principal: \t\t{uso_del_suelo[e]["Principal"]}\n'
        usos += f'Complementario: \t{uso_del_suelo[e]["Complementario"]}\n'
        usos += f'Restringido: \t\t{uso_del_suelo[e]["Restringido"]}\n'
        usos += f'Prohibido: \t\t{uso_del_suelo[e]["Prohibido"]}\n'
        usos += f'Clasificacion: \t\t{uso_del_suelo[e]["Clasificacion"]}\n'
        usos += '\n'
        for a in uso_del_suelo[e]["Articulos"].split(', '):
            if a not in arts:
                arts.append(a)
    add_arts = input('Desea agregar artículos a la lista de añadidos? Ingrese los artículos o ingrese NO: ').split(', ')
    for a in add_arts:
        if a == 'No' or a == 'NO' or a == 'no':
            print('No se agregan')
            break
        else:
            print(a, 'AGREGADO')
            arts.append(a)
    arts_text = ''
    for e in arts:
        for i in BD_Articulos.values:
            if i[0] == e:
                arts_text += i[1] + '\n'
                arts_text += '\n'
    servicio = ''
    for e in servicios:
        servicio += f'{e}, '

    respuesta = ''
    for h in resp_ciiu.keys():
        respuesta += f'Compatibilidad de las actividades de servicio: {servicio}con los usos del suelo del sector {h}\n'
        for g in resp_ciiu[h]:
            respuesta += f'Codigo CIIU: {g} = {resp_ciiu[h][g]}\n'
        respuesta += '\n'
    for j in servicios:
        for x in BD_ciiu.values:
            if j == x[0]:
                respuesta += f'{j}: {x[1]} - {x[2]}\n'
                respuesta += '\n'
    replace = {'nombre_usuario': nombre_usuario, 'Id': Id, 'celular': celular, 'direccion_notif': direccion_notif,
               'mail': mail, 'num_rad': num_rad, 'fecha_rad': fecha_rad,
               'barrio': CEDULA_CATASTRAL(ced_catast)['Barrio'], 'ced_catast': ced_catast, 'matr_inm': matr_inm,
               'usos': usos, 'direccion': direccion, 'servicio': servicio, 'arts_text': arts_text,
               'Respuesta': respuesta}
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
Cedula_Catastral = '212-2-001-000-0012-00025-00000-00000'
Matricula = '012-35669'
Direccion_predio = 'VDA EL NORAL'

## Informacion de la actividad y razon social
Servicio = [7490, 5630, 9103]
Razon_social = 'RAZON SOCIAL'

uso_suelo = searchforsoilusestable(Cedula_Catastral)
estudio = estudio_solicitud(Servicio, uso_suelo)
ciiu = searchforciiutable(Servicio)
print('--------------------USOS DEL SUELO-------------------------')
print(pd.DataFrame(uso_suelo))
print('-------------------------------------')
print('-------ACTIVIDADES COMERCIALES------')
print(pd.DataFrame(ciiu).transpose())
print('----------------')
print('-------------RESULTADO DE LA SOLICITUD------------')
print(pd.DataFrame(estudio))
print('-------------------------------')
#print('--------CIIU NO APROBADO-------')
#print(pd.DataFrame(setciiuNoAprobado(estudio)))
print('------------------- RESTRICCIONES ------------------')
print(restricciones(uso_suelo, ciiu))

#llenar_formato(nombre_usuario, Id, Celular, Direccion_notif, Mail, Radicado, fecha_rad, Cedula_Catastral, Matricula,
               #Direccion_predio, Razon_social, Servicio, uso_suelo, estudio)




