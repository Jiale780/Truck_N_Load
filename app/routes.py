from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from app.forms import LoginForm, RegistrationForm, PanCreationForm, PalletCreationForm, DeliverySelectorForm, \
    DeliveryCreationForm, CustomerCreationForm, ManifestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Pan, Delivery, Pallet, Customer, palletContent, Content
from app.models import User, Pan as pan_db, Delivery as del_db, Pallet as pallet_db, Content as Cont_db, \
    palletContent as PaC, PanCoordinator as Pc, Customer as cust_db
from werkzeug.urls import url_parse
from app.Classes.Pan import Pan as pan_class, Delivery as delivery_class;

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            app.logger.info('Failed login attempt for username "{}"'.format(form.username.data))
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        app.logger.info('User "{}" logged in'.format(form.username.data))
        flash('Login successful')

        next_page = request.args.get('next')  # For redirecting users back to the page they attempted to access
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    app.logger.info('User "{}" logged out'.format(current_user.username))
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('User: {} has been created successfully'.format(form.username.data))
        app.logger.info('User "{}" has been created'.format(form.username.data))
        return redirect(url_for('register'))  # Redirect the registration page in case they want to create more users

    return render_template('simple_form.html', title='Register', form=form)


@app.route('/administration')
@login_required
def administration():
    return render_template('administration.html', title='Admin')


@app.route('/administration/pan_selector')
@login_required
def pan_selector():
    table = {
        'headings': ['delivery id', 'delivery address'],
        'rows': []
    }
    for row in pan_db.query.with_entities(pan_db.id):
        for delivery in del_db.query.filter_by(pan_id=row.id):
            table['rows'].append({'delivery id': delivery.id, 'delivery address': delivery.address})
    return render_template('pan_selector.html', title='Pan Selector', table=table, manifestForm=ManifestForm())


@app.route('/administration/pan_creator', methods=['GET', 'POST'])
@login_required
def pan_creator():
    form = PanCreationForm()
    if form.validate_on_submit():
        pan = pan_db(
            weight=form.weight.data,
            height=form.height.data,
            width=form.width.data,
            length=form.length.data,
            rail_height=form.rail_height.data,
            cost=form.cost.data)

        db.session.add(pan)
        db.session.commit()
        app.logger.info("Pan {} has been created".format(pan_db.query.order_by(pan_db.id.desc()).first()))

        flash('Pan has been created successfully')
    return render_template('simple_form.html', title='Pan Creator', form=form)


@app.route('/administration/delivery_creator', methods=['GET', 'POST'])
@login_required
def delivery_creator():
    form = DeliveryCreationForm()
    if form.validate_on_submit():
        delivery = del_db(
            address=form.address.data,
            pan_id=form.pan_id.data
        )

        db.session.add(delivery)
        db.session.commit()
        delivery_id = del_db.query.order_by(del_db.id.desc()).first()
        app.logger.info("Delivery {} has been created".format(delivery_id))

        flash('Delivery ({}) has been created successfully'.format(delivery_id))

    return render_template('simple_form.html', title='Delivery Creator', form=form)


@app.route('/administration/customer_creator', methods=['GET', 'POST'])
@login_required
def customer_creator():
    form = CustomerCreationForm()
    if form.validate_on_submit():
        customer = cust_db(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            address=form.address.data,
            phone_number=form.phone_number.data
        )

        db.session.add(customer)
        db.session.commit()
        app.logger.info("Delivery {} has been created".format(cust_db.query.order_by(cust_db.id.desc()).first()))

        flash('Customer has been created successfully')

    return render_template('simple_form.html', title='Customer Creator', form=form)


@app.route('/pan_preparation', methods=['GET', 'POST'])
@login_required
def pan_preparation():
    form = DeliverySelectorForm()

    if form.validate_on_submit():
        return redirect(url_for('pallet_creator', delivery_id=form.delivery_id.data))

    return render_template('simple_form.html', title='Pan Preparation', form=form)


@app.route('/pan_preparation/pallet_creator', methods=['GET', 'POST'])
@login_required
def pallet_creator():
    delivery_id = request.args.get('delivery_id')
    if not delivery_id:  # if the user has no gotten to this page from the delivery selector
        abort(400)

    form = PalletCreationForm(delivery_id=delivery_id)

    if form.validate_on_submit():
        pallet = pallet_db(
            weight=form.weight.data,
            height=form.height.data,
            category=form.category.data,
            stack_able=form.can_stack.data,
            customer_id=form.customer.data,
            delivery_id=form.delivery_id.data)

        db.session.add(pallet)
        db.session.commit()
        app.logger.info("Pallet {} has been created".format(pallet_db.query.order_by(pallet_db.id.desc()).first()))

        flash('Pallet has been created successfully')

        redirect(url_for('pallet_creator', delivery_id=delivery_id))

    return render_template('simple_form.html', title='Pan Preparation', form=form)


