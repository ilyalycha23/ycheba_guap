window.blogData = {
    title: 'Блог',
    subtitle: 'Заметки о разработке, React и не только',
    
    posts: [
        {
            id: 1,
            date: '15 марта 2024',
            title: 'Как я начал учить React',
            preview: 'Спойлер: это проще, чем кажется! Делюсь своим опытом и ошибками.',
            content: 'Полный текст статьи о том, как я разбирался с React...',
            image: 'images/blog-1.jpg', // если есть картинка
            category: 'Обучение',
            author: 'Админ',
            likes: 24,
            comments: 5
        },
        {
            id: 2,
            date: '10 марта 2024',
            title: 'Топ-5 расширений для VS Code',
            preview: 'Собрал лучшие плагины, которые ускоряют разработку в 10 раз.',
            image: 'images/blog-2.jpg',
            category: 'Инструменты',
            author: 'Админ',
            likes: 18,
            comments: 3
        },
        {
            id: 3,
            date: '5 марта 2024',
            title: 'Почему React — это космос',
            preview: 'Компонентный подход, виртуальный DOM и другие плюшки, которые меняют всё.',
            image: 'images/blog-3.jpg',
            category: 'React',
            author: 'Админ',
            likes: 32,
            comments: 7
        },
        {
            id: 4,
            date: '1 марта 2024',
            title: 'Как сверстать слайдер за 15 минут',
            preview: 'Пошаговое руководство для начинающих. Без лишней воды.',
            image: 'images/blog-4.jpg',
            category: 'CSS',
            author: 'Админ',
            likes: 15,
            comments: 2
        },
        {
            id: 5,
            date: '25 февраля 2024',
            title: 'Мобильное меню: гайд для новичков',
            preview: 'Делаем бургер, выпадашки и адаптив, который не стыдно показать.',
            image: 'images/blog-5.jpg',
            category: 'Верстка',
            author: 'Админ',
            likes: 21,
            comments: 4
        }
    ],
    
    categories: [
        { name: 'Все записи', count: 5 },
        { name: 'React', count: 1 },
        { name: 'CSS', count: 1 },
        { name: 'Обучение', count: 1 },
        { name: 'Инструменты', count: 1 },
        { name: 'Верстка', count: 1 }
    ],
    
    tags: ['react', 'javascript', 'css', 'html', 'vs code', 'слайдер', 'меню'],
    
    author: {
        name: 'Алексей',
        avatar: 'images/avatar.jpg',
        bio: 'Веб-разработчик, люблю React и эксперименты'
    }
};