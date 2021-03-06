from plistlib import Data

from flask import render_template, request, url_for, flash
from werkzeug.utils import redirect

from databese import ProductModel, FeaturesModel, UserModel, OrganizationsModel, ManufacturersModel, ProductBrandsModel, \
    BrandsOrgsModel, ProductFeaturesModel, AlternativeBrandsModel, FlowModel
from app import app, db
import binascii


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/checkuser', methods=['POST'])
def checkuser():
    if request.method == 'POST':
        person_name = request.form['person_name']
        person_password = request.form['person_password']
        login = UserModel.query.filter_by(person_name=person_name, person_password=person_password).first()
        if login is not None:
            return redirect(url_for('features'))

        return redirect(url_for("hello_world"))


@app.route('/insertuser', methods=['POST'])
def insertuser():
    if request.method == 'POST':
        person_name = request.form['person_name']
        person_password = request.form['person_password']

        myUser = UserModel(person_name, person_password)
        db.session.add(myUser)
        db.session.commit()
    return redirect(url_for('hello_world'))


@app.route('/features')
def features():
    all_data = db.session.query(FeaturesModel).all()
    return render_template('features.html', feat=all_data)


@app.route('/insertfeatures', methods=['POST'])
def insertfeatures():
    if request.method == 'POST':
        feature_name = request.form['feature_name']
        myFeatures = FeaturesModel(feature_name)
        db.session.add(myFeatures)
        db.session.commit()
        # Flash("New Feature is added")

    return redirect(url_for('features'))


@app.route('/updatefeatures', methods=['GET', 'POST'])
def updatefeatures():
    if request.method == 'POST':
        m_name = request.form['feature_name']
        num = request.form['feature_id']

        my_data = db.session.query(FeaturesModel).get(num)
        my_data.feature_name = request.form['feature_name']
        db.session.commit()

    return redirect(url_for('features'))


@app.route('/deletefeatures', methods=['GET', 'POST'])
def deletefeatures():
    num = request.form['feature_id']

    my_data = db.session.query(FeaturesModel).get(num)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('features'))


@app.route('/product')
def product():
    all_data = db.session.query(ProductModel).all()
    return render_template('product.html', feat=all_data)


@app.route('/insertproduct', methods=['POST'])
def insertproduct():
    if request.method == 'POST':
        m_code = request.form['m_code']
        m_name = request.form['m_name']
        m_short_name = request.form['m_short_name']
        m_parent_code = request.form['m_parent_code']
        m_abstract = request.form['m_abstract']
        m_category = request.form['m_category']
        is_active = request.form['is_active']

        # guid_tag = binascii.unhexlify(m_abstract)
        # isac = binascii.unhexlify(is_active)
        my_data = ProductModel(m_code, m_name, m_short_name, m_parent_code, m_abstract, m_category, is_active)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('product'))


@app.route('/updateproduct', methods=['GET', 'POST'])
def updateproduct():
    if request.method == 'POST':
        m_code = request.form['m_code']
        m_name = request.form['m_name']
        m_short_name = request.form['m_short_name']
        m_parent_code = request.form['m_parent_code']
        m_abstract = request.form['m_abstract']
        m_category = request.form['m_category']
        is_active = request.form['is_active']

        # guid_tag = binascii.unhexlify(m_abstract)
        # isac = binascii.unhexlify(is_active)

        my_data = db.session.query(ProductModel).get(m_code)
        my_data.m_name = request.form['m_name']
        my_data.m_short_name = request.form['m_short_name']
        my_data.m_parent_code = request.form['m_parent_code']
        my_data.m_abstract = m_abstract
        my_data.m_category = request.form['m_category']
        my_data.is_active = is_active

        db.session.commit()
        return redirect(url_for('product'))


@app.route('/deleteproduct', methods=['GET', 'POST'])
def deleteproduct():
    num = request.form['m_syscode']

    my_data = db.session.query(ProductModel).get(num)

    num = request.form['m_syscode']

    my_data = db.session.query(ProductModel).get(num)
    organizasyon = db.session.query(ProductModel).filter(ProductModel.m_parent_code == num)
    for row in organizasyon:
        newcode = row.m_syscode
        organizasyon2 = db.session.query(ProductModel).filter(ProductModel.m_parent_code == str(newcode))
        db.session.delete(row)
        for row2 in organizasyon2:
            a = row2.m_syscode
            organizasyon3 = db.session.query(ProductModel).filter(ProductModel.m_parent_code == str(a))
            db.session.delete(row2)
            for row3 in organizasyon3:
                row3.m_parent_code = 0

    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('product'))


