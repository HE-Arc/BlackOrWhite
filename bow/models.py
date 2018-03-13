# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Camp(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    camp_icon = models.CharField(max_length=50) #icon symbolique du camp

    class Meta:
        #managed = False
        db_table = 'camp'

class Level(models.Model):
    name = models.CharField(max_length=50)
    required_experience = models.IntegerField()

    class Meta:
        #managed = False
        db_table = 'level'

class InventoryCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        #managed = False
        db_table = 'inventory_category'

class Item(models.Model):
    name = models.CharField(max_length=50)
    #required_level = models.CharField(max_length=50)
    vital_energy = models.IntegerField(default= 5)
    strength = models.IntegerField(default= 5)
    defense = models.IntegerField(default=5)
    damages = models.IntegerField(default=25)
    item_icon = models.CharField(max_length=50)
    description = models.TextField()
    cost_chf = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    cost_gold = models.IntegerField(default=0)
    category = models.ForeignKey(InventoryCategory, models.CASCADE, default=-1)
    level = models.ForeignKey(Level, models.CASCADE, default=-1)

    class Meta:
        #managed = False
        db_table = 'item'

class Characters(models.Model):
    name = models.CharField(max_length=50)
    strength = models.IntegerField(default= 5)
    defense = models.IntegerField(default=5)
    speed = models.IntegerField(default=5)
    agility = models.IntegerField(default=5)
    victories = models.IntegerField(default=0)
    fight_count = models.IntegerField(default=0)
    defeat = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    camp = models.ForeignKey(Camp, models.CASCADE, default=-1)
    level = models.ForeignKey(Level, models.DO_NOTHING, default=1)

    class Meta:
        #ordering = ['level']
        #managed = False
        db_table = 'characters'

class CharactersItem(models.Model):
    is_active = models.IntegerField(default=0)
    character = models.ForeignKey(InventoryCategory, models.CASCADE, default=-1)
    item = models.ForeignKey(Item, models.CASCADE, default=-1)

    class Meta:
        #managed = False
        db_table = 'characters_item'
        #Unicité entre un joueur et un item
        unique_together = (('character', 'item'),)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    character = models.OneToOneField(Characters, on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'user_profile'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

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

# Automatique user.profile https://www.turnkeylinux.org/blog/django-profile
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
