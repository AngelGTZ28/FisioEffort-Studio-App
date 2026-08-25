from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Creamos el enrutador automático
router = DefaultRouter()

# Registramos nuestras rutas
router.register(r'tutores', views.TutorViewSet)
router.register(r'alumnos', views.AlumnoViewSet)
router.register(r'clases', views.ClaseViewSet)
router.register(r'inscripciones', views.InscripcionViewSet)
router.register(r'pagos', views.PagoViewSet)

# Exponemos las rutas para que el proyecto principal las consuma
urlpatterns = [
    path('', include(router.urls)),
]