from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator


class Curator(models.Model):
    class Meta:
        verbose_name = "Куратор (Подразделение)"
        verbose_name_plural = "Кураторы (Подразделения)"

    title = models.CharField(
        max_length=120,
        verbose_name="Куратор"
    )

    def __str__(self):
        return self.title.__str__()


class UserTypes(models.Model):
    class Meta:
        verbose_name = "Тип пользователя"
        verbose_name_plural = "Типы пользователя"

    title = models.CharField(
        max_length=120,
        verbose_name="Тип пользователя",
        help_text="Администратор, Куратор, БПиЭА, Пользователь, Экономист, Спкциалист АСЭЗ, Юрист"
    )

    def __str__(self):
        return self.title.__str__()


class CustomUser(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name="Пользователь")
    curator = models.ForeignKey(
        Curator,
        verbose_name="Подразделение (Куратор)",
        on_delete=models.DO_NOTHING
    )
    email = models.EmailField()
    name = models.CharField(
        max_length=150,
        verbose_name="Фамилия, Имя, Отчество"
    )
    position = models.CharField(
        max_length=200,
        verbose_name="Должность",
        null=True,
        blank=True
    )
    user_type = models.ForeignKey(
        UserTypes,
        verbose_name="Тип пользователя (Пользователь, Администратор, Куратор, Суперпользователь, БПиЭА, Юрист, Экономист, Специалист АСЭЗ)",
        on_delete=models.DO_NOTHING
    )
    blocked_status = models.BooleanField(
        default=True,
        verbose_name="Активный пользователь/Заблокированный"
    )

    def __str__(self):
        return self.user.__str__()


class UserActivityJournal(models.Model):
    class Meta:
        verbose_name = 'Журнал действий пользователя'
        verbose_name_plural = 'Журналы действий пользователя'

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE
    )
    date_time_of_activity = models.DateTimeField(
        verbose_name="Дата и время работы пользователя в системе",
        auto_now_add=True
    )
    activity = models.CharField(
        max_length=200,
        verbose_name="Действия пользователя в системе",
        blank=True,
        null=True
    )
    clicks = models.PositiveIntegerField(
        verbose_name="Количество кликов пользователя",
        default=0
    )
    activity_system_module = models.CharField(
        max_length=100,
        verbose_name="Раздел системы",
        blank=True
    )

    def __str__(self):
        try:
            return 'Журнал действий пользователя: {0}'.format(self.user)
        except:
            return 'Ошибка в данных'


class FinanceCosts(models.Model):
    class Meta:
        verbose_name = 'Статья финансирования'
        verbose_name_plural = 'Статьи финансирования'

    title = models.CharField(
        verbose_name="Название статьи",
        max_length=100
    )
    def __str__(self):
        return self.title


class PurchaseType(models.Model):
    class Meta:
        verbose_name = 'Тип закупки'
        verbose_name_plural = 'Типы закупок'

    title = models.CharField(
        max_length=200,
        verbose_name="Вид закупки (Конкурентная, неконкурентная)"
    )

    def __str__(self):
        return self.title.__str__()


class ActivityForm(models.Model):
    class Meta:
        verbose_name = 'Вид деятельности'
        verbose_name_plural = 'Виды деятельности'

    title = models.CharField(
        max_length=200,
        verbose_name="Вид деятельности"
    )

    def __str__(self):
        return self.title.__str__()


class StateASEZ(models.Model):
    class Meta:
        verbose_name = 'Состояние АСЭЗ'
        verbose_name_plural = 'Состояние АСЭЗ'

    title = models.CharField(
        max_length=200,
        verbose_name="Состояние АСЭЗ"
    )

    def __str__(self):
        return self.title.__str__()


class NumberPZTRU(models.Model):
    class Meta:
        verbose_name = 'Номер пункта Положения о закупках товаров, работ, услуг ПАО "Газпром"'
        verbose_name_plural = 'Номера пунктов Положения о закупках товаров, работ, услуг ПАО "Газпром"'

    title = models.CharField(
        max_length=200,
        verbose_name="Номер пункта ПоЗТРУ"
    )

    def __str__(self):
        return self.title.__str__()


