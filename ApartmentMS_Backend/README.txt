1 - PostgreSQL'i kurun.

2 - PostgreSQL'i kurduktan sonra, klasörde bulunan ".env" uzantılı dosyayı açın 
ve DB_HOST, DB_PORT, DB_USER, DB_PASSWORD belirdeğiniz şekilde ve DB_NAME'i de olmasını istediğiniz veritabanı ismi şeklinde yeniden düzenleyip kaydedin.

3 - Daha sonra klasörde bulunan "entrypoint.sh" dosyasını açın 
ve host ve port'u belirlediğiniz şekilde düzenleyin.

4 - "entrypoint.sh" dosyayı çalıştırın. Gerekli paketler kurulup veritabanı ve tablolar oluşacaktır.
Ardından flask app, run olacaktır.

5- ApartmentMS_Frontend klasörünü açın. Gerekli diğer bilgiler oradaki README dosyasında yazacaktır.

