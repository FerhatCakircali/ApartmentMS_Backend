from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Kullanici, Duyuru, Gelir, Gider, Uye, Daire, Yetki, Blok
from database import db

def setup_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        kullanici_adi = data.get('kullanici_adi')
        sifre = data.get('sifre')

        user = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()

        if user and check_password_hash(user.sifre, sifre):
            return jsonify({'uye_id': user.uye_id, 'yetki_id': user.yetki_id}), 200
        else:
            return jsonify({'message': 'Giriş başarısız!'}), 401
        
    # Announcements routes
    @app.route('/duyurular', methods=['GET'])
    def get_duyurular():
        duyurular = Duyuru.query.all()
        return jsonify([{
            'id': d.id,
            'tarih': d.tarih.strftime('%Y-%m-%d'),
            'duyuru': d.duyuru
        } for d in duyurular])

    @app.route('/duyurular', methods=['POST'])
    def add_duyuru():
        data = request.get_json()
        yeni_duyuru = Duyuru(tarih=data['tarih'], duyuru=data['duyuru'])
        db.session.add(yeni_duyuru)
        db.session.commit()
        return jsonify({'status': 'success'}), 201

    @app.route('/duyurular/<int:id>', methods=['PUT'])
    def update_duyuru(id):
        data = request.get_json()
        duyuru = Duyuru.query.get(id)
        if duyuru:
            duyuru.tarih = data['tarih']
            duyuru.duyuru = data['duyuru']
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/duyurular/<int:id>', methods=['DELETE'])
    def delete_duyuru(id):
        duyuru = Duyuru.query.get(id)
        if duyuru:
            db.session.delete(duyuru)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    # Income routes
    @app.route('/gelir', methods=['GET'])
    def get_gelir():
        gelirler = Gelir.query.all()
        return jsonify([{
            'id': g.id,
            'tarih': g.tarih.strftime('%Y-%m-%d'),
            'gelirturu': g.gelirturu,
            'tutar': float(g.tutar)
        } for g in gelirler])

    @app.route('/gelir', methods=['POST'])
    def add_gelir():
        data = request.get_json()
        yeni_gelir = Gelir(tarih=data['tarih'], gelirturu=data['gelirturu'], tutar=data['tutar'])
        db.session.add(yeni_gelir)
        db.session.commit()
        return jsonify({'status': 'success'}), 201

    @app.route('/gelir/<int:id>', methods=['PUT'])
    def update_gelir(id):
        data = request.get_json()
        gelir = Gelir.query.get(id)
        if gelir:
            gelir.tarih = data['tarih']
            gelir.gelirturu = data['gelirturu']
            gelir.tutar = data['tutar']
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/gelir/<int:id>', methods=['DELETE'])
    def delete_gelir(id):
        gelir = Gelir.query.get(id)
        if gelir:
            db.session.delete(gelir)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    # Expense routes
    @app.route('/gider', methods=['GET'])
    def get_gider():
        giderler = Gider.query.all()
        return jsonify([{
            'id': g.id,
            'tarih': g.tarih.strftime('%Y-%m-%d'),
            'giderturu': g.giderturu,
            'tutar': float(g.tutar)
        } for g in giderler])

    @app.route('/gider', methods=['POST'])
    def add_gider():
        data = request.get_json()
        yeni_gider = Gider(tarih=data['tarih'], giderturu=data['giderturu'], tutar=data['tutar'])
        db.session.add(yeni_gider)
        db.session.commit()
        return jsonify({'status': 'success'}), 201

    @app.route('/gider/<int:id>', methods=['PUT'])
    def update_gider(id):
        data = request.get_json()
        gider = Gider.query.get(id)
        if gider:
            gider.tarih = data['tarih']
            gider.giderturu = data['giderturu']
            gider.tutar = data['tutar']
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/gider/<int:id>', methods=['DELETE'])
    def delete_gider(id):
        gider = Gider.query.get(id)
        if gider:
            db.session.delete(gider)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    # Profile route
    @app.route('/profil/<int:uye_id>', methods=['GET'])
    def get_profil(uye_id):
        uye = Uye.query.get(uye_id)
        daire = Daire.query.filter_by(uye_id=uye_id).first()
        blok = Blok.query.get(daire.blok_id) if daire else None
        if uye:
            return jsonify({
                'ad': uye.ad,
                'soyad': uye.soyad,
                'email': uye.email,
                'telefon': uye.telefon,
                'blok': blok.blok if blok else '-',
                'kat': daire.kat if daire else '-',
                'daire_numarasi': daire.daire_numarasi if daire else '-'
            })
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/yetkiler', methods=['GET'])
    def get_yetkiler():
        yetkiler = Yetki.query.all()
        return jsonify([{
            'id': y.id,
            'yetki': y.yetki
        } for y in yetkiler])

    # Blocks routes
    @app.route('/bloklar', methods=['GET'])
    def get_bloklar():
        bloklar = Blok.query.all()
        return jsonify([{
            'id': b.id,
            'blok': b.blok
        } for b in bloklar])

    @app.route('/bloklar', methods=['POST'])
    def add_blok():
        data = request.get_json()
        yeni_blok = Blok(blok=data['blok'])
        db.session.add(yeni_blok)
        db.session.commit()
        return jsonify({'status': 'success'}), 201

    @app.route('/bloklar/<int:id>', methods=['PUT'])
    def update_blok(id):
        data = request.get_json()
        blok = Blok.query.get(id)
        if blok:
            blok.blok = data['blok']
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/bloklar/<int:id>', methods=['DELETE'])
    def delete_blok(id):
        blok = Blok.query.get(id)
        if blok:
            db.session.delete(blok)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404
        
    # Users routes
    @app.route('/uyeler', methods=['GET'])
    def get_uyeler():
        uyeler = Uye.query.all()
        return jsonify([{
            'id': u.id,
            'ad': u.ad,
            'soyad': u.soyad,
            'email': u.email,
            'telefon': u.telefon
        } for u in uyeler])

    @app.route('/uyeler', methods=['POST'])
    def add_uye():
        data = request.get_json()
        yeni_uye = Uye(
            ad=data['ad'],
            soyad=data['soyad'],
            email=data['email'],
            telefon=data['telefon']
        )
        db.session.add(yeni_uye)
        db.session.commit()
        return jsonify({'status': 'success'}), 201

    @app.route('/uyeler/<int:id>', methods=['PUT'])
    def update_uye(id):
        data = request.get_json()
        uye = Uye.query.get(id)
        if uye:
            uye.ad = data['ad']
            uye.soyad = data['soyad']
            uye.email = data['email']
            uye.telefon = data['telefon']
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/uyeler/<int:id>', methods=['DELETE'])
    def delete_uye(id):
        uye = Uye.query.get(id)
        if uye:
            db.session.delete(uye)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404


    # Apartments routes
    @app.route('/daire', methods=['GET'])
    def get_daire():
        daireler = Daire.query.all()
        return jsonify([{
            'id': d.id,
            'blok_id': d.blok_id,
            'kat': d.kat,
            'daire_numarasi': d.daire_numarasi,
            'uye_id': d.uye_id
        } for d in daireler])

    @app.route('/daire', methods=['POST'])
    def add_daire():
        data = request.get_json()
        yeni_daire = Daire(
            blok_id=data['blok_id'],
            kat=data['kat'],
            daire_numarasi=data['daire_numarasi'],
            uye_id=data['uye_id']
        )
        db.session.add(yeni_daire)
        db.session.commit()
        return jsonify({'status': 'success'}), 201

    @app.route('/daire/<int:id>', methods=['PUT'])
    def update_daire(id):
        data = request.get_json()
        daire = Daire.query.get(id)
        if daire:
            daire.blok_id = data['blok_id']
            daire.kat = data['kat']
            daire.daire_numarasi = data['daire_numarasi']
            daire.uye_id = data['uye_id']
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/daire/<int:id>', methods=['DELETE'])
    def delete_daire(id):
        daire = Daire.query.get(id)
        if daire:
            db.session.delete(daire)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    # Users routes
    @app.route('/kullanicilar', methods=['GET'])
    def get_kullanicilar():
        kullanicilar = Kullanici.query.all()
        return jsonify([{
            'kullanici_adi': k.kullanici_adi,
            'sifre': k.sifre,
            'uye_id': k.uye_id,
            'yetki_id': k.yetki_id
        } for k in kullanicilar])

    @app.route('/kullanicilar', methods=['POST'])
    def add_kullanici():
        data = request.get_json()
        sifre_hash = generate_password_hash(data['sifre'])
        yeni_kullanici = Kullanici(
            kullanici_adi=data['kullanici_adi'],
            sifre=sifre_hash,
            uye_id=data['uye_id'],
            yetki_id=data['yetki_id']
        )
        db.session.add(yeni_kullanici)
        db.session.commit()
        return jsonify({'status': 'success'}), 201
    
    @app.route('/kullanicilar/<string:kullanici_adi>', methods=['PUT'])
    def update_kullanici(kullanici_adi):
        data = request.get_json()
        kullanici = Kullanici.query.get(kullanici_adi)
        
        if kullanici:
            
            if 'sifre' in data and data['sifre'].strip() != '':
                kullanici.sifre = generate_password_hash(data['sifre'])
            
            if 'uye_id' in data:
                kullanici.uye_id = data['uye_id']
            if 'yetki_id' in data:
                kullanici.yetki_id = data['yetki_id']
            
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404

    @app.route('/kullanicilar/<string:kullanici_adi>', methods=['DELETE'])
    def delete_kullanici(kullanici_adi):
        kullanici = Kullanici.query.get(kullanici_adi)
        if kullanici:
            db.session.delete(kullanici)
            db.session.commit()
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure'}), 404