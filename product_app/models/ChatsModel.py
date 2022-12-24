from django.db import models


class ChatsModel(models.Model):
    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    title = models.TextField(name="title", help_text="Название чата telegram")
    chat_id = models.TextField(name="chat_id", help_text="ID чата в telegram")

    # Metadata
    class Meta:
        db_table = "chats"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.title} | {self.chat_id}"
