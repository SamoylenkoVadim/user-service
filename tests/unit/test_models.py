from models import User, Email, PhoneNumber


def test_new_user():
    user = User(firstName="firstName", lastName="lastName")
    assert user.firstName == "firstName"
    assert user.lastName == "lastName"


def test_new_email():
    email = Email(mail="firstName@gmail.com")
    assert email.mail == "firstName@gmail.com"


def test_new_phone_number():
    phone_number = PhoneNumber(number="+491674653487")
    assert phone_number.number == "+491674653487"


def test_new_user_with_contacts():
    user = User(firstName="firstName", lastName="lastName")
    email = Email(mail="firstName@gmail.com")
    phone_number = PhoneNumber(number="+491674653487")
    user.emails.extend([email])
    user.phoneNumbers.extend([phone_number])

    assert user.firstName == "firstName"
    assert user.lastName == "lastName"
    assert user.emails == [email]
    assert user.phoneNumbers == [phone_number]



