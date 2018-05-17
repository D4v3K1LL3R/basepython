from peewee import *

db=SqliteDatabase('students.db')

class Student(Model):
    username=CharField(max_length=255, unique=True)
    points=IntegerField(default=0)

    class Meta:
        database=db

students=[
{'username':'Aldo',
 'points':6},
{'username':'Dave',
 'points':8},
{'username':'Stef',
 'points':9},
{'username':'Willy',
 'points':10},
]

#metodo para añadir estudiantes
def add_students():
    for student in students:
        try:
            #crear registro
            Student.create(username=student['username'],points=student['points'])
        except IntegrityError: #cuando ya exista el registro
            student_records=Student.get(username=student['username'])
            student_records.points=student['points']
            student_records.save()#guarda los cambios
#metodo que obtiene la calificacion más alta
def top_student():
    topcalif=Student.select().order_by(Student.points.desc()).get()
    return topcalif #retorna calificacion

if __name__ == '__main__':
    db.connect()
    db.create_tables([Student],safe=True)
    add_students()
    print('El estudiante con la nota más alta es: {}'.format(top_student().username))
