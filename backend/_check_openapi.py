"""Check current OpenAPI language."""
import json
with open('D:/PolyPlex/backend/openapi.json', 'r', encoding='utf-8') as f:
    spec = json.load(f)

print('=== TAGS ===')
for t in spec.get('tags', []):
    print(f'  {t}')

print()
print('=== PATHS (summary) ===')
for path in sorted(spec['paths'].keys()):
    methods = spec['paths'][path]
    for method in methods:
        info = methods[method]
        print(f'  {method.upper()} {path}')
        print(f'    tags: {info.get("tags", [])}')
        print(f'    summary: {info.get("summary", "")}')
        desc = info.get('description', '')
        if desc:
            print(f'    description: {desc[:80]}')
