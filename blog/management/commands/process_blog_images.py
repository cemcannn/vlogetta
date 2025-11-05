from django.core.management.base import BaseCommand
from blog.models import BlogPost
import os

class Command(BaseCommand):
    help = 'Mevcut blog kapak resimlerini otomatik olarak işler ve boyutlandırır'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Tüm resimleri zorla yeniden işle',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        # Resmi olan tüm blog postlarını al
        blog_posts = BlogPost.objects.filter(image__isnull=False).exclude(image='')
        
        if not blog_posts.exists():
            self.stdout.write(
                self.style.WARNING('Kapak resmi olan blog postu bulunamadı.')
            )
            return
        
        self.stdout.write(f'Toplam {blog_posts.count()} blog postunun kapak resmi işlenecek...')
        
        processed_count = 0
        error_count = 0
        
        for blog_post in blog_posts:
            try:
                # Resim dosyasının varlığını kontrol et
                if not os.path.exists(blog_post.image.path):
                    self.stdout.write(
                        self.style.WARNING(
                            f'❌ {blog_post.name}: Resim dosyası bulunamadı ({blog_post.image.path})'
                        )
                    )
                    error_count += 1
                    continue
                
                # Resim işleme
                self.stdout.write(f'🖼️  İşleniyor: {blog_post.name}')
                blog_post.process_cover_image()
                blog_post.create_index_thumbnail()
                processed_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {blog_post.name}: Başarıyla işlendi')
                )
                
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ {blog_post.name}: Hata - {str(e)}'
                    )
                )
        
        # Özet bilgi
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'📊 İşlem Tamamlandı!')
        self.stdout.write(f'✅ Başarılı: {processed_count}')
        self.stdout.write(f'❌ Hatalı: {error_count}')
        self.stdout.write(f'📝 Toplam: {blog_posts.count()}')
        
        if processed_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎉 {processed_count} blog postunun kapak resmi başarıyla güncellendi!'
                )
            )
        
        if error_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️ {error_count} blog postunda hata oluştu. Lütfen kontrol edin.'
                )
            )
