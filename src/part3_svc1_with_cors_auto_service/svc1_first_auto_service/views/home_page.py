from pyramid.view import view_config


@view_config(route_name='home',
             renderer='svc1_first_auto_service:templates/mytemplate.pt')
def home(_):
    return {}
