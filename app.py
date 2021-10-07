from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
db = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biblioteca'

@app.route('/')
def index():
    datos = db.connection.cursor()
    datos.execute('SELECT id_libro, libro, c_autor.autor from c_libro, c_autor where c_libro.autor = c_autor.id_autor')
    books = datos.fetchall()
    datos.execute('SELECT * from c_autor')
    authors = datos.fetchall()
    datos.close()
    return render_template('index.html', books=books, authors=authors)

@app.route('/createBook', methods=['POST'])
def createBook():
    cursor = db.connection.cursor()
    if request.method == 'POST':
        book = request.form['libro']
        author = request.form['autor']
        cursor.execute('INSERT INTO c_libro(libro, autor) values(%s, %s)',(book, author))
        cursor.connection.commit()
        cursor.close()
        print(book, author)
        return redirect('/')
    else:
        return render_template('index.html')

@app.route('/infoBook/<int:id_b>', methods=['GET'])
def infoBook(id_b):
    cursor = db.connection.cursor()
    getBook = cursor.execute("SELECT * FROM c_libro where id_libro = {}".format(id_b))
    getBook = cursor.fetchone()
    getAuthors = cursor.execute("SELECT * FROM c_autor")
    getAuthors = cursor.fetchall()
    cursor.close()
    return render_template('update.html', bookInfo=getBook, authors=getAuthors)

@app.route('/updateBook/<int:id_b>', methods=['POST'])
def updBook(id_b):
    cursor = db.connection.cursor()

    if request.method == 'POST':
        book = request.form['libro']
        author = request.form['autor']
        cursor.execute('UPDATE c_libro SET libro = %s, autor = %s where id_libro = %s',(book, author, id_b))
        cursor.connection.commit()
        cursor.close()
        return redirect('/')
    else:
        return render_template('index.html', id_book=id_b)

@app.route('/deleteBook/<int:id_b>')
def delBook(id_b):
    cursor = db.connection.cursor()
    cursor.execute('DELETE FROM c_libro where id_libro = {}'.format(id_b))
    cursor.connection.commit()
    cursor.close()
    return redirect('/')
    



if __name__ == '__main__':
    app.run(debug=True)