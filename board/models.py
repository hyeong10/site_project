from django.db import models

# Create your models here.

class Board(models.Model):
    password = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_password(self, given_password):
        if self.password != given_password:
            return False
        return True

class Comment(models.Model):
    password = models.CharField(max_length=50, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(null=False)

    def check_password(self, given_password):
        if self.password != given_password:
            return False
        return True