from application import init_app

app = init_app()

if __name__ == "__main__":
  print("wsgi")
  app.run(host='localhost')