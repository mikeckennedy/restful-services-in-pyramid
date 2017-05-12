from pyramid.view import view_config


@view_config(route_name='docs_all_autos_get',
             renderer='restful_auto_service:templates/docs/all_autos_get.pt')
def docs_all_autos_get(_):
    return {}


@view_config(route_name='docs_all_autos_post',
             renderer='restful_auto_service:templates/docs/all_autos_post.pt')
def docs_all_autos_post(_):
    return {}
