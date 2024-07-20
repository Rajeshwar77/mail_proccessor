from validator_collection import validators, errors

def validate_email(email):
    try:
        email_address = validators.email(email, allow_empty=False)
    except errors.InvalidEmailError as error:
        print(f"Error: {error}")
        raise ValueError("Invalid email address") from error
    except ValueError as error:
        print(f"Error: {error}")
        raise ValueError("Invalid value") from error
    except Exception as error:
        print(f"Error: {error}")
        raise ValueError("Invalid value") from error
    return email_address