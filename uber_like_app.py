
from tabulate import tabulate
import psycopg2 as pg
import random

host_db = '201.238.213.114' #host que les enviamos
port_db = '54321' # puerto que les enviamos
db_name = 'grupo7' # su base datos ej: grupoXXuser
name_db = 'grupo7' # usario que les mandamos
password = 'dQGu67' #contraseña que les enviamos

conn = pg.connect(dbname=db_name, user=name_db, host=host_db, port=port_db, password=password)

#############################################################################################
########################## funciones ############################################
#############################################################################################

def validar(tabla,var):
    
    sql="select * from "+str(tabla)
    cursor.execute(sql)
    
    for tup in cursor:
        
        if var in tup:
            return True

    return False

def validar_mul(tabla,var):
    
    sql="select * from "+str(tabla)
    cursor.execute(sql)
    
    for tup in cursor:
        c=0
        for num in range(len(var)):

            if var[num] in tup:
                
                c+=1
                
        if c==len(var):
        
            return True
        
    return False

def ver_local():
    
   
    
    id_local = input('Ingrese ID del local: ')
    
    c=0
    
    try:
        id_local=int(id_local)
        
    except:
        c=1
        print('\nID no valido')
        return False
    
    if c==0:
    
        val=validar('locales',id_local)
        
        if val==True:

            return id_local
        
        else:
            print('\nEl ID no existe')
            return False
        

def agregar_local():#### Check
    nombre = input('Ingrese nombre del local: ')
    
    direccion = input('Ingrese direccion del local: ')
    
    sql = "select max(id_local) from locales"
    
    cursor.execute(sql)     
    id_local=cursor.fetchone()

    sql = "INSERT INTO locales (ID_local, nombre, direccion) \
        VALUES ({},'{}','{}')".format(int(id_local[0])+1, nombre, direccion)
    
    cursor.execute(sql)
    conn.commit() 
    print('\nAgregado!') 
    
    return

def editar_local(ID): ## Check
    

    nombre=input('\nIngrese nuevo nombre: ')
    
    sql = "update locales SET nombre = '"+str(nombre)+"' where id_local="+str(ID)+str(';')
    cursor.execute(sql)
    conn.commit() 

    direccion=input('\nIngrese nueva direccion: ')

    sql = "update locales SET direccion = '"+str(direccion)+"' where id_local="+str(ID)+str(';')
    cursor.execute(sql)
    conn.commit() 
    print('\nListo')


    return

def eliminar_local(ID):
    seguro=input('\n¿Esta seguro que desea eliminar el local?\n(1)Si\n(2)No\n\nIngrese opcion:')
    
    if seguro=='1':
        
        sql ="delete from locales where id_local="+str(ID)
        cursor.execute(sql)  
        conn.commit() 
        print('\nListo!')
    
    elif seguro=='2':
        
        return
    
    else:
        print('\nOpcion invalida, intente de nuevo')
        eliminar_local(ID)
    
 
def ver_ped(mail,pedido):
    
    p_t=0
    
    sql="""select t3.nombre, t3.cantidad,t3.precio, t3.descuento, coalesce(p.descuento,0) promocion,(t3.precio-(t3.descuento+coalesce(p.descuento,0)))*t3.cantidad total from
(select t2.id_menu, t2.id_pedido,t2.nombre, t2.cantidad,t2.precio, t2.codigo_promocion codigo , coalesce(d.precio_descuento,0) descuento from 
(select * from
(select m.id_menu ,p.id_pedido, m.nombre, mp.cantidad, m.precio, p.codigo_promocion  FROM pedido p, menus_pedido mp, menus m 
where p.id_pedido="""+str(pedido)+""" and p.id_pedido=mp.id_pedido and mp.id_menu=m.id_menu ) t1
left join descuento_menu using(id_menu)) t2 left join descuento d using(id_descuento)) t3 
left join promociones p using(codigo)"""
        
    cursor.execute(sql)
    print('\nMENUS: ')
    print(tabulate(cursor,headers=['Nombre menu','Cantidad','Precio','Descuento','Promocion', 'total'],tablefmt='fancy_grid'))
    
    cursor.execute(sql)
    cur=cursor.fetchall()
    
    try:
    
        for row in cur:
            
            p_t+=row[5]
            
    except: 
        pass
    
    
    sql="""select t3.nombre, t3.cantidad,t3.precio, t3.descuento, coalesce(p.descuento,0) promocion,(t3.precio-(t3.descuento+coalesce(p.descuento,0)))*t3.cantidad total from
(select t2.id_producto, t2.id_pedido, t2.nombre, t2.cantidad,t2.precio, t2.codigo_promocion codigo , coalesce(d.precio_descuento,0) descuento from 
(select * from
(select m.id_producto ,p.id_pedido, m.nombre_producto nombre, mp.cantidad, m.precio, p.codigo_promocion  FROM pedido p, productos_pedido mp, productos m 
where p.id_pedido="""+str(pedido)+""" and p.id_pedido=mp.id_pedido and mp.id_producto=m.id_producto ) t1
left join descuento_producto using(id_producto)) t2 left join descuento d using(id_descuento)) t3 
left join promociones p using(codigo)"""
      
    
    cursor.execute(sql)
    
    print('\nPRODUCTOS: ')
    
    print(tabulate(cursor,headers=['Nombre producto','Cantidad','Precio','Descuento','Promocion', 'total'],tablefmt='fancy_grid'))
      
    cursor.execute(sql)
    cur=cursor.fetchall()
    
    try:
        for row in cur:
            
            p_t+=row[5]
            
    except:
        pass
    
    sql="select r.nombre, r.vehiculo, r.patente, r.telefono from pedido left join repartidor r using(id_repartidor)\
        where mail_usuario='"+str(mail)+"' and id_pedido="+str(pedido)+""
    
    cursor.execute(sql)
    print('\nREPARTIDOR: ')
    print(tabulate(cursor,headers=['Nombre repartidor','Vehiculo','Patente','Telefono'],tablefmt='fancy_grid'))
    
    print('\nTOTAL DE COMPRA: $',p_t)
    
    n=0
    
    while n not in ['1','2']:
    
        n=input('\n(1) Dar rating al repartidor\n(2) Volver\n\nIngrese opcion: ')
        
        if n=='1':
            
            n2=0
            
            while n2 not in ['1','2','3','4','5']:
                 
                n2=input('\nIngrese rating del 1-5: ')
                 
                if n2 in ['1','2','3','4','5']:
                 
                     sql="update pedido set rating="+str(n2)+" where id_pedido = "+str(pedido)+""
                     cursor.execute(sql)
                     conn.commit()
                     
                     print('\nListo!')
                     
                else:
                    print('\nValor no valido')

        elif n=='2':
            pass
        
        elif n not in  ['1','2']:
            print('\nOpcion no valida')
    
    return
    
    
#############################################################################################
########################## main code ############################################
#############################################################################################


cursor = conn.cursor()

sql = 'SELECT mail From usuarios limit 1'
cursor.execute(sql)
a=cursor.fetchone()

v=True

while v==True:
  
    print('\n(1) Iniciar secion\n(2) Registrarse\n(3) Cerrar programa')
    opcion=input('Ingrese opcion: ')
    
    if opcion=='1':
        
        u=False
        while u == False:
            
            print('\nIniciar sesion, ingrese mail y clave:')
            mail=input('Mail: ')                                        
            contraseña=input('Clave: ')
            
            sql = 'SELECT mail, clave From usuarios'
            cursor.execute(sql) 
            
            for usuario in cursor:
                
                if mail==usuario[0] and contraseña == usuario[1]:
                    print('\nIngresado!')
                    u=True
                    break
                
            if u==False:
                print('\nUsuario y/o clave incorrecto(s)!')
                break
            
            menu=True
            
            menus_pedido=[]
            productos_pedido=[]
            
            carrito=[]
            direccion='No seleccionada'
            rial_promo='null'
            rial_descuento=0
            
            while menu==True:
                
                print('\n(1) Locales\n(2) Categorias\n(3) Promociones\n(4) Direcciones',
                      '\n(5) Carrito\n(6) Historial\n(7) Repartidores\n(8) Cerrar secion')
                            
                opcion4=input('Ingrese opcion: ')

