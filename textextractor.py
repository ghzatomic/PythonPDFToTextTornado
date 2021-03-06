import pdftotext
import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options
import io

define("port", default=8001, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/", IndexHandler),
      (r"/upload", UploadHandler)
    ]
    tornado.web.Application.__init__(self, handlers)

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("upload_form.html")

class UploadHandler(tornado.web.RequestHandler):
  def post(self):
    file1 = self.request.files['file'][0]

    with io.BytesIO(file1['body']) as f:
      pdf = pdftotext.PDF(f) #f.read()

    text = "\n\n".join(pdf)
    print(text)

    #original_fname = file1['filename']
    #extension = os.path.splitext(original_fname)[1]
    #fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))
    #final_filename= fname+extension
    #output_file = open("uploads/" + final_filename, 'w')
    #output_file.write(file1['body'])
    self.finish(text)

def main():
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
