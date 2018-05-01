from django.test import TestCase

# Create your tests here.


from Test_py.apps.registration.models import *


print(Lecturer.objects.values_list('rfid', 'firstName'))
test = [tuple(zip(item.values(), item.values()))[0] for item in Audience.objects.values("audience_id")]
print(test)
