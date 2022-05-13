from module.main import Frame
import module.views as v


urls = {
    '/': v.index,
    '/tashkent': v.tashkent,
    '/kazan': v.kazan,
    '/saint_petersburg': v.saint_petersburg
}

Frame.route_register(urls)
app = Frame()
