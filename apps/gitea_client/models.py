from django.db import models


class SovereignRepository(models.Model):
    """
    Cached and tracked metadata of sovereign repositories managed via BantuDevLab.
    Linked optionally to a SovereignOrganization for multi-tenancy.
    """

    organization = models.ForeignKey(
        "core.SovereignOrganization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="repositories",
        help_text="Organisation souveraine de rattachement",
    )
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    html_url = models.URLField()
    clone_url = models.CharField(max_length=512)
    is_private = models.BooleanField(default=False)
    sovereignty_score = models.IntegerField(default=95, help_text="Sovereignty Score (0-100%)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"
