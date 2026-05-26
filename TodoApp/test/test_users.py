from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_users):
    response = client.get('/user/detail')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'shelbytest'
    assert response.json()['email'] == 'shelbytest@email.com'
    assert response.json()['first_name'] == 'Shelby'
    assert response.json()['last_name'] == 'Test'
    assert response.json()['phone_number'] == '+1 555 555 555'
    assert response.json()['role'] == 'admin'

def test_change_password_success(test_users):
    response = client.put('/user/change_password',json={'password':'testpassword','new_password':'newpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_failure(test_users):
    response = client.put('/user/change_password',json={'password':'wrongpassword','new_password':'newpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid Old Password'

def test_change_phone_number_success(test_users):
    response = client.put("user/change_phone?phone_number=+1 555 555 55")
    assert response.status_code == status.HTTP_204_NO_CONTENT