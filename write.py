#!/usr/bin/env python
# -*- coding: utf-8 -*-

__name__="write"

import cPickle
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from difflib import SequenceMatcher
import unicodedata

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def delete_words(s):
    bannedWord = ['residencial', 'la', "las", "fracc.", "fraccionamiento", "del", "el", "los", "cond.", "condominio", "condominios", "colonia"]
    s = s.lower()
    s = ' '.join(i for i in s.split() if i not in bannedWord)
    s = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    return s

def expectAlert(driver):
    time.sleep(shortWaitTime)
    try:
        driver.switch_to.alert.accept()
    except:
        pass

shortWaitTime = 3
longWaitTime = 10

#cargamos archivo de lectura
datos = cPickle.load(open("datos.data","r"))

driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://www.casasyterrenospro.com/")
driver.find_element_by_xpath("//*[@id=\"top_home\"]/div/div/div[3]/p[2]/input").click()
time.sleep(shortWaitTime)
driver.find_element_by_id("user").send_keys("FRANCISCOGLEZ")
driver.find_element_by_id("pass").send_keys("12345678")
driver.find_element_by_id("botonlogin").click()
time.sleep(longWaitTime)
#agregamos todas las propiedades
for dato in datos:
    driver.get("http://www.casasyterrenospro.com/admin/propiedades_registro/paso_uno")
    time.sleep(longWaitTime)
    tipo_inmueble = dato["tipo_inmueble"]
    if tipo_inmueble == "Casa":
        Select(driver.find_element_by_id("tipo_inmueble")).select_by_value("18")
        time.sleep(shortWaitTime)
        driver.find_element_by_id("uso_1").click()
        driver.find_element_by_id("fin_venta").click()
        driver.find_element_by_id("precio_venta").send_keys(dato["precio"])
        Select(driver.find_element_by_id("atri_6")).select_by_value(dato["habitaciones"])
        #baños :/
        banos = float(0)
        if dato["baños"]!="":
            banos = float(dato["baños"])
        if dato["medioBaños"]!="":
            banos += float(dato["medioBaños"])*.5
        Select(driver.find_element_by_id("atri_1")).select_by_value(str(banos))
        #estacionamiento
        if dato["estacionamiento"]!="":
            Select(driver.find_element_by_id("atri_3")).select_by_value(dato["estacionamiento"])
        #niveles
        if dato["niveles"]!="":
            Select(driver.find_element_by_id("atri_8")).select_by_value(dato["niveles"])

        terreno = "10"
        if dato["terreno"]!="":
            terreno = dato["terreno"]
        driver.find_element_by_id("atri_12").send_keys(terreno)

        construccion = "10"
        if dato["construccion"]!="":
            construccion = dato["construccion"]
        driver.find_element_by_id("atri_13").send_keys(construccion)

        driver.find_element_by_id("descripcion").send_keys(dato["descripcion"])
        Select(driver.find_element_by_id("u_estado")).select_by_value("25")
        time.sleep(shortWaitTime)

        selectMunicipios = Select(driver.find_element_by_id("u_municipio"))
        options = selectMunicipios.options
        municipio = dato["municipio"]
        for option in options:
            if municipio.find(option.text) > -1:
                selectMunicipios.select_by_value(option.get_attribute("value"))
                break
        time.sleep(shortWaitTime)

        selectColonias = Select(driver.find_element_by_id("u_colonia"))
        options = selectColonias.options
        colonia = delete_words(dato["colonia"])
        mas_similar=0
        option_value="1"
        for option in options:
            value = option.get_attribute("value")
            coloniaOption = delete_words(option.text)
            ratio = similar(colonia,coloniaOption)
            if ratio==1:
                #print(coloniaOption)
                option_value = value
                break
            elif ratio > mas_similar:
                #print(coloniaOption)
                mas_similar = ratio
                option_value = value
        selectColonias.select_by_value(option_value)

        #Un posible alert puede aparecer
        expectAlert(driver)

        driver.find_element_by_id("u_calle").send_keys(dato["calle"])
        driver.find_element_by_id("u_numero").send_keys(dato["numero_exterior"])
        driver.find_element_by_id("u_numero_int").send_keys(dato["numero_interior"])

        driver.find_element_by_id("continuar_sub").click()
        time.sleep(longWaitTime)
    elif tipo_inmueble=="Departamento":
        Select(driver.find_element_by_id("tipo_inmueble")).select_by_value("19")
        time.sleep(shortWaitTime)
        driver.find_element_by_id("uso_1").click()
        driver.find_element_by_id("fin_venta").click()
        driver.find_element_by_id("precio_venta").send_keys(dato["precio"])
        Select(driver.find_element_by_id("atri_6")).select_by_value(dato["habitaciones"])
        # baños :/
        banos = float(0)
        if dato["baños"] != "":
            banos = float(dato["baños"])
        if dato["medioBaños"] != "":
            banos += float(dato["medioBaños"]) * .5
        Select(driver.find_element_by_id("atri_1")).select_by_value(str(banos))
        # estacionamiento
        if dato["estacionamiento"] != "":
            Select(driver.find_element_by_id("atri_3")).select_by_value(dato["estacionamiento"])
        # niveles
        if dato["niveles"] != "":
            Select(driver.find_element_by_id("atri_4")).select_by_value(dato["niveles"])

        terreno = "10"
        if dato["terreno"] != "":
            terreno = dato["terreno"]
        driver.find_element_by_id("atri_12").send_keys(terreno)

        construccion = "10"
        if dato["construccion"] != "":
            construccion = dato["construccion"]
        driver.find_element_by_id("atri_13").send_keys(construccion)

        driver.find_element_by_id("descripcion").send_keys(dato["descripcion"])
        Select(driver.find_element_by_id("u_estado")).select_by_value("25")
        time.sleep(shortWaitTime)

        selectMunicipios = Select(driver.find_element_by_id("u_municipio"))
        options = selectMunicipios.options
        municipio = dato["municipio"]
        for option in options:
            if municipio.find(option.text) > -1:
                selectMunicipios.select_by_value(option.get_attribute("value"))
                break
        time.sleep(shortWaitTime)

        selectColonias = Select(driver.find_element_by_id("u_colonia"))
        options = selectColonias.options
        colonia = delete_words(dato["colonia"])
        mas_similar = 0
        option_value = "1"
        for option in options:
            value = option.get_attribute("value")
            coloniaOption = delete_words(option.text)
            ratio = similar(colonia, coloniaOption)
            if ratio == 1:
                # print(coloniaOption)
                option_value = value
                break
            elif ratio > mas_similar:
                # print(coloniaOption)
                mas_similar = ratio
                option_value = value
        selectColonias.select_by_value(option_value)

        # Un posible alert puede aparecer
        expectAlert(driver)

        driver.find_element_by_id("u_calle").send_keys(dato["calle"])
        driver.find_element_by_id("u_numero").send_keys(dato["numero_exterior"])
        driver.find_element_by_id("u_numero_int").send_keys(dato["numero_interior"])

        driver.find_element_by_id("continuar_sub").click()
        time.sleep(longWaitTime)
    elif tipo_inmueble=="Local":
        Select(driver.find_element_by_id("tipo_inmueble")).select_by_value("26")
        time.sleep(shortWaitTime)
        driver.find_element_by_id("uso_2").click()
        driver.find_element_by_id("fin_venta").click()
        driver.find_element_by_id("precio_venta").send_keys(dato["precio"])

        # baños :/
        banos = float(0)
        if dato["baños"] != "":
            banos = float(dato["baños"])
        if dato["medioBaños"] != "":
            banos += float(dato["medioBaños"]) * .5
        Select(driver.find_element_by_id("atri_1")).select_by_value(str(banos))
        # estacionamiento
        if dato["estacionamiento"] != "":
            Select(driver.find_element_by_id("atri_3")).select_by_value(dato["estacionamiento"])

        terreno = "10"
        if dato["terreno"] != "":
            terreno = dato["terreno"]
        driver.find_element_by_id("atri_12").send_keys(terreno)

        construccion = "10"
        if dato["construccion"] != "":
            construccion = dato["construccion"]
        driver.find_element_by_id("atri_13").send_keys(construccion)

        driver.find_element_by_id("descripcion").send_keys(dato["descripcion"])
        Select(driver.find_element_by_id("u_estado")).select_by_value("25")
        time.sleep(shortWaitTime)

        selectMunicipios = Select(driver.find_element_by_id("u_municipio"))
        options = selectMunicipios.options
        municipio = dato["municipio"]
        for option in options:
            if municipio.find(option.text) > -1:
                selectMunicipios.select_by_value(option.get_attribute("value"))
                break
        time.sleep(shortWaitTime)

        selectColonias = Select(driver.find_element_by_id("u_colonia"))
        options = selectColonias.options
        colonia = delete_words(dato["colonia"])
        mas_similar = 0
        option_value = "1"
        for option in options:
            value = option.get_attribute("value")
            coloniaOption = delete_words(option.text)
            ratio = similar(colonia, coloniaOption)
            if ratio == 1:
                # print(coloniaOption)
                option_value = value
                break
            elif ratio > mas_similar:
                # print(coloniaOption)
                mas_similar = ratio
                option_value = value
        selectColonias.select_by_value(option_value)

        # Un posible alert puede aparecer
        expectAlert(driver)

        driver.find_element_by_id("u_calle").send_keys(dato["calle"])
        driver.find_element_by_id("u_numero").send_keys(dato["numero_exterior"])
        driver.find_element_by_id("u_numero_int").send_keys(dato["numero_interior"])

        driver.find_element_by_id("continuar_sub").click()
        time.sleep(longWaitTime)

driver.quit()
print("Proceso terminado")