@app.route('/insorg')
def insorg():
    return render_template('RegisterOrganization.html')


@app.route('/insertorganization', methods=['POST'])
def insertorganization():
    if request.method == 'POST':
        org_name = request.form['org_name']
        org_Address = request.form['org_Adress']
        org_District = request.form['org_District']
        parent_org = 0
        org_abstract = ''
        isac = 1
        org_City = 0
        org_Type = 0
        myOrg = OrganizationsModel(org_name, parent_org, isac, org_Address, org_City, org_District, org_Type)
        db.session.add(myOrg)
        db.session.commit()
        person_name = request.form['person_name']
        person_password = request.form['person_password']
        myUser = UserModel(person_name, person_password)
        db.session.add(myUser)
        db.session.commit()
    return redirect(url_for('hello_world'))


@app.route('/manufacturers')
def manufacturers():
    all_data = db.session.query(ManufacturersModel).all()
    return render_template('manufacturer.html', feat=all_data)


@app.route('/insertmanufacturers', methods=['POST'])
def insertmanufacturers():
    if request.method == 'POST':
        manufacturer_id = request.form['manufacturer_id']
        manufacturer_name = request.form['manufacturer_name']
        manufacturer_address = request.form['manufacturer_address']
        city = request.form['city']
        country = request.form['country']
        my_data = ManufacturersModel(manufacturer_id, manufacturer_name, manufacturer_address, city, country)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('manufacturers'))


@app.route('/updatemanufacturers', methods=['GET', 'POST'])
def updatemanufacturers():
    if request.method == 'POST':
        manufacturer_id = request.form['manufacturer_id']
        manufacturer_name = request.form['manufacturer_name']
        manufacturer_address = request.form['manufacturer_address']
        city = request.form['city']
        country = request.form['country']

        my_data = db.session.query(ManufacturersModel).get(manufacturer_id)
        my_data.manufacturer_id = request.form['manufacturer_id']
        my_data.manufacturer_name = request.form['manufacturer_name']
        my_data.manufacturer_address = request.form['manufacturer_address']
        my_data.city = request.form['city']
        my_data.country = request.form['country']

        db.session.commit()
        return redirect(url_for('manufacturers'))


@app.route('/deletemanufacturers', methods=['GET', 'POST'])
def deletemanufacturers():
    manufacture_id = request.form['manufacturer_id']

    my_data = db.session.query(ManufacturersModel).get(manufacture_id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('manufacturers'))


@app.route('/productbrands')
def productbrands():
    all_data = db.session.query(ProductBrandsModel).all()
    return render_template('productbrands.html', feat=all_data)


@app.route('/insertproductbrands', methods=['POST'])
def insertproductbrands():
    if request.method == 'POST':
        brand_barcode = request.form['brand_barcode']
        m_syscode = request.form['m_syscode']
        brand_name = request.form['brand_name']
        manufacturer_id = request.form['manufacturer_id']
        my_data = ProductBrandsModel(brand_barcode, m_syscode, brand_name, manufacturer_id)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('productbrands'))


@app.route('/updateproductbrands', methods=['GET', 'POST'])
def updateproductbrands():
    if request.method == 'POST':
        brand_barcode = request.form['brand_barcode']
        m_syscode = request.form['m_syscode']
        brand_name = request.form['brand_name']
        manufacturer_id = request.form['manufacturer_id']

        my_data = db.session.query(ProductBrandsModel).get({'brand_barcode': brand_barcode, 'm_syscode': m_syscode})
        my_data.brand_barcode = request.form['brand_barcode']
        my_data.m_syscode = request.form['m_syscode']
        my_data.brand_name = request.form['brand_name']
        my_data.manufacturer_id = request.form['manufacturer_id']

        db.session.commit()
        return redirect(url_for('productbrands'))


@app.route('/deleteproductbrands', methods=['GET', 'POST'])
def deleteproductbrands():
    brand_barcode = request.form['brand_barcode']
    m_syscode = request.form['m_syscode']

    my_data = db.session.query(ProductBrandsModel).get({'brand_barcode': brand_barcode, 'm_syscode': m_syscode})
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('productbrands'))


