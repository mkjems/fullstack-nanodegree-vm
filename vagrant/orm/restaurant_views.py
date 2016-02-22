def restaurants_list_view(model):
    output = "<html><body>"
    for restaurant in model:
        output += "<h3>%s</h3>" % restaurant.name
        output += '<a href="/restaurant/edit/{0}">Edit</a> '.format(restaurant.id)
        output += '<a href="/restaurant/delete/%s">Delete</a>' % restaurant.id

    output += '<h2><a href="/restaurant/new">Create a new restaurant</a></h2>'
    output += "</body></html>"
    return output


def restaurant_create_view():
    output = "<html><body>"
    output += '''
        <form method="POST" enctype="multipart/form-data"
            action="/restaurant/new">
        <h1>Make a new Restaurant</h1>
        <input name="restaurant_name" type="text"/>
        <input type="submit" value="Submit"/>
        </form>
    '''
    output += "</body></html>"
    return output


def restaurant_update_view(restaurant):
    output = "<html><body>"
    output += '<form method="POST" enctype="multipart/form-data" action="/restaurant/update">'
    output += "<h1>Update Restaurant</h1>"
    output += '<input name="restaurant_name" type="text" value="%s"/>' % restaurant.name
    output += '<input type="hidden" name="restaurant_id" value="%s"/>' % restaurant.id
    output += '''
        <input type="submit" value="Rename"/>
        </form>
    '''
    output += "</body></html>"
    return output


def restaurant_delete_view(restaurant):
    output = "<html><body>"
    output += '<form method="POST" enctype="multipart/form-data" action="/restaurant/delete">'
    output += "<h1>Do you want to delete Restaurant %s</h1>" % restaurant.name
    output += '<input type="hidden" name="restaurant_id" value="%s"/>' % restaurant.id
    output += '<input type="submit" value="Delete"/>'
    output += '</form>'
    output += "</body></html>"
    return output
