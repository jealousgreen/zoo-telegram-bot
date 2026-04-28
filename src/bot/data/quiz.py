from __future__ import annotations

from .models import Animal, AnswerOption, Question

ANIMALS: dict[str, Animal] = {
    "manul": Animal(
        id="manul",
        title="Манул Тимофей",
        short_title="манул",
        species_url="https://moscowzoo.ru/animals/kinds/manul",
        description=(
            "Вы наблюдатель, стратег и мастер режима «меня тут нет». "
            "Ваш тотем - манул: спокойный, внимательный и немного мемный хищник."
        ),
        adoption_pitch=(
            "Опека над таким животным — способ поддержать редкие виды и работу зоопарка, "
            "а еще повод следить за любимым обитателем не только в ленте."
        ),
    ),
    "sea_lion": Animal(
        id="sea_lion",
        title="Сивуч Дино",
        short_title="сивуч",
        species_url="https://moscowzoo.ru/animals/kinds/sivuch",
        description=(
            "Вы умеете отдыхать так, что рядом сами появляются волны. "
            "Ваш тотем - сивуч: мощный, водный и с врожденным талантом устраивать шоу."
        ),
        adoption_pitch=(
            "Опека помогает зоопарку заботиться о крупных морских животных: корм, ветеринария, "
            "обогащение среды и ежедневный уход требуют много ресурсов."
        ),
    ),
    "otter": Animal(
        id="otter",
        title="Выдры Рубен и Найроби",
        short_title="выдра",
        species_url="https://moscowzoo.ru/animals/kinds/vydra",
        description=(
            "Вы быстры, любопытны и не против рыбного ужина. "
            "Ваш тотем - выдра: энергия, вода и ловкость в одном пушистом комплекте."
        ),
        adoption_pitch=(
            "Опекун поддерживает не только кормление, но и игровые элементы среды, "
            "которые помогают животным оставаться активными."
        ),
    ),
    "leopard": Animal(
        id="leopard",
        title="Леопард Мизер",
        short_title="леопард",
        species_url="https://moscowzoo.ru/animals/kinds/dalnevostochnyy_leopard",
        description=(
            "Вы выбираете движение, точность и охоту на сложные задачи. "
            "Ваш тотем - леопард: редкий, собранный и очень эффектный."
        ),
        adoption_pitch=(
            "Поддержка редких кошачьих особенно заметна: это вклад в сохранение видов, "
            "просвещение и качественные условия содержания."
        ),
    ),
    "elephant": Animal(
        id="elephant",
        title="Слониха Капри",
        short_title="слон",
        species_url="https://moscowzoo.ru/animals/kinds/aziatskiy_slon",
        description=(
            "Вы надежный человек с большим сердцем и аппетитом к жизни. "
            "Ваш тотем - слон: мудрость, память, семья и бананы в промышленных масштабах."
        ),
        adoption_pitch=(
            "Опека над крупным животным — серьезная помощь: рацион, уход, тренинг и ветеринарное "
            "сопровождение требуют постоянного внимания."
        ),
    ),
    "penguin": Animal(
        id="penguin",
        title="Пингвин Гумбольдта",
        short_title="пингвин",
        species_url="https://moscowzoo.ru/animals/kinds/pingvin_gumboldta",
        description=(
            "Вы командный игрок: умеете держаться стильно даже на камне и не терять достоинства "
            "в любой погоде. Ваш тотем — пингвин Гумбольдта."
        ),
        adoption_pitch=(
            "Опека помогает поддерживать условия для птиц, их рацион и работу специалистов, "
            "которые следят за здоровьем колонии."
        ),
    ),
    "meerkat": Animal(
        id="meerkat",
        title="Семейство сурикатов",
        short_title="сурикат",
        species_url="https://moscowzoo.ru/animals/kinds/surikat",
        description=(
            "Вы за своих горой, быстро собираете команду и всегда знаете, кто сегодня дежурит на вышке. "
            "Ваш тотем — сурикат."
        ),
        adoption_pitch=(
            "Опека - хороший способ поддержать животных, за которыми особенно интересно наблюдать "
            "семьям и посетителям канала."
        ),
    ),
    "sloth": Animal(
        id="sloth",
        title="Ленивец",
        short_title="ленивец",
        species_url="https://moscowzoo.ru/animals/kinds/dvupalyy_lenivets",
        description=(
            "Вы не медлите — вы экономите энергию для главного. "
            "Ваш тотем - ленивец: спокойный, вдумчивый и уверенный в своем темпе."
        ),
        adoption_pitch=(
            "Даже спокойным животным нужны грамотное содержание, рацион и забота специалистов; "
            "опека помогает делать эту работу устойчивой."
        ),
    ),
    "raccoon": Animal(
        id="raccoon",
        title="Енот Света",
        short_title="енот",
        species_url="https://moscowzoo.ru/animals/kinds/enot_poloskun",
        description=(
            "Вы находите вкусняшки там, где другие видят только шкаф. "
            "Ваш тотем — енот: любопытство, ловкие лапы и стратегический запас печенек."
        ),
        adoption_pitch=(
            "Опека помогает поддерживать ежедневный уход и занятия для умных животных, "
            "которым важно постоянно что-то исследовать."
        ),
    ),
    "muskox": Animal(
        id="muskox",
        title="Мохнатый овцебык",
        short_title="овцебык",
        species_url="https://moscowzoo.ru/animals/kinds/ovtsebyk",
        description=(
            "Вы человек зимней выдержки: холод не пугает, а только добавляет драматичный пар изо рта. "
            "Ваш тотем - овцебык."
        ),
        adoption_pitch=(
            "Опека поддерживает условия содержания северных животных и помогает рассказывать "
            "посетителям об их приспособлениях к суровому климату."
        ),
    ),
}

