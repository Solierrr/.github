# Workflows de preview

`preview-gallery.yml` e `preview-storybook.yml` publicam os ambientes de preview no GitHub Pages (ambiente `PREVIEW`) e fazem o check de pull request. O repositório que chama concede `pages: write` e `id-token: write` no job que chama o workflow (não no nível do workflow, o que o SonarCloud reprova), publica no push da `main` e só confere (typecheck e build) na pull request.

## Galeria Vite

```yaml
name: Preview

on:
  push:
    branches: [main]
  pull_request:
    paths:
      - "gallery/**"
      - ".github/workflows/preview.yml"
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: preview-${{ github.event_name == 'pull_request' && github.ref || 'pages' }}
  cancel-in-progress: true

jobs:
  preview:
    permissions:
      contents: read
      pages: write
      id-token: write
    uses: Solierrr/.github/.github/workflows/preview-gallery.yml@main
    with:
      publish: ${{ github.event_name != 'pull_request' }}
```

Entradas: `working-directory` (padrão `gallery`, com `package.json` próprio e os scripts `typecheck` e `build`, que gera `dist`), `node-version` (24), `root-install` e `root-command` (para galerias que importam o código do projeto: instalam as dependências e rodam, por exemplo, o build na raiz antes) e `publish`. O build recebe `VITE_COMMIT` e `VITE_REPOSITORY` para o rodapé da galeria.

## Storybook

```yaml
jobs:
  preview:
    permissions:
      contents: read
      pages: write
      id-token: write
    uses: Solierrr/.github/.github/workflows/preview-storybook.yml@main
    with:
      publish: ${{ github.event_name != 'pull_request' }}
```

Entradas: `node-version` (24), `test` e `test-command` (testes das histórias, desligados por padrão) e `publish`. O build é `npm run build-storybook` e a saída, `storybook-static`.

## Regras

- Publicação só da `main`; o Pages do repositório precisa estar no modo `workflow`.
- Os builds usam caminhos relativos, para funcionar em `<org>.github.io/<repositório>/` e no proxy do portal de documentação.
- Cada repositório descreve o preview em um `gallery.json` na raiz, lido pelo portal.
- Se o job `deploy` falhar sem nenhum passo, olhe a anotação do job: o ambiente `PREVIEW` do repositório pode ter uma regra de branch que não inclui a `main` (Settings, Environments, PREVIEW, Deployment branches); o log do job não aparece nesse caso.
