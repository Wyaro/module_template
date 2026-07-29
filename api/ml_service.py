"""
Rule-based text classification model — учебный пример для СКБ.

Модель анализирует входящий текст по ключевым словам и базовым признакам,
определяя категорию, приоритет и балл важности обращения.

Для замены на настоящую ML-модель достаточно изменить функцию `predict`:
  - загрузить обученный классификатор (sklearn, pytorch и т.п.),
  - передать текст через векторизатор,
  - вернуть структуру с теми же полями.
"""

from typing import Dict, List, Tuple
import re

from django.utils.translation import gettext as _

# ---------------------------------------------------------------------------
# Словарь правил: (категория, ключевые слова, базовый приоритет)
# ---------------------------------------------------------------------------
_RULES: List[Tuple[str, List[str], str]] = [
    ('error', [
        'ошибка', 'error', 'exception', 'упал', 'падает', 'сбой',
        'критическ', 'fail', 'краш', 'краш', '500', '503', '401', '403',
        'не работает', 'недоступен', 'не запускается',
    ], 'high'),
    ('urgent', [
        'срочно', 'urgent', 'asap', 'немедленно', 'прямо сейчас',
        'блокирует', 'критично для', 'production',
    ], 'high'),
    ('request', [
        'запрос', 'прошу', 'предоставьте', 'нужна информация',
        'уточните', 'как получить', 'как настроить', 'как использовать',
        'вопрос', 'подскажите', 'помогите', 'request',
    ], 'medium'),
    ('report', [
        'отчёт', 'отчет', 'report', 'аналитика', 'статистика',
        'данные за', 'результаты', 'сводка', 'итоги', 'анализ',
        'динамика', 'рост', 'снижение',
    ], 'low'),
    ('task', [
        'задача', 'задание', 'task', 'реализовать', 'доработать',
        'разработать', 'добавить', 'внедрить', 'создать', 'сделать',
        'улучшить', 'оптимизировать',
    ], 'medium'),
]

# ---------------------------------------------------------------------------
# Вычисление балла из признаков текста
# ---------------------------------------------------------------------------
def _compute_score(text: str, matched: List[str], priority: str) -> float:
    """Балл от 0 до 100 на основе признаков текста."""
    base = {'high': 70, 'medium': 45, 'low': 20}.get(priority, 30)
    keyword_bonus = min(len(matched) * 5, 20)
    exclamation_bonus = min(text.count('!') * 3, 9)
    length_penalty = -5 if len(text) < 20 else 0
    return round(min(100, base + keyword_bonus + exclamation_bonus + length_penalty), 1)


def _classify(text: str) -> Dict:
    """Основная логика классификации."""
    lower = text.lower()
    best_category = 'other'
    best_priority = 'low'
    best_keywords: List[str] = []
    best_match_count = 0

    for category, keywords, priority in _RULES:
        matched = [kw for kw in keywords if kw in lower]
        if len(matched) > best_match_count:
            best_match_count = len(matched)
            best_category = category
            best_priority = priority
            best_keywords = matched

    # Если несколько слов срочности — повышаем приоритет
    urgent_words = [kw for kw in _RULES[1][1] if kw in lower]
    if urgent_words and best_priority != 'high':
        best_priority = 'high'
        best_keywords += urgent_words

    return {
        'category': best_category,
        'priority': best_priority,
        'matched_keywords': list(set(best_keywords)),
        'score': _compute_score(text, best_keywords, best_priority),
        'text_length': len(text),
        'sentence_count': len(re.findall(r'[.!?]+', text)) or 1,
    }


# ---------------------------------------------------------------------------
# Публичный API ml_service
# ---------------------------------------------------------------------------
def predict(payload: Dict) -> Dict:
    text = str(payload.get('text', '')).strip()
    if not text:
        return {
            'category': 'other',
            'priority': 'low',
            'score': 0.0,
            'matched_keywords': [],
            'text_length': 0,
            'sentence_count': 0,
            'note': _('Текст не передан — классификация невозможна.'),
        }
    return _classify(text[:2000])  # защита от очень длинных текстов


def get_model_meta() -> Dict:
    return {
        'model_name': 'RuleBasedClassifier',
        'model_version': '1.0.0',
        'model_type': 'rule-based',
        'description': _(
            'Учебная модель классификации текстов на основе словарных правил. '
            'Демонстрирует контракт predict/meta API для модулей СКБ.'
        ),
        'categories': ['error', 'urgent', 'request', 'report', 'task', 'other'],
        'priority_levels': ['low', 'medium', 'high'],
        'max_input_length': 2000,
        'replace_hint': _(
            'Для подключения реальной ML-модели замените функцию predict() '
            'в api/ml_service.py на вызов своего обученного классификатора.'
        ),
    }
