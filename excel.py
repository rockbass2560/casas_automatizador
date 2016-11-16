#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas

excel = pandas.read_excel("C:\Users\Francisco\Downloads\Propiedades-OPORTUNIDADES-INMOBILIARIAS-6671249141(2016-11-16).xlsx")

#datos = [u'Clave', u'Clave Int.', u'Estatus', u'Tiempo Estatus', u'Tiempo Total',
       #u'Interesados', u'Pactada', u'Colaboración', u'Pais', u'Estado',
       #u'Ciudad/Delegación', u'C.P.', u'Latitud', u'Longitud', u'Colonia',
       #u'Calle', u'Num. Ext.', u'Num. Int.', u'Sector', u'Tipo', u'Operación',
       #u'Precio', u'Moneda', u'Hab.', u'Baños', u'M2 Constr.', u'M2 Terreno',
       #u'Fotos']

time_wait = 10

driver = webdriver.Chrome("D:\chromedriver.exe")
driver.get("http://www.casasyterrenospro.com/")
driver.find_element_by_css_selector("input.blue_button.myboton").click()
driver.find_element_by_id("user").send_keys("FRANCISCOGLEZ")
driver.find_element_by_id("pass").send_keys("12345678")
driver.find_element_by_id("botonlogin").click()
driver.implicitly_wait(time_wait)
#probable proceso para agregar las casas
driver.find_element_by_id("ui-accordion-accordion-header-1").click()
driver.find_element_by_xpath("//*[@id=\"ui-accordion-accordion-panel-1\"]/div[2]/ul/li[7]/a").click()