##################  LOCALES   ################################3
                    
                if opcion4=='1':    
                    
                    while u == True:
                        
                        sql = 'SELECT id_local, nombre, direccion From locales order by id_local'
                        cursor.execute(sql) 
                        print(tabulate(cursor,headers=['ID','nombre','direccion'],tablefmt='fancy_grid'))
                        
                        print('\n(1) Ver local\n(2) Agregar local\n(3) Volver al menu principal')
                        opcion2=input('Ingrese opcion: ')
                        
                        sql = 'SELECT id_local, nombre, direccion From locales order by id_local'
                        cursor.execute(sql) 
                        
                        
                        if opcion2 == '1':
                            
                            id_local=ver_local()
                           
                            
                            if id_local != False: 
                                
                                in_loc=True
                                
                                while in_loc==True:
                                    
                                    
                                    print('\n(1) Editar local\n(2) Eliminar local\n(3) Ver menus\n(4) Ver productos',
                                          '\n(5) Categorias\n(6) Favoritos\n(7) Rating\n(8) Volver')
                                    
                                    opcion3=input('\nIngrese opcion: ')
                                
                                    if opcion3=='1':
                                        
                                        editar_local(id_local)
                                    
                                    elif opcion3=='2':
                                        
                                        eliminar_local(id_local)
                                    
                                    elif opcion3=='3':
                                        
                                        menus=True
                                        
                                        while menus==True:
                                        
                                            sql="select nombre,precio from menus where id_local="+str(id_local)
                                            cursor.execute(sql)  
                                        
                                            print(tabulate(cursor,headers=['Nombre','Precio'],showindex=True,tablefmt='fancy_grid'))
                                            
                                            print('\n(1) Ver menu\n(2) Agregar nuevo menu\n(3) Volver')
                                    
                                            opcionm=input('\nIngrese opcion: ')
                                            
                                            if opcionm=='1':
                                                
                                                menue=input('\nIngrese numero de menu: ')
                                                
                                                
                                                sql="select nombre ,precio from menus where id_local="+str(id_local)
                                                cursor.execute(sql)
                                                
                                                me=0
                                                
                                                try:
                                                    
                                                    menue=int(menue)
                                                    
                                                    menuex=cursor.fetchall()
                                                    
                                                    
                                                    if menue >= 0 and menue < len(menuex):
                                                        
                                                        me=1
                                                      
                                                    else:
                                                        print('\nMenu no valido')
                                               
                                                except:
                                                    
                                                    print('\nMenu no valido')
                                                    
                                                if me==1:
                                                    
                                                    inmen=True
                                                    
                                                    sql="select id_menu from menus where id_local="+str(id_local)+" limit "+str(menue+1)+" offset "+str(menue)
                                                    cursor.execute(sql)
                                                    id_menu=cursor.fetchone()
                                                    
                                                    id_menu=id_menu[0]
                                                    
                                                    while inmen==True:
                                                    
                                                        sql="select p.nombre_producto from\
                                                            (select * from menus left join productos_menu using(id_menu)\
                                                             where id_menu="+str(id_menu)+") t1\
                                                            left join productos p using(id_producto)"
                                                        cursor.execute(sql)
                                                        print(tabulate(cursor,headers=['Nombre productos'],showindex=True,tablefmt='fancy_grid'))
                                                    
                                                        sql="select coalesce(precio_descuento,0) from \
                                                            (select * from menus left join descuento_menu using(id_menu) where id_menu="+str(id_menu)+") t1\
                                                            left join descuento using(id_descuento)"
                                                        
                                                        cursor.execute(sql)
                                                        print(tabulate(cursor,headers=['Descuento menu'],showindex=True,tablefmt='fancy_grid'))
                                                    
                                                        print('\n(1) Agregar menu a carrito\n(2) Eliminar producto de menu\n(3) Editar menu',
                                                              '\n(4) Eliminar menu\n(5) Descuento\n(6) Volver')
                                        
                                                        opcioninmen=input('\nIngrese opcion: ')
                                                        
                                                        if opcioninmen=='1':
                                                            
                                                            menus_pedido.append(id_menu)
                                                            
                                                            sql="select nombre, cantidad, precio, descuento, 0, precio-descuento total from \
                                                                (select nombre, precio, cantidad, coalesce(precio_descuento,0) descuento from\
                                                                (select nombre, precio, 1 cantidad, id_descuento  from menus left\
                                                                 join descuento_menu using(id_menu)\
                                                                where id_menu="+str(id_menu)+") t1 left join descuento using(id_descuento)) t2"
                                                                    
                                                                    
                                                            cursor.execute(sql)
                                                            cursorl=cursor.fetchone()
                                                            precarro=[]
                                                            
                                                            for r in cursorl:
                                                                precarro.append(r)
                                                            
                                                            carrito.append(precarro)
                                                            print('\nAgregado\n')
                                                                
                                                        
                                                        elif opcioninmen=='2':
                                                            
                                                            productoel=input('\nIngrese numero de producto a eliminar: ')
                                                
                                                
                                                            sql="select p.nombre_producto from\
                                                            (select * from menus left join productos_menu using(id_menu)\
                                                             where id_menu="+str(id_menu)+") t1\
                                                            left join productos p using(id_producto)"
                                                            cursor.execute(sql)
                                                            
                                                            pel=0
                                                            
                                                            try:
                                                                
                                                                productoel=int(productoel)
                                                                
                                                                productoex=cursor.fetchall()
                                                                
                                                                
                                                                if productoel >= 0 and productoel < len(productoex):
                                                                    
                                                                    pel=1
                                                                  
                                                                else:
                                                                    print('\nProducto no valido')
                                                           
                                                            except:
                                                                
                                                                print('\nProducto no valido')
                                                                
                                                            if pel==1:
                                                                
                                                                sql="select id_p_m from menus left join productos_menu using(id_menu)\
                                                                    where id_menu="+str(id_menu)+" limit "+str(productoel+1)+" offset "+str(productoel)
                                                                    
                                                                cursor.execute(sql)
                                                                id_p_m=cursor.fetchone()
                                                                
                                                                sql="delete from productos_menu where id_p_m="+str(id_p_m[0])
                                                                cursor.execute(sql)
                                                                conn.commit()
                                                                print('\nEliminado\n')
                                                                
                                                        elif opcioninmen=='3':
                                                            
                                                            nombrem=input('\nIngrese nuevo nombre: ')
                                                            preciom=input('\nIngrese nuevo precio: ')
                                                            desc=input('\nIngrese nueva descripcion: ')
                                                            ñ=0
                                                            
                                                            try:
                                                                preciom=int(preciom)
                                                                ñ=1
                                                                
                                                            except:
                                                                print('\nPrecio no valido')
                                                            
                                                            if ñ==1:
                                                                sql="update menus set nombre='"+str(nombrem)+"', precio="+str(preciom)+", descripcion='"+str(desc)+"' where id_menu="+str(id_menu)
                                                                cursor.execute(sql)
                                                                conn.commit()
                                                                print('\nListo\n')
                                                                inmen=False
                                                            
                                                        elif opcioninmen=='4':
                                                            
                                                            sql="delete from menus where id_menu="+str(id_menu)
                                                            cursor.execute(sql)
                                                            conn.commit()
                                                            print('\nListo')
                                                        
                                                        elif opcioninmen=='5':
                                                            
                                                            sql="select coalesce(id_descuento,0) from menus left join descuento_menu using(id_menu)\
                                                                where id_menu="+str(id_menu)
                                                                
                                                            cursor.execute(sql)
                                                            
                                                            dsn=cursor.fetchone()
                                                            dsn=dsn[0]
                                                            
                                                            if int(dsn)==0:
                                                                
                                                                preciod=input('\nIngrese precio de descuento: ')
                                                                g=0
                                                                try:
                                                                    preciod=int(preciod)
                                                                    
                                                                    g=1
                                                                except:
                                                                    print('\nPrecio no valido\n')
                                                                    g=0
                                                                    
                                                                if g==1:
                                                                    sql="select max(id_descuento) from descuento"
                                                                    cursor.execute(sql)
                                                                    id_desc=cursor.fetchone()
                                                                    
                                                                    
                                                                    sql = "INSERT INTO descuento (ID_descuento,porcentaje_descuento,precio_descuento) \
                                                                        VALUES ({},{},{})".format(id_desc[0]+1,0,preciod)
                                                
                                                                    cursor.execute(sql)
                                                                    conn.commit()
                                                                    
                                                                    sql = "INSERT INTO descuento_menu (ID_menu,id_descuento) \
                                                                        VALUES ({},{})".format(id_menu,id_desc[0]+1)
                                                
                                                                    cursor.execute(sql)
                                                                    conn.commit()
                                                                    
                                                                    print('\nAgregado\n')
                                                                   
                                                            else:
                                                                
                                                                sql="delete from descuento where id_descuento ="+str(dsn)
                                                                
                                                                cursor.execute(sql)
                                                                conn.commit()
                                                        
                                                        elif opcioninmen=='6':
                                                            inmen=False
                                                        
                                                        elif opcioninmen not in ['1','2','3'',4'',5','6']:
                                                            print('\nOpcion no valida')
                                                    
                                            elif opcionm=='2':
                                                
                                                nombrem=input('\nIngrese nombre del menu:')
                                                descm=input('\nIngrese descripcion del menu:')
                                                preciom=input('\nIngrese precio del menu:')
                                                
                                                np=0
                                                
                                                try:
                                                    int(preciom)
                                                    np=1
                                                except:
                                                    print('\nPrecio no valido')
                                                    
                                                if np==1:
                                                    
                                                    sql="select max(id_menu) from menus"
                                                    cursor.execute(sql)
                                                    id_nmenu=cursor.fetchone()
                                                    
                                                    sql = "INSERT INTO menus (ID_menu,ID_local,precio,descripcion, nombre) \
                                                    VALUES ({},{},{},'{}','{}')".format(id_nmenu[0]+1,id_local,preciom,descm, nombrem)
                                                
                                                    cursor.execute(sql)
                                                    conn.commit() 
                                                    print('\nAgregado!') 
                                             
                                            elif opcionm=='3':
                                                
                                                menus=False
                                            
                                            elif opcionm not in ['1','2','3']:
                                                
                                                print('\nOpcion no valida')
        
        
                                    elif opcion3=='4':
                                        
                                        productos=True
                                        
                                        while productos==True:
                                        
                                            sql="select nombre_producto ,precio from productos where id_local="+str(id_local)
                                            cursor.execute(sql)  
                                        
                                            print(tabulate(cursor,headers=['Nombre','Precio'],showindex=True,tablefmt='fancy_grid'))
                                            print('\n(1) Ver producto\n(2) Agregar nuevo producto\n(3) Volver')

                                            opcionp=input('\nIngrese opcion: ')
                                            
                                            if opcionp=='1':
                                                
                                                productoe=input('\nIngrese numero de producto: ')
                                                
                                                
                                                sql="select nombre_producto ,precio from productos where id_local="+str(id_local)
                                                cursor.execute(sql)
                                                
                                                pe=0
                                                
                                                try:
                                                    
                                                    productoe=int(productoe)
                                                    
                                                    productoex=cursor.fetchall()
                                                    
                                                    
                                                    if productoe >= 0 and productoe < len(productoex):
                                                        
                                                        pe=1
                                                      
                                                    else:
                                                        print('\nProducto no valido')
                                               
                                                except:
                                                    
                                                    print('\nProducto no valido')
                                                    
                                                if pe==1:
                                                    pro1=0
                                                    
                                                    sql="select id_producto from productos where id_local=\
                                                            "+str(id_local)+" limit "+str(productoe+1)+" offset "+str(productoe)
                                                        
                                                    cursor.execute(sql)
                                                    
                                                    id_producto=cursor.fetchone()
                                                    
                                                    id_producto=id_producto[0]
                                                    
                                                    while pro1 != '6':
                                                        
                                                
                                                    
                                                        sql="select nombre, precio, coalesce(precio_descuento,0) descuento, precio-coalesce(precio_descuento,0) total from\
                                                            (select nombre_producto nombre, precio, id_descuento from productos left join\
                                                            descuento_producto using(id_producto) where id_local="+str(id_local)+" and id_producto="+str(id_producto)+") t1 left join \
                                                            descuento using(id_descuento)"
                                                        cursor.execute(sql) 
                                                        print(tabulate(cursor,headers=['Nombre producto','Precio','Descuento','Total'],tablefmt='fancy_grid'))
                                                            
                                                        print('\n(1) Agregar a carrito\n(2) Agregar a menu\n(3) Editar producto\
                                                              \n(4) Eliminar producto\n(5) Descuento\n(6) Volver')
                                                              
                                                        pro1=input('\nIngrese opcion: ')
                                                        
                                                        if pro1=='1':
                                                            
                                                            productos_pedido.append(id_producto)
                                                            
                                                            sql="select nombre,1, precio, coalesce(precio_descuento,0) descuento, 0, precio-coalesce(precio_descuento,0) total from\
                                                            (select nombre_producto nombre, precio, id_descuento from productos left join\
                                                            descuento_producto using(id_producto) where id_local="+str(id_local)+" and id_producto="+str(id_producto)+") t1 left join \
                                                            descuento using(id_descuento)"
                                                            cursor.execute(sql) 
                                                            
                                                            cursorl=cursor.fetchone()
                                                            precarro=[]
                                                            
                                                            for r in cursorl:
                                                                precarro.append(r)
                                                            
                                                            carrito.append(precarro)
                                                            print('\nAgregado\n')
                                                        
                                                        elif pro1=='2':
                                                            
                                                            
                                                            sql="select nombre from menus where id_local="+str(id_local)
                                                            cursor.execute(sql)
                                                            print(tabulate(cursor,headers=['Nombre menu'],showindex=True,tablefmt='fancy_grid'))
                                                            
                                                            p_m=input('\nIngrese el menu al que se agregara: ')
                                                            
                                                            pe=0
                                                            
                                                            sql="select nombre from menus where id_local="+str(id_local)
                                                            cursor.execute(sql)
                                                            
                                                            try:
                                                                
                                                                p_m=int(p_m)
                                                                
                                                                p_mx=cursor.fetchall()
                                                                
                                                                
                                                                if p_m >= 0 and p_m < len(p_mx):
                                                                    
                                                                    pe=1
                                                                  
                                                                else:
                                                                    print('\nMenu no valido\n')
                                                           
                                                            except:
                                                                
                                                                print('\nMenu no valido\n')
                                                                
                                                            if pe==1:
                                                                
                                                                sql="select max(id_p_m) from productos_menu"
                                                                cursor.execute(sql)
                                                                id_p_m=cursor.fetchone()
                                                                id_p_m=id_p_m[0]
                                                                
                                                                sql="select * from menus where id_local="+str(id_local)+" limit "+str(p_m+1)+" offset "+str(p_m)
                                                                cursor.execute(sql)
                                                                p_m=cursor.fetchone()
                                                                p_m=p_m[0]
                                                                
                                                                sql = "INSERT INTO productos_menu (ID_p_m, ID_producto, id_menu) \
                                                                VALUES ({},{},{})".format(id_p_m+1,id_producto,p_m)
                                                            
                                                                cursor.execute(sql)
                                                                conn.commit() 
                                                                print('\nAgregado\n') 
                                                            
                                                            
                                                        elif pro1=='3':
                                                            
                                                            nombrem=input('\nIngrese nuevo nombre: ')
                                                            preciom=input('\nIngrese nuevo precio: ')
                                                            
                                                            ñ=0
                                                            
                                                            try:
                                                                preciom=int(preciom)
                                                                ñ=1
                                                                
                                                            except:
                                                                print('\nPrecio no valido\n')
                                                            
                                                            if ñ==1:
                                                                sql="update productos set nombre_producto='"+str(nombrem)+"', precio="+str(preciom)+" where id_producto="+str(id_producto)
                                                                cursor.execute(sql)
                                                                conn.commit()
                                                                print('\nListo\n')
                                                                inmen=False
                                                        
                                                        elif pro1=='4':
                                                            
                                                            sql="delete from productos where id_producto="+str(id_producto)
                                                            cursor.execute(sql)
                                                            conn.commit()
                                                            print('\nListo\n')
                                                            
                                                            pro1='6'
                                                            
                                                        elif pro1=='5':
                                                            
                                                            sql="select coalesce(id_descuento,0) from productos left join descuento_producto using(id_producto)\
                                                                where id_producto="+str(id_producto)
                                                                
                                                            cursor.execute(sql)
                                                            
                                                            dsn=cursor.fetchone()
                                                            dsn=dsn[0]
                                                            
                                                            if int(dsn)==0:
                                                                
                                                                preciod=input('\nIngrese precio de descuento: ')
                                                                g=0
                                                                try:
                                                                    preciod=int(preciod)
                                                                    
                                                                    g=1
                                                                except:
                                                                    print('\nPrecio no valido\n')
                                                                    g=0
                                                                
                                                                if g==1:
                                                                    sql="select max(id_descuento) from descuento"
                                                                    cursor.execute(sql)
                                                                    id_desc=cursor.fetchone()
                                                                    
                                                                    
                                                                    sql = "INSERT INTO descuento (ID_descuento,porcentaje_descuento,precio_descuento) \
                                                                        VALUES ({},{},{})".format(id_desc[0]+1,0,preciod)
                                                
                                                                    cursor.execute(sql)
                                                                    conn.commit()
                                                                    
                                                                    sql = "INSERT INTO descuento_producto (ID_producto,id_descuento) \
                                                                        VALUES ({},{})".format(id_producto,id_desc[0]+1)
                                                
                                                                    cursor.execute(sql)
                                                                    conn.commit()
                                                                    
                                                                    print('\nAgregado\n')
                                                                    
                                                            else:
                                                                
                                                                sql="delete from descuento where id_descuento ="+str(dsn)
                                                                
                                                                cursor.execute(sql)
                                                                conn.commit()
                                                        
                                                        elif pro1=='6':
                                                            pass
                                                        
                                                        elif pro1 not in ['1','2','3','4','5','6']:
                                                            print('\nOpcion no valida\n')
                                                        
                                                          
                                            elif opcionp=='2':
                                                
                                                nombrep=input('\nIngrese nombre del producto: ')
                                                preciop=input('\nIngrese precio del producto: ')
                                                
                                                np=0
                                                
                                                try:
                                                    int(preciop)
                                                    np=1
                                                except:
                                                    print('\nPrecio no valido')
                                                    
                                                if np==1:
                                                    
                                                    sql="select max(id_producto) from productos"
                                                    cursor.execute(sql)
                                                    id_nproducto=cursor.fetchone()
                                                    
                                                    sql = "INSERT INTO productos (ID_producto,ID_local,precio, nombre_producto) \
                                                    VALUES ({},{},{},'{}')".format(id_nproducto[0]+1,id_local,preciop, nombrep)
                                                
                                                    cursor.execute(sql)
                                                    conn.commit() 
                                                    print('\nAgregado!') 
                                            
                                            elif opcionp=='3':
                                                
                                                productos=False
                                            
                                            elif opcionp not in ['1','2','3']:
                                                
                                                print('\nOpcion no valida')
            
                                    
                                    elif opcion3=='5':
                                        
                                        cate=True
                                        
                                        while cate==True:
                                        
                                            sql="select c.nombre from\
                                                (select l.id_local, l.nombre nombre, cl.id_categoria from locales l left join categorias_local cl using(id_local)) t1\
                                                left join categorias c using(id_categoria)\
                                                where t1.id_local="+str(id_local)
                                                
                                            cursor.execute(sql)
                                            print(tabulate(cursor,headers=['Local','Categoria'],showindex=True,tablefmt='fancy_grid'))
                                            
                                            print('\n(1) Agregar categoria\n(2) Eliminar categoria\n(3) Volver')
                                            op_cate=input('\nIngrese opcion: ')
                                            
                                            try:
                                                op_cate=int(op_cate)
                                                
                                                if op_cate==1:
                                                    
                                                    sql="select nombre from categorias where nombre not in \
                                                        (select nombre from categorias left join categorias_local\
                                                         using(id_categoria) where id_local="+str(id_local)+")"
                                                            
                                                    cursor.execute(sql)
                                                    print(tabulate(cursor,headers=['Categoria'],showindex=True,tablefmt='fancy_grid'))
                                                    
                                                    agr_cat=input('\n¿Que numero de categoria desea agregar?: ')
                                                    
                                                    try:
                                                        agr_cat=int(agr_cat)
                                                        
                                                        sql="select nombre from categorias where nombre not in \
                                                        (select nombre from categorias left join categorias_local\
                                                         using(id_categoria) where id_local="+str(id_local)+")"
                                                            
                                                        cursor.execute(sql)
                                                        catego=cursor.fetchall()
                                                        
                                                        nombre_cat=catego[agr_cat][0]
                                                        
                                                        sql="select id_categoria from categorias where nombre='"+str(nombre_cat)+"'"
                                                        
                                                        cursor.execute(sql)
                                                        id_new_cat=cursor.fetchone()
     
                                                        sql="INSERT INTO categorias_local (id_categoria, id_local) \
                                                            VALUES ({},{})".format(id_new_cat[0],id_local)
                                                            
                                                        cursor.execute(sql)
                                                        conn.commit()
                                                    
                                                    except:
                                                        print('\nCategoria no valida\n')
                                                    
                                                    
                                                elif op_cate==2:
                                                    
                                                    el_cat=input('\n¿Que numero de categoria desea eliminar?: ')
                                                    
                                                    try:
                                                        el_cat=int(el_cat)
                                                        
                                                        sql="select c.nombre from\
                                                            (select l.id_local, l.nombre nombre, cl.id_categoria from locales l left join categorias_local cl using(id_local)) t1\
                                                            left join categorias c using(id_categoria)\
                                                            where t1.id_local="+str(id_local)
                                                            
                                                        cursor.execute(sql)
                                                        catego=cursor.fetchall()
                                                        
                                                        nombre_cat=catego[el_cat][0]
                                                        
                                                        sql="select id_categoria from categorias where nombre='"+str(nombre_cat)+"'"
                                                        
                                                        cursor.execute(sql)
                                                        catego=cursor.fetchall()
                                                        
                                                        id_categor=catego[0][0]
                                                        
                                                        sql="delete from categorias_local where id_local="+str(id_local)+"\
                                                            and id_categoria="+str(id_categor)
                                                            
                                                        cursor.execute(sql)
                                                        conn.commit()
                                                        
                                                    except:
                                                        print('\nCategoria no valida\n')
                                                    
                                                elif op_cate==3:
                                                    cate=False
                                                
                                                elif op_cate not in [1,2,3]:
                                                    print('\nOpcion no valida')
                                                
                                            except:
                                                print('\nOpcion no valida')
                                          
                                    elif opcion3=='6':
                                        
                                        sql="select * from favoritos where mail_usuario='"+str(mail)+"'\
                                            and id_local = "+str(id_local)
                                        cursor.execute(sql)
                                        fav=cursor.fetchone()
                                        
                                        if fav is None:
                                            
                                            sql="INSERT INTO favoritos (mail_usuario, id_local) \
                                                VALUES ('{}',{})".format(mail,id_local)
                                            cursor.execute(sql)
                                            conn.commit()
                                            print('\nAgregado')
                                                
                                        elif fav[0] == mail:
                                            
                                            sql="delete from favoritos where id_local ="+str(id_local)
                                            cursor.execute(sql)
                                            conn.commit()
                                            print('\nEliminado')
                                            
                                        sql="select f.mail_usuario, l.nombre from locales l left join favoritos f using(id_local) where f.mail_usuario='"+str(mail)+"'"
                                        cursor.execute(sql)
                                        print(tabulate(cursor,headers=['Usuario','Local'],showindex=True,tablefmt='fancy_grid'))
                                         
                                        input('\nPresione cualquier tecla: ')
                                    
                                    elif opcion3=='7':
                                        
                                        ratin=True
                                        
                                        while ratin==True:
                                            
                                            sql="select r.mail_usuario, l.nombre, r.rating from locales l left join rating_locales r using(id_local) where mail_usuario= '"+str(mail)+"'\
                                                and id_local ="+str(id_local)
                                                
                                            cursor.execute(sql)
                                            print(tabulate(cursor,headers=['Usuario','Local', 'rating'],showindex=False,tablefmt='fancy_grid'))
                                             
                                            rat=input('\n¿Que rating desea darle a este local?: ')
                                            
                                            r=0
                                            
                                            try:
                                                rat=int(rat)
                                                
                                                if rat>=1 and rat<=5:
                                                    
                                                    ratin=False
                                                    r=1
                                     
                                                else:
                                                    print('\nValores no validos, deben ser entre 1 y 5')
                                                
                                            except:
                                                print('\nRating no valido')
                                                
                                            if r==1:
                                                
                                                sql="select r.rating from locales l left join rating_locales r using(id_local) where mail_usuario= '"+str(mail)+"'\
                                                and id_local ="+str(id_local)
                                                
                                                cursor.execute(sql)
                                                ratin=cursor.fetchone()
                                                
                                                
                                                try:
                                                    ratin=ratin[0]
                                                    int(ratin)
                                                    
                                                    sql="update rating_locales set rating= "+str(rat)+"\
                                                        where id_local ='"+str(id_local)+"' and mail_usuario ='"+str(mail)+"'"
                                                    cursor.execute(sql)
                                                    conn.commit()
                                                    print('\nListo\n') 
                                                    
                                                except:
                                                    sql="INSERT INTO rating_locales (mail_usuario, id_local, rating) \
                                                        VALUES ('{}',{},{})".format(mail,id_local,rat)
                                                    cursor.execute(sql)
                                                    conn.commit()
                                                    print('\nListo\n')
                                                    
                                    elif opcion3=='8':
                                        
                                        in_loc=False
                                    
                                    elif opcion3 not in ['1','2','3','4','5','6','7','8']:
                                        
                                        print('\nOpcion no valida')
                            
                        elif opcion2 == '2':###Check
            
                            agregar_local()
                        
                        elif opcion2 == '3': ### Check
                            u=False
                        
                        elif opcion2 not in ['1','2','3']: ##Check
                            print('\nOpcion no valida')
              
                    u=True

