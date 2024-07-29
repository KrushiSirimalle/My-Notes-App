from flask import Flask, render_template, redirect, request
from db import noteTablesCreate
from db import Note, readAllNotes, createNote
from db import updateNote, readNoteById, deleteNote, search

noteTablesCreate()    #if db not there, creates db. if no table, creates it.
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html',
                menu = 'search')
    elif request.method == 'POST':
        title = request.form['title']
        notes_text = request.form['notes']
        notes = search(title, notes_text)
        for I in range(len(notes)):
            notes[I].sno = I + 1
        return render_template('list.html',
                    notes=notes,
                    menu = 'list')
 

@app.route("/list", methods=["GET"])
def list_notes():
    notes = readAllNotes()
    for I in range(len(notes)):
        notes[I].sno = I+1
    return render_template('list.html', 
            notes = notes,
            menu = 'list')

@app.route("/create", methods=['GET','POST'])
def create_notes():
    note = Note()
    if request.method == 'POST':
        note.title = request.form['title']
        note.notes = request.form['notes']
        createNote(note)
        return redirect('/list')
    elif request.method == 'GET':
        return render_template('create.html', 
                menu = 'create')

@app.route("/list/view/<id>", methods=['GET'])
def view_notes(id):
    note = readNoteById(id)
    return render_template('view.html',
                note=note, 
                menu = 'list')

@app.route("/list/edit/<id>", methods=['GET', 'POST'])
def edit_notes(id):
    note=readNoteById(id)
    if request.method == 'GET':
        return render_template('edit.html', 
                note=note,
                menu = 'edit')
    elif request.method == 'POST':
        note.title = request.form['title']
        note.notes = request.form['notes']
        updateNote(note)
        return redirect('/list')

@app.route("/delete", methods=[ 'POST'])
def delete_notes():
    if request.method == 'POST':
        id = request.form['id']
        deleteNote(id)
        return redirect('/list')