# Echo Music - Aplicação de Streaming de Música

## Descrição

Echo Music é uma aplicação web desenvolvida em Django que simula um serviço de streaming de música. A aplicação permite aos usuários buscar músicas, criar playlists personalizadas e gerenciar suas coleções musicais.

## Funcionalidades Implementadas

### História 1: Página Inicial com Busca de Músicas
- Interface principal com design moderno e gradiente roxo
- Barra de busca funcional que permite pesquisar por título da música ou nome do artista
- Exibição de músicas em cards organizados em grid responsivo
- Seção "Mais Gêneros" com playlists curadas (Músicas para relaxar, Viagem, Balada)
- Sidebar com navegação e acesso às playlists do usuário

### História 2: Sistema de Playlists
- Criação de playlists personalizadas pelos usuários
- Visualização detalhada de playlists com lista de músicas
- Funcionalidade para adicionar músicas às playlists
- Funcionalidade para remover músicas das playlists
- Cálculo automático da duração total e número de músicas na playlist
- Interface similar ao Spotify com design dark e elementos visuais modernos

## Tecnologias Utilizadas

- **Backend**: Django 5.2.6
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Banco de Dados**: SQLite (desenvolvimento)
- **Estilo**: CSS customizado com gradientes e efeitos de blur

## Estrutura do Projeto

```
echo_music/
├── core/                   # App principal
│   ├── templates/core/
│   │   └── home.html      # Página inicial
│   └── views.py           # Views da página inicial e busca
├── music/                 # App de músicas
│   ├── models.py          # Modelos Artist e Music
│   └── admin.py           # Configuração do admin
├── playlists/             # App de playlists
│   ├── models.py          # Modelo Playlist
│   ├── views.py           # Views de gerenciamento de playlists
│   ├── templates/playlists/
│   │   ├── detail.html    # Página de detalhes da playlist
│   │   └── create.html    # Página de criação de playlist
│   └── urls.py            # URLs das playlists
├── templates/
│   └── base.html          # Template base
└── echo_music/            # Configurações do projeto
    ├── settings.py
    └── urls.py
```

## Modelos de Dados

### Artist
- `name`: Nome do artista
- `created_at`: Data de criação

### Music
- `title`: Título da música
- `artist`: Referência ao artista (ForeignKey)
- `duration`: Duração no formato "mm:ss"
- `file_url`: URL do arquivo de áudio (opcional)
- `created_at`: Data de criação

### Playlist
- `name`: Nome da playlist
- `user`: Usuário proprietário (ForeignKey)
- `musics`: Músicas da playlist (ManyToManyField)
- `created_at`: Data de criação
- Métodos: `get_total_duration()`, `get_music_count()`

## Como Executar

1. **Instalar dependências**:
   ```bash
   pip install django
   ```

2. **Executar migrações**:
   ```bash
   python manage.py migrate
   ```

3. **Criar superusuário** (opcional):
   ```bash
   python manage.py createsuperuser
   ```

4. **Executar servidor**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

5. **Acessar a aplicação**:
   - Interface principal: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Dados de Exemplo

O projeto inclui dados de exemplo com:
- Artistas: Matue, Gorilla Roxo
- 7 músicas de diferentes durações
- 1 playlist de exemplo ("Máquina do tempo") com todas as músicas

## Funcionalidades Técnicas

- **Busca**: Implementada com Django Q objects para buscar por título ou artista
- **AJAX**: Usado para adicionar/remover músicas das playlists sem recarregar a página
- **Responsivo**: Interface adaptável para diferentes tamanhos de tela
- **Autenticação**: Sistema de usuários do Django para gerenciar playlists pessoais
- **Admin**: Interface administrativa para gerenciar músicas, artistas e playlists

## Design

O design foi inspirado nas imagens fornecidas, replicando:
- Gradiente roxo de fundo
- Cards com efeito de blur e transparência
- Tipografia moderna e limpa
- Layout com sidebar e área principal
- Efeitos hover e transições suaves
- Paleta de cores consistente com o tema musical

## Próximos Passos

- Implementar reprodução de áudio
- Adicionar sistema de favoritos
- Implementar upload de músicas
- Adicionar sistema de recomendações
- Implementar player de música com controles

- Adicionar sistema de compartilhamento de playlists

