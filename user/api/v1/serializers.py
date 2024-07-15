from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from ...models import User
from rest_framework import serializers

Get_USER = get_user_model()



class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'profile_image']




class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Get_USER
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
        user = Get_USER(
            email=data['email'],
            username=data['username']
        )
        user.set_password(data['password'])
        user.is_active = False
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Get_USER
        fields = (
            "id",
            "email",
            "realname",
            "phone_number",
            "profile_image",
            "location",
            "bio"
        )

    def update(self, instance, validated_data):
        if "profile_image" not in validated_data or not validated_data["profile_image"]:
            validated_data["profile_image"] = instance.profile_image
        return super().update(instance, validated_data)