@app.route('/brand_organization')
def brandOrganization():
    data = db.session.query(OrganizationsModel.org_name, OrganizationsModel.org_id, BrandsOrgsModel,
                            ProductBrandsModel.brand_barcode, ProductBrandsModel.brand_name).filter(
        OrganizationsModel.org_id == BrandsOrgsModel.org_id).filter(
        ProductBrandsModel.brand_barcode == BrandsOrgsModel.brand_barcode).all()
    organizationData = db.session.query(OrganizationsModel)
    brandData = db.session.query(ProductBrandsModel)
    return render_template('brand_organization.html', feat=data, orgData=organizationData, brandData=brandData)


@app.route('/linkbrandsorgs', methods=['POST'])
def linkbrandsorgs():
    if request.method == 'POST':
        lot_id = request.form['lot_id']
        brand_barcode = request.form['Brand-select']
        org_id = request.form['Organization-select']
        in_amount = request.form['in_amount']
        out_amount = request.form['out_amount']
        totalamount = int(in_amount) + int(out_amount)
        my_data = BrandsOrgsModel(lot_id, org_id, brand_barcode, in_amount, out_amount, totalamount)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('brandOrganization'))


@app.route('/brand_alternativebrand')
def BrandAlternativeBrand():
    data = db.session.query(AlternativeBrandsModel.alternative_brand_code, ProductBrandsModel.brand_name,
                            ProductBrandsModel.brand_barcode).filter(
        AlternativeBrandsModel.brand_barcode == ProductBrandsModel.brand_barcode).all()

    altBrandsData = db.session.query(AlternativeBrandsModel.alternative_brand_code, ProductBrandsModel.brand_name,
                                     ProductBrandsModel.brand_barcode).filter(
        AlternativeBrandsModel.alternative_brand_code == ProductBrandsModel.brand_barcode)
    BrandData = db.session.query(ProductBrandsModel).all()

    return render_template('brand-alternativebrand.html', feat=data, altFeat=altBrandsData, brand=BrandData)


@app.route('/link_alternative_brands', methods=['POST'])
def link_alternative_brands():
    if request.method == 'POST':
        brand_barcode = request.form['Brand-select']
        alternative_brand_barcode = request.form['Alternative-Brand-select']
        m_syscode = request.form['m_syscode']
        alternative_m_syscode = request.form['alternative-m_syscode']
        my_data = AlternativeBrandsModel(brand_barcode, alternative_brand_barcode, m_syscode, alternative_m_syscode)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('BrandAlternativeBrand'))


@app.route('/flow')
def flow():
    source = db.session.query(FlowModel.source_lot_id, OrganizationsModel.org_id, OrganizationsModel.org_name).filter(
        FlowModel.source_org_id == OrganizationsModel.org_id).all()
    target = db.session.query(FlowModel.target_lot_id, FlowModel.target_org_id, FlowModel.brand_brandcode,
                              OrganizationsModel.org_id,
                              OrganizationsModel.org_name).filter(
        FlowModel.target_org_id == OrganizationsModel.org_id).all()
    brand = db.session.query(ProductBrandsModel.brand_barcode, ProductBrandsModel.brand_name).all()
    orgs = db.session.query(OrganizationsModel.org_id, OrganizationsModel.org_name).all()
    brOrg = db.session.query(BrandsOrgsModel.lot_id, BrandsOrgsModel.brand_barcode).all()

    return render_template('flow.html', source=source, target=target, brand=brand, orgs=orgs, brOrg=brOrg)


@app.route('/flowBrand', methods=['GET', 'POST'])
def flowBrand():
    BrandBarcode = request.form['Brand-select']
    SourceOrgID = request.form['Organization-select']
    TargetOrgID = request.form['Target-Organization-select']
    SourceLotID = request.form['Source-lot-select']
    TargetLotID = request.form['target-lot-id']
    flowMd = FlowModel(SourceLotID, SourceOrgID, TargetLotID, TargetOrgID, BrandBarcode)
    db.session.add(flowMd)
    db.session.commit()

    my_data = db.session.query(BrandsOrgsModel).get(
        {'lot_id': SourceLotID, 'org_id': SourceOrgID, 'brand_barcode': BrandBarcode})
    my_data.lot_id = TargetLotID
    my_data.org_id = TargetOrgID
    db.session.commit()

    return redirect(url_for('flow'))


