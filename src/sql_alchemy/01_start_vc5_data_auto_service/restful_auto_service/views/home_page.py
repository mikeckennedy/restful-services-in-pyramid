from pyramid.view import view_config


@view_config(route_name='home',
             renderer='restful_auto_service:templates/mytemplate.pt')
def home(_):
    return {}
