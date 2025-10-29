# TODO: Adicionar Música "Noite Perfeita" de Branão e Funcionalidades

## 1. Adicionar Música ao Banco de Dados
- [x] Criar artista "Branão" se não existir.
- [x] Adicionar música "Noite Perfeita" com duração, file_url e cover (usar valores padrão ou placeholder).
- [x] Adicionar mais duas músicas: "Música 1" de "Artista 1" e "Música 2" de "Artista 2".

## 2. Implementar Seleção de Música no Player
- [x] Modificar player_view para aceitar parâmetro de música selecionada (via GET ou session).
- [x] Atualizar player.html para tornar itens do showcase e next_musics clicáveis, redirecionando para player com música selecionada.

## 3. Adicionar Funcionalidade de Favoritar
- [x] Criar modelo Favorite (ManyToMany entre User e Music).
- [x] Adicionar botão de favoritar no player.html.
- [x] Criar view para favoritar/desfavoritar música.
- [x] Atualizar player_view para mostrar status de favorito.

## 4. Implementar Notificação ao Clicar na Música
- [x] Adicionar JavaScript para mostrar toast notificação quando clicar em música (antes de ir ao player).
- [x] Implementar lógica para adicionar música à fila de reprodução (usar session para armazenar fila).
- [x] Atualizar player.html com toast CSS/JS.

## 5. Atualizar Modelos e Migrações
- [x] Adicionar modelo Favorite em music/models.py.
- [x] Criar migração para novo modelo.

## 6. Atualizar Views e URLs
- [x] Modificar music/views.py para novas funcionalidades.
- [x] Adicionar URLs em music/urls.py para favoritar e selecionar música.
- [x] Adicionar views para adicionar/remover da fila e obter fila.

## 7. Adicionar Botão de Fila na Página Inicial
- [x] Adicionar botão "Adicionar à Fila" nas músicas da página inicial.

## 8. Melhorar Player com Controles de Fila
- [x] Adicionar botão "+" para adicionar à fila nas músicas do player.
- [x] Implementar navegação anterior/próxima usando a fila.
- [x] Atualizar controles para usar fila quando disponível.

## 9. Testes e Verificações
- [x] Executar migrações.
- [x] Testar upload ou adição manual da música.
- [x] Verificar se música aparece no player quando selecionada.
- [x] Testar favoritar e notificação.
- [x] Testar adição à fila e navegação.
