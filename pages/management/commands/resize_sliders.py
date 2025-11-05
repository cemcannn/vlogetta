from django.core.management.base import BaseCommand
from pages.models import Slider

class Command(BaseCommand):
    help = 'Mevcut slider resimlerini yeniden boyutlandır'

    def handle(self, *args, **options):
        sliders = Slider.objects.all()
        
        if not sliders.exists():
            self.stdout.write(
                self.style.WARNING('Hiç slider bulunamadı.')
            )
            return
        
        for slider in sliders:
            if slider.image:
                try:
                    # save() metodunu çağırarak resize işlemini tetikle
                    slider.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ {slider.title} - resim başarıyla yeniden boyutlandırıldı'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ {slider.title} - hata: {str(e)}'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️ {slider.title} - resim yok'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 İşlem tamamlandı! {sliders.count()} slider kontrol edildi.'
            )
        )
