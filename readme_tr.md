
# Vector Job

Vector Job, Baykar Savunma Sanayisine başvuru çalışması olarak oluşturulmuştur. Birden fazla teknoloji ve yazılım araçları kullanılmıştır.

## İçindekiler
* [Vector Job Nedir?](#vectorjob)
* [Kullanılan Teknolojiler](#tech)
* [Kurulum](#setup)

<a name="vectorjob">
<h2>Vector Job Nedir?</h2>
</a>

Vector Job, kolayca iş bulabileceğiniz ve başvurularınızı yönetebileceğiniz, eğer bir yönetici iseniz iş ilanı açabileceğiniz bir iş arama platformudur. Kendinize uygun iş ilanlarını filtreleyerek iş akışınızda görüntüleyebilir ve beğendiğiniz bir veya birden fazla iş ilanına başvurabilirsiniz.

**Not:** Kayıt olurken email adresinize bir aktivasyon linki gönderilecektir. Aktivasyon linkine tıklamadan hesabınız aktif olmayacaktır. Eğer mail'i görüntüleyemiyorsanız lütfen spam'ları da kontol etmeyi unutmayınız!

<code>Vecor Job Web Sitesi: http://ec2-52-12-227-159.us-west-2.compute.amazonaws.com </code>

<a name="tech">
<h2>Kullanılan Teknolojiler</h2>
</a>

Vector Job birden fazla teknoloji ve araç kullanılarak oluşturulmuştur. Aşağıdaki teknolojiler ile Vector Job projesi geliştirilmiştir.

* AWS (Amazon Web Services)
* Docker
* Docker Compose
* NGINX
* Git / Github (for easy deployment integration)
* PostgreSQL
* Django
* Python
* HTML / CSS / Javascript
* Bash Script
* uWSGI

Docker kullanılarak geliştirilen Vector Job kolay ve kullanışlı bir CI/CD operasyon süreci sunmaktadır. Github ile entegre bir şekilde çalışan Docker, bir kaç komut ile test ortamından production ortamına entegre edilebilmektedir.

AWS tarafında ise EC2 (Elastic Compute Cloud) ile beraber ( Ubuntu 22.04 LTS Server kullanılmıştır) bulut tabanlı bir sistem tasarlanmıştır. Docker ve Git / Github teknolojileri tarafından sağlanan kolay entegrasyon ile beraber Vector Job projesi yerel sunucularda veyahut dilediğiniz bir sunucuda çalışabilmektedir. Kurulum ile ilgili detaylı bilgi [kurulum](#setup) başlığı altında paylaşılacaktır.


<a name="setup">
<h2>Kurulum</h2>
</a>

Öncelikle projeyi indirmeniz ve proje dizinine gitmeniz gerekmektedir.

```bash
git clone https://github.com/veyselaksin/vector-job.git
cd vector-job
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

Eğer projeyi yerel bir sunucuda başlatmak ve deploy etmek istiyorsanız aşağıdaki komut satırlarını çalıştırmanız gerekmektedir.

```bash
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml run --rm app sh -c "python manage.py createsuperuser"
docker-compose -f docker-compose-prod.yml run --rm app sh -c "python manage.py makemigrations"
docker-compose -f docker-compose-prod.yml up -d
```

Production mod üzerinde çalışırken <code> -f docker-compose-prod.yml </code> parametreleri eklenmiştir. "-f" ifadesi spesifik olarak bir dosyanın build edileceğini ifade etmektedir. Eğer production modda çalışmayacaksanız lütfen bu komut satırlarını kullanmayız.
