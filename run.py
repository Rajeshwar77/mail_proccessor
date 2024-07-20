import sys
from utils.validator import validate_email
from utils.config import config
from mail.provider import get_email_provider
from utils.common import log_error, log_debug, log_info

if __name__ == "__main__":
    try:
        # Ensure the user has entered the email address correctly
        counter = 0
        while counter < config.input_max_attempts:
            try:
                # Get dynamic inputs
                if len(sys.argv) > 1 and counter == 0:
                    input_email = sys.argv[1]
                else:
                    input_email = input("Enter the email to process: ")
                email = validate_email(input_email)
                log_info(f"Valid email: {email}")
                break
            except BaseException:
                counter = counter + 1
                print(f" Invalid email. Please try again. You have {config.input_max_attempts - counter} attempts left.")
                if counter == config.input_max_attempts:
                    log_debug("You have exceeded the number of attempts. Exiting the program.")
                # Loop will continue until a valid email is entered
        
        # Process the email
        provider_name = "gmail"

        provider = get_email_provider(provider_name, email)
        email_data = provider.fetch_store_emails()
        # provider.mark_as_read()
    except ImportError as e:
        log_error("Error: Missing required modules. Please ensure all dependencies are installed.", e)
        sys.exit(1)
    except Exception as e:
        log_error(f"An unexpected error occurred: ",e)
        sys.exit(1)
    
    
    