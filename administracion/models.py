from django.db import models

# Create your models here.

from django.db import models

class Tutor(models.Model):
    # Todo cliente, sea niño o adulto, tendrá un tutor asociado para temas de contacto y pagos.
    nombre_completo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo

class Alumno(models.Model):
    # Relación uno a muchos: Un tutor puede tener varios alumnos (ej. una mamá con dos hijas).
    # Si el alumno es adulto, su tutor será él mismo.
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='alumnos')
    nombre_completo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    
    # Aquí está el candado que pidió tu hermana para el historial
    ha_tomado_clase_prueba = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_completo

class Clase(models.Model):
    # El catálogo de disciplinas que imparten
    nombre = models.CharField(max_length=100) # Ej. Ballet, Judo, Entrenamiento Funcional
    profesor = models.CharField(max_length=100)
    capacidad_maxima = models.IntegerField(default=15)
    
    def __str__(self):
        return f"{self.nombre} - {self.profesor}"

class Inscripcion(models.Model):
    # La tabla puente que conecta a los alumnos con las clases
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateField(auto_now_add=True)
    
    TIPO_INSCRIPCION = [
        ('PRUEBA', 'Clase de Prueba'),
        ('REGULAR', 'Mensualidad Regular'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_INSCRIPCION, default='REGULAR')

    def __str__(self):
        return f"{self.alumno.nombre_completo} en {self.clase.nombre}"

class Pago(models.Model):
    # Conectamos el pago a la inscripción específica del alumno en una clase
    inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE, related_name='pagos')

    # max_digits=8 permite hasta 999,999.99 (suficiente para colegiaturas)
    monto = models.DecimalField(max_digits=8, decimal_places=2)

    # Registra automáticamente el día y la hora exacta en que se hace el pago en el sistema
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Para saber qué mes están pagando (ej. "Agosto 2026", "Septiembre 2026")
    mes_cubierto = models.CharField(max_length=50)

    METODO_OPCIONES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia bancaria'),
    ]
    metodo_pago = models.CharField(max_length=20, choices=METODO_OPCIONES, default='EFECTIVO')

    def __str__(self):
        return f"{self.inscripcion.alumno.nombre_completo} - {self.inscripcion.clase.nombre} ({self.mes_cubierto})"