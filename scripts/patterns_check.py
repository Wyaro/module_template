#!/usr/bin/env python3
"""Проверка каталога эталонов module_template (core_patterns.json).

Выход:
  0 — все записи со status=demoed указывают на существующие файлы
  1 — есть битые пути или записи planned
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


MODULE_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = MODULE_ROOT / 'client' / 'js' / 'core_patterns.json'
PROJECT_ROOT = MODULE_ROOT.parents[1]


def _configure_stdout() -> None:
    """Windows-консоль часто cp1252 — включаем UTF-8 для русских сообщений."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, 'reconfigure', None)
        if callable(reconfigure):
            try:
                reconfigure(encoding='utf-8', errors='replace')
            except Exception:
                pass


def _ok(msg: str) -> None:
    print(f'[OK] {msg}')


def _warn(msg: str) -> None:
    print(f'[WARNING] {msg}')


def _err(msg: str) -> None:
    print(f'[ERROR] {msg}')


def main() -> int:
    _configure_stdout()
    if not CATALOG_PATH.is_file():
        _err(f'Каталог не найден: {CATALOG_PATH.relative_to(PROJECT_ROOT)}')
        return 1

    try:
        data = json.loads(CATALOG_PATH.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        _err(f'Некорректный JSON: {exc}')
        return 1

    patterns = data.get('patterns')
    if not isinstance(patterns, list) or not patterns:
        _err('В core_patterns.json нет списка patterns')
        return 1

    missing_files = 0
    planned = 0
    demoed = 0

    print(f'[INFO] Каталог: {CATALOG_PATH.relative_to(PROJECT_ROOT)}')
    print(f'[INFO] Записей: {len(patterns)}')

    for item in patterns:
        if not isinstance(item, dict):
            _err('Элемент patterns должен быть объектом')
            missing_files += 1
            continue

        pattern_id = item.get('id') or '<без id>'
        status = item.get('status') or 'planned'
        demo_file = item.get('demoFile') or ''
        rule = item.get('rule') or ''

        if status == 'demoed':
            demoed += 1
            if not demo_file:
                _err(f'{pattern_id}: status=demoed, но demoFile пуст')
                missing_files += 1
                continue
            path = MODULE_ROOT / demo_file
            if path.is_file():
                _ok(f'{pattern_id} → {demo_file}' + (f' ({rule})' if rule else ''))
            else:
                _err(f'{pattern_id}: файл не найден: {demo_file}')
                missing_files += 1
        else:
            planned += 1
            _warn(f'{pattern_id}: status={status} — добавьте демо в module_template')

    print()
    print(f'[INFO] demoed={demoed}, planned={planned}, broken={missing_files}')

    if missing_files:
        _err('Проверка не пройдена: исправьте пути demoFile или статус записей')
        return 1

    if planned:
        _warn(
            'Есть паттерны без демо (planned). '
            'Новый функционал ядра для модулей обязан появиться здесь со status=demoed.',
        )
        return 1

    _ok('Все паттерны каталога имеют рабочее демо')
    return 0


if __name__ == '__main__':
    sys.exit(main())
