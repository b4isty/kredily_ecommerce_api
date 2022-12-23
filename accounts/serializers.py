from django.contrib.auth import get_user_model
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for the signup view.
    """
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

        extra_kwargs = {
            'password': {
                # write only cause we don't want to send the password back
                'write_only': True,
                # input type to password so we can't see it in rest framework api doc
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """
        Override to hash the password before saving the user.
        otherwise password will be saved as plain text in the database.
        """
        user = get_user_model().objects.create_user(**validated_data)
        return user
