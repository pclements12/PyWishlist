from django.shortcuts import get_object_or_404
from wishlist_app.models import Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


@login_required
@require_POST
def delete(request, comment_id):
    c = get_object_or_404(Comment, pk=comment_id)
    if not request.user == c.commenter:
        raise PermissionDenied("Can't delete someone else's comment")
    c.delete()
    return HttpResponse("comment deleted")
