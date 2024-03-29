from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Fazenda(models.Model):
    """Propriedade rural"""

    codigo = models.CharField(max_length=15)
    nome_fazenda = models.CharField(max_length=255)
    nome_produtor = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    uf = models.CharField(max_length=2)
    area_total = models.IntegerField()
    area_vegetacao = models.IntegerField()
    area_cultura = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_fazenda


class Cultura(models.Model):
    """Culturas plantadas"""

    TIPOS_CULTURA = [
        ("Soja", "Soja"),
        ("Milho", "Milho"),
        ("Algodão", "Algodão"),
        ("Café", "Café"),
        ("Cana", "Cana"),
    ]

    fazenda = models.ForeignKey(
        Fazenda, on_delete=models.CASCADE, related_name="culturas"
    )
    tipo_cultura = models.CharField(max_length=15, choices=TIPOS_CULTURA)
    area = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.area} HA de {self.tipo_cultura}"
