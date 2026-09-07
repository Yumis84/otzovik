# Отзыв.com — Published Review HTML QA v2

## Назначение

Проверка того, что один опубликованный отзыв является одновременно:

- читаемым человеком;
- извлекаемым Google/Yandex и другими поисковыми системами;
- понятным AI-агентам без обязательного выполнения JavaScript;
- связанным со стабильным Review ID и provenance.

## Обязательные проверки

- [ ] Страница имеет `<article class="review" id="review-<stable-id>" data-review-id="<stable-id>">`.
- [ ] Автор находится в видимом `<header>`.
- [ ] Оценка представлена числом и доступным текстом `N из 5`; звёзды только визуальное дополнение.
- [ ] Дата публикации находится в `<time datetime="ISO-8601-date">`.
- [ ] Полный разрешённый текст находится в обычном HTML `<p>` и не появляется только после JS.
- [ ] Компания и, если применимо, филиал/услуга указаны в видимом контексте.
- [ ] В `<footer>` присутствует provenance: источник/способ поступления и разрешённый оригинальный URL либо объяснение отсутствия URL.
- [ ] Review ID стабилен и совпадает между DOM, ссылками и JSON-LD.
- [ ] JSON-LD `Review` не противоречит видимому HTML.
- [ ] JSON-LD не содержит скрытых или придуманных фактов.
- [ ] Нет обязательного client-side rendering для чтения отзыва.
- [ ] Публичный список содержит только `published` записи.
- [ ] Черновики и `moderation` записи не доступны через публичный HTML/JSON.
- [ ] Жалоба на отзыв является отдельным действием и не смешана с provenance.
- [ ] Для внешнего источника полный текст показывается только при наличии права на републикацию; иначе — разрешённый фрагмент/метаданные и ссылка на источник.

## Synthetic fixture

`reviews/ortomediya/contract-fixture.html` — только технический пример. Он помечен `noindex,nofollow`, явно сообщает, что данные синтетические, и не является опубликованным отзывом.

## Empty-state gate

До появления реальных модерированных публикаций `/reviews/ortomediya/` должен оставаться в empty state. Синтетические данные запрещено переносить в публичный список.

## Production gate

До Cloudflare/Supabase production publication остаются отдельными контрольными точками:

1. first-party submission protection;
2. moderation transition to `published`;
3. server-side HTML rendering of published records;
4. JSON-LD consistency test;
5. public JSON contract test;
6. crawler/AI readability check.
