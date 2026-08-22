from django.contrib import admin

from .models import BirthdayList, BirthdayName, HeadcountImport, HeadcountMember


class HeadcountMemberInline(admin.TabularInline):
    model = HeadcountMember
    extra = 0
    readonly_fields = ('nome', 'turno', 'work_group', 'team', 'area')
    can_delete = False


@admin.register(HeadcountImport)
class HeadcountImportAdmin(admin.ModelAdmin):
    list_display = ('mes', 'total_membros', 'criado_em')
    list_filter = ('mes', 'criado_em')
    search_fields = ('mes',)
    inlines = [HeadcountMemberInline]


@admin.register(HeadcountMember)
class HeadcountMemberAdmin(admin.ModelAdmin):
    list_display = ('nome', 'turno', 'work_group', 'team', 'area', 'importacao')
    list_filter = ('turno', 'work_group', 'team', 'importacao__mes')
    search_fields = ('nome', 'work_group', 'team', 'area')


class BirthdayNameInline(admin.TabularInline):
    model = BirthdayName
    extra = 0
    readonly_fields = ('nome', 'membro')


@admin.register(BirthdayList)
class BirthdayListAdmin(admin.ModelAdmin):
    list_display = ('mes', 'headcount', 'criado_em')
    list_filter = ('mes', 'criado_em')
    inlines = [BirthdayNameInline]

# Register your models here.
