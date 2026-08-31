from rest_framework import serializers
from .models import Tutor, Alumno, Clase, Inscripcion, Pago


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__' # Esto le dice que convierta todos los campos de la tabla a JSON

class AlumnoSerializer(serializers.ModelSerializer):
    nombre_tutor = serializers.CharField(source='tutor.nombre_completo', read_only=True, allow_null=True)
    clases_inscritas = serializers.SerializerMethodField()

    class Meta:
        model = Alumno
        fields = [
            'id',
            'nombre_completo',
            'fecha_nacimiento',
            'ha_tomado_clase_prueba',
            'activo',
            'tutor',
            'nombre_tutor',
            'clases_inscritas'
        ]
    def get_clases_inscritas(self, obj):
        inscripciones = Inscripcion.objects.filter(alumno=obj)
        return [inscripcion.clase.nombre for inscripcion in inscripciones]

class ClaseSerializer(serializers.ModelSerializer):
    alumnos_inscritos = serializers.SerializerMethodField()
    lugares_disponibles = serializers.SerializerMethodField()

    class Meta:
        model = Clase
        fields = [
            'id',
            'nombre',
            'capacidad_maxima',
            'alumnos_inscritos',
            'lugares_disponibles'
        ]

    def get_alumnos_inscritos(self, obj):
        inscripciones = Inscripcion.objects.filter(clase=obj, alumno__activo=True)
        return [inscripcion.alumno.nombre_completo for inscripcion in inscripciones]

    def get_lugares_disponibles(self, obj):
        # ¡Aquí estaba el detalle! Cambiamos 'self.get_alumnos_inscritos' por 'Inscripcion.objects.filter'
        inscritos = Inscripcion.objects.filter(clase=obj, alumno__activo=True).count()
        return obj.capacidad_maxima - inscritos

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'

    def validate(self, data):
        alumno = data.get('alumno')
        clase = data.get('clase')
        tipo = data.get('tipo')

        # Buscamos si ya existe una inscripción con este alumno y esta clase
        if Inscripcion.objects.filter(alumno=alumno, clase=clase).exists():
            raise serializers.ValidationError({
                "alumno": f"El alumno ya se encuentra inscrito en la clase de {clase.nombre}."
            })
        
        # Contamos cuántas inscripciones existen para esta clase específica
        inscritos_actuales = Inscripcion.objects.filter(clase=clase).count()
        if inscritos_actuales >= clase.capacidad_maxima:
            raise serializers.ValidationError({
                "clase": f"Esta clase ya ha alcanzado su capacidad máxima de {clase.capacidad_maxima} alumnos."
            })

        # 2. Validación de la Clase de Prueba
        if tipo == 'PRUEBA':
            if alumno.ha_tomado_clase_prueba:
                raise serializers.ValidationError({
                    "tipo": "Operación rechazada: Este alumno ya tomó su clase de prueba gratuita anteriormente."
                })

        return data

    def create(self, validated_data):
        # 3. Automatización del Estado del Alumno
        tipo = validated_data.get('tipo')
        alumno = validated_data.get('alumno')
        
        # Si la inscripción es de prueba y pasó la validación, actualizamos al alumno
        if tipo == 'PRUEBA':
            alumno.ha_tomado_clase_prueba = True
            alumno.save()

        # Finalmente, creamos la inscripción de manera normal
        return super().create(validated_data)

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


