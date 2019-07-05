from flask import Flask, redirect, render_template, request, url_for
from models import User, Meal, Order
from store import Admin, MealStore
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = b"\xdb\x87\xdb\x1b\x99\xcb\xee\xdej'\x93\x8f\xa0\x0bn\x8d"
login_manager = LoginManager()
login_manager.init_app(app)

all_users = {'admin':User("admin",generate_password_hash("secret"))}

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)


meals = [
    Meal(id=1,
          name='Green Salad',
          photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/9/9254dc12058bb5c3d408a97a4cd1f805e35eb2ca_2_517x343.jpeg",
          details='green salad with black olives',
          price='$10'),
    Meal(id=2,
         name="Pizza Supreme",
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/5/5d0c3f982a91251fefc3f2d0d06532ae614e468d_2_516x345.jpeg",
          details='',
         price='$20'),
    Meal(id=3,
         name='omlet eggs',
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/c/c974a7d22cd172477a2f19f94f689b8dc4cf7b11_2_517x343.jpeg",
          details='',
         price='$20'),
    Meal(id=4,
         name='pasta',
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/9/9e76e134af069ba18491ee2495798ec6cae96c1e_2_517x343.jpeg",
          details='',
         price='$30'),
    Meal(id=5,
         name='Burger king',
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/f/f50c99817d4e3b56a92ddf9509ef21b7d043c9eb_2_318x375.jpeg",
          details=' ',
         price='$20'),
    Meal(id=6,
         name='beef shawarma',
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/3/3375f351a84cc82749880c69036612b61dc8a9dc_2_447x375.jpeg",
          details='',
         price='$20'),
    Meal(id=7,
         name='fillet fish meal',
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/5/53f83b26de24a55127ee1e9963523d187632853f_2_499x375.jpeg",
          details='',
         price='$20'),
    Meal(id=8,
         name='chicken meal',
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/c/cbf3500b1ff23cb173193bb8135b2925a7d39eff_2_517x343.jpeg",
          details='',
         price='$20'),
    Meal(id=9,
         name='chicken shawarma',
         photo_url="https://academy-discorce-s3.s3.dualstack.us-east-2.amazonaws.com/upload/optimized/2X/9/9e9b999cc4b7dc27ce05c81e9f724442e2a37369_2_517x291.jpeg" ,
          details='',
         price='$20')
      ]


meal_store = Admin()
for meal in meals:
    meal_store.add_meal(meal)

client = MealStore()
app.current_id=10
app.order_id = 0


@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

@app.route('/')
def home():
    return render_template('index.html',meals=client.get_all_meals())


@app.route('/meals/meal/<int:id>')
def show_meal(id):
    id = meal.id
    return render_template('meal.html',meal=meal_store.get_meal_by_id(id))

@app.route('/meals/add_order/', methods=['GET','POST'])
def apply_order():
    if request.method == 'POST':
        new_order = Order(id=app.order_id,
        name=request.form['name'],
        address=request.form['address'],
        phone=request.form['phone'],
        meal=request.form['meal']
        )
        client.add_order(new_order)
        app.order_id += 1
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('order_apply.html')

@app.route('/cart/')
def cart():
    return render_template('user_orders.html')

@app.route('/cart/delete/,<int:id>')
def delete_order(id):
    meal_store.delete(id)
    return render_template('user_orders.html',orders=meal_store.get_all_orders())

@app.route('/admin')
def admin():
    return render_template('admin.html',meals=meal_store.get_all_meals())

@app.route('/admin/orders')
def orders_admin():
    return render_template('admin_orders.html',orders=meal_store.get_all_orders())


@app.route('/admin/add',methods=['GET','POST'])
def meal_add():
    if request.method == 'POST':
        new_meal = Meal(id=app.current_id,
                        name=request.form['name'],
                        photo_url=request.form['photo_url'],
                        details=request.form['details'],
                        price=request.form['price'])
        meal_store.add_meal(new_meal)
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        return render_template('add_meal.html')



@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)

    username = request.form["username"]
    if username not in all_users:
        return render_template("login.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["password"]):
        return render_template("login.html", error=True)

    login_user(user)
    return redirect(url_for('admin'))


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



app.run(debug=True)
