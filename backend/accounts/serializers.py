from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Token に追加の情報を埋め込む
        token['user_id'] = user.id
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser

        return token
    

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # トークンからユーザを取得
        refresh = RefreshToken(attrs['refresh'])
        user_id = refresh['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise InvalidToken('User not found.')
        
        # トークンを再発行する
        token = AccessToken.for_user(user)
        token['user_id'] = user.id
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser

        data['access'] = str(token)
        return data