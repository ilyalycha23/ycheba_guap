#!/usr/bin/env python3
"""Full metadata rename refactor: computer club -> cinema center."""
from __future__ import annotations

import os
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"

# Longest-first text replacements across all source files
REPLACEMENTS: list[tuple[str, str]] = [
    # Tabular sections (before parent documents)
    (
        "Document.ПоступлениеКомпьютеров.TabularSection.Компьютеры.Attribute.Компьютер",
        "Document.ВводЗалаВЭксплуатацию.TabularSection.Кинозалы.Attribute.Кинозал",
    ),
    (
        "Document.ПоступлениеКомпьютеров.TabularSection.Компьютеры",
        "Document.ВводЗалаВЭксплуатацию.TabularSection.Кинозалы",
    ),
    (
        "Document.СписаниеКомпьютеров.TabularSection.Компьютеры.Attribute.Компьютер",
        "Document.ВыводЗалаИзЭксплуатации.TabularSection.Кинозалы.Attribute.Кинозал",
    ),
    (
        "Document.СписаниеКомпьютеров.TabularSection.Компьютеры",
        "Document.ВыводЗалаИзЭксплуатации.TabularSection.Кинозалы",
    ),
    # Report templates
    (
        "Report.ЗагруженностьПК.Template.ОсновнаяСхемаКомпоновкиДанных",
        "Report.ЗаполняемостьЗалов.Template.ОсновнаяСхемаКомпоновкиДанных",
    ),
    # Business process
    (
        "BusinessProcessRoutePointRef.ОбслуживаниеКлиента",
        "BusinessProcessRoutePointRef.ОбслуживаниеПосетителя",
    ),
    (
        "BusinessProcess.ОбслуживаниеКлиента.Attribute.ЗаказУслуги",
        "BusinessProcess.ОбслуживаниеПосетителя.Attribute.ЗаказВБар",
    ),
    ("BusinessProcessManager.ОбслуживаниеКлиента", "BusinessProcessManager.ОбслуживаниеПосетителя"),
    ("BusinessProcessObject.ОбслуживаниеКлиента", "BusinessProcessObject.ОбслуживаниеПосетителя"),
    ("BusinessProcessSelection.ОбслуживаниеКлиента", "BusinessProcessSelection.ОбслуживаниеПосетителя"),
    ("BusinessProcessList.ОбслуживаниеКлиента", "BusinessProcessList.ОбслуживаниеПосетителя"),
    ("BusinessProcessRef.ОбслуживаниеКлиента", "BusinessProcessRef.ОбслуживаниеПосетителя"),
    ("BusinessProcess.ОбслуживаниеКлиента", "BusinessProcess.ОбслуживаниеПосетителя"),
    # Documents
    ("DocumentObject.ПоступлениеКомпьютеров", "DocumentObject.ВводЗалаВЭксплуатацию"),
    ("DocumentRef.ПоступлениеКомпьютеров", "DocumentRef.ВводЗалаВЭксплуатацию"),
    ("DocumentManager.ПоступлениеКомпьютеров", "DocumentManager.ВводЗалаВЭксплуатацию"),
    ("DocumentList.ПоступлениеКомпьютеров", "DocumentList.ВводЗалаВЭксплуатацию"),
    ("DocumentSelection.ПоступлениеКомпьютеров", "DocumentSelection.ВводЗалаВЭксплуатацию"),
    ("Document.ПоступлениеКомпьютеров", "Document.ВводЗалаВЭксплуатацию"),
    ("DocumentObject.СписаниеКомпьютеров", "DocumentObject.ВыводЗалаИзЭксплуатации"),
    ("DocumentRef.СписаниеКомпьютеров", "DocumentRef.ВыводЗалаИзЭксплуатации"),
    ("DocumentManager.СписаниеКомпьютеров", "DocumentManager.ВыводЗалаИзЭксплуатации"),
    ("DocumentList.СписаниеКомпьютеров", "DocumentList.ВыводЗалаИзЭксплуатации"),
    ("DocumentSelection.СписаниеКомпьютеров", "DocumentSelection.ВыводЗалаИзЭксплуатации"),
    ("Document.СписаниеКомпьютеров", "Document.ВыводЗалаИзЭксплуатации"),
    ("DocumentObject.СеансБронирования", "DocumentObject.ПродажаБилетов"),
    ("DocumentRef.СеансБронирования", "DocumentRef.ПродажаБилетов"),
    ("DocumentManager.СеансБронирования", "DocumentManager.ПродажаБилетов"),
    ("DocumentList.СеансБронирования", "DocumentList.ПродажаБилетов"),
    ("DocumentSelection.СеансБронирования", "DocumentSelection.ПродажаБилетов"),
    ("Document.СеансБронирования", "Document.ПродажаБилетов"),
    ("DocumentObject.ЗаявкаНаБронь", "DocumentObject.ЗаявкаНаБроньБилетов"),
    ("DocumentRef.ЗаявкаНаБронь", "DocumentRef.ЗаявкаНаБроньБилетов"),
    ("DocumentManager.ЗаявкаНаБронь", "DocumentManager.ЗаявкаНаБроньБилетов"),
    ("DocumentList.ЗаявкаНаБронь", "DocumentList.ЗаявкаНаБроньБилетов"),
    ("DocumentSelection.ЗаявкаНаБронь", "DocumentSelection.ЗаявкаНаБроньБилетов"),
    ("Document.ЗаявкаНаБронь", "Document.ЗаявкаНаБроньБилетов"),
    ("DocumentObject.ЗаказУслуги", "DocumentObject.ЗаказВБар"),
    ("DocumentRef.ЗаказУслуги", "DocumentRef.ЗаказВБар"),
    ("DocumentManager.ЗаказУслуги", "DocumentManager.ЗаказВБар"),
    ("DocumentList.ЗаказУслуги", "DocumentList.ЗаказВБар"),
    ("DocumentSelection.ЗаказУслуги", "DocumentSelection.ЗаказВБар"),
    ("Document.ЗаказУслуги", "Document.ЗаказВБар"),
    # Registers
    (
        "InformationRegisterRecordSet.ИсторияСтатусовПК",
        "InformationRegisterRecordSet.ИсторияСтатусовЗалов",
    ),
    (
        "InformationRegisterRecordKey.ИсторияСтатусовПК",
        "InformationRegisterRecordKey.ИсторияСтатусовЗалов",
    ),
    (
        "InformationRegisterRecord.ИсторияСтатусовПК",
        "InformationRegisterRecord.ИсторияСтатусовЗалов",
    ),
    (
        "InformationRegisterSelection.ИсторияСтатусовПК",
        "InformationRegisterSelection.ИсторияСтатусовЗалов",
    ),
    (
        "InformationRegisterList.ИсторияСтатусовПК",
        "InformationRegisterList.ИсторияСтатусовЗалов",
    ),
    (
        "InformationRegisterManager.ИсторияСтатусовПК",
        "InformationRegisterManager.ИсторияСтатусовЗалов",
    ),
    ("InformationRegister.ИсторияСтатусовПК", "InformationRegister.ИсторияСтатусовЗалов"),
    (
        "AccumulationRegisterRecordSet.ВыручкаИВремя",
        "AccumulationRegisterRecordSet.ВыручкаПоБилетам",
    ),
    (
        "AccumulationRegisterRecordKey.ВыручкаИВремя",
        "AccumulationRegisterRecordKey.ВыручкаПоБилетам",
    ),
    (
        "AccumulationRegisterRecord.ВыручкаИВремя",
        "AccumulationRegisterRecord.ВыручкаПоБилетам",
    ),
    (
        "AccumulationRegisterSelection.ВыручкаИВремя",
        "AccumulationRegisterSelection.ВыручкаПоБилетам",
    ),
    ("AccumulationRegisterList.ВыручкаИВремя", "AccumulationRegisterList.ВыручкаПоБилетам"),
    (
        "AccumulationRegisterManager.ВыручкаИВремя",
        "AccumulationRegisterManager.ВыручкаПоБилетам",
    ),
    ("AccumulationRegister.ВыручкаИВремя", "AccumulationRegister.ВыручкаПоБилетам"),
    # Catalogs
    ("Catalog.Компьютеры.Attribute.СебестоимостьВЧас", "Catalog.Кинозалы.Attribute.СебестоимостьЗала"),
    ("Catalog.Компьютеры.Attribute.Характеристики", "Catalog.Кинозалы.Attribute.ОписаниеЗала"),
    ("Catalog.Компьютеры.Attribute.Категория", "Catalog.Кинозалы.Attribute.КлассЗала"),
    ("CatalogObject.Компьютеры", "CatalogObject.Кинозалы"),
    ("CatalogRef.Компьютеры", "CatalogRef.Кинозалы"),
    ("CatalogSelection.Компьютеры", "CatalogSelection.Кинозалы"),
    ("CatalogList.Компьютеры", "CatalogList.Кинозалы"),
    ("CatalogManager.Компьютеры", "CatalogManager.Кинозалы"),
    ("Catalog.Компьютеры", "Catalog.Кинозалы"),
    ("Catalog.Тарифы.Attribute.ТипТарифа", "Catalog.ТипыБилетов.Attribute.КатегорияБилета"),
    ("CatalogObject.Тарифы", "CatalogObject.ТипыБилетов"),
    ("CatalogRef.Тарифы", "CatalogRef.ТипыБилетов"),
    ("CatalogSelection.Тарифы", "CatalogSelection.ТипыБилетов"),
    ("CatalogList.Тарифы", "CatalogList.ТипыБилетов"),
    ("CatalogManager.Тарифы", "CatalogManager.ТипыБилетов"),
    ("Catalog.Тарифы", "Catalog.ТипыБилетов"),
    # Enums
    ("EnumRef.СостоянияКомпьютеров", "EnumRef.СостоянияЗалов"),
    ("EnumManager.СостоянияКомпьютеров", "EnumManager.СостоянияЗалов"),
    ("EnumList.СостоянияКомпьютеров", "EnumList.СостоянияЗалов"),
    ("Enum.СостоянияКомпьютеров", "Enum.СостоянияЗалов"),
    ("EnumRef.СтатусыКомпьютеров", "EnumRef.СтатусыЗалов"),
    ("EnumManager.СтатусыКомпьютеров", "EnumManager.СтатусыЗалов"),
    ("EnumList.СтатусыКомпьютеров", "EnumList.СтатусыЗалов"),
    ("Enum.СтатусыКомпьютеров", "Enum.СтатусыЗалов"),
    # Reports & subsystems
    ("ReportObject.ЗагруженностьПК", "ReportObject.ЗаполняемостьЗалов"),
    ("ReportManager.ЗагруженностьПК", "ReportManager.ЗаполняемостьЗалов"),
    ("Report.ЗагруженностьПК", "Report.ЗаполняемостьЗалов"),
    ("Subsystem.СкладскойУчет", "Subsystem.БарКинотеатра"),
    ("Subsystem.Бронирование", "Subsystem.ПродажаБилетов"),
    # BSL Russian types
    ("Документ.ПоступлениеКомпьютеров", "Документ.ВводЗалаВЭксплуатацию"),
    ("Документ.СписаниеКомпьютеров", "Документ.ВыводЗалаИзЭксплуатации"),
    ("Документ.СеансБронирования", "Документ.ПродажаБилетов"),
    ("Документ.ЗаявкаНаБронь", "Документ.ЗаявкаНаБроньБилетов"),
    ("Документ.ЗаказУслуги", "Документ.ЗаказВБар"),
    ("ДокументСсылка.СеансБронирования", "ДокументСсылка.ПродажаБилетов"),
    ("ДокументСсылка.ЗаявкаНаБронь", "ДокументСсылка.ЗаявкаНаБроньБилетов"),
    ("ДокументСсылка.ЗаказУслуги", "ДокументСсылка.ЗаказВБар"),
    ("Справочник.Компьютеры", "Справочник.Кинозалы"),
    ("Справочник.Тарифы", "Справочник.ТипыБилетов"),
    ("Справочники.Должности", "Справочники.Должности"),
    ("БизнесПроцессы.ОбслуживаниеКлиента", "БизнесПроцессы.ОбслуживаниеПосетителя"),
    ("БизнесПроцесс.ОбслуживаниеКлиента", "БизнесПроцесс.ОбслуживаниеПосетителя"),
    ("Перечисления.СостоянияКомпьютеров", "Перечисления.СостоянияЗалов"),
    ("Перечисления.СтатусыКомпьютеров", "Перечисления.СтатусыЗалов"),
    ("РегистрНакопления.ВыручкаИВремя", "РегистрНакопления.ВыручкаПоБилетам"),
    ("РегистрСведений.ИсторияСтатусовПК", "РегистрСведений.ИсторияСтатусовЗалов"),
    # Query / report field paths
    ("ВыручкаИВремя.ОтработаноЧасовОборот", "ВыручкаПоБилетам.КоличествоБилетовОборот"),
    ("ВыручкаИВремя.Компьютер.СебестоимостьВЧас", "ВыручкаПоБилетам.Кинозал.СебестоимостьЗала"),
    ("ВыручкаИВремя.Компьютер", "ВыручкаПоБилетам.Кинозал"),
    ("ВыручкаИВремя.Тариф", "ВыручкаПоБилетам.ТипБилета"),
    ("ВыручкаИВремя.", "ВыручкаПоБилетам."),
    ("ИсторияСтатусовПК.", "ИсторияСтатусовЗалов."),
    # Route points
    ("ВстречаИПосадкаКлиента", "ВстречаПосетителя"),
    ("ОкончаниеУслугИОплата", "ОплатаБилетов"),
    ("ИгроваяСессия", "ПросмотрФильма"),
    # Form commands & handlers
    ("СоздатьНаОснованииЗаказУслуги", "СоздатьНаОснованииЗаказВБар"),
    ("ТарифПриИзменении", "ТипБилетаПриИзменении"),
    # Attributes & resources (after object paths)
    ("ОтработаноЧасовОборот", "КоличествоБилетовОборот"),
    ("ОтработаноЧасов", "КоличествоБилетов"),
    ("СебестоимостьВЧас", "СебестоимостьЗала"),
    ("ТипТарифа", "КатегорияБилета"),
    ("Catalog.Кинозалы.Attribute.Категория", "Catalog.Кинозалы.Attribute.КлассЗала"),
    # Tabular section & attribute short names in BSL/XML
    ("TabularSection.Компьютеры", "TabularSection.Кинозалы"),
    (".Attribute.Компьютер", ".Attribute.Кинозал"),
    (">Компьютер<", ">Кинозал<"),
    (".Dimension.Компьютер", ".Dimension.Кинозал"),
    (".Attribute.Тариф", ".Attribute.ТипБилета"),
    (">Тариф<", ">ТипБилета<"),
    (".Dimension.Тариф", ".Dimension.ТипБилета"),
    ("AccumulationRegister.ВыручкаПоБилетам.Resource.КоличествоБилетов", "AccumulationRegister.ВыручкаПоБилетам.Resource.КоличествоБилетов"),
    # Enum values
    ("СостоянияЗалов.Списан", "СостоянияЗалов.Закрыт"),
    ("СтатусыЗалов.Списан", "СтатусыЗалов.Закрыт"),
    # BSL identifiers
    ("Движения.ВыручкаИВремя", "Движения.ВыручкаПоБилетам"),
    ("Движения.ИсторияСтатусовПК", "Движения.ИсторияСтатусовЗалов"),
    ("Объект.Тариф", "Объект.ТипБилета"),
    ("Объект.Компьютер", "Объект.Кинозал"),
    # Variables in BSL (word boundaries approximated by common patterns)
    ("= Тариф", "= ТипБилета"),
    ("(Тариф)", "(ТипБилета)"),
    (" Тариф.", " ТипБилета."),
    (" Тариф,", " ТипБилета,"),
    (" Тариф ", " ТипБилета "),
    ("= Компьютер", "= Кинозал"),
    ("(Компьютер)", "(Кинозал)"),
    (" Компьютер.", " Кинозал."),
    (" Компьютер,", " Кинозал,"),
    (" Компьютер ", " Кинозал "),
    ("БП.Компьютер", "БП.Кинозал"),
    ("ДанныеЗаполнения.Компьютер", "ДанныеЗаполнения.Кинозал"),
    ("ДанныеЗаполнения.Тариф", "ДанныеЗаполнения.ТипБилета"),
    ("Заказ.Компьютер", "Заказ.Кинозал"),
    ("СтрокаТЧ.Компьютер", "СтрокаТЧ.Кинозал"),
    ("Движение.Компьютер", "Движение.Кинозал"),
    ("Движение.Тариф", "Движение.ТипБилета"),
    ("ДвижениеСтатус.Компьютер", "ДвижениеСтатус.Кинозал"),
    ("ДвижениеСтатус2.Компьютер", "ДвижениеСтатус2.Кинозал"),
    ("ИмяТарифа", "ИмяТипаБилета"),
    ("ДанныеТарифа", "ДанныеТипаБилета"),
    ("ПолучитьДанныеТарифа", "ПолучитьДанныеТипаБилета"),
    ("КатегорияПК", "КлассЗала"),
    ("Компьютер.Категория", "Кинозал.КлассЗала"),
    ("Компьютер.Состояние", "Кинозал.Состояние"),
    ("КомпОбъект", "ЗалОбъект"),
    ("Из Кинозалы", "Из Кинозалы"),  # noop guard
    ("Из Компьютеры", "Из Кинозалы"),
    ("Для Каждого СтрокаТЧ Из Компьютеры", "Для Каждого СтрокаТЧ Из Кинозалы"),
    # Form XML field names
    ('name="Компьютер"', 'name="Кинозал"'),
    ('name="Тариф"', 'name="ТипБилета"'),
    ('name="КомпьютерКонтекстноеМеню"', 'name="КинозалКонтекстноеМеню"'),
    ('name="КомпьютерРасширеннаяПодсказка"', 'name="КинозалРасширеннаяПодсказка"'),
    ('name="ТарифКонтекстноеМеню"', 'name="ТипБилетаКонтекстноеМеню"'),
    ('name="ТарифРасширеннаяПодсказка"', 'name="ТипБилетаРасширеннаяПодсказка"'),
    # Metadata object names in Properties
    ("<Name>ПоступлениеКомпьютеров</Name>", "<Name>ВводЗалаВЭксплуатацию</Name>"),
    ("<Name>СписаниеКомпьютеров</Name>", "<Name>ВыводЗалаИзЭксплуатации</Name>"),
    ("<Name>СеансБронирования</Name>", "<Name>ПродажаБилетов</Name>"),
    ("<Name>ЗаявкаНаБронь</Name>", "<Name>ЗаявкаНаБроньБилетов</Name>"),
    ("<Name>ЗаказУслуги</Name>", "<Name>ЗаказВБар</Name>"),
    ("<Name>Компьютеры</Name>", "<Name>Кинозалы</Name>"),
    ("<Name>Тарифы</Name>", "<Name>ТипыБилетов</Name>"),
    ("<Name>ИсторияСтатусовПК</Name>", "<Name>ИсторияСтатусовЗалов</Name>"),
    ("<Name>ВыручкаИВремя</Name>", "<Name>ВыручкаПоБилетам</Name>"),
    ("<Name>ЗагруженностьПК</Name>", "<Name>ЗаполняемостьЗалов</Name>"),
    ("<Name>ОбслуживаниеКлиента</Name>", "<Name>ОбслуживаниеПосетителя</Name>"),
    ("<Name>Бронирование</Name>", "<Name>ПродажаБилетов</Name>"),
    ("<Name>СкладскойУчет</Name>", "<Name>БарКинотеатра</Name>"),
    ("<Name>СтатусыКомпьютеров</Name>", "<Name>СтатусыЗалов</Name>"),
    ("<Name>СостоянияКомпьютеров</Name>", "<Name>СостоянияЗалов</Name>"),
    ("<Name>ЗаказУслуги</Name>", "<Name>ЗаказВБар</Name>"),
    ("<Name>Характеристики</Name>", "<Name>ОписаниеЗала</Name>"),
    ("<Name>Категория</Name>", "<Name>КлассЗала</Name>"),
    ("<Name>Списан</Name>", "<Name>Закрыт</Name>"),
    # ChildObjects in Configuration
    ("<Catalog>Компьютеры</Catalog>", "<Catalog>Кинозалы</Catalog>"),
    ("<Catalog>Тарифы</Catalog>", "<Catalog>ТипыБилетов</Catalog>"),
    ("<Document>СеансБронирования</Document>", "<Document>ПродажаБилетов</Document>"),
    ("<Document>ЗаявкаНаБронь</Document>", "<Document>ЗаявкаНаБроньБилетов</Document>"),
    ("<Document>ЗаказУслуги</Document>", "<Document>ЗаказВБар</Document>"),
    ("<Document>ПоступлениеКомпьютеров</Document>", "<Document>ВводЗалаВЭксплуатацию</Document>"),
    ("<Document>СписаниеКомпьютеров</Document>", "<Document>ВыводЗалаИзЭксплуатации</Document>"),
    ("<Enum>СтатусыКомпьютеров</Enum>", "<Enum>СтатусыЗалов</Enum>"),
    ("<Enum>СостоянияКомпьютеров</Enum>", "<Enum>СостоянияЗалов</Enum>"),
    ("<Report>ЗагруженностьПК</Report>", "<Report>ЗаполняемостьЗалов</Report>"),
    ("<InformationRegister>ИсторияСтатусовПК</InformationRegister>", "<InformationRegister>ИсторияСтатусовЗалов</InformationRegister>"),
    ("<AccumulationRegister>ВыручкаИВремя</AccumulationRegister>", "<AccumulationRegister>ВыручкаПоБилетам</AccumulationRegister>"),
    ("<BusinessProcess>ОбслуживаниеКлиента</BusinessProcess>", "<BusinessProcess>ОбслуживаниеПосетителя</BusinessProcess>"),
    ("<Subsystem>Бронирование</Subsystem>", "<Subsystem>ПродажаБилетов</Subsystem>"),
    ("<Subsystem>СкладскойУчет</Subsystem>", "<Subsystem>БарКинотеатра</Subsystem>"),
    # dataPath in reports
    ("<dataPath>Компьютер</dataPath>", "<dataPath>Кинозал</dataPath>"),
    ("<field>Компьютер</field>", "<field>Кинозал</field>"),
    ("<dataPath>Тариф</dataPath>", "<dataPath>ТипБилета</dataPath>"),
    ("<field>Тариф</field>", "<field>ТипБилета</field>"),
    ("<dataPath>ОтработаноЧасов</dataPath>", "<dataPath>КоличествоБилетов</dataPath>"),
    ("<field>ОтработаноЧасов</field>", "<field>КоличествоБилетов</field>"),
    ("Сумма(ОтработаноЧасов)", "Сумма(КоличествоБилетов)"),
    ("КАК Компьютер,", "КАК Кинозал,"),
    ("КАК Тариф,", "КАК ТипБилета,"),
    ("КАК ОтработаноЧасов,", "КАК КоличествоБилетов,"),
]

