from .models import CustomUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match'})

        user = CustomUser(
            email=self.validated_data['email'])
        user.set_password(password)

        user.save()
        Token.objects.create(user=user)
        return user


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        password = validated_data['password']

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError(
                    {'error': 'Invalid Credentials'})
        return validated_data
