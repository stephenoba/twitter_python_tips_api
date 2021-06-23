from django.db import models


class Tip(models.Model):
    tweet_id = models.IntegerField("Tweet ID", unique=True, db_index=True)
    full_text = models.CharField(
        "Full Tweet Text", max_length=280)
    num_retweets = models.IntegerField("Number of retweets", db_index=True)
    num_likes = models.IntegerField("Number of likes", db_index=True)
    timestamp = models.DateTimeField("Timestamp")

    def __str__(self):
        return f"Python tip #{self.tweet_id}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Tip'
        verbose_name_plural = 'Tips'


class Link(models.Model):
    tip = models.ForeignKey(
        Tip, on_delete=models.CASCADE, related_name="links")
    url = models.URLField("URL")
    display_url = models.CharField("Display URL", max_length=128)

    def __str__(self):
        return f"Python tip #{self.tip.tweet_id} link"

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'


class Entry(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    python_tip = models.TextField("Python Tip")
    twitter_id = models.CharField("Twitter ID", max_length=50, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    published = models.BooleanField("Published?", default=False)

    def __str__(self):
        return f"Entry {self.id}"

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'
