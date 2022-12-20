from django.db import models


class Patient(models.Model):
    # The available countries to use.
    country_choices = [('AF', 'Afeganistão'), ('ZA', 'África do Sul'), ('AX', 'Aland, Ilhas'), ('AL', 'Albânia'),
                       ('DE', 'Alemanha'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguila'), ('AQ', 'Antártida'),
                       ('AG', 'Antígua e Barbuda'), ('SA', 'Arábia Saudita'), ('DZ', 'Argélia'), ('AR', 'Argentina'),
                       ('AM', 'Armênia'), ('AW', 'Aruba'), ('AU', 'Austrália'), ('AT', 'Áustria'), ('AZ', 'Azerbaijão'),
                       ('BS', 'Bahamas'), ('BD', 'Bangladexe'), ('BB', 'Barbados'), ('BH', 'Barém'), ('BE', 'Bélgica'),
                       ('BZ', 'Belize'), ('BJ', 'Benim'), ('BM', 'Bermudas'), ('BY', 'Bielorrússia'), ('BO', 'Bolívia'),
                       ('BQ', 'Bonaire, Santo Eustáquio e Saba'), ('BA', 'Bósnia e Herzegovina'), ('BW', 'Botsuana'),
                       ('BV', 'Bouvet, Ilha'), ('BR', 'Brasil'), ('BN', 'Brunei'), ('BG', 'Bulgária'),
                       ('BF', 'Burquina Fasso'), ('BI', 'Burundi'), ('BT', 'Butão'), ('CV', 'Cabo Verde'),
                       ('KY', 'Caimã, Ilhas'), ('KH', 'Camboja'), ('CM', 'Camarões'), ('CA', 'Canadá'), ('QA', 'Catar'),
                       ('KZ', 'Cazaquistão'), ('CF', 'Centro-Africana, República'), ('TD', 'Chade'), ('CZ', 'Chéquia'),
                       ('CL', 'Chile'), ('CN', 'China'), ('CY', 'Chipre'), ('CC', 'Cocos, Ilhas'), ('CO', 'Colômbia'),
                       ('KM', 'Comores'), ('CG', 'Congo, República do'),
                       ('CD', 'Congo, República Democrática do (antigo Zaire)'), ('CK', 'Cook, Ilhas'),
                       ('KR', 'Coreia do Sul'), ('KP', 'Coreia, República Democrática da ( Coreia do Norte)'),
                       ('CI', 'Costa do Marfim'), ('CR', 'Costa Rica'), ('HR', 'Croácia'), ('CU', 'Cuba'),
                       ('CW', 'Curaçau'), ('DK', 'Dinamarca'), ('DJ', 'Djibuti'), ('DM', 'Dominica'),
                       ('DO', 'Dominicana, República'), ('EG', 'Egito'), ('SV', 'El Salvador'),
                       ('AE', 'Emirados Árabes Unidos'), ('EC', 'Equador'), ('ER', 'Eritreia'), ('SK', 'Eslováquia'),
                       ('SI', 'Eslovênia'), ('ES', 'Espanha'), ('US', 'Estados Unidos'), ('EE', 'Estónia'),
                       ('SZ', 'Essuatíni'), ('SJ', 'Esvalbarde e Jan Mayen'), ('ET', 'Etiópia'), ('FO', 'Feroé, Ilhas'),
                       ('FJ', 'Fiji'), ('PH', 'Filipinas'), ('FI', 'Finlândia'), ('FR', 'França'), ('GA', 'Gabão'),
                       ('GM', 'Gâmbia'), ('GH', 'Gana'), ('GE', 'Geórgia'),
                       ('GS', 'Geórgia do Sul e Sanduíche do Sul, Ilhas'), ('GI', 'Gibraltar'), ('GD', 'Granada'),
                       ('GR', 'Grécia'), ('GL', 'Groenlândia'), ('GP', 'Guadalupe'), ('GU', 'Guam'),
                       ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GY', 'Guiana'), ('GF', 'Guiana Francesa'),
                       ('GW', 'Guiné-Bissau'), ('GN', 'Guiné-Conacri'), ('GQ', 'Guiné Equatorial'), ('HT', 'Haiti'),
                       ('HM', 'Heard e Ilhas McDonald, Ilha'), ('HN', 'Honduras'), ('HK', 'Hong Kong'),
                       ('HU', 'Hungria'), ('YE', 'Iémen'), ('IN', 'Índia'), ('ID', 'Indonésia'), ('IQ', 'Iraque'),
                       ('IR', 'Irã'), ('IE', 'Irlanda'), ('IS', 'Islândia'), ('IL', 'Israel'), ('IT', 'Itália'),
                       ('JM', 'Jamaica'), ('JP', 'Japão'), ('JE', 'Jersey'), ('JO', 'Jordânia'), ('KW', 'Kuwait'),
                       ('LA', 'Laos'), ('LS', 'Lesoto'), ('LV', 'Letônia'), ('LB', 'Líbano'), ('LR', 'Libéria'),
                       ('LY', 'Líbia'), ('LI', 'Listenstaine'), ('LT', 'Lituânia'), ('LU', 'Luxemburgo'),
                       ('MO', 'Macau'), ('MK', 'Macedônia do Norte'), ('MG', 'Madagáscar'), ('YT', 'Maiote'),
                       ('MY', 'Malásia'), ('MW', 'Maláui'), ('MV', 'Maldivas'), ('ML', 'Mali'), ('MT', 'Malta'),
                       ('FK', 'Malvinas, Ilhas(Falkland)'), ('IM', 'Man, Ilha de'), ('MP', 'Marianas Setentrionais'),
                       ('MA', 'Marrocos'), ('MH', 'Marshall, Ilhas'), ('MQ', 'Martinica'), ('MU', 'Maurícia'),
                       ('MR', 'Mauritânia'), ('UM', 'Menores Distantes dos Estados Unidos, Ilhas'), ('MX', 'México'),
                       ('MM', 'Mianmar (antiga Birmânia)'), ('FM', 'Micronésia, Estados Federados da'),
                       ('MZ', 'Moçambique'), ('MD', 'Moldávia'), ('MC', 'Mônaco'), ('MN', 'Mongólia'),
                       ('MS', 'Monserrate'), ('ME', 'Montenegro'), ('NA', 'Namíbia'),
                       ('CX', 'Natal, Ilha do (Ilha Christmas)'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NI', 'Nicarágua'),
                       ('NE', 'Níger'), ('NG', 'Nigéria'), ('NU', 'Niue'), ('NF', 'Norfolque, Ilha'), ('NO', 'Noruega'),
                       ('NC', 'Nova Caledônia'), ('NZ', 'Nova Zelândia (Aotearoa)'), ('OM', 'Omã'),
                       ('NL', 'Países Baixos (Holanda)'), ('PW', 'Palau'), ('PS', 'Palestina'), ('PA', 'Panamá'),
                       ('PG', 'Papua-Nova Guiné'), ('PK', 'Paquistão'), ('PY', 'Paraguai'), ('PE', 'Peru'),
                       ('PN', 'Pitcairn'), ('PF', 'Polinésia Francesa'), ('PL', 'Polônia'), ('PR', 'Porto Rico'),
                       ('PT', 'Portugal'), ('KE', 'Quênia'), ('KG', 'Quirguistão'), ('KI', 'Quiribáti'),
                       ('GB', 'Reino Unido da Grã-Bretanha e Irlanda do Norte'), ('RE', 'Reunião'), ('RO', 'Romênia'),
                       ('RW', 'Ruanda'), ('RU', 'Rússia'), ('EH', 'Saara Ocidental'), ('AS', 'Samoa Americana'),
                       ('WS', 'Samoa (Samoa Ocidental)'), ('SB', 'Salomão, Ilhas'), ('SM', 'San Marino'),
                       ('SH', 'Santa Helena'), ('LC', 'Santa Lúcia'), ('BL', 'São Bartolomeu'),
                       ('KN', 'São Cristóvão e Neves'), ('MF', 'São Martinho (França)'),
                       ('SX', 'São Martinho (Países Baixos)'), ('PM', 'São Pedro e Miquelão'),
                       ('ST', 'São Tomé e Príncipe'), ('VC', 'São Vicente e Granadinas'), ('SC', 'Seicheles'),
                       ('SN', 'Senegal'), ('LK', 'Seri Lanca'), ('SL', 'Serra Leoa'), ('RS', 'Sérvia'),
                       ('SG', 'Singapura'), ('SY', 'Síria'), ('SO', 'Somália'), ('SD', 'Sudão'), ('SS', 'Sudão do Sul'),
                       ('SE', 'Suécia'), ('CH', 'Suíça'), ('SR', 'Suriname'), ('TH', 'Tailândia'), ('TW', 'Taiwan'),
                       ('TJ', 'Tajiquistão'), ('TZ', 'Tanzânia'),
                       ('TF', 'Terras Austrais e Antárticas Francesas (TAAF)'),
                       ('IO', 'Território Britânico do Oceano Índico'), ('TL', 'Timor-Leste'), ('TG', 'Togo'),
                       ('TO', 'Tonga'), ('TK', 'Toquelau'), ('TT', 'Trindade e Tobago'), ('TN', 'Tunísia'),
                       ('TC', 'Turcas e Caicos'), ('TM', 'Turcomenistão'), ('TR', 'Turquia'), ('TV', 'Tuvalu'),
                       ('UA', 'Ucrânia'), ('UG', 'Uganda'), ('UY', 'Uruguai'), ('UZ', 'Usbequistão'), ('VU', 'Vanuatu'),
                       ('VA', 'Vaticano'), ('VE', 'Venezuela'), ('VN', 'Vietnã'), ('VI', 'Virgens Americanas, Ilhas'),
                       ('VG', 'Virgens Britânicas, Ilhas'), ('WF', 'Wallis e Futuna'), ('ZM', 'Zâmbia'),
                       ('ZW', 'Zimbábue')]

    gender_choices = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("I", "Indeterminado"),
    ]

    subsystem_choices = [
        ("5017", "ADMINISTRAÇÃO DO PORTO DE LISBOA"),
        ("5016", "ADMINISTRAÇÃO DOS PORTOS DOURO E LEIXÕES"),
        ("5066", "AEGON SEGUROS GENERALES,SA"),
        ("5079", "AIG"),
        ("5056", "ASSISTUR"),
        ("5024", "AXA PORTUGAL - COMPANHIA DE SEGUROS, SA"),
        ("5028", "BPA VIDA-COMPANHIA DE SEGUROS VIDA, SA"),
        ("5021", "C SEG A SOCIAL"),
        ("5067", "C SEG AIDE ASSISTENCE"),
        ("5078", "C SEG COMERC UNION (ALBA)"),
        ("5070", "C SEG COMMERC U ASSURANCE"),
        ("5029", "C SEG EAGLE STAR VIDA"),
        ("5092", "C SEG EURESAP"),
        ("5052", "C SEG GARANTIA"),
        ("5053", "C SEG GESA"),
        ("5034", "C SEG GUARDIAN"),
        ("5072", "C SEG GUARDIAN ASSURANCE"),
        ("5073", "C SEG INSURANCE"),
        ("5035", "C SEG INTER-ATLANTICO SA"),
        ("5036", "C SEG LA EQUITATIVA"),
        ("5074", "C SEG LA PRESERVATRICE"),
        ("5055", "C SEG LEGAL & GENERAL"),
        ("5098", "C SEG LIBERTY EUROPEIA"),
        ("5058", "C SEG MAAF"),
        ("5038", "C SEG METROPOLE SA"),
        ("5075", "C SEG MUTUELLE ASSURANCE"),
        ("5090", "C SEG NORTHERN"),
        ("5039", "C SEG o TRABALHO SA"),
        ("5040", "C SEG OCEANICA"),
        ("5102", "C SEG OK TELESEGURO"),
        ("5041", "C SEG PEARL PORTUGAL SA"),
        ("5077", "C SEG PHOENIX ASSURANCE"),
        ("5054", "C SEG PORTUGAL"),
        ("5080", "C SEG PRESERVATRICE FONCI"),
        ("5043", "C SEG ROYAL EXCHANGE"),
        ("5044", "C SEG ROYAL INSURANCE"),
        ("5046", "C SEG SCOTTISH UNION PORT"),
        ("5061", "C SEG SOCIED PORT SEGUROS"),
        ("5081", "C SEG SUN ALLIANCE PORTUG"),
        ("5047", "C SEG TAGUS SA"),
        ("5082", "C SEG TIARD PFA"),
        ("5049", "C SEG ULTRAMARINA SA"),
        ("5076", "C SEG UNION ASSURAN PARIS"),
        ("5069", "C SEG UNION FENIX"),
        ("5100", "C.A.SEGUROS"),
        ("5026", "COMPANHIA DE SEGUROS ASSICURAZIONI GENERAL SpA"),
        ("5023", "COMPANHIA DE SEGUROS AÇOREANA, SA"),
        ("5042", "COMPANHIA DE SEGUROS ALLIANZ PORTUGAL, SA"),
        ("5019", "COMPANHIA EUROPEIA DE SEGUROS, SA"),
        ("5020", "COMPANHIA PORTUGUESA SEGUROS SAUDE, SA"),
        ("5022", "COMPANHIA SEGUROS ABEILLE VIE-GROUPE COMMERCIAL UNION"),
        ("5025", "COMPANHIA SEGUROS ALICO-AMERICAN LIFE INSURANCE COMPANY"),
        ("5030", "COMPANHIA SEGUROS FIDELIDADE-MUNDIAL. SA"),
        ("5094", "COMPANHIA SEGUROS SAGRES,SA"),
        ("5048", "COMPANHIA SEGUROS TRANQUILIDADE SA"),
        ("5000", "DIRECÇÃO-GERAL PROTECÇÃO SOCIAL AOS FUNCIONARIOS E AGENTES DA ADMINISTRAÇÃO PUBLICA"),
        ("5051", "ESPAÑA. SA - COMPAÑIA NACIONAL SEGUROS"),
        ("5097", "ESPIRITO SANTO. - COMPANHIA SEGUROS,SA"),
        ("5071", "EUROP ASSISTANCE - COMPANHIA PORTUGUESA SEGUROS DE ASSISTÊNCIA,SA"),
        ("5031", "GAN PORTUGAL SEGUROS, SA"),
        ("5101", "GENERALI C.SEGUROS,SpA"),
        ("5032", "GENESIS SEGUROS ENERALES,SOCIEDADANONIMA SEGUROS Y REASEGUROS"),
        ("5033", "GLOBAL - COMPANHIA DE SEGUROS,SA"),
        ("5093", "IBERO ASSISTENCIA SA"),
        ("5087", "IMA INTER MUTUELLE ASSIST"),
        ("5095", "IMPERIO BONANCA C SEG SA"),
        ("5027", "IMPERIO BONANÇA. COMPANHIA DE SEGUROS, SA"),
        ("5014", "IMPRENSA NACIONAL CASA MOEDA"),
        ("5001", "INSTITUTO ACÇÃO SOCIAL FORÇAS ARMADAS"),
        ("5063", "INSTITUTO SEGUROS DE PORTUGAL"),
        ("5062", "INSTITUTO NACIONAL DE SEGUROS"),
        ("5099", "LONDON GENERAL INSURANCE"),
        ("5037", "LUSITÂNIA COMPANHIA SEGUROS, SA"),
        ("5068", "MAPFRE SEGUROS GERAIS,SA"),
        ("5088", "MATMUT/SCOTTISH (CARES)"),
        ("5104", "MUTUAMAR-MÚTUA SEGUROS ARMADORES PESCA ARRASTO"),
        ("5059", "OCIDENTAL - COMPANHIA PORTUGUESA SEGUROS, SA"),
        ("5018", "PAIS DE ACORDO"),
        ("5064", "PFA SEGUROS"),
        ("5015", "RADIODIFUSAO PORTUGUESA"),
        ("5060", "REAL SEGUROS, SA"),
        ("5091", "RURAL SEGUROS-COMPANHIA SEGUROS RAMOS REAIS, SA"),
        ("5004", "SAD MUNICIPAL CM LISBOA"),
        ("5005", "SAD MUNICIPAL CM PORTO"),
        ("5086", "SCOTTISH UNION(LA FRANCE)"),
        ("5057", "SEG LUSO ATLANTICA SA"),
        ("5083", "SEG MARSH & MCLENNAN LDA"),
        ("5045", "SEGURO DIRECTO GERE-COMPANHIA SEGUROS,SA"),
        ("5084", "SEGUROS LLOYDS"),
        ("5103", "SEGUROS LOGO SA"),
        ("5096", "SERVAIDE-ASSIST SERVICOS"),
        ("5003", "SERVIÇO ASSISTÊNCIA DOENÇA - POLICIA SEGURANÇA PUBLICA"),
        ("5006", "SERVIÇO ASSISTÊNCIA DOENÇA - SERVIÇO ESTRANGEIROS E FRONTEIRAS"),
        ("5002", "SERVIÇO ASSISTÊNCIA DOENÇA AOS MILITARES DA GUARDA NACIONAL REPUBLICANA"),
        ("5009", "SERVIÇO ASSISTÊNCIA MEDICO-SOCIAL - QUADROS TECNICOS"),
        ("5008", "SERVIÇO ASSISTÊNCIA MEDICO-SOCIAL BANCÁRIOS CENTRO"),
        ("5007", "SERVIÇO ASSISTÊNCIA MEDICO-SOCIAL BANCÁRIOS NORTE"),
        ("543", "Serviço Nacional Saúde"),
        ("5010", "SERVIÇOS SOCIAIS CAIXA GERAL DEPOSITOS"),
        ("5011", "SERVIÇOS SOCIAIS MINISTERIO JUSTICA"),
        ("5012", "SERVIÇOS SOCIAIS TAP AIR PORTUGAL"),
        ("5013", "SERVIÇOS SOCIAIS TELEFONES LISBOA E PORTO"),
        ("5065", "SOC PORTUGUESA SEG (AGF)"),
        ("5085", "VAN AMEYDE PORTUGAL"),
        ("5050", "VICTORIA - COMPANHIA SEGUROS, SA"),
        ("5089", "ZURICH - COMPANHIA SEGUROS, SA"),
    ]

    # The unique identifier of the patient.
    identifier = models.CharField(max_length=64, unique=True)
    # The name of the patient.
    name = models.CharField(max_length=128)
    # The SNS number.
    sns_number = models.CharField(max_length=10, unique=True)
    # The social security number of the patient.
    social_security_number = models.CharField(max_length=10, unique=True)
    # The patients phone number.
    phone_number = models.CharField(max_length=9)
    # The gender of the patient.
    gender = models.CharField(max_length=1, choices=gender_choices, default="M")
    # The address of the patient.
    address = models.CharField(max_length=256)
    # The patient's postal code.
    postal_code = models.CharField(max_length=8)
    # The patient's locality.
    locality = models.CharField(max_length=50)
    # The country of the origin.
    country = models.CharField(max_length=2, choices=country_choices, default="PT")
    # The nationality of this patient.
    nationality = models.CharField(max_length=2, choices=country_choices, default="PT")
    # The date of birth of the patient.
    birth_date = models.DateField()
    # The health subsystem for this patient.
    subsystem = models.CharField(max_length=4, default="543", choices=subsystem_choices)

    # The date of creation of this patient.
    created = models.DateTimeField(auto_now_add=True)
    # The date of the last modification to this entry.
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