#############      LOCALES    ###########################
                    
#############        CATEGORIAS    ##################### Check
       
                if opcion4=='2':
                    
                    c=False
                    
                    while c==False:
                    
                        sql = "SELECT * From categorias"
                        cursor.execute(sql) 
                        print(tabulate(cursor,headers=['ID','Nombre de categoria'],tablefmt='fancy_grid'))
                            
                        print('\n(1) Agregar categoria\n(2) Editar categoria\n(3) Eliminar categoria\n(4) Volver al menu principal')
                            
                        op_cat=input('\nIngrese opcion: ')
                        
                        
                        if op_cat=='1':
                                
                            n_c=input('\nIngrese nombre de categoria: ')
                            
                            sql = "select max(id_categoria) from categorias"
    
                            cursor.execute(sql)     
                            id_cat=cursor.fetchone()
                            
                            sql = "INSERT INTO categorias (id_categoria,nombre) \
                                    VALUES ({},'{}')".format(id_cat[0]+1,n_c)
        
                            cursor.execute(sql)
                            conn.commit() 
                            print('\nAgregado!') 
                            
                        if op_cat=='2':
                            
                            id_cat=input('\nIngrese ID de categoria: ')
                            
                            l=0
                            
                            try:
                                id_cat=int(id_cat)
                                
                            except:
                                l=1
                                print('\nID invalido1')
                                
                            if l==0:
                            
                                tabla='categorias'
                                
                                if validar(tabla,id_cat)==True:
                                    
                                    nom=input('\nIngrese nuevo nombre: ')
                                    sql = "update categorias set nombre='"+str(nom)+"' where id_categoria='"+str(id_cat)+"'"
                                    cursor.execute(sql)
                                    conn.commit()
                                    print('\nListo!')
                                
                                elif validar(tabla,id_cat)!=True:
                                    
                                    print('\nID invalido2')
                        
                        elif op_cat=='3':
                            
                            id_cat=input('\nIngrese ID de categoria: ')
                            l2=0
                            
                            try:
                                id_cat=int(id_cat)
                                
                            except:
                                
                                l2=1
                        
                            if l2==0:
                            
                                tabla='categorias'
                                
                                if validar(tabla,id_cat)==True:
                                
                                    sql = "delete from categorias where id_categoria='"+str(id_cat)+"'"
                                    cursor.execute(sql)
                                    conn.commit()
                                    print('\nListo!')
                                
                                elif validar(tabla,id_cat)!=True:
                                    
                                    print('\nOpcion no valida')
          
                        elif op_cat=='4':
                            c=True
                        
                        elif op_cat not in ['1','2','3']:
                            print('\nOpcion no valida')
                            
