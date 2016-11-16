#!/usr/bin/env python
# -*- coding: utf-8 -*-

__name__="Main"

import cPickle
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

shortWaitTime = 5
longWaitTime = 20
veryLongTime = 45

driver = webdriver.Chrome("D:\chromedriver.exe")
driver.get("https://www.nocnok.com/")
driver.find_element_by_id("js-login").click()
time.sleep(shortWaitTime)
driver.find_element_by_xpath("//*[@id=\"ko-login-form\"]/form/div[2]/div/input").send_keys("francisco_gon18@hotmail.com")
driver.find_element_by_xpath("//*[@id=\"ko-login-form\"]/form/div[3]/div/input").send_keys("880928")
driver.find_element_by_xpath("//*[@id=\"ko-login-form\"]/form/button").click()
time.sleep(shortWaitTime)
driver.find_element_by_xpath("//*[@id=\"Menu\"]/ul[1]/li[4]/a").click()
driver.find_element_by_xpath("//*[@id=\"Menu\"]/ul[1]/li[4]/ul/li[1]/a").click()
time.sleep(longWaitTime)
#Cantidad de paginaciones
total_paginas = driver.find_element_by_xpath("//*[@id=\"RealtySearch\"]/div[4]/div/div[2]/div[3]/span").text
for pagina_actual in range(1,int(total_paginas)+1):
    if pagina_actual>1: #Cambiar de pagina
        driver.get("https://www.nocnok.com/real-estate-agent/realties-admin")
        time.sleep(shortWaitTime)
        driver.find_element_by_xpath(
            "// *[ @ id = \"RealtySearch\"] / div[4] / div / div[2] / div[3] / input").send_keys(
            Keys.SHIFT + Keys.HOME + Keys.DELETE)
        driver.find_element_by_xpath(
            "// *[ @ id = \"RealtySearch\"] / div[4] / div / div[2] / div[3] / input").send_keys(str(pagina_actual))
        driver.find_element_by_xpath(
            "// *[ @ id = \"RealtySearch\"] / div[4] / div / div[2] / div[3] / input").send_keys(Keys.ENTER)
    ids = []
    elems = driver.find_elements_by_css_selector("a.popover-realty.code")
    for elem in elems:
        ids.append(elem.get_attribute("id").replace("realty-code-", ""))
    datos = []
    for id in ids: #elem = elems[0]
        dato = {}
        dato["internalCode"] = id
        driver.get("https://www.nocnok.com/realty/edit?id="+id)
        time.sleep(longWaitTime)
        dato["municipio"] = Select(driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[1]/div[3]/div[2]/select")).first_selected_option.text
        dato["colonia"] = driver.find_element_by_css_selector(".select2-container.select2-container-multi.inputText.recipient-suggest > ul > li.select2-search-choice > div").text
        dato["codigo_postal"] = driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[1]/div[6]/div[2]/input").get_attribute("value")
        dato["calle"] = driver.find_element_by_xpath("// *[ @ id = \"RealtyEditForm\"] / fieldset[1] / div[7] / div[2] / input").get_attribute("value")
        dato["numero_exterior"] = driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[1]/div[8]/div[2]/input").get_attribute("value")
        dato["numero_interior"] = driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[1]/div[9]/div[2]/input").get_attribute("value")
        dato["clave_nocnok"] = driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[1]/div[2]/span").get_attribute("value")
        dato["tipo_inmueble"] = Select(driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[2]/div[2]/select")).first_selected_option.text
        dato["subtipo_inmueble"] = Select(driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[3]/div[2]/select")).first_selected_option.text
        dato["precio"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[5]/div[2]/input").get_attribute("value")
        dato["habitaciones"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[6]/div[2]/input").get_attribute("value")
        dato["baños"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[7]/div[2]/div/div[1]/input").get_attribute("value")
        dato["medioBaños"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[7]/div[2]/div/div[2]/input").get_attribute("value")
        dato["terreno"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[8]/div[2]/div/input").get_attribute("value")
        dato["construccion"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[9]/div[2]/div/input").get_attribute("value")
        dato["niveles"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[12]/div[2]/input").get_attribute("value")
        dato["estacionamiento"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[2]/div[13]/div[2]/input").get_attribute("value")
        dato["descripcion"] =  driver.find_element_by_xpath("//*[@id=\"RealtyEditForm\"]/fieldset[3]/div[1]/div[2]/textarea").get_attribute("value")
        #Boton guardar
        driver.get("https://www.nocnok.com/realty/detail?id=" + id)
        time.sleep(longWaitTime)
        dato["urlFotografia"] =  driver.find_element_by_xpath("// *[ @ id = \"RealtyCarousel\"] / div[1] / div[1] / div / img").get_attribute("src")
        datos.append(dato)

driver.quit()

#Guardamos los datos
cPickle.dump(datos,open("datos.data","w"))
