def split_email(email_address):
    """Returns a two-item tuple with username and domain.

        string -> tuple of strings"""
    i=0
    for character in email_address:
        if character == '@':
            break
        else:
            i += 1
    user = email_address[:i]
    domain = email_address[i+1:]
    return (user,domain)