###############     CATEGORIAS    ################################ Check
         
###############     PROMOCIONES   ################################ Check 

                if opcion4=='3':
                
                    prom=0
 
                    while prom!='4':
                    
                        sql = "SELECT codigo, descuento*cantidad From promociones "
                        cursor.execute(sql)  
                        print(tabulate(cursor,headers=['Codigo','Descuento'],showindex=True,tablefmt='fancy_grid'))

                        print('\n(1) Agregar promocion nueva\n(2) Agregar promocion a cuenta\n(3) Eliminar promocion\n(4) Volver al menu principal')

                        prom=input('\nIngrese opcion: ')
                        
                        if prom == '1':
                            
                            c=0
                            
                            n_prom=input('\nIngrese nombre de promocion: ')
                            descuento=input('\nIngrese descuento: ') 
                            print('\nIngrese fecha caducidad')
                            
                            dia=input('\nDia: ')
                            mes=input('\nMes: ')
                            año=input('\nAño: ')
                            
                            cantidad=input('\nIngrese cantidad de veces a usar : ')
                            desc=input('\nIngrese descripcion de la promocion: ')
                            
                            try:
                                tabla='promociones'
                                val=validar(tabla,n_prom)
                                
                                if val==True:
                                    c=1
                                    print('\nOpcion no valida, nombre ya existente\n')
                                    
                                b=int(dia)
                                
                                if b<0 or b>31:
                                    
                                    c=1
                                    print('\nOpcion no valida, dia invalido\n')
                                    
                                b=int(mes)
                                
                                if b<0 or b>12:
                                    
                                    c=1
                                    print('\nOpcion no valida, mes invalido\n')
                                
                                b=int(año)
                                b=int(cantidad)
                                b=int(descuento)
                            
                            except:
                                c=1
                                print('\nOpcion no valida, fecha, cantidad o descuento invalido\n')
                  
                            if c!=1:
                            
                                sql="INSERT INTO promociones(codigo,descuento,fecha_caducidad,cantidad, descripcion)\
                                    VALUES ('{}',{},'{}',{},'{}')".format(n_prom,descuento,dia+'/'+mes+'/'+año, cantidad, desc)
                            
                                cursor.execute(sql)
                                conn.commit()
            
                        elif prom == '2':
                            
                            c=0
                            n_prom=input('\nIngrese nombre de promocion: ')  
                            
                            
                            tabla='promociones'
                            var=validar(tabla,n_prom)
                            
                            if var!=True:
                                c=1
                                print('\nOpcion no valida, la promocion no existe\n')
                            
                            tabla='promociones_usuarios'
                            val=validar_mul(tabla,[n_prom,mail])
                            
                            if val==True:
                                c=1
                                print('\nOpcion no valida, el usuario ya tiene esta promocion\n')
       
                            if c!=1:
                                
                                sql="INSERT INTO promociones_usuarios(codigo,usuario)\
                                VALUES ('{}','{}')".format(n_prom,mail)
                            
                                cursor.execute(sql)
                                conn.commit()
                                
                                sql = "SELECT * From promociones_usuarios where usuario='"+str(mail)+"'"
                                cursor.execute(sql)    
                                print(tabulate(cursor,headers=['Codigo','Usuario'],showindex=True,tablefmt='fancy_grid'))
                                
                                print('\nListo!')
                                
                                _=input('\nPresione cualquier tecla: ')
                                
                          
                        elif prom=='3':
                            
                            el_promo=input('\nIngrese numero de promocion a eliminar: : ')
                            el_pro=0
                            
                            sql = "SELECT * From promociones "
                            cursor.execute(sql)  

                            try:
                                el_promo=int(el_promo)
                                
                                lar_prom=cursor.fetchall()
                                
                                if el_promo >= 0 and el_promo < len(lar_prom):
                                    el_pro=1
                                
                                else:
                                    print('\nOpcion no valida')
                                
                            except:
                                print('\nOpcion no valida')
                                
                            if el_pro==1:
                                
                                sql="select codigo from promociones limit "+str(el_promo+1)+" offset "+str(el_promo)
                                cursor.execute(sql)
                                codigo=cursor.fetchone()
                                codigo=codigo[0]
                                
                                sql="delete from promociones where codigo='"+str(codigo)+"'"
                                cursor.execute(sql)
                                conn.commit()
                                
                                print('\nListo\n')
                        
                        elif prom=='4':
                            pass
                        
                        elif prom not in ['1','2','3']:
                            print('\nOpcion no valida')
                
