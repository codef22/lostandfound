from core.models import Item


ALLOWED_TRANSITION = {
    Item.Status.OPEN : [
        Item.Status.REVIEWING,
    ],
    Item.Status.REVIEWING : [
        Item.Status.OPEN,
        Item.Status.DELIVERED,
    ],
    Item.Status.DELIVERED : [
        Item.Status.CLOSED,
    ],
    Item.Status.CLOSED : [],
}


def can_transition(item, new_status):

    allowed = ALLOWED_TRANSITION.get(
        item.status,
        []
    )

    return new_status in allowed


def can_create_claim(item, user):
    return (
        item.status == Item.Status.OPEN and
        item.created_by != user
    )
