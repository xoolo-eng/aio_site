from rest.url.router import Controller
from rest.web.home import views


Controller.add("", views.HomePage, name="home_page")