##################  PROMOCIONES  ################################Check
                
##################   DIRECCIONES ################################# 

                if opcion4=='4':
                    
                    direccion=False
                    
                    while direccion==False:
                    
                        sql = "SELECT * From direccion where mail_usuario='"+str(mail)+"'"
                        cursor.execute(sql) 
                        print(tabulate(cursor,headers=['Nombre de direccion','Mail','Region','Comuna','Calle','Numero','Depto/block'],showindex=True,tablefmt='fancy_grid'))
                        
                        print('\n(1) Ver direccion\n(2) Agregar direccion\n(3) Volver al menu principal')
                        
                        op_dir=input('\nIngrese opcion: ')
                        
                        if op_dir=='1':
                            
                            dire=input('\nIngrese posicion de direccion: ')
                            sql = "SELECT * From direccion where mail_usuario='"+str(mail)+"'"
                            cursor.execute(sql) 
                            
                            d=0
                            
                            try:
                                dire=int(dire)
                                len_dire=cursor.fetchall()
                                
                                if dire >= 0 and dire < len(len_dire):
                                    
                                    d=1
                                    
                                else:
                                    print('\nDireccion no valida\n')
                                
                            except:
                                print('\nDireccion no valida\n')
                                
                            if d==1:
                                
                                op=0
                                
                                while op!='3':
                                    
                                    sql = "SELECT * From direccion where mail_usuario='"+str(mail)+"' limit "+str(dire+1)+" offset "+str(dire)
                                    cursor.execute(sql) 
                                    print(tabulate(cursor,headers=['Nombre de direccion','Mail','Region','Comuna','Calle','Numero','Depto/block'],showindex=True,tablefmt='fancy_grid'))
                                    sql = "SELECT id_direccion From direccion where mail_usuario='"+str(mail)+"' limit "+str(dire+1)+" offset "+str(dire)
                                    cursor.execute(sql) 
                                    var=cursor.fetchone()
                                    var=var[0]
                                    
                                    print('\n(1) Editar direccion\n(2) Eliminar direccion\n(3) Volver')
        
                                    op=input('\nIngrese opcion: ')
                                    
                                    if op=='1':
                                        
                                        n_n=input('\nIngrese nuevo nombre de direccion: ')
                                        region=input('\nIngrese nueva region: ')
                                        comuna=input('\nIngrese nueva comuna: ')
                                        calle=input('\nIngrese nueva calle: ')
                                        numero=input('\nIngrese nuevo numero: ')
                                        depto=input('\nIngrese nuevo depto/block: ')
                                        
                                        c=0
                                        
                                        try:
                                            numero=int(numero)
                                            
                                        except:
                                            print('\nNumero de direccion agregado no valido\n')
                                            c=1
                                        
                                        if c==0:
                                            
                                            sql = "update direccion set region='"+str(region)+"' where id_direccion='"+str(var)+"'"
                                            cursor.execute(sql)
                                            conn.commit() 
                                            
                                            sql = "update direccion set comuna='"+str(comuna)+"' where id_direccion='"+str(var)+"'"
                                            cursor.execute(sql)
                                            conn.commit()             
                                            
                                            sql = "update direccion set calle='"+str(calle)+"' where id_direccion='"+str(var)+"'"
                                            cursor.execute(sql)
                                            conn.commit()             
                                            
                                            sql = "update direccion set numero="+str(numero)+" where id_direccion='"+str(var)+"'"
                                            cursor.execute(sql)
                                            conn.commit()             
                                            
                                            sql = "update direccion set depto_block='"+str(depto)+"' where id_direccion='"+str(var)+"'"
                                            cursor.execute(sql)
                                            conn.commit()  
                                            
                                            sql = "update direccion set ID_direccion='"+str(n_n)+"' where id_direccion='"+str(var)+"'"
                                            cursor.execute(sql)
                                            conn.commit() 
                            
                                            print('\nListo!')
                                            
                                    elif op=='2':
                                        
                                        sql = "delete from direccion where id_direccion='"+str(var)+"'"
                                        cursor.execute(sql)
                                        conn.commit()             
                                        
                                        
                                        print('\nListo!')
                                        
                                        op='3'
                                        
                                    
                                    elif op=='3':
                                        
                                        pass
                                        
                                    
                                    elif op not in ['1','2','3']:
                                        print('\nOpcion no valida')
                            
                            
                        elif op_dir=='2':
                            
                            n_n=input('\nIngrese nombre de direccion: ')
                            region=input('\nIngrese region: ')
                            comuna=input('\nIngrese comuna: ')
                            calle=input('\nIngrese calle: ')
                            numero=input('\nIngrese numero: ')
                            depto=input('\nIngrese depto/block: ')
                            
                            l3=0
                            
                            try:
                                numero=int(numero)                    
                            
                            except:
                                l3=1
                                print('\nNumero de direccion invalido')
                            
                            
                            if l3==0:
                            
                                sql = "INSERT INTO direccion (id_direccion, mail_usuario, region, comuna, calle, numero, depto_block) \
                                        VALUES ('{}','{}','{}','{}','{}',{},'{}')".format(n_n, mail, region, comuna, calle, numero, depto)
        
                                cursor.execute(sql)
                                conn.commit() 
                                print('\nAgregado!') 
                        
                        elif op_dir=='3':
                            direccion=True
                        
                        elif op_dir not in ['1','2','3']:
                            print('\nOpcion no valida')
                            
