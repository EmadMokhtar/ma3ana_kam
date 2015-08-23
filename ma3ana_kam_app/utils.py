from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_model(model, page, per_page=10):
    '''
    return
    :param model:
    :param page:
    :param per_page:
    :return: slice of model data according to page and per page
    '''
    paginator = Paginator(model, page)
    try:
        sliced_of_model = paginator.page(page)
    except PageNotAnInteger:
        sliced_of_model = paginator.page(1)
    except EmptyPage:
        sliced_of_model = paginator.page(paginator.num_pages)

    return sliced_of_model