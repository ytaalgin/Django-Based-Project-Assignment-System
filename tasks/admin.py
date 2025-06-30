from django.urls import path
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse
from .models import Task, CustomUser, Unavailability
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.db.models import Count, Sum
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# Customize Admin Site Headers
admin.site.site_header = _("ÇELİKKANAT RS Admin")
admin.site.site_title = _("ÇELİKKANAT RS Admin Portal")
admin.site.index_title = _("Welcome to the ÇELİKKANAT RS Administration")

# Register Unavailability model
admin.site.register(Unavailability)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'is_completed', 'score']
    list_filter = ['is_completed']
    search_fields = ['title', 'assigned_to__email']
    fieldsets = (
        (None, {
            'fields': (
            'title', 'description', 'start_date', 'end_date', 'assigned_to', 'is_completed', 'score', 'document',
            'completed_date')
        }),
    )

    @admin.display(description='Document')
    def document(self, obj):
        if obj.document:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.document.url)
        return "No document uploaded"


admin.site.register(Task, TaskAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('is_admin',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_admin'),
        }),
    )

    # Kullanıcının tamamladığı görevlere verilen puanların toplamı
    def total_score(self, obj):
        score = Task.objects.filter(assigned_to=obj, is_completed=True).aggregate(total_score=Sum('score'))
        return score['total_score'] or 0  # Eğer puan yoksa 0 göster

    total_score.short_description = 'Total Score'

    # Müsait olmayan günler ve toplam puanları göster
    list_display = ['email', 'is_admin', 'total_score', 'get_unavailabilities']  # Sadece var olan alanları kullanıyoruz
    list_filter = ['is_admin']  # 'is_completed' yanlış, çünkü bu CustomUser ile ilgili değil
    search_fields = ['email']
    ordering = []

    def get_unavailabilities(self, obj):
        return ", ".join([str(a) for a in obj.unavailability_set.all()])

    get_unavailabilities.short_description = 'Unavailable Days'

    # Performans grafiği için verileri toplar ve context'e ekler
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        labels, data = self.get_performance_data()
        extra_context['labels'] = labels
        extra_context['data'] = data
        return super().changelist_view(request, extra_context=extra_context)

    # Kullanıcıların tamamladığı görevler için puanlama verilerini alır
    @staticmethod
    def get_performance_data():
        performance_data = (
            Task.objects.filter(is_completed=True)
            .values('assigned_to__email')
            .annotate(total_score=Sum('score'))
            .order_by('-total_score')
        )
        labels = [item['assigned_to__email'] for item in performance_data]
        data = [item['total_score'] for item in performance_data]
        return labels, data

    # Admin sayfasında performans grafiği ekleyebilmek için gerekli URL'leri ekler
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('performance-data/', self.admin_site.admin_view(self.performance_data_view), name='performance_data'),
        ]
        return custom_urls + urls

    # Performans verilerini JSON formatında döndürmek için bir view oluşturur
    def performance_data_view(self, request):
        labels, data = self.get_performance_data()
        return JsonResponse({'labels': labels, 'data': data})


admin.site.register(CustomUser, CustomUserAdmin)
