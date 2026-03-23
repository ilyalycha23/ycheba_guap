// Компонент меню
const Menu = () => {
    const [activeItem, setActiveItem] = React.useState('home');
    
    const menuItems = [
        { id: 'home', label: 'Главная' },
        { id: 'about', label: 'О нас' },
        { id: 'services', label: 'Услуги' },
        { id: 'blog', label: 'Блог' },
        { id: 'contacts', label: 'Контакты' }
    ];
    
    const handleClick = (itemId, e) => {
        e.preventDefault();
        setActiveItem(itemId);
        
        // Вызываем функцию обновления контента
        if (window.updateContent) {
            window.updateContent(itemId);
        } else {
            console.error('Функция updateContent не найдена!');
        }
    };
    
    return (
        <nav className="menu">
            <div className="menu-container">
                <a href="/" className="logo" onClick={(e) => handleClick('home', e)}>
                    МойСайт
                </a>
                <ul className="menu-items">
                    {menuItems.map(item => (
                        <li key={item.id}>
                            <a 
                                href="#"
                                className={activeItem === item.id ? 'active' : ''}
                                onClick={(e) => handleClick(item.id, e)}
                            >
                                {item.label}
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        </nav>
    );
};

// Рендерим меню
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Menu />);