from . models import Shopcart


def cartcount(request):
    reading = Shopcart.objects.filter(user__username = request.user.username, paid=False)

    cartread = 0
    for item in reading:
        cartread += item.quantity

    return {'cartread':cartread}