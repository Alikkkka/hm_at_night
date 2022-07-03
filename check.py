from models import *

result = []
for user in User.query.all():
    result.append(user.to_dict())
    print