######################    DIRECCIONES   ############################# 

######################   CARRITO     #########################

                elif opcion4=='5':
                    
                    car=True
                    
                    while car==True:
                        for n in carrito:
                                    
                            n[5]=n[5]+n[4]
                            n[4]=rial_descuento
                            n[5]=n[5]-n[4]
                        
                        precio=0
                                
                        for c in carrito:
                        
                            precio+=c[5]
                            
                        dir_tot=[]
                        dir_tot.append(direccion)
                        dir_tot.append(precio)
                        dir_tot1=[]
                        dir_tot1.append(dir_tot)
                        
                        print('\nCARRITO:')
                        print(tabulate(carrito,headers=['Nombre item','Cantidad','Precio P/U','Descuento','Promocion','Precio total item'],showindex=True,tablefmt='fancy_grid'))
                        
                        print(tabulate(dir_tot1,headers=['Direccion','Precio total'],showindex=False,tablefmt='fancy_grid'))
                        print('\n(1) Eliminar item\n(2) Vaciar carrito\n(3) Elegir promocion\n(4) Elegir direccion\n(5) Confirmar pedido\n(6) Volver al menu principal')
                        op_car=input('\nIngrese opcion: ')
                        
                        if op_car=='1':
                            el=input('\n¿Que numero quiere eliminar?: ')
                            
                            try:
                                carrito.pop(int(el))
                                
                            except:
                                print('\nNumero no valido')
              
                        elif op_car=='2':
                            carrito=[]
                            print('\nListo!')
                        
                        elif op_car=='3':
                            
                            sql="select pu.codigo, p.descuento from promociones_usuarios pu left join promociones p using(codigo) where usuario ='"+str(mail)+"'"
                            cursor.execute(sql)
                            print(tabulate(cursor,headers=['Promocion','Descuento'],showindex=True,tablefmt='fancy_grid'))
                            
                            pro=input('\nIngrese numero de promocion: ')
                            
                            sql="select pu.codigo, p.descuento from promociones_usuarios pu left join promociones p using(codigo) where usuario ='"+str(mail)+"'"
                            cursor.execute(sql)
                            
                            p=0
                            
                            try:
                                
                                pro=int(pro)
                                
                                prom=cursor.fetchall()
                                
                                if pro >= 0 and pro < len(prom):
                                    
                                    p=1
                                  
                                else:
                                    print('\nPromocion no valida')
                           
                            except:
                                
                                print('\nPromocion no valida')
                                
                            
                            if p==1:
                                sql="select pu.codigo, p.descuento from promociones_usuarios pu left join promociones p using(codigo) where usuario ='"+str(mail)+"' limit "+str(pro+1)+" offset "+str(pro)
                                cursor.execute(sql)
                                rial_prom=cursor.fetchone()
                                
                                rial_promo=rial_prom[0]
                                rial_descuento=rial_prom[1]
                          
                        elif op_car=='4':
                            
                            sql="select id_direccion,region,comuna,calle,numero,depto_block from direccion where\
                                mail_usuario='"+str(mail)+"'"
                                
                            cursor.execute(sql)
                            print(tabulate(cursor,headers=['Direccion','Region','Comuna','Calle','Numero','Depto/Block'],showindex=True,tablefmt='fancy_grid'))
                        
                            dir1=input('\nIngrese posicion de direccion: ')
                        
                            sql="select id_direccion,region,comuna,calle,numero,depto_block from direccion where\
                                mail_usuario='"+str(mail)+"'"
                            
                            cursor.execute(sql)
                            
                            p=0
                            
                            try:
                                
                                dir1=int(dir1)
                                
                                prom=cursor.fetchall()
                                
                                if dir1 >= 0 and dir1 < len(prom):
                                    
                                    p=1
                                  
                                else:
                                    print('\nPosicion de direccion no valida')
                           
                            except:
                                
                                print('\nPosicion de direccion no valida')
                                
                            
                            if p==1:
                                
                                sql="select id_direccion from direccion where\
                                mail_usuario='"+str(mail)+"' limit "+str(dir1+1)+" offset "+str(dir1)
                                
                                cursor.execute(sql)
                                direccion=cursor.fetchone()
                                direccion=direccion[0]
                                
                        elif op_car=='5':
                            
                            if direccion != 'No seleccionada':
                            
                                sql="select id_repartidor from repartidor"
                                cursor.execute(sql)
                                
                                repartidor1=cursor.fetchall()
                                repar=[]
                                
                                for r in repartidor1:
                                    repar.append(r[0])
                                    
                                repartidor=random.choice(repar)
                                
                                sql="select max(id_pedido) from pedido"
                                cursor.execute(sql)
                                id_n_pedido=cursor.fetchone()
                                id_n_pedido=id_n_pedido[0]
                                
                                if rial_promo != 'null':
                                    
                                    sql= "INSERT INTO pedido (id_pedido, mail_usuario, direccion_usuario, ID_repartidor, codigo_promocion,  precio)  \
                                        VALUES ({},'{}','{}',{},'{}',{})".format(id_n_pedido+1,mail,direccion,repartidor,rial_promo,precio)
                                
                                else:
                                    
                                    sql= "INSERT INTO pedido (id_pedido, mail_usuario, direccion_usuario, ID_repartidor,  precio)  \
                                        VALUES ({},'{}','{}',{},{})".format(id_n_pedido+1,mail,direccion,repartidor,precio)
                                
                                cursor.execute(sql)
                                conn.commit()
                                
                                for m in menus_pedido:
                                    
                                    sql= "INSERT INTO menus_pedido (id_menu,id_pedido,cantidad)  \
                                    VALUES ({},{},{})".format(m,id_n_pedido+1,1)
                                    cursor.execute(sql)
                                    conn.commit()
                                    
                                for p in productos_pedido:
                                    
                                    sql= "INSERT INTO productos_pedido (id_producto,id_pedido,cantidad)  \
                                    VALUES ({},{},{})".format(p,id_n_pedido+1,1)
                                    cursor.execute(sql)
                                    conn.commit()
                                
                                carrito=[]
                                
                                print('\nConfirmado\n')
                                
                            else:
                                print('\nSeleccione direccion antes de pedir\n')
                        
                        elif op_car=='6':
                            car=False
                        
                        elif op_car not in ['1','2','3','4','5','6']:
                            print('\nOpcion no valida')
                            
