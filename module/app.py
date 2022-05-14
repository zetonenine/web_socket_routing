from module.main import Frame
import module.views as v


urls = {
    '/': v.index,
    '/location': v.locations,
    '/location/<city>': v.location
}

Frame.route_register(urls)
app = Frame()
