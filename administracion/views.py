from rest_framework import viewsets
from .models import Tutor, Alumno, Clase, Inscripcion, Pago
from .serializers import TutorSerializer, AlumnoSerializer, ClaseSerializer, InscripcionSerializer, PagoSerializer

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.all()
    serializer_class = ClaseSerializer

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all().order_by('-fecha_registro') # Los pagos más recientes primero
    serializer_class = PagoSerializer