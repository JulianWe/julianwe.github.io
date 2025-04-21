" https://vimawesome.com/

" spaces & tabs
set shiftwidth=4
set tabstop=4
set softtabstop=4
set smarttab
set expandtab
set autoindent
set number

" spell checking
set nospell
nnoremap <C-E> :setlocal spell! spelllang=en<CR>
nnoremap <C-G> :setlocal spell! spelllang=de<CR>

" shortcutting split navigation, saving a keypress:
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l

" set leader Key
let mapleader =" "
" set local leader to \
let maplocalleader = "\\"

call plug#begin('~/.config/nvim/plugged')

    "  spellchecker 
    " ansible snippets
    Plug 'phenomenes/ansible-snippets'
    " ansible highlight
    Plug 'pearofducks/ansible-vim'
    " Quick  Comment
    Plug 'tpope/vim-commentary'
    " bar airline
    Plug 'vim-airline/vim-airline'
    Plug 'vim-airline/vim-airline-themes'
    " Colorschemes
    Plug 'sonph/onehalf', { 'rtp': 'vim' }
    " vimdiff colorscheme 
    Plug 'challenger-deep-theme/vim', { 'as': 'challenger-deep' }
    " Unix Filter
    "Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    " Intelisense 
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
    " Autocomplte
    Plug 'jiangmiao/auto-pairs'
    " Icons
    Plug 'ryanoasis/vim-devicons'
    " Vim Prettier
    Plug 'prettier/vim-prettier', { 'do': 'yarn install --frozen-lockfile --production' }

call plug#end()

" Start NERDTree and leave the cursor in it.
"autocmd VimEnter * NERDTree

"  vimdiff colors
hi DiffText     ctermfg=DarkCyan    ctermbg=Red
hi DiffAdded    ctermfg=black       ctermbg=DarkCyan
hi DiffRemoved  ctermfg=Blue        ctermbg=NONE
hi DiffDelete   ctermfg=LightBlue   ctermbg=LightBlue
hi DiffChange   ctermfg=NONE        ctermbg=NONE

" UTF-8 encoding for Icons
set encoding=UTF-8

" let g:lightline = {'colorscheme': 'archery'}
let g:lightline = { 'colorscheme': 'challenger_deep'}


set wrapmargin=0
set nowrap

" basic colorscheme
set t_Co=256
" highlight Normal gui=NONE guifg=NONE guibg=NONE ctermfg=NONE ctermbg=NONE
highlight nonText gui=NONE guifg=NONE guibg=NONE ctermfg=NONE ctermbg=NONE
" highlight CursorLineNr gui=NONE guifg=NONE guibg=NONE ctermfg=11 ctermbg=NONE
" highlight CursorLine  gui=NONE guifg=NONE guibg=NONE guifg=NONE ctermbg=NONE
" highlight LineNr gui=NONE guifg=NONE guibg=NONE ctermfg=8 ctermbg=NONE
set background=dark

" ansible plugin config
let g:ansible_unindent_after_newline = 1
let g:ansible_yamlKeyName = 'yamlKey'
let g:ansible_attribute_highlight = "ob"
let g:ansible_extra_keywords_highlight = 1
let g:ansible_normal_keywords_highlight = 'Constant'
let g:ansible_with_keywords_highlight = 'Constant'
let g:ansible_template_syntaxes = { '*.rb.j2': 'ruby' }
let g:ansible_name_highlight = 'b'
au BufRead,BufNewFile /playbooks/.yml set filetype=yaml.ansible