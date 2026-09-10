# Padrões e Regras para Contribuições internas

> É esperado, que todos os membros e contribuidores sigam as diretrizes abaixo antes de enviar qualquer revisão ou contribuição em qualquer repostório da organização.

## Convenções

> *O repositório deve **obrigatoriamente** seguir todas as convenções, padrões e diretrizes estabelecidos nesta documentação. **É esperado** que seja garantido sua estrutura, organização, nomenclatura e implementação. O cumprimento dessas convenções é **imprescindível** para manter a **consistência**, a **legibilidade** e a **qualidade do projeto**.*

### Convenção de Commits

Commits devem ser **atômicos** e **bem distribuídos**. Nunca agrupe múltiplas mudanças não relacionadas em um único commit, nem faça commits redundantes. A mensagem **deve seguir obrigatoriamente** o padrão `{pattern}: {message}`, sempre em `lowercase`. Não há convenção fixa de idioma para o commit, mas mantenha consistência dentro do repositório, normalmente definida pelo *CODEOWNER*: se o histórico já está em inglês, continue em inglês.

#### Exemplos de Commits Patterns

- `fix:` para solução de bugs ou problemas. *Exemplo:* `fix: resolve login validation bug`
- `feat:` para adição de nova funcionalidade. *Exemplo:* `feat: introduce user profile system`
- `docs:` para mudanças em documentação. *Exemplo:* `docs: update installation guide`
- `style:` para alterações visuais ou formatação sem impacto funcional. *Exemplo:* `style: adjust code indentation`
- `refactor:` para reestruturação interna sem alterar comportamento. *Exemplo:* `refactor: simplify authentication logic`
- `build:` para mudanças no sistema de build ou dependências. *Exemplo:* `build: update gradle dependencies`
- `test:` para adição ou modificação de testes. *Exemplo:* `test: add unit tests for login service`
- `ci:` normalmente utilizado para teste ou ajustes de pipeline. *Exemplo:* `ci: implementing docker-hub push workflow`
- `chore:` para tarefas de manutenção e configuração. *Exemplo:* `chore: update project configuration`

### Convenção de Branches

> *Sem exceção, **todas** as branches devem **obrigatoriamente** seguir os padrões e convenções estabelecidos abaixo. **É esperado** que seu uso seja garantido de forma consistente, mantendo a **organização**, a **padronização** e a **qualidade** do fluxo de desenvolvimento.*

Branches de trabalho ficam sempre em `lowercase`, sem espaços ou caracteres especiais, no formato `{pattern}/{descricao-curta}`.

> Branches padrão de repositórios: `main` *&* `qa` (para serviços com deploy no render)

#### Exemplos de Branch Patterns

- `feat/` para nova funcionalidade. *Exemplo:* `feat/user-profile-system`
- `fix/` para correção de bug. *Exemplo:* `fix/login-validation`
- `docs/` para documentação. *Exemplo:* `docs/installation-guide`
- `style/` para formatação/visual. *Exemplo:* `style/code-formatting`
- `refactor/` para refatoração. *Exemplo:* `refactor/authentication-logic`
- `build/` para build/dependências. *Exemplo:* `build/gradle-update`
- `test/` para testes. *Exemplo:* `test/login-service`
- `chore/` para manutenção/configuração. *Exemplo:* `chore/project-configuration`
- `ci/` para pipeline de CI. *Exemplo:* `ci/github-workflow`
- `hotfix/` para correção urgente em produção. *Exemplo:* `hotfix/payment-crash`
- `release/` para preparação de release. *Exemplo:* `release/v1.0.0`

Pull Requests devem sempre ser mergeadas inicialmente em `qa`, nunca abra Pull Request direto para `main`. Caso uma Pull Request seja feita diretamente na `main`, será aberto automaticamente um Pull Request de sincronização, que deverá ser analisado.

## Pull Requests

- Preencha o template de Pull Request (`.github/pull_request_template.md`) por
  completo.
- A descrição da Pull Request deve ser em português.
- Só abra o Pull Request quando o CI estiver passando.
- É esperado que antes do merge, o CI esteja passando.

## Code Owners

- Mudanças em caminhos cobertos pelo [`.github/CODEOWNERS`](./CODEOWNERS)
  exigem aprovação do(s) dono(s) listado(s) antes do merge.

## Regras de Código

- Siga o padrão de código já existente no repositório (nomenclatura,
  estrutura de pastas, estilo de formatação).
- Evite complexidade arquitetural desnecessária, não introduza camadas,
  abstrações ou padrões de design sem uma necessidade concreta e imediata.
- Priorize soluções simples e diretas sobre soluções "genéricas" ou
  "escaláveis" que não foram pedidas.

## Variáveis de Ambiente (Infisical)

