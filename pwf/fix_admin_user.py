from django.contrib.auth.models import User

username = 'admin58'
password = 'admin5858'
email = 'admin@email.com'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.email = email
    user.save()
    print(f"Kullanıcı '{username}' admin yapıldı ve şifresi sıfırlandı.")
except User.DoesNotExist:
    User.objects.create_superuser(username, email, password)
    print(f"Yeni admin kullanıcısı '{username}' oluşturuldu.") 