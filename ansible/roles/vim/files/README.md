# Vimconfig Cheatsheet

![](../images/VimCheat.jpg)

**VIM Tutor:**
```sh
nvim +Tutor
```

Jump to end of File
```sh
Shift + G
```

Jump to beginn of file:
```sh
gg
```

Search & Replace:
```sh
:s/foo/bar/g
```

Multiline comment:
```sh
gcc
```

Search:
```sh
/
```

Jump to Line:
```sh
:42
```

Compare Two files:
```sh
vimdiff file1.txt file2.txt
```

Insert Visual Block Mode:
```sh
Control + V, Shift + I   or Delete with x
```

Visual Line Mode:
```sh
Shift + V
```

Switch between windows:
```sh
control + w
```

**Install Plugins**
[VIM PLUG](https://github.com/junegunn/vim-plug)
```sh
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
``` 

**[Awesome VIM Colorschemes: https://github.com/rafi/awesome-vim-colorschemes](https://github.com/rafi/awesome-vim-colorschemes)**

**create ~/.vimrc file**
```yml
" spaces & tabs
set shiftwidth=4
set tabstop=4
set softtabstop=4
set smarttab
set expandtab
set autoindent

set number

" Spell checking
set nospell
nnoremap <C-E> :setlocal spell! spelllang=en<CR>
nnoremap <C-G> :setlocal spell! spelllang=de<CR>

" Shortcutting split navigation, saving a keypress:
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l

" set leader Key
let mapleader =" "
" set local leader to \
let maplocalleader = "\\"

" buffer navigation

nnoremap <C-P> :bprev<CR>
" map esc to jk
inoremap jk <esc>

call plug#begin('~/.config/nvim/plugged')

    " Ansible snippets
    Plug 'phenomenes/ansible-snippets'
    " Ansible highlight
    Plug 'pearofducks/ansible-vim'
    " Quick  Comment
    Plug 'tpope/vim-commentary'
    " Bar airline things
    Plug 'vim-airline/vim-airline'
    Plug 'vim-airline/vim-airline-themes'
    " Colorschemes
    Plug 'sonph/onehalf', { 'rtp': 'vim' }
    " System Explorer
    Plug 'preservim/nerdtree'
    " Unix Filter
    Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
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
autocmd VimEnter * NERDTree


" UTF-8 encoding for Icons
set encoding=UTF-8



" basic colorscheme
let g:lightline = {'colorscheme': 'archery'}
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
```  

[VIMAWESOME](https://vimawesome.com/)



[FZF - fuzzy finder](https://github.com/junegunn/fzf)
"It's an interactive Unix filter for command-line that can be used with any list; files, command history, processes, hostnames, bookmarks, git commits, etc."

Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }


[File Search](https://github.com/BurntSushi/ripgrep)
```sh
brew install ripgrep
```

[Intelisense](https://github.com/neoclide/coc.nvim)
![](https://private-user-images.githubusercontent.com/251450/266519386-05f60ab8-dcb1-40f7-9e4a-3c03f5db5398.gif?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDUxOTE4NTQsIm5iZiI6MTc0NTE5MTU1NCwicGF0aCI6Ii8yNTE0NTAvMjY2NTE5Mzg2LTA1ZjYwYWI4LWRjYjEtNDBmNy05ZTRhLTNjMDNmNWRiNTM5OC5naWY_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNDIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDQyMFQyMzI1NTRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mMTg2NzllNzI2MWVlMGMxNjkzMDdiMTIzMGQ0YmNmZjUwMzVjMWQyZDRjMzAzOGRmMTg5OTQzNThhNzc3ODJkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.IAvai8k5Dt-002j64Ks3fcKfB8cZh7ALur6z1NurDIk)

Plug 'neoclide/coc.nvim', {'branch': 'release'}


[Autocomplete](https://github.com/jiangmiao/auto-pairs)

Plug 'jiangmiao/auto-pairs'


[System Explorer - nerdtree](https://github.com/preservim/nerdtree)
"The NERDTree is a file system explorer for the Vim editor. Using this plugin, users can visually browse complex directory hierarchies, quickly open files for reading or editing, and perform basic file system operations."

Plug 'preservim/nerdtree'


[Git - vim-fugitive](https://github.com/tpope/vim-fugitive)
"Fugitive is the premier Vim plugin for Git. Or maybe it's the premier Git plugin for Vim? Either way, it's "so awesome, it should be illegal". That's why it's called Fugitive."


[vim-devicons](https://github.com/ryanoasis/vim-devicons)
"Folder Icons"


Plug 'ryanoasis/vim-devicons'

set encoding=UTF-8

[vim-prettier](https://github.com/prettier/vim-prettier)
[vscode neovim](https://github.com/vscode-neovim/vscode-neovim)
[vscode react](https://github.com/xabikos/vscode-react)


**Install Plugin from .vimrc config**
```sh
:PlugInstall
```

![](../images/vim.jpg)


**Install zsh on mac cli** 
[Source ohmyzsh](https://github.com/ohmyzsh/ohmyzsh/tree/master)
```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"


vi ~/.zshrc

plugins=(
  git
  bundler
  dotenv
  macos
  rake
  rbenv
  ruby
)
```

![](../images/zsh.jpg)

**Introducing [vscode-neovim](https://github.com/vscode-neovim/vscode-neovim)**

[GitHub zsh Themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Themes)
[GitHub zsh Plugin](https://github.com/ohmyzsh/ohmyzsh/blob/master/plugins/git/git.plugin.zsh)

**List of Vim Plugins:**
https://github.com/gitui-org/gitui