> *Toda variável de ambiente (credencial, config, chave de terceiro) da organização vive centralizada no **Infisical** — não existe mais `.env` preenchido manualmente nem secret guardado só na cabeça de alguém. O `.env.example` de cada repositório só documenta os nomes esperados; o valor real sempre vem do Infisical.*

- **Projeto**: `2296d19c-5f3b-41e1-afa3-fcde39966a71` (org "Solaria").
- **Ambientes**: `local`, `qa`, `prod` (não existe `dev`).
- **Organização**: pastas por categoria/tecnologia (`/auth`, `/database`, `/redis`, `/google`, `/llm`, `/cloudinary`, `/otel`, `/databricks`, `/vite`, `/service-urls`, `/recommendation`, `/mcp`, `/agent-queue`, `/outbox`, `/docker`, `/shared`), nunca por serviço — uma credencial usada por 2+ serviços (ex.: mesma instância Postgres) vive uma única vez na pasta da tecnologia, não duplicada por repositório.

### Instalar o CLI

```bash
npm install -g @infisical/cli
```

> No Windows/Git Bash, o wrapper instalado pelo npm costuma falhar com `Permission denied`. Se isso acontecer, chame o binário direto:
> `~/AppData/Roaming/npm/node_modules/@infisical/cli/bin/infisical.exe`
> e rode `export MSYS_NO_PATHCONV=1` antes de qualquer comando com `--path=/...` (senão o Git Bash converte o `/` num caminho de arquivo do Windows).

Depois de instalado, autentique com sua conta pessoal:

```bash
infisical login
```

### Adicionar uma variável nova

1. Decida a pasta pela **tecnologia/categoria** que a variável representa (não pelo nome do serviço que vai consumi-la).
2. Adicione o valor em cada ambiente onde ela se aplica:

```bash
infisical secrets set "MINHA_CHAVE=valor" \
  --projectId=2296d19c-5f3b-41e1-afa3-fcde39966a71 \
  --env=<local|qa|prod> \
  --path=/<pasta>
```

3. O `.env.example` do repositório deve ser atualizado com o nome da variável (sem o valor), documentando que ela existe.

> ⚠️ **QA hoje tem uma particularidade temporária**: por um bug de permissão ainda em investigação numa das Machine Identities, os serviços em QA leem as secrets pela raiz (`--path=/`, não-recursivo) em vez de por pasta. Enquanto isso não for resolvido, replique a variável também na raiz do ambiente `qa`:
>
> ```bash
> infisical secrets set "MINHA_CHAVE=valor" \
>   --projectId=2296d19c-5f3b-41e1-afa3-fcde39966a71 \
>   --env=qa \
>   --path=/
> ```
>
> Depois de adicionar a secret (pasta + raiz em `qa`), é necessário **reiniciar o serviço no Render** — a leitura só acontece no boot do container, não há hot-reload.

### Usar as variáveis localmente

Não é necessário preencher um `.env` na mão. Duas opções:

**Rodar o serviço já com as variáveis injetadas** (recomendado):

```bash
infisical run \
  --projectId=2296d19c-5f3b-41e1-afa3-fcde39966a71 \
  --env=local \
  --path=/ \
  --recursive \
  -- <comando de start do repositório>
```

**Gerar um `.env` de verdade** (para quem prefere, ex.: IDE que só lê `.env`):

`infisical export` não tem `--recursive` como o `run` — rode um export por pasta e concatene (só as pastas que o repositório realmente consome, ver `.env.example`):

```bash
for pasta in database redis llm; do
  infisical export \
    --projectId=2296d19c-5f3b-41e1-afa3-fcde39966a71 \
    --env=local \
    --path=/$pasta \
    --format=dotenv >> .env
done
```

## Referência

Este documento resume as convenções oficiais de Git da organização. Em caso
de dúvida ou divergência, a fonte da verdade é o Confluence:

- [Convenções](https://interdesctruction.atlassian.net/wiki/spaces/Arquitetur/pages/76283905/Conven+es) (página-índice com todas as convenções do projeto)
- [Commit Pattern](https://interdesctruction.atlassian.net/wiki/spaces/Arquitetur/pages/28901387/Commit+Pattern) (padronização das mensagens de commit)
- [Branches Pattern](https://interdesctruction.atlassian.net/wiki/spaces/Arquitetur/pages/33128466/Branches+Pattern) (padronização de nomes de branch)
- [Convenção de código](https://interdesctruction.atlassian.net/wiki/spaces/Arquitetur/pages/36339713/Conven+o+de+c+digo) (nomenclatura de variáveis, classes e constantes por linguagem)
- [Nomenclatura de repositórios](https://interdesctruction.atlassian.net/wiki/spaces/Arquitetur/pages/75890706/Nomeclatura+de+reposit+rios) (prefixos usados para nomear novos repositórios)
