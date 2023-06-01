from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from .models import ReferenceTable, Machine, Maintenance, Reclamation


class LoginRequestSerializer(serializers.Serializer):
    model = User
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class ReferenceTableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReferenceTable
        fields = '__all__'


class ReferenceTableSerializerAnonymous(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ReferenceTable
        fields = ['title']


class MachineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class MachineSerializerAnonymous(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Machine
        fields = ['model', 'model_serial',
                  'engine', 'engine_serial',
                  'transmission', 'transmission_serial',
                  'driving_bridge', 'driving_bridge_serial',
                  'controlled_bridge', 'controlled_bridge_serial']


class MaintenanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'


class ReclamationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reclamation
        fields = '__all__'


@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReferenceTableViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return ReferenceTableSerializer
        else:
            return ReferenceTableSerializerAnonymous

    def get_queryset(self):
        _type = self.request.query_params.get('type')
        if _type is None:
            return ReferenceTable.objects.all()
        else:
            return ReferenceTable.objects.filter(type=_type)


class MachineViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return MachineSerializer
        else:
            return MachineSerializerAnonymous

    def get_queryset(self):
        # выдаем разный queryset в зависимости от авторизованного пользователя
        if not self.request.user.is_authenticated:
            # неавторизованный пользователь
            return Machine.objects.filter(model_serial=self.request.query_params.get('serial', None))
        elif Group.objects.get(name='manager').id in list(self.request.user.groups.values_list('id', flat=True)):
            # user is manager
            return Machine.objects.all()
        else:
            # клиент или сервис для машины
            return Machine.objects.filter(Q(client_user=self.request.user) | Q(service_user=self.request.user))


class MaintenanceViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Maintenance.objects.all()
        else:
            return Maintenance.objects.none()


class ReclamationViewSet(viewsets.ModelViewSet):
    serializer_class = ReclamationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Reclamation.objects.all()
        else:
            return Reclamation.objects.none()


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'referencetable', ReferenceTableViewSet, basename='referencetable')
router.register(r'machine', MachineViewSet, basename='machine')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'reclamation', ReclamationViewSet, basename='reclamation')