########################## CARRITO    ############################

##########################  HISTORIAL   ######################## Check
                
                elif opcion4=='6':
                    
                    historial=False
                    
                    while historial==False:
                    
                        sql = "SELECT id_pedido, direccion_usuario, fecha, precio From pedido where mail_usuario='"+str(mail)+"'"
                        cursor.execute(sql) 
                        print(tabulate(cursor,headers=['ID','Direccion','Fecha','Precio'],showindex=False,tablefmt='fancy_grid'))
                        
                        print('\n(1) Ver pedido\n(2) Volver al menu principal')
                        
                        op_dir=input('\nIngrese opcion: ')
                        
                        if op_dir=='1':
                            
                            id_ped=input('\nIngrese ID de pedido: ')
                            
                            g=0
                            
                            try:
                                id_ped=int(id_ped)
                                
                            except:
                                print('\nValor no valido')
                                g=1
                                
                            if g==0:
                            
                                sql="select id_pedido from pedido where mail_usuario='"+str(mail)+"'"
                                cursor.execute(sql) 
                                cur=cursor.fetchall()
                                
                                val=False
                                
                                for row in cur:
                                    
                                    if id_ped==row[0]:
                                        val=True
                                
                                
                                if val == True:
                                    
                                        ver_ped(mail,id_ped)
                                
                                elif val != True:
                                    
                                    print('\nValor no valido')
                        
                        elif op_dir=='2':
                            historial=True
                        
                        elif op_dir not in ['1','2']:
                            print('\nOpcion no valida')                    

