from django.db import models
from login.models import *

# Create your models here.
class CommentManager(models.Manager):
    def valid(me,error_loc,d):
        errors=[]
        V=d['msg_text']
        if not len(V)>=1:
             errors.append(f"{error_loc}|Body must not be empty.")
        return errors

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="received_comments", on_delete = models.CASCADE)
    poster = models.ForeignKey(User, related_name="created_comments", on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=CommentManager()
    def __repr__(self):
        return f"<Comment ({self.id})>"

class SubComment(models.Model):
    parent_comment = models.ForeignKey(Comment, related_name="replies", on_delete = models.CASCADE)
    poster = models.ForeignKey(User, related_name="created_subcomments", on_delete = models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=CommentManager()
    def __repr__(self):
        return f"<Sub-Comment ({self.id})>"