class ContractStatus(models.Model):
    class Meta:
        verbose_name = 'Статус договора'
        verbose_name_plural = 'Статусы договоров'

    title = models.CharField(
        max_length=200,
        verbose_name="Статус договора"
    )

    def __str__(self):
        return self.title.__str__()


class Currency(models.Model):
    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Типы валют'

    title = models.CharField(
        max_length=10,
        verbose_name="Валюта"
    )

    def __str__(self):
        return self.title.__str__()


class ContractType(models.Model):
    class Meta:
        verbose_name = 'Тип договора (Центр/Филиал)'
        verbose_name_plural = 'Типы договоров (Центр/Филиал)'

    title = models.CharField(
        max_length=150,
        help_text="Тип договора(Центр, Филиал)"
    )

    def __str__(self):
        return self.title.__str__()


class ContractMode(models.Model):
    class Meta:
        verbose_name = 'Вид договора (Основной/ доп. соглашение)'
        verbose_name_plural = 'Виды договоров (Основной/ доп. соглашение)'

    title = models.CharField(
        max_length=150,
        help_text="Вид договора (Основной, доп.соглашение)"
    )

    def __str__(self):
        return self.title.__str__()


class Counterpart(models.Model):
    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    name = models.CharField(
        max_length=100,
        verbose_name="Контрагент"
    )
    email = models.EmailField(blank=True)
    reg_addr = models.CharField(
        max_length=255,
        verbose_name="Юридический адрес",
        blank=True
    )
    UNP = models.CharField(
        max_length=100,
        verbose_name="УНП",
        blank=True
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона",
        blank=True
    )

    def __str__(self):
        try:
            return '%s УНП: %s' % (self.name, str(self.UNP))
        except:
            return 'Ошибка в данных'


