from user import models
from user.api import serializers
# Dictionary to map the role to the model usage on the custom jwt authentication
role_to_model = {
    'student': models.Student,
    'coordinator': models.Coordinator,
    'speaker': models.Speaker,
}

serializer_class_map = {
    'Student': serializers.StudentSerializer,
    'Coordinator': serializers.CoordinatorSerializer,
    'Speaker': serializers.SpeakerSerializer,
}