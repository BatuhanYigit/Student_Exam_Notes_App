<a name="tech">
<h2>Kullanılan Teknolojiler</h2>
</a>

* Docker
* Docker Compose
* Git / Github (for easy deployment integration)
* PostgreSQL
* Python
* Fastapi

Docker kullanılarak geliştirilen Vector Job kolay ve kullanışlı bir CI/CD operasyon süreci sunmaktadır. Github ile entegre bir şekilde çalışan Docker, bir kaç komut ile test ortamından production ortamına entegre edilebilmektedir.


<a name="setup">
<h2>Kurulum</h2>
</a>

Öncelikle projeyi indirmeniz ve proje dizinine gitmeniz gerekmektedir.

```bash
git clone https://github.com/BatuhanYigit/Student_Exam_Notes_App
cd Student_Exam_Notes_App
```

Eğer projeyi yerel bir bilgisayarda başlatmak ve test etmek istiyorsanız aşağıdaki komut satırlarını çalıştırmanız gerekmektedir.

**Not:** Projeyi çalıştırabilmek için docker gerekmektedir. Aksi halde proje çalıştırmayı durduracak ve hata alacaksınız.

**Not 2:** Eğer projede docker-compose version hatası alırsanız <code>docker-compose</code> versionunuzu güncellemeyi unutmayınız!

**Not 3:** Linux işletim sistemine sahip bir bilgisayarda çalışıyorsanız lütfen projenin ana dizinine gelip <code> sudo chmod -R a+rwx ./data </code> komutunu terminal üzerinde çalıştırınız.

```bash
docker-compose build
docker-compose run --rm app sh -c "python manage.py createsuperuser"
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose up
```

* <code>docker-compose build</code> komutu docker dosyasının çalıştırılabilir hale gelmesini sağlar.
* <code>docker-compose run --rm app sh -c "python manage.py createsuperuser"</code> komutu Django Uygulamamızın admin paneline girişi için kullanıcı adı ve şifre oluşturmamıza yardımcı olan komuttur.
* <code>docker-compose run --rm app sh -c "python manage.py makemigrations"</code> komutu database modelleri üzerinde bir değişiklik, ekleme ve çıkarma yapıldığı zaman kullanılan bir komuttur. Eğer birden fazla veritabanı kullanıyorsanız lütfen kullanırken spesifik olarak veritabanını belirtiniz!
* <code>docker-compose up</code> ise projenin ayağa kalkmasını sağlayan komuttur.

```
Projeyi Docker üzerinden ayağa kaldırdıktan sonra http://localhost:8000/docs üzerinden fastapinin bize sağladığı swagger üzerinden apileri kontrol edip database e erişebilirsiniz.