@app.route('/product_features')
def product_features():
    data = db.session.query(ProductModel.m_syscode, ProductModel.m_code, ProductModel.m_name, ProductFeaturesModel,
                            FeaturesModel.feature_id, FeaturesModel.feature_name).filter(
        ProductModel.m_syscode == ProductFeaturesModel.m_syscode).filter(FeaturesModel.feature_id == ProductFeaturesModel.feature_id).all()
    productData = db.session.query(ProductModel)
    featuresData = db.session.query(FeaturesModel)
    return render_template('product_features.html', feat=data, productData=productData, featuresData=featuresData)


@app.route('/linkproductfeatures', methods=['POST'])
def linkproductfeatures():
    if request.method == 'POST':
        m_syscode = request.form['Product M_Syscode-Select']
        feature_id = request.form['Feature ID-select']
        minval = request.form['minval']
        my_data = ProductFeaturesModel(m_syscode, feature_id, minval)
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('product_features'))

@app.route('/organization')
def organization():
    all_data = db.session.query(OrganizationsModel).all()
    return render_template('organization.html', feat=all_data)


@app.route('/insertorganizationTable', methods=['POST'])
def insertorganizationTable():
    if request.method == 'POST':
        org_name = request.form['org_name']
        org_Address = request.form['org_Adress']
        org_District = request.form['org_District']
        parent_org = request.form['parent_org']
        org_abstract = request.form['org_abstract']
        org_City = request.form['org_City']
        org_Type = request.form['org_Type']
        if (parent_org == ''):
            parent_org = None
        myOrg = OrganizationsModel(org_name, parent_org, org_abstract, org_Address, org_City, org_District,
                                   org_Type)
        db.session.add(myOrg)
        db.session.commit()
    return redirect(url_for('organization'))


@app.route('/deleteorganization', methods=['GET', 'POST'])
def deleteorganization():
    num = request.form['org_id']

    my_data = db.session.query(OrganizationsModel).get(num)
    organizasyon = db.session.query(OrganizationsModel).filter(OrganizationsModel.parent_org == num)
    for row in organizasyon:
        newcode = row.org_id
        organizasyon2 = db.session.query(OrganizationsModel).filter(OrganizationsModel.parent_org == newcode)
        db.session.delete(row)
        for row2 in organizasyon2:
            a = row2.org_id
            organizasyon3 = db.session.query(OrganizationsModel).filter(OrganizationsModel.parent_org == a)
            db.session.delete(row2)
            for row3 in organizasyon3:
                row3.parent_org = 0

    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('organization'))


@app.route('/updateorganization', methods=['GET', 'POST'])
def updateorganization():
    if request.method == 'POST':
        org_name = request.form['org_name']
        org_Address = request.form['org_Adress']
        org_District = request.form['org_District']
        parent_org = request.form['parent_org']
        org_abstract = request.form['org_abstract']
        org_City = request.form['org_City']
        org_Type = request.form['org_Type']
        num = request.form['org_id']
        my_data = db.session.query(OrganizationsModel).get(num)
        my_data.org_name = request.form['org_name']
        my_data.org_Adress = request.form['org_Adress']
        my_data.org_District = request.form['org_District']
        my_data.parent_org = request.form['parent_org']
        my_data.org_abstract = request.form['org_abstract']
        my_data.org_City = request.form['org_City']
        my_data.org_Type = request.form['org_Type']
        db.session.commit()

    return redirect(url_for('organization'))


@app.route('/safedeleteorganization', methods=['GET', 'POST'])
def safedeleteorganization():
    num = request.form['org_id']

    my_data = db.session.query(OrganizationsModel).get(num)
    newcode = my_data.parent_org
    organizasyon = db.session.query(OrganizationsModel).filter(OrganizationsModel.parent_org == num)
    for row in organizasyon:
        row.parent_org = newcode
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('organization'))


@app.route('/safedeleteproduct', methods=['GET', 'POST'])
def safedeleteproduct():
    num = request.form['m_syscode']

    my_data = db.session.query(ProductModel).get(num)
    newcode = my_data.m_parent_code
    pro = db.session.query(ProductModel).filter(ProductModel.m_parent_code == num)
    for row in pro:
        row.m_parent_code = newcode
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('product'))


if __name__ == '__main__':
    app.run()