class Contract(models.Model):
    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    title = models.CharField(
        max_length=150,
        verbose_name="Наименование договора"
    )
    finance_cost = models.ForeignKey(
        FinanceCosts,
        on_delete=models.DO_NOTHING,
        verbose_name="Статья финансирования")
    curator = models.ForeignKey(
        Curator,
        on_delete=models.DO_NOTHING,
        verbose_name="Куратор"
    )
    contract_type = models.ForeignKey(
        ContractType,
        verbose_name="Тип договора",
        on_delete=models.DO_NOTHING,
        help_text="Филиал или центръ"
    )
    contract_mode = models.ForeignKey(
        ContractMode,
        verbose_name="Вид договора",
        on_delete=models.DO_NOTHING,
        help_text="Основной либо доп.согл.")
    purchase_type = models.ForeignKey(
        PurchaseType,
        verbose_name="Тип закупки",
        on_delete=models.DO_NOTHING,
        help_text="Вид закупки (конкурентная, неконкурентная)"
    )
    activity_form = models.ForeignKey(
        ActivityForm,
        verbose_name="Вид деятельности",
        on_delete=models.DO_NOTHING
    )
    stateASEZ = models.ForeignKey(
        StateASEZ,
        verbose_name="Состояние в Автоматизированной системе эллектронных закупок",
        on_delete=models.DO_NOTHING
    )
    number_ppz = models.CharField(
        max_length=150,
        verbose_name="Номер позиции плана закупок",
        null=True,
        blank=True
    )
    number_PZTRU = models.ForeignKey(
        NumberPZTRU,
        verbose_name="ПЗТРУ",
        help_text="Номер Положения о закупках товаров, работ, услуг",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    contract_status = models.ForeignKey(
        ContractStatus,
        verbose_name="Статус договора",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    plan_load_date_ASEZ = models.DateField(
        verbose_name="планируемая дата загрузки в АСЭЗ",
    )
    fact_load_date_ASEZ = models.DateField(
        verbose_name="фактическая дата загрузки в АСЭЗ",
        null=True,
        blank=True
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.DO_NOTHING,
        verbose_name="Валюта договора",
        blank=True,
        null=True
    )
    number_KGG = models.CharField(
        max_length=100,
        verbose_name="номер договора от центрального органа",
        null=True,
        blank=True
    )
    register_number_SAP = models.CharField(
        max_length=100,
        verbose_name="Регистрационный номер в САП",
        null=True,
        blank=True
    )
    contract_number = models.CharField(
        max_length=100,
        verbose_name="Номер договора",
        null=True,
        blank=True
    )
    plan_sign_date = models.DateField(
        verbose_name="Планируемая дата подписания договора"
    )
    fact_sign_date = models.DateField(
        verbose_name="Фактическая дата подписания договора",
        null=True,
        blank=True
    )
    start_date = models.DateField(
        verbose_name="дата начала контракта"
    )
    end_time = models.DateField(
        verbose_name="дата окончания",
        null=True, blank=True
    )
    counterpart = models.ForeignKey(
        Counterpart,
        on_delete=models.DO_NOTHING,
        verbose_name="Контрагент"
    )
    related_contract = models.ForeignKey(
        "Contract",
        on_delete=models.DO_NOTHING,
        verbose_name="Связанный договор",
        blank=True,
        null=True
    )
    contract_active = models.BooleanField(
        default=True,
        verbose_name="Действующий/Удаленный договор",
        blank=True,
        null=True
    )

    def __str__(self):
        try:
            return 'Договор %s, куратор %s, ст. фин %s' % (self.title,
                                                           self.curator,
                                                           self.finance_cost)
        except:
            return 'Ошибка в данных'

    def get_absolute_url(self):
        return reverse('planes:change_contract', kwargs={'contract_id':self.id})


class SumsRUR(models.Model): # TODO is that only in RUR or in eny foregin currency?
    class Meta:
        verbose_name = 'Показатели договора в иностранной валюте'
        verbose_name_plural = 'Показатели договора в иностранной валюте'

    YEARS = [ # TODO make YEARS as FK to YEARS model?
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
    ]

    contract = models.ForeignKey(
        Contract,
        verbose_name="Контракт",
        on_delete=models.CASCADE
    )
    year = models.CharField(
        verbose_name="Год",
        choices=YEARS,
        max_length=4
    )
    start_max_price_ASEZ_NDS = MoneyField(
        verbose_name="стартовая цена АСЭЗ с НДС ",
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        default_currency=('RUR', 'RUB')
    )
    currency_rate_on_load_date_ASEZ_NDS = MoneyField(
        verbose_name="Курс валюты на дату загрузки в бел.руб.",
        null=True,
        blank=True,
        decimal_places=5,
        max_digits=12,
        default_currency=('RUR', 'RUB')
    )
    contract_sum_NDS_RUB = MoneyField(
        verbose_name="Сумма договора с НДС рос.руб.",
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency=('RUR', 'RUB')
    )
    currency = models.ForeignKey( # TODO what to do with this
        Currency,
        verbose_name="Валюта",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    delta_data_ASEZ = MoneyField(
        verbose_name="Отклонение от НМЦ в АСЭЗ",
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency=('RUR', 'RUB')
    )

    def __str__(self):
        try:
            return 'Показатели договора %s в российских рублях' % (self.contract)
        except:
            return 'Ошибка в данных'

    def save(self, *args, **kwargs):
        try:
            sum_byn = SumsBYN.objects.filter(year=self.year).filter(period='year').get(contract_id=self.contract_id).contract_sum_with_NDS_BYN
            self.contract_sum_NDS_RUB = sum_byn * self.currency_rate_on_load_date_ASEZ_NDS
            self.delta_data_ASEZ = self.start_max_price_ASEZ_NDS - self.contract_sum_NDS_RUB
        except:
            self.contract_sum_NDS_RUB = 0
            self.delta_data_ASEZ = 0
        super().save(*args, **kwargs)


class SumsBYN(models.Model):
    class Meta:
        verbose_name = 'Показатели договора в белорусских рублях'
        verbose_name_plural = 'Показатели договора в белорусских рублях'
       # unique_together = [['contract', 'year', 'period']]

    YEARS = [
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
    ]
    PERIODS = [
        ("year", "year"),
        ("1quart", "1 quarter"),
        ("2quart", "2 quarter"),
        ("3quart", "3 quarter"),
        ("4quart", "4 quarter"),
        ("6months", "6months"),
        ("9months", "9months"),
        ("10months", "10months"),
        ("11months", "11months"),
        ("jan", "january"),
        ("feb", "february"),
        ("mar", "march"),
        ("apr", "april"),
        ("may", "may"),
        ("jun", "june"),
        ("jul", "july"),
        ("aug", "august"),
        ("sep", "september"),
        ("oct", "october"),
        ("nov", "november"),
        ("dec", "december")
    ]
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        verbose_name="Контракт"
    )
    year = models.CharField(
        verbose_name="Год",
        choices=YEARS,
        max_length=4
    )
    period = models.CharField(
        choices=PERIODS,
        verbose_name="Период",
        max_length=15
    )
    plan_sum_SAP = MoneyField(
        verbose_name="Плановая сумма САП",
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    contract_sum_without_NDS_BYN = MoneyField(
        verbose_name="Сумма всего договора без НДС",
        default=0,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    contract_sum_with_NDS_BYN = MoneyField(
        verbose_name="Сумма договора с НДС бел.руб.",
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    contract_total_sum_with_sub_BYN = MoneyField(
        verbose_name='Общая сумма договора всего с доп соглашениями, б.р. без ндс',
        null=True,
        blank=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    forecast_total = MoneyField(
        verbose_name='Прогноз',
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    economy_total = MoneyField(
        verbose_name='Экономия',
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    fact_total = MoneyField(
        verbose_name='Факт',
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    economy_contract_result = MoneyField(
        verbose_name='Экономия по результатам исполнения договоров всего',
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    total_sum_unsigned_contracts = MoneyField( # TODO wat IT IS
        verbose_name='Сумма средств по незаключенным договорам',
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )
    economy_total_absolute = MoneyField(
        verbose_name='Абсолютная экономия по договору, всего',
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=12,
        default_currency='BYN'
    )

    def __str__(self):
        try:
            return 'Показатели договора %s в белорусских рублях за %s год %s' % (self.contract, self.year, self.period)
        except:
            return 'Ошибка в данных'


class ContractRemarks(models.Model):
    class Meta:
        verbose_name = 'Примечание к договору'
        verbose_name_plural = 'Примечания к договору'

    contract = models.ForeignKey(
        Contract,
        verbose_name="Контракт",
        on_delete=models.CASCADE
    )
    remark_text = models.TextField(
        verbose_name="Текст примечания"
    )

    def __str__(self):
        try:
            return 'Примечание к Договору {0}'.format(self.contract)
        except:
            return 'Ошибка в данных'


class ContractPaymentSchedule(models.Model):
    class Meta:
        verbose_name = 'График платежей по договору'
        verbose_name_plural = 'Графики платежей по договору'

    contract = models.ForeignKey(
        Contract,
        verbose_name="Договора",
        on_delete=models.CASCADE
    )
    payment_date = models.DateField(
        verbose_name="Дата платежа"
    )

    def __str__(self):
        try:
            return 'График платежей по договору : {0}, оплата до: {1}'.format(self.contract, self.payment_date)
        except:
            return 'Ошибка в данных'


class Planning(models.Model):
    class Meta:
        verbose_name = 'Планирование'
        verbose_name_plural = 'Планирование'
        unique_together = [['FinanceCosts', 'curator', 'year']]

    YEARS = [
        ("2018", "2018"),
        ("2019", "2019"),
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
    ]

    FinanceCosts = models.ForeignKey(
        FinanceCosts,
        verbose_name="Статья финансирования",
        on_delete=models.DO_NOTHING,
        related_name='with_planning',
    )
    curator = models.ForeignKey(
        Curator,
        verbose_name="Куратор",
        on_delete=models.DO_NOTHING
    )
    year = models.CharField(
        verbose_name="Год",
        choices=YEARS,
        max_length=4
    )
    q_1 = models.DecimalField(
        verbose_name="Сумма лимита 1 квартал",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
    )
    q_2 = models.DecimalField(
        verbose_name="Сумма лимита 2 квартал",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
    )
    q_3 = models.DecimalField(
        verbose_name="Сумма лимита 3 квартал",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
    )
    q_4 = models.DecimalField(
        verbose_name="Сумма лимита 4 квартал",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
    )
    q_all = models.DecimalField(
        verbose_name="Сумма лимита за весь год",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True
    )

    def __str__(self):
        return '{0} : {1}'.format(self.FinanceCosts.title, self.curator.title)
        
    def save(self, *args, **kwargs):
        self.q_all = self.q_1 + self.q_2 + self.q_3 + self.q_4
        super().save(*args, **kwargs)

