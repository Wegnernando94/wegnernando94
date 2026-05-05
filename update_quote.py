import random
import re
from datetime import datetime

QUOTES = [
    ('💡', '"A qualidade nunca é um acidente; é sempre o resultado de um esforço inteligente."', 'John Ruskin'),
    ('🚀', '"Automatize o repetível para liberar tempo para o que importa."', 'Fernando Wegner'),
    ('🔍', '"Testar é questionar o software com inteligência, não apenas executar casos."', 'James Bach'),
    ('⚡', '"A melhor performance é aquela que o usuário nunca percebe que existiu."', 'Anônimo'),
    ('🛡️', '"Segurança não é um produto, é um processo contínuo."', 'Bruce Schneier'),
    ('🤖', '"CI/CD não acelera o deploy — acelera o aprendizado."', 'Jez Humble'),
    ('📊', '"Sem métricas, qualidade é apenas uma opinião."', 'Tom DeMarco'),
    ('🌐', '"A cloud não é o destino, é o meio para entregar valor mais rápido."', 'Werner Vogels'),
    ('🧪', '"Um bug encontrado em produção custa 100x mais do que encontrado em teste."', 'Barry Boehm'),
    ('🎯', '"Qualidade é responsabilidade de todos, mas começa com quem testa."', 'Anônimo'),
    ('💻', '"O código limpo faz uma coisa bem feita."', 'Robert C. Martin'),
    ('🔧', '"DevOps é cultura primeiro, ferramentas depois."', 'Patrick Debois'),
    ('📈', '"Monitore tudo. Você não pode melhorar o que não mede."', 'Peter Drucker'),
    ('🏆', '"Excelência não é uma habilidade, é uma atitude."', 'Ralph Marston'),
    ('🌱', '"Todo sistema legado já foi moderno algum dia. Respeite-o enquanto o evolui."', 'Anônimo'),
]

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    today = datetime.utcnow()
    random.seed(today.year * 1000 + today.month * 31 + today.day)
    emoji, quote, author = random.choice(QUOTES)

    new_quote = f'  <!-- QUOTE_START -->\n  <i>{emoji} {quote} — {author}</i>\n  <!-- QUOTE_END -->'
    content = re.sub(
        r'  <!-- QUOTE_START -->.*?<!-- QUOTE_END -->',
        new_quote,
        content,
        flags=re.DOTALL
    )

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Quote updated: {emoji} {quote} — {author}")

if __name__ == '__main__':
    update_readme()
