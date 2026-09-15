// счетчики на главной странице
function createStats(stats) {
    if (!stats || !stats.length) return '';
    
    return `
        <div class="stats-grid">
            ${stats.map(stat => `
                <div class="stat-card">
                    <div class="stat-icon">${stat.icon}</div>
                    <div class="stat-value" data-target="${stat.value}">0</div>
                    <div class="stat-label">${stat.label}</div>
                </div>
            `).join('')}
        </div>
    `;
}

// карточки преимуществ
function createFeatures(features) {
    if (!features || !features.length) return '';
    
    return `
        <div class="features-section">
            <h2>Наши преимущества</h2>
            <div class="features-grid">
                ${features.map(f => `
                    <div class="feature-card">
                        <div class="feature-icon">${f.icon}</div>
                        <h3>${f.title}</h3>
                        <p>${f.desc}</p>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// ВСПОМОГАТЕЛЬНЫЙ РЕНДЕР СЛАЙДЕРА ОТЗЫВОВ 
function renderTestimonialsInner(testimonials) {
    return `
            <div class="testimonials-slider">
                <button class="testimonial-btn prev" data-testimonial-action="prev">❮</button>
                <div class="testimonials-container" id="testimonialsContainer">
                    ${testimonials.map((t, i) => `
                        <div class="testimonial-card" data-index="${i}">
                            <div class="testimonial-rating">${'⭐'.repeat(t.rating)}</div>
                            <p class="testimonial-text">"${t.text}"</p>
                            <div class="testimonial-author">— ${t.name}</div>
                        </div>
                    `).join('')}
                </div>
                <button class="testimonial-btn next" data-testimonial-action="next">❯</button>
            </div>
            <div class="testimonial-dots" id="testimonialDots">
                ${testimonials.map((_, i) => `
                    <span class="testimonial-dot ${i === 0 ? 'active' : ''}" data-testimonial-index="${i}"></span>
                `).join('')}
            </div>
    `;
}


// прогресс-бары навыков
function createSkills(skills) {
    if (!skills || !skills.length) return '';
    
    return `
        <div class="skills-section">
            <h2>Мои навыки</h2>
            <div class="skills-container">
                ${skills.map(s => `
                    <div class="skill-item">
                        <div class="skill-header">
                            <span class="skill-name">${s.name}</span>
                            <span class="skill-percent">${s.level}%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: ${s.level}%"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}


// КОМПОНЕНТ технологий
function createTechStack(techs) {
    if (!techs || !techs.length) return '';
    
    return `
        <div class="tech-section">
            <h2>Технологии</h2>
            <div class="tech-cloud">
                ${techs.map(tech => `
                    <span class="tech-tag">${tech}</span>
                `).join('')}
            </div>
        </div>
    `;
}

// 7. АНИМАЦИЯ ЦИФР (плавный подсчет статистики)
function animateNumbers() {
    const stats = document.querySelectorAll('.stat-value');
    stats.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                stat.textContent = target;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(current);
            }
        }, 20);
    });
}

// логика слайдера
let currentTestimonial = 0;
let activePostData = null;

function prevTestimonial() {
    const testimonials = window.homeData?.testimonials || [];
    if (testimonials.length === 0) return;
    currentTestimonial = (currentTestimonial - 1 + testimonials.length) % testimonials.length;
    updateTestimonialDisplay();
}

function nextTestimonial() {
    const testimonials = window.homeData?.testimonials || [];
    if (testimonials.length === 0) return;
    currentTestimonial = (currentTestimonial + 1) % testimonials.length;
    updateTestimonialDisplay();
}

function goToTestimonial(index) {
    currentTestimonial = index;
    updateTestimonialDisplay();
}

