from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class TwitterSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Extends the DefaultSocialAccountAdapter to save users twitter handle
    in the twitter_id field.
    """
    def populate_user(self, request, sociallogin, data):
        username = data.get("username")
        email = data.get("email")
        name = data.get("name")
        try:
            first_name, last_name = name.split(" ")
        except ValueError:
            first_name, last_name = name.split(" ", 1)
        user = sociallogin.user
        user.email = email
        user.twitter_id = username
        user.first_name = first_name
        user.last_name = last_name
        return user
