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
        # Solo inscripciones activas (no las que fueron retiradas/reemplazadas).
        # Devolvemos objetos (no solo el nombre) para que el frontend pueda
        # identificar cada inscripción y ofrecer la opción de "quitar de esta clase".
        inscripciones = Inscripcion.objects.filter(alumno=obj, activa=True).select_related('clase')
        return [
            {
                'inscripcion_id': inscripcion.id,
                'clase_id': inscripcion.clase.id,
                'clase_nombre': inscripcion.clase.nombre,
                'tipo': inscripcion.tipo,
            }
            for inscripcion in inscripciones
        ]

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
        # Solo inscripciones activas de alumnos activos.
        inscripciones = Inscripcion.objects.filter(
            clase=obj, alumno__activo=True, activa=True
        ).select_related('alumno')
        return [
            {
                'inscripcion_id': inscripcion.id,
                'alumno_id': inscripcion.alumno.id,
                'alumno_nombre': inscripcion.alumno.nombre_completo,
            }
            for inscripcion in inscripciones
        ]

    def get_lugares_disponibles(self, obj):
        inscritos = Inscripcion.objects.filter(clase=obj, alumno__activo=True, activa=True).count()
        return obj.capacidad_maxima - inscritos

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'

    def validate(self, data):
        # En actualizaciones parciales (ej. PATCH {"activa": false} para retirar
        # a un alumno de una clase) no siempre vienen 'alumno'/'clase'/'tipo' en
        # el payload. Solo validamos estas reglas de negocio cuando de verdad se
        # está definiendo o cambiando a qué alumno/clase pertenece la inscripción.
        alumno = data.get('alumno', getattr(self.instance, 'alumno', None))
        clase = data.get('clase', getattr(self.instance, 'clase', None))
        tipo = data.get('tipo', getattr(self.instance, 'tipo', None))

        if not alumno or not clase:
            return data

        # Buscamos si ya existe una inscripción ACTIVA con este alumno y esta clase
        inscripciones_activas = Inscripcion.objects.filter(alumno=alumno, clase=clase, activa=True)
        if self.instance:
            inscripciones_activas = inscripciones_activas.exclude(pk=self.instance.pk)
        if inscripciones_activas.exists():
            raise serializers.ValidationError({
                "alumno": f"El alumno ya se encuentra inscrito en la clase de {clase.nombre}."
            })

        # Contamos cuántas inscripciones ACTIVAS existen para esta clase específica
        inscritos_actuales = Inscripcion.objects.filter(clase=clase, activa=True)
        if self.instance:
            inscritos_actuales = inscritos_actuales.exclude(pk=self.instance.pk)
        if inscritos_actuales.count() >= clase.capacidad_maxima:
            raise serializers.ValidationError({
                "clase": f"Esta clase ya ha alcanzado su capacidad máxima de {clase.capacidad_maxima} alumnos."
            })

        # 2. Validación de la Clase de Prueba
        if tipo == 'PRUEBA' and alumno.ha_tomado_clase_prueba:
            # Si esta misma inscripción ya era la clase de prueba registrada,
            # no la rechaces al editarla (ej. al reactivarla).
            es_su_propia_prueba = self.instance is not None and self.instance.tipo == 'PRUEBA'
            if not es_su_propia_prueba:
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
    # Campos de solo lectura para mandar datos limpios al frontend
    alumno_nombre = serializers.CharField(source='inscripcion.alumno.nombre_completo', read_only=True)
    clase_nombre = serializers.CharField(source='inscripcion.clase.nombre', read_only=True)

    class Meta:
        model = Pago
        fields = [
            'id',
            'inscripcion',
            'alumno_nombre',
            'clase_nombre',
            'monto',
            'fecha_registro',
            'mes_cubierto',
            'metodo_pago'
        ]