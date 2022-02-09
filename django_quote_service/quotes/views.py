from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView as GenericDetail, ListView as GenericList
from django.views.generic.edit import (
    CreateView as GenericCreate,
    DeleteView as GenericDelete,
    UpdateView as GenericUpdate,
)
from rules.contrib.views import PermissionRequiredMixin

from .models import CharacterGroup


# Create your views here.


class CharacterGroupListView(LoginRequiredMixin, GenericList):
    """
    Displays Character Groups owned by the user.
    TODO: For now, only user owned groups, we won't bother with public options.
    """

    model = CharacterGroup
    context_object_name = "groups"
    template_name = "quotes/character_group_list.html"
    paginate_by = 15

    def get_queryset(self):
        return CharacterGroup.objects.filter(owner=self.request.user)


class CharacterGroupDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, GenericDetail
):
    """
    Displays details for a character group.
    """

    model = CharacterGroup
    context_object_name = "group"
    template_name = "quotes/character_group_detail.html"
    permission_required = "quotes.read_charactergroup"


class CharacterGroupUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, GenericUpdate
):
    """
    Update an existing character group
    """

    model = CharacterGroup
    context_object_name = "group"
    template_name = "quotes/character_group_create.html"
    permission_required = "quotes.edit_charactergroup"
    fields = ["name", "description", "public"]


class CharacterGroupDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, GenericDelete
):
    """
    Delete and existing character group.
    """

    model = CharacterGroup
    context_object_name = "group"
    template_name = "quotes/character_group_delete.html"
    permission_required = "quotes.delete_charactergroup"


class CharacterGroupCreateView(LoginRequiredMixin, GenericCreate):
    """
    Create a new character group.
    """

    model = CharacterGroup
    template_name = "quotes/character_group_create.html"
    fields = ["name", "description", "public"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
