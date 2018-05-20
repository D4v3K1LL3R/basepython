#-*- coding: utf-8 -*-
from peewee import *
import datetime
from collections import OrderedDict
import sys
import sqlite3

db=SqliteDatabase('diary.db')

class Entry(Model):
    content=TextField()
    timestamp=DateTimeField(default=datetime.datetime.now)
    class Meta:
        database=db

def add_entry():
    """Agregar un registro"""
    print("Introduzca un registro, presione Ctrl+Z y Enter para Terminar")
    data=sys.stdin.read().strip()
    if data:
        if input("Desea Guardar Este Registro) [Y/N]: ").lower()=='y':
            Entry.create(content=data)
            print("SE HA GUARDADO EXITOSAMENTE!")

def view_entries():
    """ver registros"""
    entries=Entry.select().order_by(Entry.timestamp.desc())
    for entry in entries:
        timestamp=entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print("*************************")
        print(entry.content)
        print("n--> Ver el Siguiente Registro")
        print("q--> Salir del Menu")
        next_entry=input("Desea Ver la siguiente entrada? [n/q]").lower().strip()
        if next_entry == 'q':
            break
def delete_entries():
    """eliminar registros"""

def search_entries():
    """BUSCAR COINCIDENCIAS EN LOS REGISTROS"""

    try:
        bd=sqlite3.connect("diary.db")
        cursor=bd.cursor()

        sear=input("Escriba lo que desea buscar: ").strip()
        if not sear:
            print("Busqueda Invalida")
            exit()

        sentence="SELECT * FROM entry WHERE content LIKE ?;"

        cursor.execute(sentence, [ "%{}%".format(sear) ])

        entres=cursor.fetchall()
        print("+{:-<20}+{:-<10}+{:-<50}+".format("", "", ""))
        print("|{:^20}|{:^10}|{:^50}|".format("ID", "Contenido", "Fecha"))
        print("+{:-<20}+{:-<10}+{:-<50}+".format("", "", ""))

        for id, content, timestamp in entres:
            print("|{:^20}|{:^10}|{:^50}|".format(id , content, timestamp))

        print("+{:-<20}+{:-<10}+{:-<50}+".format("", "", ""))

        #print(entres)
    except sqlite3.OperationalError as error:
        print("Error al Abrir", error)

menu=OrderedDict([
    ('a',add_entry),
    ('v',view_entries),
    ('s',search_entries),
])

def menu_loop():
    """Mostrar opciones"""
    choice=None
    while choice!='x':
        print("Presiona 'x' para salir")
        for key, value in menu.items(): #nos permite correr por cada uno de los elementos
            print('{}-->{}'.format(key,value.__doc__))
        choice=input("Elija una opcion: ").lower().strip()#strip elimina espacios o caracteres no deseados
        if choice in menu:
            menu[choice]()


def init():
    db.connect()
    db.create_tables([Entry],safe=True)
if __name__ == '__main__':
    init()
    menu_loop()