# Path renames: relative to SRC, deepest first
PATH_RENAMES: list[tuple[str, str]] = [
    ("Reports/ЗагруженностьПК/Templates/ОсновнаяСхемаКомпоновкиДанных/Ext/Template.xml", "Reports/ЗаполняемостьЗалов/Templates/ОсновнаяСхемаКомпоновкиДанных/Ext/Template.xml"),
    ("Reports/ЗагруженностьПК/Templates/ОсновнаяСхемаКомпоновкиДанных/Ext", "Reports/ЗаполняемостьЗалов/Templates/ОсновнаяСхемаКомпоновкиДанных/Ext"),
    ("Reports/ЗагруженностьПК/Templates/ОсновнаяСхемаКомпоновкиДанных.xml", "Reports/ЗаполняемостьЗалов/Templates/ОсновнаяСхемаКомпоновкиДанных.xml"),
    ("Reports/ЗагруженностьПК/Templates", "Reports/ЗаполняемостьЗалов/Templates"),
    ("Reports/ЗагруженностьПК.xml", "Reports/ЗаполняемостьЗалов.xml"),
    ("Reports/ЗагруженностьПК", "Reports/ЗаполняемостьЗалов"),
    ("BusinessProcesses/ОбслуживаниеКлиента/Ext/Flowchart.xml", "BusinessProcesses/ОбслуживаниеПосетителя/Ext/Flowchart.xml"),
    ("BusinessProcesses/ОбслуживаниеКлиента/Ext/ObjectModule.bsl", "BusinessProcesses/ОбслуживаниеПосетителя/Ext/ObjectModule.bsl"),
    ("BusinessProcesses/ОбслуживаниеКлиента/Ext", "BusinessProcesses/ОбслуживаниеПосетителя/Ext"),
    ("BusinessProcesses/ОбслуживаниеКлиента.xml", "BusinessProcesses/ОбслуживаниеПосетителя.xml"),
    ("BusinessProcesses/ОбслуживаниеКлиента", "BusinessProcesses/ОбслуживаниеПосетителя"),
    ("Documents/СеансБронирования/Forms/ФормаДокумента/Ext/Form/Module.bsl", "Documents/ПродажаБилетов/Forms/ФормаДокумента/Ext/Form/Module.bsl"),
    ("Documents/СеансБронирования/Forms/ФормаДокумента/Ext/Form.xml", "Documents/ПродажаБилетов/Forms/ФормаДокумента/Ext/Form.xml"),
    ("Documents/СеансБронирования/Forms/ФормаДокумента/Ext/Form", "Documents/ПродажаБилетов/Forms/ФормаДокумента/Ext/Form"),
    ("Documents/СеансБронирования/Forms/ФормаДокумента/Ext", "Documents/ПродажаБилетов/Forms/ФормаДокумента/Ext"),
    ("Documents/СеансБронирования/Forms/ФормаДокумента.xml", "Documents/ПродажаБилетов/Forms/ФормаДокумента.xml"),
    ("Documents/СеансБронирования/Forms/ФормаДокумента", "Documents/ПродажаБилетов/Forms/ФормаДокумента"),
    ("Documents/СеансБронирования/Forms", "Documents/ПродажаБилетов/Forms"),
    ("Documents/СеансБронирования/Ext/ObjectModule.bsl", "Documents/ПродажаБилетов/Ext/ObjectModule.bsl"),
    ("Documents/СеансБронирования/Ext", "Documents/ПродажаБилетов/Ext"),
    ("Documents/СеансБронирования.xml", "Documents/ПродажаБилетов.xml"),
    ("Documents/СеансБронирования", "Documents/ПродажаБилетов"),
    ("Documents/ЗаявкаНаБронь/Forms/ФормаДокумента/Ext/Form/Module.bsl", "Documents/ЗаявкаНаБроньБилетов/Forms/ФормаДокумента/Ext/Form/Module.bsl"),
    ("Documents/ЗаявкаНаБронь/Forms/ФормаДокумента/Ext/Form.xml", "Documents/ЗаявкаНаБроньБилетов/Forms/ФормаДокумента/Ext/Form.xml"),
    ("Documents/ЗаявкаНаБронь/Forms/ФормаДокумента/Ext/Form", "Documents/ЗаявкаНаБроньБилетов/Forms/ФормаДокумента/Ext/Form"),
    ("Documents/ЗаявкаНаБронь/Forms/ФормаДокумента/Ext", "Documents/ЗаявкаНаБроньБилетов/Forms/ФормаДокумента/Ext"),
    ("Documents/ЗаявкаНаБронь/Forms/ФормаДокумента.xml", "Documents/ЗаявкаНаБроньБилетов/Forms/ФормаДокумента.xml"),
    ("Documents/ЗаявкаНаБронь/Forms/ФормаДокумента", "Documents/ЗаявкаНаБроньБилетов/Forms/ФормаДокумента"),
    ("Documents/ЗаявкаНаБронь/Forms", "Documents/ЗаявкаНаБроньБилетов/Forms"),
    ("Documents/ЗаявкаНаБронь/Ext/ObjectModule.bsl", "Documents/ЗаявкаНаБроньБилетов/Ext/ObjectModule.bsl"),
    ("Documents/ЗаявкаНаБронь/Ext", "Documents/ЗаявкаНаБроньБилетов/Ext"),
    ("Documents/ЗаявкаНаБронь.xml", "Documents/ЗаявкаНаБроньБилетов.xml"),
    ("Documents/ЗаявкаНаБронь", "Documents/ЗаявкаНаБроньБилетов"),
    ("Documents/ЗаказУслуги/Forms/ФормаДокумента/Ext/Form/Module.bsl", "Documents/ЗаказВБар/Forms/ФормаДокумента/Ext/Form/Module.bsl"),
    ("Documents/ЗаказУслуги/Forms/ФормаДокумента/Ext/Form.xml", "Documents/ЗаказВБар/Forms/ФормаДокумента/Ext/Form.xml"),
    ("Documents/ЗаказУслуги/Forms/ФормаДокумента/Ext/Form", "Documents/ЗаказВБар/Forms/ФормаДокумента/Ext/Form"),
    ("Documents/ЗаказУслуги/Forms/ФормаДокумента/Ext", "Documents/ЗаказВБар/Forms/ФормаДокумента/Ext"),
    ("Documents/ЗаказУслуги/Forms/ФормаДокумента.xml", "Documents/ЗаказВБар/Forms/ФормаДокумента.xml"),
    ("Documents/ЗаказУслуги/Forms/ФормаДокумента", "Documents/ЗаказВБар/Forms/ФормаДокумента"),
    ("Documents/ЗаказУслуги/Forms", "Documents/ЗаказВБар/Forms"),
    ("Documents/ЗаказУслуги/Ext/ObjectModule.bsl", "Documents/ЗаказВБар/Ext/ObjectModule.bsl"),
    ("Documents/ЗаказУслуги/Ext", "Documents/ЗаказВБар/Ext"),
    ("Documents/ЗаказУслуги.xml", "Documents/ЗаказВБар.xml"),
    ("Documents/ЗаказУслуги", "Documents/ЗаказВБар"),
    ("Documents/ПоступлениеКомпьютеров/Ext/ObjectModule.bsl", "Documents/ВводЗалаВЭксплуатацию/Ext/ObjectModule.bsl"),
    ("Documents/ПоступлениеКомпьютеров/Ext", "Documents/ВводЗалаВЭксплуатацию/Ext"),
    ("Documents/ПоступлениеКомпьютеров.xml", "Documents/ВводЗалаВЭксплуатацию.xml"),
    ("Documents/ПоступлениеКомпьютеров", "Documents/ВводЗалаВЭксплуатацию"),
    ("Documents/СписаниеКомпьютеров/Ext/ObjectModule.bsl", "Documents/ВыводЗалаИзЭксплуатации/Ext/ObjectModule.bsl"),
    ("Documents/СписаниеКомпьютеров/Ext", "Documents/ВыводЗалаИзЭксплуатации/Ext"),
    ("Documents/СписаниеКомпьютеров.xml", "Documents/ВыводЗалаИзЭксплуатации.xml"),
    ("Documents/СписаниеКомпьютеров", "Documents/ВыводЗалаИзЭксплуатации"),
    ("Catalogs/Компьютеры/Ext/ObjectModule.bsl", "Catalogs/Кинозалы/Ext/ObjectModule.bsl"),
    ("Catalogs/Компьютеры/Ext", "Catalogs/Кинозалы/Ext"),
    ("Catalogs/Компьютеры.xml", "Catalogs/Кинозалы.xml"),
    ("Catalogs/Компьютеры", "Catalogs/Кинозалы"),
    ("Catalogs/Тарифы.xml", "Catalogs/ТипыБилетов.xml"),
    ("Catalogs/Тарифы", "Catalogs/ТипыБилетов"),
    ("Enums/СтатусыКомпьютеров.xml", "Enums/СтатусыЗалов.xml"),
    ("Enums/СостоянияКомпьютеров.xml", "Enums/СостоянияЗалов.xml"),
    ("InformationRegisters/ИсторияСтатусовПК.xml", "InformationRegisters/ИсторияСтатусовЗалов.xml"),
    ("AccumulationRegisters/ВыручкаИВремя.xml", "AccumulationRegisters/ВыручкаПоБилетам.xml"),
    ("Subsystems/Бронирование.xml", "Subsystems/ПродажаБилетов.xml"),
    ("Subsystems/СкладскойУчет.xml", "Subsystems/БарКинотеатра.xml"),
]


def apply_text_replacements() -> int:
    count = 0
    extensions = {".xml", ".bsl", ".html", ".txt", ".md"}
    for path in SRC.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8-sig")
        original = text
        for old, new in REPLACEMENTS:
            if old == new:
                continue
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            count += 1
            print(f"  updated: {path.relative_to(SRC)}")
    return count


def rename_paths() -> None:
    # Sort by depth descending so files rename before parents
    sorted_renames = sorted(PATH_RENAMES, key=lambda x: x[0].count("/"), reverse=True)
    for old_rel, new_rel in sorted_renames:
        old = SRC / old_rel.replace("/", os.sep)
        new = SRC / new_rel.replace("/", os.sep)
        if old.exists() and not new.exists():
            new.parent.mkdir(parents=True, exist_ok=True)
            old.rename(new)
            print(f"  renamed: {old_rel} -> {new_rel}")


def main() -> None:
    print("Applying text replacements...")
    n = apply_text_replacements()
    print(f"Modified {n} files")
    print("Renaming paths...")
    rename_paths()
    print("Done.")


if __name__ == "__main__":
    main()
