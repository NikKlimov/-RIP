from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class Status(models.Model):
#     name = models.CharField(max_length=30)
    

#     class Meta:
#         managed = True
#         db_table = 'status'



class Applications(models.Model):
    def get_default_user():
        return AuthUser.objects.get(username='Dell')
    DRAFT = "dr"
    DELETED = "de"
    CREATED = "cr"
    FINISHED = "fi"
    CANCELLED = "ca"
    STATUS_CHOICES = [
        (DRAFT, "Черновик"),
        (DELETED, "Удален"),
        (CREATED, "Сформирован"),
        (FINISHED, "Завершен"),
        (CANCELLED, "Отклонен"),
    ]
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True, default=get_default_user)
    status = models.CharField(blank=True, null=True, max_length=30, choices=STATUS_CHOICES, default=DRAFT)
    created_date = models.DateField(auto_now_add=True)
    ended_date = models.DateField(blank=True, null=True)
    modified_date = models.DateField(auto_now=True)
    moderator = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True, related_name="moderated_applications")
    services=models.ManyToManyField('Services', db_table='services_applications',blank=True)

    class Meta:
        managed = False
        db_table = 'applications'

    def __str__(self):
        if self.user is None:
            return str(self.id)
        return self.user.username


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(AbstractUser):
    USER= "US"
    MODERATOR = "MO"
    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
    ]
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    user_role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    class Meta:
        managed = False
        db_table = 'auth_user'
    def __str__(self):
        return self.username


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
        

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Services(models.Model):
    PRODUCT = "pr"
    VALUES = "va"
    MONEY = "mo"
    TRANSPORT = "tr"
    MEDICAL = "me"
    TYPE_CHOICES = [
        (PRODUCT, "Товар"),
        (VALUES, "Ценности"),
        (MONEY, "Деньги"),
        (TRANSPORT, "Транспорт"),
        (MEDICAL, "Мед товары"),
    ]
    name = models.CharField(max_length=50)
    image=models.ImageField(upload_to='images', blank=True, null=True)
    text=models.TextField(max_length=10000)
    type=models.CharField(blank=True, null=True, max_length=30, choices=TYPE_CHOICES)
    price=models.IntegerField()
    published = models.BooleanField(max_length=30, default=True)
    unit = models.CharField(blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'services'
    def __str__(self):
        return str(self.name)
        # return self.name


class ServicesApplications(models.Model):
    services = models.ForeignKey(Services, models.DO_NOTHING, blank=True, null=True)
    applications = models.ForeignKey(Applications, models.DO_NOTHING, blank=True, null=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'services_applications'
    def __str__(self):
        return self.services.name