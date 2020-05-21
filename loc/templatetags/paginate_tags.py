from django import template

register = template.Library()

@register.filter
def paginate_range(page_obj, width=3):
    '''Calculate a reasonable range of pages for paginating. With `width` set to 3,
    it shows the current page and the next lower and next higher page number.

    '''

    max_page = page_obj.paginator.num_pages
    current_page = page_obj.number

    # convert width to distance to both directions. By using integer division,
    # we force the width to be an odd number - otherwise it's rounded down.
    width = (width - 1) // 2

    # calculate lower bound, but do not go below 1
    lb = max(current_page - width, 1)
    # lower bound shall stay away 2 * width from max_page, but not below 1
    lb = min(lb, max(max_page - 2 * width, 1))
    # upper bound is limited to max_page
    ub = min(lb + 2 * width, max_page)

    return [i for i in range(lb, ub + 1)]
