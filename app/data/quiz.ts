export type PersonalityKey = 'adventurer' | 'classic' | 'sweet' | 'zen' | 'social' | 'owl';

export interface Personality {
  key: PersonalityKey;
  name: string;
  coffee: string;
  tagline: string;
  image: string;
}

export interface QuizOption {
  emoji: string;
  text: string;
  personality: PersonalityKey;
}

export interface QuizQuestion {
  id: number;
  text: string;
  options: QuizOption[];
}

export const personalities: Record<PersonalityKey, Personality> = {
  adventurer: {
    key: 'adventurer',
    name: 'Смелый искатель приключений',
    coffee: 'Двойной эспрессо',
    tagline: 'Ты живёшь ради интенсивности',
    image: '/images/espresso.jpg',
  },
  classic: {
    key: 'classic',
    name: 'Уютный классик',
    coffee: 'Обычный фильтр-кофе',
    tagline: 'Комфорт в каждой кружке',
    image: '/images/drip-coffee.jpg',
  },
  sweet: {
    key: 'sweet',
    name: 'Любитель сладкого',
    coffee: 'Карамельный латте',
    tagline: 'Жизнь слишком коротка для горечи',
    image: '/images/latte.jpg',
  },
  zen: {
    key: 'zen',
    name: 'Дзен-минималист',
    coffee: 'Чёрный кофе, single origin',
    tagline: 'Просто. Чисто. Идеально.',
    image: '/images/black-coffee.jpg',
  },
  social: {
    key: 'social',
    name: 'Душа компании',
    coffee: 'Капучино',
    tagline: 'Кофе лучше в хорошей компании',
    image: '/images/cappuccino.jpg',
  },
  owl: {
    key: 'owl',
    name: 'Сова',
    coffee: 'Red Eye (кофе + шот эспрессо)',
    tagline: 'Сон — опционален',
    image: '/images/dark-coffee.jpg',
  },
};

export const questions: QuizQuestion[] = [
  {
    id: 1,
    text: 'Как ты проводишь идеальный выходной?',
    options: [
      { emoji: '🚀', text: 'Адреналин, новые приключения, экстрим', personality: 'adventurer' },
      { emoji: '🏡', text: 'Уютный диван, книга, спокойствие', personality: 'classic' },
      { emoji: '🎉', text: 'Вечеринка с друзьями, веселье', personality: 'social' },
      { emoji: '🧘', text: 'Медитация, природа, гармония', personality: 'zen' },
      { emoji: '🍰', text: 'Вкусная еда, десерты, удовольствие', personality: 'sweet' },
      { emoji: '🌙', text: 'Ночные приключения, клубы, вечеринки', personality: 'owl' },
    ],
  },
  {
    id: 2,
    text: 'Какой вымышленный персонаж больше всего похож на тебя?',
    options: [
      { emoji: '⚡', text: 'Тони Старк (смелый, дерзкий)', personality: 'adventurer' },
      { emoji: '🧙', text: 'Дамблдор (мудрый, спокойный)', personality: 'zen' },
      { emoji: '💛', text: 'Пэрис Хилтон (общительная, светская)', personality: 'social' },
      { emoji: '📖', text: 'Рэйчел Грин (стильная, уютная)', personality: 'classic' },
      { emoji: '🎀', text: 'Эль Вудс (энергичная, сладкая)', personality: 'sweet' },
      { emoji: '🦇', text: 'Бэтмен (ночной боец, интенсивный)', personality: 'owl' },
    ],
  },
  {
    id: 3,
    text: 'Твой идеальный отпуск — это...',
    options: [
      { emoji: '🏔️', text: 'Альпинизм, трекинг, экстремальный спорт', personality: 'adventurer' },
      { emoji: '🏖️', text: 'Пляж, расслабление, спа', personality: 'classic' },
      { emoji: '🌍', text: 'Путешествие с друзьями по городам', personality: 'social' },
      { emoji: '🧘', text: 'Йога-ретрит, медитация на острове', personality: 'zen' },
      { emoji: '🍽️', text: 'Гастротур, лучшие рестораны мира', personality: 'sweet' },
      { emoji: '🌃', text: 'Ночные клубы, вечеринки в больших городах', personality: 'owl' },
    ],
  },
  {
    id: 4,
    text: 'Какой цвет тебя лучше всего описывает?',
    options: [
      { emoji: '🔴', text: 'Красный (энергия, страсть)', personality: 'adventurer' },
      { emoji: '🟤', text: 'Коричневый (стабильность, комфорт)', personality: 'classic' },
      { emoji: '🟡', text: 'Золотой (тепло, радость)', personality: 'sweet' },
      { emoji: '⚪', text: 'Белый (чистота, минимализм)', personality: 'zen' },
      { emoji: '🟣', text: 'Фиолетовый (творчество, общение)', personality: 'social' },
      { emoji: '⚫', text: 'Чёрный (таинственность, интенсивность)', personality: 'owl' },
    ],
  },
  {
    id: 5,
    text: 'Что ты предпочитаешь делать в одиночестве?',
    options: [
      { emoji: '🎮', text: 'Видеоигры, экшены, адреналин', personality: 'adventurer' },
      { emoji: '📚', text: 'Читать, смотреть фильмы, релаксировать', personality: 'classic' },
      { emoji: '🍰', text: 'Готовить, кулинарные эксперименты', personality: 'sweet' },
      { emoji: '🧘', text: 'Медитировать, заниматься йогой', personality: 'zen' },
      { emoji: '📱', text: 'Общаться в социальных сетях, планировать встречи', personality: 'social' },
      { emoji: '🌙', text: 'Работать, учиться, продуктивность ночью', personality: 'owl' },
    ],
  },
  {
    id: 6,
    text: 'Как бы ты ответил на вопрос "Ты скорее..."?',
    options: [
      { emoji: '🦁', text: 'Лев (смелый, лидер)', personality: 'adventurer' },
      { emoji: '🐱', text: 'Кот (независимый, спокойный)', personality: 'zen' },
      { emoji: '🐶', text: 'Собака (верный, общительный)', personality: 'social' },
      { emoji: '🦊', text: 'Лиса (хитрая, умная)', personality: 'classic' },
      { emoji: '🦋', text: 'Бабочка (красивая, яркая)', personality: 'sweet' },
      { emoji: '🦉', text: 'Сова (ночная, загадочная)', personality: 'owl' },
    ],
  },
];
