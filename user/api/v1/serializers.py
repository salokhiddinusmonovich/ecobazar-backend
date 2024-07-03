from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password1 does not match Password2')
        return attrs

    def create(self, data):
        user = User(
            email=data['email'],
            username=data['username']
        )
        user.set_password(data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    old_password_again = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, attrs):
        user = self.context['request'].user

        old_password = attrs.get('old_password')
        old_password_again = attrs.get('old_password_again')

        # Validate both old_password and old_password_again
        if old_password != old_password_again:
            raise serializers.ValidationError({"old_password_again": "Old passwords do not match"})

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance