from flask import Flask
from flask import render_template,request,redirect,url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os


app= Flask(__name__)
app.secret_key="Develoteca"

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='MySql'
app.config['MYSQL_DATABASE_BD']='sistema'
mysql.init_app(app)

CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)


@app.route('/')
def index():

    sql ="USE sistema;"
    sql2 ="SELECT * FROM `empleados`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    cursor.execute(sql2)

    employes=cursor.fetchall()

    #print(employes)
    #print(app.config['CARPETA'])
    #path='/empleados'
    #print(os.getcwd())
    #print(os.path.join(app.config['CARPETA']))
   
    conn.commit()
    return render_template('empleados/index.html',employes=employes)

@app.route('/destroy/<int:id>')
def destroy(id):
    sql ="USE sistema;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    cursor.execute("SELECT photo FROM empleados WHERE id=%s", id)
    fila=cursor.fetchall()

    #os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    #os.remove(os.path.join("C:/SistemaEmpleado/templates/empleados/uploads/",fila[0][0]))
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):
    sql ="USE sistema;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    cursor.execute("SELECT * FROM `empleados` WHERE id=%s;",(id))

    employes=cursor.fetchall()
    print(employes)

    conn.commit()
    return render_template('empleados/edit.html',employes=employes)


@app.route('/update', methods=['POST'])
def update():
    _name=request.form['txtname']
    _email=request.form['txtemail']
    _photo=request.files['txtphoto']
    id=request.form['txtid']

    sql ="USE sistema;"
    sql2 ="UPDATE `empleados` SET `nombre`=%s,`email`=%s WHERE id=%s;"

    datos=(_name,_email,id)

    conn= mysql.connect()
    cursor=conn.cursor()

    now= datetime.now()
    time=now.strftime("%Y%H%M%S")
    cursor.execute(sql)

    if _photo.filename!='':
        newphotoname=time+_photo.filename
        _photo.save("uploads/"+newphotoname)

        cursor.execute("SELECT photo FROM empleados WHERE id=%s", id)
        fila=cursor.fetchall()

        #os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        #os.remove(os.path.join("C:/SistemaEmpleado/templates/empleados/uploads/",fila[0][0]))
        os.remove(os.path.join(os.path.join(app.config['CARPETA'],fila[0][0])))
        cursor.execute("UPDATE empleados set photo =%s WHERE id=%s",(newphotoname,id))
        conn.commit()
    
    cursor.execute(sql2,datos)
    conn.commit()

    return redirect('/')


@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _name=request.form['txtname']
    _email=request.form['txtemail']
    _photo=request.files['txtphoto']

    if _name=='' or _email=='' or _photo=='':
        flash('Remember fill all data')
        return redirect(url_for('create'))

    now= datetime.now()
    time=now.strftime("%Y%H%M%S")

    if _photo.filename!='':
        newphotoname=time+_photo.filename
        #_photo.save("C:/SistemaEmpleado/uploads/"+newphotoname)
        _photo.save("uploads/"+newphotoname)
        datos=(_name,_email,newphotoname)
    else:
        datos=(_name,_email,_photo.filename)


    sql ="USE sistema;"
    sql2 ="INSERT INTO `empleados` (`id`, `nombre`, `email`, `photo`) VALUES (NULL, %s, %s, %s);"

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    cursor.execute(sql2,datos)
    conn.commit()
    #return render_template('empleados/index.html')
    return redirect('/')


if __name__== '__main__':
    app.run(debug=True)
