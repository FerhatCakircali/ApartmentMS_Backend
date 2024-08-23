1 - PostgreSQL'i kurun.

2 - ApartmentMS_Backend klasöründe ".env" dosyası açın ve DB bilgilerini giri. Örnek şu şekildedir:

FLASK_ENV=development
# İlgili PostgreSQL bilgileri değiştirebilir.
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=12345
DB_NAME=dbApartmentMS # Belirlemek istediğiniz veritabanı ismi


3 - Daha sonra klasörde bulunan "entrypoint.sh" dosyasını açın 
ve host ve port'u belirlediğiniz şekilde düzenleyin.

4 - "entrypoint.sh" dosyayı çalıştırın. Gerekli paketler kurulup veritabanı ve tablolar oluşacaktır.
Ardından flask app, run olacaktır.

5- ApartmentMS_Frontend projesini indirin - > https://github.com/FerhatCakircali/ApartmentMS_Frontend
6- ApartmentMS_Frontend klasörünü açın. Gerekli diğer bilgiler oradaki README dosyasında yazacaktır.