@app.route('/loading/pallet_display', methods=['GET', 'POST'])
@login_required
def pallet_display():
    form = DeliverySelectorForm()

    if not form.validate_on_submit():
        return render_template('simple_form.html', title='loading', form=form)
    else:
        delivery_id = request.args.get('delivery_id')

        table = {
            'headings': ['pallet', 'width_coord', 'length_coord', 'height_coord', 'rail', 'delivery'],
            'rows': []
        }

        # Sorting via length then width then above rail all in ascending order is optimal and required for the next section
        # Storage into the list is done via. the list containing a list that signifies the length of the pan
        # the length of the pan also contains a list that signifies the width and the width contains a list to signify the
        # height
        # Storage on the height is done such that [bottom pallet, 'rail', top pallet] or [bottom pallet, top pallet] etc.
        # it is apparent when reading into the HTML you reverse this order, so that you display the top pallet first then
        # the rest
        for row in del_db.query.with_entities(del_db.id):
            for pallets in Pc.query.filter_by(delivery_id=row.id).order_by(Pc.length_position.asc(),
                                                                           Pc.width_position.asc(), Pc.above_rail.asc()
                                                                           ):
                table['rows'].append({'pallet': pallet_db.query.filter_by(id=pallets.pallet_id).first(),
                                      'width_coord': pallets.width_position,
                                      'length_coord': pallets.length_position,
                                      'height_coord': pallets.height_position,
                                      'rail': pallets.above_rail,
                                      'delivery': del_db.query.filter_by(id=pallets.delivery_id).first()})

        rows = table['rows']
        pallet = table['headings'][0]
        width = table['headings'][1]
        length = table['headings'][2]
        height = table['headings'][3]
        rail = table['headings'][4]
        delivery = table['headings'][5]
        pan = []

        for row in range(len(rows)):
            # if there is already an existing data in the list. we would like to skip over it. Otherwise we would have to
            # deal with duplicate entries
            if len(pan) != 0:
                flag = False
                for le in pan:
                    for we in le:
                        for h in we:
                            if rows[row][pallet].id == h[0].id:
                                flag = True
                                break
                        if flag is True:
                            break
                    if flag is True:
                        break
                if flag is True:
                    continue

            l = []
            w = []
            w1 = []
            w.append([rows[row][pallet], rows[row][height], rows[row][rail], rows[row][delivery]])
            # l.append(w)

            for row_2 in range(row + 1, len(rows)):
                if rows[row][length] == rows[row_2][length]:  # if in the same length
                    if rows[row][width] == rows[row_2][width]:  # if same row and length
                        w.append([rows[row_2][pallet], rows[row_2][height], rows[row_2][rail], rows[row_2][delivery]])

                    if rows[row][width] != rows[row_2][width]:  # if same length but not same row
                        w1.append([rows[row_2][pallet], rows[row_2][height], rows[row_2][rail], rows[row_2][delivery]])
            l.append(w)
            l.append(w1)
            if len(l) != 0:
                pan.append(l)

        # The following methods is to find the contents in the data base.
        # Stores them in a dictionary of lists. that is the pallet id
        conts = {}
        for row in rows:
            p_c_t = PaC.select(whereclause=(PaC.columns.pallet_id == row[pallet].id))
            res = db.engine.execute(p_c_t)
            conts[row[pallet].id] = []
            for contents in res:
                c = Cont_db.query.filter_by(id=contents.content_id).first()
                conts[row[pallet].id].append([c.id, contents.quantity, c.name])

    return render_template('pallet_display.html', title='Pallet Display', conts=conts, pan=pan)


