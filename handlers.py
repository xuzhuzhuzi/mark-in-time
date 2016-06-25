class Handler:
    """
    deal with the objects of functions from Parser
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if hasattr(method, '__call__'):
            return method(*args)

    def start(self, name):
        self.callback('start_', name)

    def end(self, name):
        self.callback('end_', name)

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                match.group(0)
            return result
        return substitution


class HTMLRender(Handler):
    """
    it is mainly used to produce HTML
    """

    def start_document(self):
        print("<html><head><title>...</title></head><body>")

    def end_document(self):
        print("</body></html>")

    def start_paragraph(self):
        print("<p>")

    def end_paragraph(self):
        print("</p>")

    def start_heading(self):
        print("<h2>")

    def end_heading(self):
        print("</h2>")

    def start_list(self):
        print("<ul>")

    def end_list(self):
        print("</ul>")

    def start_listitem(self):
        print("<li>")

    def end_listitem(self):
        print("</li>")

    def start_title(self):
        print("<h1>")

    def end_list(self):
        print("</h1>")

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)

    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))

    def feed(self, data):
        print(data)