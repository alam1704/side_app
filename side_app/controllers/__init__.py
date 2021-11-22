from controllers.pharmacy_controller import pharmacies
from controllers.user_controller import users
from controllers.image_controller import user_images

registerable_controllers = [pharmacies, users, user_images]

# Import our new controller and apply that blueprint to our app.