@app.route('/manifest', methods=['GET', 'POST'])
@login_required
def manifest():
    form = ManifestForm()
    form.id.choices = [(row.id, str(row.id) + ': ' + row.address) for row in Delivery.query.all()]
    ptable = None
    message = "An error has occurred: "
    itable = None
    if form.validate_on_submit():
        #print("yes")
        table = Delivery.query.filter_by(id=form.id.data)
        if table.first() is None:
            ptable = None
            message += "No delivery by that ID"
        else:
            ptable = Customer.query.join(Pallet, Pallet.customer_id==Customer.id).add_columns(
                Customer.first_name,Pallet.id, Pallet.category, Pallet.weight, Pallet.height

                ).filter_by(delivery_id=table.first().id)
            if ptable.first() is None:
                message += "No pallets on that delivery"
                #print("no pallets")
            else:
                #print("pallets exist")
                #print(ptable.first())
                message = "Manifest for delivery " + str(table.first().id) + " destined for " + str(
                    table.first().address)
                itable = db.session.query(Content.name,db.func.sum(palletContent.columns.quantity).label('quantity')).join(
                    palletContent,Pallet).filter_by(delivery_id=table.first().id).group_by(Content.name)
                #print(itable)
    else:
        #print("no")
        if form.is_submitted():
            message = "Form has errors"
        else:
            message = "Please submit the form"
        #print(form.errors)
    return render_template('manifest.html', form=form, message=message, ptable=ptable, itable=itable)


@app.route('/administration/pan_cost')
@login_required
def pan_cost():
    delivery_id = request.args.get('delivery_id')
    delivery = Delivery.query.filter_by(id=delivery_id).first()
    dry_pallets = Pallet.query.filter_by(delivery_id=delivery_id,category='D')
    total_pallets = len(Pallet.query.filter_by(delivery_id=delivery_id).all())
    print(dry_pallets.all())
    dry_weight = db.session.query(db.func.sum(Pallet.weight).label('weight')).filter_by(delivery_id=delivery_id,
                                                                                     category='D')
    chilled_weight = db.session.query(db.func.sum(Pallet.weight).label('weight')).filter_by(delivery_id=delivery_id,
                                                                                     category='C')
    frozen_weight = db.session.query(db.func.sum(Pallet.weight).label('weight')).filter_by(delivery_id=delivery_id,
                                                                                     category='F')
    print(dry_weight.first().weight)
    return render_template('pan_cost.html', title='Pan Cost', address=delivery.address,
                           total_pallets=total_pallets,
                           dry_pallets=len(dry_pallets.all()),
                           chilled_pallets=len(Pallet.query.filter_by(delivery_id=delivery_id,category='C').all()),
                           frozen_pallets=len(Pallet.query.filter_by(delivery_id=delivery_id,category='F').all()),
                           cost=Pan.query.filter_by(id=delivery.pan_id).first().cost,
                           dry_weight=dry_weight.first().weight if dry_weight.first().weight else 0,
                           chilled_weight=chilled_weight.first().weight if chilled_weight.first().weight else 0,
                           frozen_weight=frozen_weight.first().weight if frozen_weight.first().weight else 0)


@app.route('/administration/unused_space_cost')
@login_required
def unused_space_cost():
    delivery_id = request.args.get('delivery_id')
    table = None;
    if(delivery_id == None):
        flash('Need a ID, go back')
        abort(400)
    delivery = Delivery.query.filter_by(id=delivery_id);
    if(delivery):
        pallets = Pallet.query.filter_by(delivery_id=delivery.first().id)
        print("We have "+str(len(pallets.all()))+" pallets")
        delivery = delivery.first()
        cost = Pan.query.filter_by(id=delivery.pan_id).first().cost;
        print(cost)
        table = [];
        #pan = pan_class(delivery.pan_id,Pan.query.filter_by(id=delivery.pan_id).first().width,
        #                Pan.query.filter_by(id=delivery.pan_id).first().length,
        #                Pan.query.filter_by(id=delivery.pan_id).first().height,
        #                Pan.query.filter_by(id=delivery.pan_id).first().rail_height,
        #                delivery=delivery_class.Delivery(delivery.id,delivery.address),
        #                pallets=table
        #                )
        #pan.get_wasted_space(pallets)
    else:
        flash('No delivery by that id')
        abort(400)
    return render_template('unused_space_cost.html', title='Unused Space Cost',
                subtitle=delivery.address if delivery else None,
                pallet_count=len(pallets.all()),
                chilled_pallets=len(Pallet.query.filter_by(delivery_id=delivery_id, category='C').all()),
                frozen_pallets=len(Pallet.query.filter_by(delivery_id=delivery_id, category='F').all()),
                dry_pallets=len(Pallet.query.filter_by(delivery_id=delivery_id, category='D').all()),
                           )

