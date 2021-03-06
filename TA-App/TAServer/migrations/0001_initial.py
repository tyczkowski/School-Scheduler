# Generated by Django 2.1.2 on 2018-12-14 06:10

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnum', models.CharField(max_length=4)),
                ('dept', models.CharField(max_length=10)),
                ('name', models.CharField(blank=True, default='', max_length=40)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
            ],
            options={
                'permissions': (('can_view_course', 'Can view course data'), ('can_edit_course', 'Can edit course data'), ('can_delete_course', 'Can delete a course'), ('can_create_course', 'Can create courses'), ('can_add_course', 'Cam add a course'), ('can_assign_ins', 'Can assign instructors')),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snum', models.CharField(max_length=4)),
                ('stype', models.CharField(blank=True, choices=[('lab', 'Lab'), ('lecture', 'Lecture'), (None, 'None')], default=None, max_length=10, null=True)),
                ('room', models.IntegerField(blank=True, default=-1, null=True)),
                ('days', models.CharField(blank=True, choices=[('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('H', 'Thursday'), ('F', 'Friday'), ('MW', 'Monday Wednesday'), ('TH', 'Tuesday Thursday'), ('MWF', 'Monday Wednesday Friday'), (None, 'None')], default=None, max_length=5, null=True)),
                ('time', models.CharField(blank=True, default=None, max_length=15, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TAServer.Course')),
            ],
            options={
                'permissions': (('can_create_section', 'Can create sections'), ('can_edit_section', 'Can edit sections'), ('can_delete_section', 'Can delete sections'), ('can_view_section', 'Can view sections'), ('can_assign_ta', "Can assign TA's")),
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('firstname', models.CharField(blank=True, default='', max_length=30)),
                ('lastname', models.CharField(blank=True, default='', max_length=30)),
                ('bio', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.CharField(blank=True, default='', max_length=30)),
                ('role', models.CharField(choices=[('T', 'TA'), ('I', 'Instructor'), ('A', 'Administrator'), ('S', 'Supervisor'), ('D', 'Default')], default='', max_length=13)),
                ('phonenum', models.CharField(blank=True, default='', max_length=10)),
                ('address', models.CharField(blank=True, default='', max_length=30)),
                ('courses', models.ManyToManyField(blank=True, to='TAServer.Course')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('sections', models.ManyToManyField(blank=True, to='TAServer.Section')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('can_create_user', 'Can create users'), ('can_edit_user', 'Can edit users'), ('can_edit_self', 'Can edit users'), ('can_delete_user', 'Can delete users'), ('can_view_user', 'Can view users'), ('can_view_private', 'Can view private user data'), ('can_email_all', 'Can send emails to all users'), ('can_email_tas', 'Can send emails')),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='instructor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='sec', to='TAServer.Section'),
        ),
    ]