############################ HISTORIAL ####################   Check     

###########################   REPARTIDORES  ########################

                elif opcion4=='7':
                    
                    rep=False
                    
                    while rep==False:
                    
                        sql = "SELECT id_repartidor, nombre, patente From repartidor"
                        cursor.execute(sql) 
                        print(tabulate(cursor,headers=['ID','Nombre','Patente'],showindex=False,tablefmt='fancy_grid'))
                        
                        print('\n(1) Ver repartidor\n(2) Agregar repartidor\n(3) Volver al menu principal')
                        
                        op_rep=input('\nIngrese opcion: ')
                        
                        if op_rep=='1':
                            
                            var=input('\nIngrese ID_repartidor: ')
                            val=False
                            
                            try:
                                id_rep=int(var)
                                
                                tabla='repartidor'
                            
                                val=validar(tabla, id_rep)
                                
                                if val==False:
                                    print('\nID invalido')
                                
                                
                            except:
                                print('\nID invalido')
                                
                            
                            if val==True:
                                    
                                    rep2=False
                                    
                                    while rep2==False:
                                    
                                        sql = "SELECT * From repartidor where id_repartidor="+str(id_rep)
                                        cursor.execute(sql) 
                                        print(tabulate(cursor,headers=['ID','Nombre','Vehiculo','Patente','Telefono'],showindex=False,tablefmt='fancy_grid'))
                            
                                        print('\n(1) Editar repartidor\n(2) Eliminar repartidor\n(3) Volver')
                            
                                        op_rep2=input('\nIngrese opcion: ')
                                        
                                        if op_rep2=='1':
                                            
                                            n_r=input('\nIngrese nuevo nombre del repartidor: ')
                                            ve=input('\nIngrese nuevo vehiculo: ')
                                            pat=input('\nIngrese nueva patente: ')
                                            tel=input('\nIngrese nuevo telefono: ')
                                            
                                            vr=0
                                            
                                            try:
                                                int(tel)
                                            
                                            except:
                                                vr=1
                                                print('\nTelefono no valido')
                                                
                                            if vr==0:
                                                
                                                sql = "update repartidor set nombre='"+str(n_r)+"' where id_repartidor="+str(id_rep)
                                                cursor.execute(sql)
                                                conn.commit() 
                                                
                                                sql = "update repartidor set vehiculo='"+str(ve)+"' where id_repartidor="+str(id_rep)
                                                cursor.execute(sql)
                                                conn.commit() 
                                                
                                                sql = "update repartidor set patente='"+str(pat)+"' where id_repartidor="+str(id_rep)
                                                cursor.execute(sql)
                                                conn.commit() 
                                                
                                                sql = "update repartidor set telefono="+str(tel)+" where id_repartidor="+str(id_rep)
                                                cursor.execute(sql)
                                                conn.commit() 
                                        
                                        elif op_rep2=='2':
                                            
                                            sql="delete from repartidor where id_repartidor="+str(id_rep)
                                            cursor.execute(sql)
                                            conn.commit()
                                            print('\nListo!')
                                            rep2=True
                                        
                                        elif op_rep2=='3':
                                            rep2=True
                                        
                                        elif op_rep2 not in ['1','2','3']:
                                            print('\nOpcion no valida\n')
                            
                        
                        elif op_rep=='2':
                            
                            n_r=input('\nIngrese nombre del repartidor: ')
                            ve=input('\nIngrese vehiculo: ')
                            pat=input('\nIngrese patente: ')
                            tel=input('\nIngrese telefono: ')
                            
                            sql = "select max(id_repartidor) from repartidor"
    
                            cursor.execute(sql)     
                            id_rep=cursor.fetchone()
                            
                            c=0
                            
                            try:
                                int(tel)
                                
                            except:
                                c=1
                                print('\nOpcion no valida, el telefono no es un numero')
                            
                            if c==0:
                            
                                sql = "INSERT INTO repartidor (id_repartidor, nombre, vehiculo, patente, telefono) \
                                        VALUES ({},'{}','{}','{}',{})".format(id_rep[0]+1, n_r, ve, pat, tel)
        
                                cursor.execute(sql)
                                conn.commit() 
                                print('\nAgregado!') 

                        elif op_rep=='3':
                            rep=True
                            
                        elif op_rep not in ['1','2','3']:
                            print('\nOpcion no valida\n')


############################   REPARTIDORES  ##########################

############################   CERRAR SECION  ######################### Check
                
                elif opcion4=='8':
                    
                    menu=False
                    
############################   CERRAR SECION  ######################### Check
                    
                elif opcion4 not in ['1','2','3','4','5','6','7','8']:
                    print('\nOpcion no valida')

################# de aqui a abajo no te preocupes ################## Check
            
    elif opcion=='2':
        
        e=False
        vrr=0
        while e == False and vrr != '1':
            
            
            
            nombre = input('Ingrese nombre: ')
            mail = input('Ingrese mail: ')
            clave = input('Ingrese clave: ')
            telefono = input('Ingrese telefono: ')
            
            t=0
            
            try:
                int(telefono)
            
            except:
                print('\nTelefono no valido')
                t=1
                vrr=input('\n(1) Volver\n(2) Intentarlo de nuevo\n\nIngrese opcion: ')
            
            if t==0:
            
                sql = 'SELECT mail, telefono From usuarios'
                cursor.execute(sql)
                
                e=True
                
                for usuario in cursor:
    
                    if usuario[0]==mail:
                        print('\nEste mail ya esta inscrito, prueba de nuevo.')
                        e=False
                        vrr=input('\n(1) Volver\n(2) Intentarlo de nuevo\n\nIngrese opcion: ')
                        break
                    
                    if int(usuario[1])==int(telefono):
                        print('\nEste telefono ya esta inscrito, prueba de nuevo.')
                        e=False
                        vrr=input('\n(1) Volver\n(2) Intentarlo de nuevo\n\nIngrese opcion: ')
                        break
            
            if e == True:
                
                sql = "INSERT INTO usuarios (mail, nombre, telefono, clave) \
                    VALUES ('{}','{}',{},{})".format(mail, nombre, telefono, clave)
                
                cursor.execute(sql)
                conn.commit() 
                
                print('\nInscrito con exito!')          
            
    elif opcion=='3':
        v=False
        
    else:
        print('\nOpcion no valida')

        
print('\nHasta pronto!')

conn.close()