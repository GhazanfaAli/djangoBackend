from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom user model


class UserManager(BaseUserManager):
    def create_user(self, email, name,password=None, password2 = None,bio="" ):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            bio=bio,
          
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,  password=None):
        user = self.create_user(
            email=email,
            name=name,
          
            password=password,  # Ensure correct argument order
    )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True) 
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True) # when account is created
    updated_at = models.DateTimeField(auto_now=True) # when account is updated

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
# ////////////////////////////////////////////////////////// Posts //////////////////////////////////////////////////////////
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    image_url = models.URLField()  # This will store the Cloudinary image URL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}'s Post"    