QUESTIONS: list[Question] = [
    Question(
        text="1/8. Идеальный выходной: что выбираете?",
        options=[
            AnswerOption("Полениться в воде, делать волны и пускать пузыри", {"sea_lion": 3, "otter": 1}),
            AnswerOption("Пройти много шагов и победить коробку из-под телевизора", {"leopard": 3, "manul": 1}),
            AnswerOption("Собрать большую компанию и играть вместе", {"meerkat": 3, "penguin": 1}),
            AnswerOption("Двигаться медленно, зато очень осознанно", {"sloth": 3, "muskox": 1}),
        ],
    ),
    Question(
        text="2/8. Ваша суперсила в офисе?",
        options=[
            AnswerOption("Тихо наблюдать и появляться с решением в нужный момент", {"manul": 3, "leopard": 1}),
            AnswerOption("Держать команду вместе и поднимать настроение", {"meerkat": 3, "elephant": 1}),
            AnswerOption("Найти спрятанный запас кофе и печенек", {"raccoon": 3, "otter": 1}),
            AnswerOption("Не паниковать: мой темп медленный, но дедлайны живы", {"sloth": 3, "muskox": 1}),
        ],
    ),
    Question(
        text="3/8. Что закажем на ужин?",
        options=[
            AnswerOption("Что-нибудь рыбное", {"otter": 3, "penguin": 2, "sea_lion": 2}),
            AnswerOption("Стейк, которому позавидовал бы хищник", {"leopard": 3, "manul": 1}),
            AnswerOption("Бананы, фрукты и еще немного бананов", {"elephant": 3, "sloth": 1}),
            AnswerOption("Семечки, кукуруза и секретные вкусняшки", {"raccoon": 3, "meerkat": 1}),
        ],
    ),
    Question(
        text="4/8. Где вам комфортнее жить?",
        options=[
            AnswerOption("У воды: шум, брызги, рыба — красота", {"sea_lion": 3, "otter": 2, "penguin": 1}),
            AnswerOption("В укромном месте, где меня не дергают", {"manul": 3, "sloth": 1}),
            AnswerOption("Там, где рядом семья или надежная стая", {"elephant": 2, "meerkat": 3, "penguin": 1}),
            AnswerOption("Там, где холодно, свежо и можно выглядеть эпично", {"muskox": 3, "penguin": 2}),
        ],
    ),
    Question(
        text="5/8. Какой пункт из зоопаркового адвента ближе всего?",
        options=[
            AnswerOption("Облизать нос, как манул Тимофей", {"manul": 3}),
            AnswerOption("Поиграть в мяч, как пингвины Гумбольдта", {"penguin": 3, "meerkat": 1}),
            AnswerOption("Обрадоваться спрятанным вкусняшкам, как енот Света", {"raccoon": 3}),
            AnswerOption("Выдыхать облака пара на улице, как овцебыки", {"muskox": 3}),
        ],
    ),
    Question(
        text="6/8. В командном проекте вы чаще всего…",
        options=[
            AnswerOption("Разведчик: первым замечаю риски", {"meerkat": 2, "manul": 2}),
            AnswerOption("Тяжелая артиллерия: беру на себя сложное", {"elephant": 3, "muskox": 1}),
            AnswerOption("Спринтер: быстро включаюсь, когда задача интересная", {"otter": 2, "leopard": 2}),
            AnswerOption("Хранитель спокойствия: снижаю градус хаоса", {"sloth": 3, "penguin": 1}),
        ],
    ),
    Question(
        text="7/8. Что лучше всего описывает ваш стиль общения?",
        options=[
            AnswerOption("Мало слов, много выразительного взгляда", {"manul": 3, "leopard": 1}),
            AnswerOption("Обнимашки, поддержка и память на дни рождения", {"elephant": 3, "meerkat": 1}),
            AnswerOption("Шумно, весело, с внезапным нырком в тему", {"otter": 2, "sea_lion": 2}),
            AnswerOption("Дипломатично стою в толпе и выгляжу безупречно", {"penguin": 3, "muskox": 1}),
        ],
    ),
    Question(
        text="8/8. Финальный выбор: какой девиз ваш?",
        options=[
            AnswerOption("Сначала посмотрю из укрытия, потом решу", {"manul": 3}),
            AnswerOption("Главное — свои рядом", {"meerkat": 2, "elephant": 2, "penguin": 1}),
            AnswerOption("Вода точит камень, а я — дедлайн", {"sea_lion": 2, "otter": 2}),
            AnswerOption("Тише едешь — мемнее будешь", {"sloth": 3, "raccoon": 1}),
        ],
    ),
]
