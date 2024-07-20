
def get_email_provider(provider_name, email):
    if provider_name == 'gmail' or provider_name == 'itilite':
        from provider.gmail import GmailProvider
        return GmailProvider(email)
    elif provider_name == 'outlook':
        from provider.outlook import OutlookProvider
        return OutlookProvider()
    else:
        raise ValueError("Unsupported email provider")