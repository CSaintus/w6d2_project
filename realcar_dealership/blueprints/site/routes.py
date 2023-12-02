from flask import Blueprint, render_template



from realcar_dealership.models import Car, db
from realcar_dealership.forms import carform



site = Blueprint('site', __name__, template_folder='site_templates' )

@site.route("/")
def dealer():


    allcars = Car.query.all()


    return render_template('dealer.html', cars=allcars)


@site.route("/addcar", methods=["GET", "POST"])
def addcar():

    addform = carform()

    if request.method == "POST" and addform.validate_on_submit():
        make = addform.make.data
        model = addform.model.data
        year = addform.year.data
        color = addform.color.data
        price = addform.price.data
        description = addform.description.data

        newcar = Car(make, model, year, color, price, description)

        db.session.add(newcar)
        db.session.commit()

        flash("Car added", "success")
        return redirect("/")

    elif request.method == "POST":
        flash("Error adding car", "danger")
        return redirect("/")

    return render_template("addcar.html", addform=addform)

@site.route("/update/<int:car_id>", methods=["GET", "POST"])
def updatecar(car_id):
    car = Car.query.get(car_id)
    updateform = carform(obj=car)
    if request.method == "POST" and updateform.validate_on_submit():
        car.make = updateform.make.data
        car.model = updateform.model.data
        car.year = updateform.year.data
        car.color = updateform.color.data
        car.price = updateform.price.data
        car.description = updateform.description.data

        db.session.commit()

        flash("Car updated", "success")
        return redirect("/")

    elif request.method == "POST":
        flash("Error updating car", "danger")
        return redirect("/")


    return render_template("updatecar.html", updateform=updateform)


@site.route("/delete/<int:car_id>")
def deletecar(car_id):

    car = Car.query.get(car_id)
    db.session.delete(car)
    db.session.commit()


    flash("Car deleted", "success")

    return redirect("/")