// Обновление активного отзыва и точек слайдера
function updateTestimonialDisplay() {
    const container = document.getElementById('testimonialsContainer');
    const dots = document.querySelectorAll('.testimonial-dot');
    
    if (container) {
        container.style.transform = `translateX(-${currentTestimonial * 100}%)`;
    }
    
    dots.forEach((dot, index) => {
        if (index === currentTestimonial) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

//  ПОСТРОЕНИЕ СТРАНИЦЫ  
function buildPage(pageId) {
    
    let data;
    if (pageId === 'privacy-policy') {
        data = window.privacyPolicyData;
    } else if (pageId === 'terms-of-use') {
        data = window.termsOfUseData;
    } else {
        data = window[pageId + 'Data'];
    }
    
    if (!data) {
        return `<h1>Ошибка загрузки</h1><p>Данные для страницы "${pageId}" не найдены</p>`;
    }
    
    let html = `<h1>${data.title || ''}</h1>`;
    
    if (pageId === 'home') {
    html += `
        <div class="home-page">
            <div class="home-grid">
                ${data.image ? `
                    <div class="home-image">
                        <img src="${data.image}" alt="${data.name || 'Фото'}">
                    </div>
                ` : ''}
                
                <div class="home-content">
                    ${data.name ? `<h2>${data.name}</h2>` : ''}
                    
                    ${data.bio || ''}
                    
                    <!-- ===== ИСПРАВЛЕНО: используем data.skills ===== -->
                    ${data.skills ? `
                        <div class="skills-section">
                            <h3>За эти годы я освоил:</h3>
                            <ul class="skills-list">
                                ${data.skills.map(skill => `<li>${skill}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    <!-- ========================================= -->
                    
                    ${data.projectsText || ''}
                </div>
            </div>
            
            ${data.stats ? createStats(data.stats) : ''}     
            ${data.features ? createFeatures(data.features) : ''}
            ${data.skillsProgress ? createSkills(data.skillsProgress) : ''}
            ${data.techStack ? createTechStack(data.techStack) : ''}
        </div>
    `;
    } else if (pageId === 'portfolio') {
    html += `
        <div class="portfolio-page">
            <div class="portfolio-grid">
                ${data.projects ? data.projects.map(project => `
                    <div class="portfolio-card">
                        <div class="portfolio-image">
                            <img src="${project.image || 'https://via.placeholder.com/400x250/667eea/ffffff?text=Проект'}" alt="${project.name}">
                        </div>
                        <div class="portfolio-info">
                            <h3>${project.name}</h3>
                            <p class="portfolio-year">${project.year || ''}</p>
                            <p class="portfolio-desc">${project.description || ''}</p>
                            <div class="portfolio-tech">
                                ${project.technologies ? project.technologies.map(tech => 
                                    `<span class="tech-badge">${tech}</span>`
                                ).join('') : ''}
                            </div>
                            ${project.photo ? `
                                <a href="${project.photo}" class="portfolio-link" target="_blank" rel="noopener noreferrer">Посмотреть →</a>
                            ` : ''}
                        </div>
                    </div>
                `).join('') : ''}
            </div>
            
            <!-- Отзывы клиентов -->
            ${window.homeData?.testimonials ? `
                <div class="portfolio-testimonials">
                    <h3>Что говорят клиенты</h3>
                    ${renderTestimonialsInner(window.homeData.testimonials)}
                </div>
            ` : ''}
            
            ${data.contactText ? `
            <div class="portfolio-contact">
                <p>Хотите такой же сайт? <a href="#" data-nav-target="contacts">Свяжитесь со мной</a> в разделе "Контакты"!</p>
            </div>
        ` : ''}
        </div>
    `;
} else if (pageId === 'services') {
        html += `
            <div class="services-page">
                <div class="services-grid">
        `;
        
        if (data.items && data.items.length) {
            data.items.forEach(item => {
                html += `
                    <div class="service-card">
                        <div class="service-icon">${item.icon || '🔧'}</div>
                        <h3>${item.name}</h3>
                        <div class="service-time">⏱️ ${item.time}</div>
                        <p class="service-description">${item.description || ''}</p>
                        <div class="service-price">${item.price || 'Цена договорная'}</div>
                        <button class="service-order" data-order-service="${item.name}">Заказать сайт</button>
                    </div>
                `;
            });
        }
        
        html += `
                </div>
                
                <div class="services-disclaimer">
                    <p>${data.disclaimer || ''}</p>
                    <small>${data.note || ''}</small>
                </div>
            </div>
        `;
    } else if (pageId === 'blog') {
        if (data.posts && data.posts.length) {
            html += '<div class="blog-posts">';
            
            data.posts.forEach((post, index) => {
                html += `
                    <div class="blog-card">
                        ${post.image ? `
                            <div class="blog-card-image">
                                <img src="${post.image}" alt="${post.title}">
                            </div>
                        ` : ''}
                        <div class="blog-card-content">
                            <div class="blog-meta">
                                <span class="blog-date">${post.date || ''}</span>
                                <span class="blog-category">${post.category || ''}</span>
                            </div>
                            <h3>${post.title || ''}</h3>
                            <p class="blog-preview">${post.preview || ''}</p>
                            <div class="blog-footer">
                                <div class="blog-stats">
                                    <span>❤️ ${post.likes || 0}</span>
                                    <span>💬 ${post.comments || 0}</span>
                                </div>
                                <button class="read-more" data-post-id="${index + 1}">Читать →</button>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        }
    } else if (pageId === 'contacts') {
        html += `
            <div class="contacts-page">
                <div class="contacts-grid">
                    <!-- Левая колонка с контактами -->
                    <div class="contacts-info">
                        <h2>Свяжитесь со мной</h2>
                        
                        <div class="contact-card">
                            <div class="contact-item">
                                <span class="contact-icon">👤</span>
                                <div>
                                    <strong>${data.name || ''}</strong><br>
                                    <span>${data.company || ''}</span>
                                </div>
                            </div>
                            
                            ${data.phone ? `
                                <div class="contact-item">
                                    <span class="contact-icon">📞</span>
                                    <div>
                                        <strong>Телефон:</strong><br>
                                        <a href="tel:${data.phone}">${data.phone}</a>
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${data.email ? `
                                <div class="contact-item">
                                    <span class="contact-icon">✉️</span>
                                    <div>
                                        <strong>Email:</strong><br>
                                        <a href="mailto:${data.email}">${data.email}</a>
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${data.address ? `
                                <div class="contact-item">
                                    <span class="contact-icon">📍</span>
                                    <div>
                                        <strong>Адрес:</strong><br>
                                        <span>${data.address}</span>
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${data.workHours ? `
                                <div class="contact-item">
                                    <span class="contact-icon">⏰</span>
                                    <div>
                                        <strong>Часы работы:</strong><br>
                                        <span>${data.workHours}</span><br>
                                        ${data.weekend ? `<span>${data.weekend}</span>` : ''}
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                        
                        ${data.responseTime ? `
                            <div class="contact-response">
                                ${data.responseTime}
                            </div>
                        ` : ''}
                        
                        ${data.languages ? `
                            <div class="contact-languages">
                                <strong>Языки:</strong> ${data.languages.join(', ')}
                            </div>
                        ` : ''}
                        
                        ${data.workWith ? `
                            <div class="contact-work-with">
                                <strong>Работаю с:</strong> ${data.workWith}
                            </div>
                        ` : ''}
                    </div>
                    
                    <div class="contacts-right">
                        <div class="contact-form-section">
                            <h3>Напишите мне</h3>
                            <form class="contact-form" id="contactForm">
                                <input type="text" placeholder="Ваше имя" required>
                                <input type="email" placeholder="Ваш email" required>
                                <input type="text" placeholder="Тема">
                                <textarea placeholder="Ваше сообщение" rows="5" required></textarea>
                                <button type="submit" class="submit-btn">Отправить сообщение</button>
                            </form>
                        </div>
                        
                        ${data.social ? `
                            <div class="contact-social">
                                <h3>Я в соцсетях</h3>
                                <div class="social-grid">
                                    ${data.social.map(s => `
                                        <a href="${s.url}" target="_blank" class="social-contact-card">
                                            <span class="social-contact-icon">${s.icon}</span>
                                            <div class="social-contact-info">
                                                <strong>${s.name}</strong>
                                                <small>${s.username || ''}</small>
                                            </div>
                                        </a>
                                    `).join('')}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
                
                <div class="contact-map">
                    <h3>Как нас найти</h3>
                    <div class="map-placeholder" data-map-url="https://yandex.ru/maps/?ll=${data.coordinates.lng},${data.coordinates.lat}&z=17&pt=${data.coordinates.lng},${data.coordinates.lat},pm2blm">
                        <div class="map-overlay">
                            <span>🗺️ Открыть карту</span>
                            <small>${data.address || 'Нажмите чтобы открыть'}</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
        } else if (pageId === 'privacy-policy') {
    console.log('📢 СТРОИМ privacy-policy, data:', data);
    html += `
        <div class="legal-page">
            <div class="legal-content">${data.content}</div>
            <button class="nav-btn" data-nav-target="home">← На главную</button>
        </div>
    `;
} else if (pageId === 'terms-of-use') {
    console.log('📢 СТРОИМ terms-of-use, data:', data);
    html += `
        <div class="legal-page">
            <div class="legal-content">${data.content}</div>
            <button class="nav-btn" data-nav-target="home">← На главную</button>
        </div>
    `;
}
    
    return `<div class="page">${html}</div>`;
}

//   ОБНОВЛЕНИЕ КОНТЕНТА  
window.updateContent = function(pageId) {
    const content = document.getElementById('content');
    if (content) {
        content.innerHTML = buildPage(pageId);
        
        if (pageId === 'home') {
            setTimeout(animateNumbers, 500);
        }
    }
};

//  ФУНКЦИЯ ДЛЯ ПОКАЗА ОТДЕЛЬНОГО ПОСТА БЛОГА 
window.showPost = function(postId) {
    console.log('Открываем пост:', postId);
    
    // Получение данны х конкретного поста
    const post = window['post' + postId + 'Data'];
    
    if (!post) {
        alert('Пост не найден!');
        return;
    }
    
    const postHtml = `
        <div class="post-page">
            <button class="back-btn" data-nav-target="blog">← Назад к блогу</button>
            
            <article class="post-article">
                <h1>${post.title}</h1>
                
                <div class="post-meta">
                    <span>📅 ${post.date}</span>
                    <span>🏷️ ${post.category}</span>
                    <span>✍️ ${post.author}</span>
                </div>
                
                ${post.image ? `<img src="${post.image}" alt="${post.title}" class="post-image">` : ''}
                
                <div class="post-content">
                    ${post.content}
                </div>
                
                ${post.tags ? `
                    <div class="post-tags">
                        ${post.tags.map(tag => `<span class="post-tag">#${tag}</span>`).join('')}
                    </div>
                ` : ''}
                
                <div class="post-stats">
                    <span>❤️ ${post.likes} лайков</span>
                    <span>💬 ${post.comments} комментариев</span>
                </div>
                
                <div class="post-navigation">
                    <button class="nav-btn" data-nav-target="blog">← Все статьи</button>
                    <button class="nav-btn" data-action="share-post">📤 Поделиться</button>
                </div>
            </article>
        </div>
    `;
    
    // пост в контент
    document.getElementById('content').innerHTML = postHtml;
    
    activePostData = post;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

//  если Web Share API не поддерживается или упал 
function fallbackShare(shareData) {
    // модальное окно с выбором действия
    const action = confirm(
        `Поделиться статьей:\n\n` +
        `Заголовок: ${shareData.title}\n\n` +
        `Нажмите OK, чтобы скопировать ссылку, или Отмена, чтобы поделиться в Telegram`
    );
    
    if (action) {
        navigator.clipboard.writeText(shareData.url).then(() => {
            alert(`✅ Ссылка скопирована!\n\nТеперь вы можете вставить её куда угодно.`);
        }).catch(() => {
            prompt('Скопируйте ссылку:', shareData.url);
        });
    } else {
        const telegramUrl = `https://t.me/share/url?url=${encodeURIComponent(shareData.url)}&text=${encodeURIComponent(shareData.title)}`;
        window.open(telegramUrl, '_blank', 'width=600,height=400');
    }
}

async function shareActivePost() {
    if (!activePostData) return;

    const shareData = {
        title: activePostData.title,
        text: activePostData.preview || activePostData.content.replace(/<[^>]*>/g, '').substring(0, 100) + '...',
        url: window.location.href
    };

    if (navigator.share) {
        try {
            await navigator.share(shareData);
            console.log('Успешно поделились!');
            return;
        } catch (err) {
            if (err.name !== 'AbortError') {
                console.error('Ошибка шаринга:', err);
                fallbackShare(shareData);
            }
            return;
        }
    }

    fallbackShare(shareData);
}

// переопределение функции updateContent, чтобы онаработала и с post-* ID
const originalUpdateContent = window.updateContent;
window.updateContent = function(pageId) {
    console.log('📢 updateContent (новая) вызвана для:', pageId);
    
    if (pageId === 'blog') {
        originalUpdateContent('blog');
    } else if (pageId.startsWith('post-')) {
        const postId = pageId.replace('post-', '');
        window.showPost(postId);
    } else {
        originalUpdateContent(pageId);
    }
};
console.log('✅ updateContent переопределена');

//  ОТПРАВКА ФОРМЫ В TELEGRAM (через Bot API) 
window.handleFormSubmit = async function(event) {
    event.preventDefault();
    
    // данные 
    const form = event.target;
    const name = form.querySelector('input[placeholder="Ваше имя"]').value;
    const email = form.querySelector('input[placeholder="Ваш email"]').value;
    const subject = form.querySelector('input[placeholder="Тема"]').value;
    const message = form.querySelector('textarea').value;
    
    const TOKEN = 'UR_TOKEN';
    const CHAT_ID = 'UR_CHAT_ID';
    
    let text = `
        📬 НОВОЕ СООБЩЕНИЕ С САЙТА
        ━━━━━━━━━━━━━━━━
        👤 Имя: ${name}
        📧 Email: ${email}
        📌 Тема: ${subject || 'не указана'}
        ━━━━━━━━━━━━━━━━
        💬 Сообщение:
        ${message}
        ━━━━━━━━━━━━━━━━
        ⏰ Время: ${new Date().toLocaleString('ru-RU')}
    `.trim();

    if (text.length > 4090) {
        text = text.slice(0, 4087) + '...';
    }

    const actionUrl = `https://api.telegram.org/bot${TOKEN}/sendMessage`;

    // 1)  fetch — если среда не режет CORS
    try {
        const response = await fetch(actionUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: CHAT_ID, text: text })
        });
        const data = await response.json().catch(() => ({}));
        if (response.ok && data.ok) {
            alert(`✅ Спасибо, ${name}! Сообщение отправлено в Telegram.\nЯ отвечу вам на ${email} в ближайшее время.`);
            form.reset();
            return;
        }
        if (data.description) {
            console.error('Telegram API:', data);
            alert(`❌ Ошибка Telegram: ${data.description}\n\nПроверь токен, Chat ID и что ты написал боту /start.`);
            return;
        }
    } catch (e) {
        console.warn('fetch к Telegram не сработал (часто CORS) — пробуем отправку через iframe:', e);
    }

    // 2) Fallback: POST формой в скрытый iframe (CORS на ответ не мешает доставке запроса)
    let iframe = document.getElementById('telegramSubmitFrame');
    if (!iframe) {
        iframe = document.createElement('iframe');
        iframe.name = 'telegramSubmitFrame';
        iframe.id = 'telegramSubmitFrame';
        iframe.title = 'Telegram';
        iframe.setAttribute('aria-hidden', 'true');
        iframe.style.cssText = 'width:0;height:0;border:0;visibility:hidden;position:absolute';
        document.body.appendChild(iframe);
    }

    const proxyForm = document.createElement('form');
    proxyForm.method = 'POST';
    proxyForm.action = actionUrl;
    proxyForm.target = 'telegramSubmitFrame';
    proxyForm.acceptCharset = 'UTF-8';
    proxyForm.style.display = 'none';

    const addField = (n, v) => {
        const inp = document.createElement('input');
        inp.type = 'hidden';
        inp.name = n;
        inp.value = v;
        proxyForm.appendChild(inp);
    };
    addField('chat_id', String(CHAT_ID));
    addField('text', text);

    document.body.appendChild(proxyForm);
    proxyForm.submit();
    setTimeout(() => proxyForm.remove(), 2000);

    alert(
        `✅ Запрос отправлен.\n\nЕсли сообщения нет в Telegram через минуту — проверь токен в script.js, Chat ID и что ты написал боту /start.`
    );
    form.reset();
};

//  ФУНКЦИЯ ДЛЯ ЗАПОЛНЕНИЯ ФОРМЫ ПРИ ЗАКАЗЕ УСЛУГИ 
window.orderService = function(serviceName) {
    window.updateContent('contacts');
    
    setTimeout(() => {
        const subjectInput = document.querySelector('input[placeholder="Тема"]');
        if (subjectInput) {
            subjectInput.value = `Заказ услуги: ${serviceName}`;
            // подсветка поля
            subjectInput.style.borderColor = '#667eea';
            subjectInput.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
            
            // минус подсветка через 2 секунды
            setTimeout(() => {
                subjectInput.style.borderColor = '';
                subjectInput.style.boxShadow = '';
            }, 2000);
        }
    }, 300);
};

//  инициализация
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', (event) => {
        const navLink = event.target.closest('[data-nav-target]');
        if (navLink) {
            event.preventDefault();
            window.updateContent(navLink.dataset.navTarget);
            return;
        }

        const testimonialBtn = event.target.closest('[data-testimonial-action]');
        if (testimonialBtn) {
            const action = testimonialBtn.dataset.testimonialAction;
            if (action === 'prev') prevTestimonial();
            if (action === 'next') nextTestimonial();
            return;
        }

        const testimonialDot = event.target.closest('[data-testimonial-index]');
        if (testimonialDot) {
            goToTestimonial(Number(testimonialDot.dataset.testimonialIndex));
            return;
        }

        const serviceBtn = event.target.closest('[data-order-service]');
        if (serviceBtn) {
            window.orderService(serviceBtn.dataset.orderService);
            return;
        }

        const readMoreBtn = event.target.closest('[data-post-id]');
        if (readMoreBtn) {
            window.showPost(readMoreBtn.dataset.postId);
            return;
        }

        const mapBlock = event.target.closest('[data-map-url]');
        if (mapBlock) {
            window.open(mapBlock.dataset.mapUrl, '_blank', 'noopener,noreferrer');
            return;
        }

        const shareBtn = event.target.closest('[data-action="share-post"]');
        if (shareBtn) {
            shareActivePost();
        }
    });

    document.addEventListener('submit', (event) => {
        const form = event.target;
        if (form && form.id === 'contactForm') {
            window.handleFormSubmit(event);
        }
    });

    window.updateContent('home');
});