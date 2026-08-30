# NoCode Folio

NoCode Folio e uma pagina de perfil modular no estilo link-in-bio, organizada em uma grade Bento. O projeto apresenta links sociais, projetos, newsletter e localizacao em blocos responsivos com tema escuro.

## Tecnologias

- React 19 e TypeScript
- TanStack Start e TanStack Router
- Vite
- Tailwind CSS
- shadcn/ui e Radix UI
- dnd-kit
- Supabase

## Recursos

- Grade Bento responsiva: uma coluna em telas pequenas, duas em tablets e quatro em desktop.
- Cartao de perfil, links sociais, vitrine de conteudo, newsletter e mapa.
- Modo de edicao para reorganizar os blocos.
- Dados de perfil e widgets integrados ao Supabase.
- Interface em tema escuro com efeito de vidro.

## Desenvolvimento local

Requisitos: Node.js 20 ou superior e npm.

```sh
npm install
npm run dev
```

O servidor exibira no terminal o endereco local para abrir no navegador.

## Outros comandos

```sh
npm run build
npm run lint
npm run preview
```

## Estrutura principal

```text
src/
  components/bento/   # Grade e conteudo dos widgets
  integrations/       # Cliente e tipos do Supabase
  lib/                # Consultas e utilitarios
  routes/             # Rotas do TanStack Start
  styles.css          # Estilos globais
public/images/        # Imagens usadas na pagina
```

## Lovable

Este projeto esta conectado ao [Lovable](https://lovable.dev). Alteracoes enviadas para a branch conectada sao sincronizadas com o editor.
