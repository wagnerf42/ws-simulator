"" ensimag vim config file version 1.0.0
"" this file is intended for vim 8
"" before using it you will need to
"" - install plug with :
""      curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
"" (see https://github.com/junegunn/vim-plug)
"" - install the languageserver server for each language you indend to use :
""    * pyls for python (see https://github.com/palantir/python-language-server)
""    * rls for rust (see https://github.com/rust-lang-nursery/rls)
""    * clangd for c
"" - install some font with powerline symbols for eye candy and icons
"" (see https://github.com/powerline/fonts)
"" - change plugin directory to ~/.vim/plugged
"" (uncomment line 22 and comment line 21)

"" after that copy this file as your ~/.vimrc and execute :PlugInstall

set nocompatible
filetype off

" call plug#begin('/etc/vim/plugged')
call plug#begin('~/.vim/plugged')

Plug 'tpope/vim-sensible' " sane defaults

" eye candy
Plug 'vim-airline/vim-airline' " status bar (needs special fonts)
Plug 'vim-airline/vim-airline-themes'
Plug 'morhetz/gruvbox' " very nice and soft color theme
Plug 'ryanoasis/vim-devicons' " various symbols (linux, rust, python, ...)

" essential plugins
" see for example https://github.com/autozimu/LanguageClient-neovim/issues/35#issuecomment-288731665
Plug 'maralla/completor.vim' " auto-complete
Plug 'autozimu/LanguageClient-neovim', {
    \ 'branch': 'next',
    \ 'do': 'bash install.sh',
    \ } " as of july 2018 this branch is needed for vim8

" rust
Plug 'rust-lang/rust.vim' " syntax highlighting
Plug 'mattn/webapi-vim' " used for rust playpen


" not essential
Plug 'tpope/vim-fugitive' " git
Plug 'scrooloose/nerdtree' " browse files tree
" Plug 'junegunn/fzf' " fuzzy files finding

" snippets allow to easily 'fill' common patterns
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

call plug#end()

filetype plugin indent on

" configure maralla/completor to use tab
inoremap <expr> <Tab> pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <cr> pumvisible() ? "\<C-y>\<cr>" : "\<cr>"

" airline :
" for terminology you will need either to export TERM='xterm-256color'
" or run it with '-2' option
let g:airline_powerline_fonts = 1
set laststatus=2
au VimEnter * exec 'AirlineTheme hybrid'

set encoding=utf-8

syntax on

colo gruvbox
set background=dark
set number

let NERDTreeIgnore=['\.pyc$', '\~$'] "ignore files in NERDTree

" replace tabs
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab

" highlight trailing whitespace
highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+\%#\@<!$/

" some more rust
let g:LanguageClient_loadSettings = 1 " this enables you to have per-projects languageserver settings in .vim/settings.json
let g:rustfmt_autosave = 1
let g:rust_conceal = 1
set hidden
au BufEnter,BufNewFile,BufRead *.rs syntax match rustEquality "==\ze[^>]" conceal cchar=≟
au BufEnter,BufNewFile,BufRead *.rs syntax match rustInequality "!=\ze[^>]" conceal cchar=≠

" let's autoindent c files
au BufWrite *.c call LanguageClient#textDocument_formatting()

" run language server for python, rust and c
let g:LanguageClient_autoStart = 1
let g:LanguageClient_serverCommands = {
    \ 'python': ['pyls'],
    \ 'rust': ['rustup', 'run', 'stable', 'rls'],
    \ 'javascript': ['javascript-typescript-stdio'],
    \ 'go': ['go-langserver'],
    \ 'c' : ['clangd'] }
