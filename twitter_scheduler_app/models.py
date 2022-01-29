from datetime import timedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Credential(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="credential",
    )
    api_key = models.TextField(null=True, blank=True, default=None)
    api_key_secret = models.TextField(null=True, blank=True, default=None)
    bearer_token = models.TextField(null=True, blank=True, default=None)
    access_token = models.TextField(null=True, blank=True, default=None)
    access_token_secret = models.TextField(null=True, blank=True, default=None)
    client_id = models.TextField(null=True, blank=True, default=None)
    client_secret = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.user.email


class PostStatus(models.TextChoices):
    SCHEDULED = 'SH', _('SCHEDULED')
    SENT = 'S', _('SENT')
    FAILED = 'F', _('FAILED')


class Post(models.Model):
    content = models.TextField()

    # This ID is what twitter saves as ID and returns when posted update. 
    # This will be used when posting in parent thread.
    twitter_post_id = models.PositiveIntegerField(null=True, blank=True, db_index=True, editable=False)
    twitter_response = models.TextField(null=True, blank=True, default=None)

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, related_name="posts")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="children")
    status = models.CharField(
        max_length=2,
        choices=PostStatus.choices,
        default=PostStatus.SCHEDULED,
    )

    sent_at = models.DateTimeField(null=True, blank=True, db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    schedule = models.DateTimeField(blank=True, db_index=True)
    # auxiliary fields below. Priority: Schedule, hours_from_parent, hours_from_now
    hours_from_parent = models.PositiveIntegerField(null=True, blank=True)
    hours_from_now = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.content[:50]

    def save(self,  *args, **kwargs):
        # schedule logic
        now = timezone.now()
        if self.parent_id and self.parent_id == self.id:
            raise ValueError("Self parent")
        if self.status == PostStatus.SENT and now - self.sent_at > timedelta(seconds=10):
        	raise ValueError("Post already sent")
        elif self.status == PostStatus.SCHEDULED:
            if not self.schedule or self.schedule <= now:
                if self.hours_from_parent:
                    if self.parent:
                        self.schedule = self.parent.schedule + timedelta(hours=self.hours_from_parent)
                    else:
                        raise ValueError("No parent speficified")
                elif self.hours_from_now:
                    self.schedule = now + timedelta(hours=self.hours_from_now)
                    if self.parent and self.schedule < self.parent.schedule:
                        self.schedule = self.parent.schedule
                elif self.schedule:
                    self.schedule = self.schedule + timedelta(minutes=2)
                    if self.schedule <= now:
                        raise ValueError("Schedule is earlier time")
                else:
                    raise ValueError("Schedule is empty")

        super(Post, self).save(*args, **kwargs)

    def try_sending(self):
        import tweepy
        credential = self.user.credential
        auth = tweepy.OAuthHandler(credential.api_key, credential.api_key_secret)
        auth.set_access_token(credential.access_token, credential.access_token_secret)
        api = tweepy.API(auth)
        kwargs = {"status": self.content}
        if self.parent:
            if not self.parent.twitter_post_id:
                self.parent.try_sending()
            kwargs["in_reply_to_status_id"] = self.parent.twitter_post_id

        try:
            response = api.update_status(**kwargs)
            if response.id:
                self.twitter_post_id = response.id
                self.sent_at = timezone.now()
                self.status = PostStatus.SENT
            else:
                self.status = PostStatus.FAILED
            self.twitter_response = response.__dict__
        except Exception as e:
            self.status = PostStatus.FAILED
            self.twitter_response = e.__dict__
        finally:
            self.save()


    @classmethod
    def posts_to_send(cls):
        return cls.objects.filter(schedule__lte=timezone.now(), status=PostStatus.SCHEDULED)

    @classmethod
    def send_scheduled_posts(cls):
        for post in cls.posts_to_send():
            post.try_sending()
