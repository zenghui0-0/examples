from django.db import models
from django.contrib.auth.models import AbstractUser

TEAMS = (
    (0, 'others'),
    (1, 'gpu-sw'),
)

# Create your models here.
class Users(AbstractUser):
# Fields inherited from AbstractUser (as seen from MySQL)
# +--------------+--------------+------+-----+---------+----------------+
# | Field        | Type         | Null | Key | Default | Extra          |
# +--------------+--------------+------+-----+---------+----------------+
# | id           | int(11)      | NO   | PRI | NULL    | auto_increment |
# | password     | varchar(128) | NO   |     | NULL    |                |
# | last_login   | datetime(6)  | YES  |     | NULL    |                |
# | is_superuser | tinyint(1)   | NO   |     | NULL    |                |
# | username     | varchar(150) | NO   | UNI | NULL    |                |
# | first_name   | varchar(30)  | NO   |     | NULL    |                |
# | last_name    | varchar(150) | NO   |     | NULL    |                |
# | email        | varchar(254) | NO   |     | NULL    |                |
# | is_staff     | tinyint(1)   | NO   |     | NULL    |                |
# | is_active    | tinyint(1)   | NO   |     | NULL    |                |
# | date_joined  | datetime(6)  | NO   |     | NULL    |                |
    ntid = models.CharField(max_length=64, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    preferred_name = models.CharField(max_length=64, null=True, blank=True)
    teams = models.IntegerField(choices=TEAMS, default=0, null=True, blank=True)